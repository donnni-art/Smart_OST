"""
machine_monitor.py
==================
จัดการการเชื่อมต่อ TCP กับ Raspberry Pi หลายเครื่องพร้อมกัน
ส่ง signal machine_updated(machine_id, data) ทุกครั้งที่ได้รับข้อมูลใหม่

Signals:
  machine_updated(str, dict)  — (machine_id, plc_data)
  machine_status (str, str)   — (machine_id, "connected"|"reconnecting"|"disconnected")

การใช้งาน:
  monitor = MachineMonitor()
  monitor.machine_updated.connect(on_data)
  monitor.machine_status.connect(on_status)
  monitor.start()
  ...
  monitor.stop()
"""

import json
import socket
import time
import random

from PySide6.QtCore import QObject, Signal, QThread, QTimer

from src.config_manager import config_manager
from src.app_logger import get_logger

log = get_logger("machine_monitor")


# ─────────────────────────────────────────────────────────────────────────────
# Worker ทำงานใน background thread — เชื่อมต่อ TCP กับ Pi เครื่องเดียว
# ─────────────────────────────────────────────────────────────────────────────
class MachineTCPWorker(QObject):
    data_ready     = Signal(str, dict)   # (machine_id, data_dict)
    status_changed = Signal(str, str)    # (machine_id, status_str)
    finished       = Signal()

    def __init__(self, machine_id: str, pi_ip: str, pi_port: int,
                 reconnect_interval: int = 5):
        super().__init__()
        self.machine_id        = machine_id
        self.pi_ip             = pi_ip
        self.pi_port           = pi_port
        self.reconnect_interval = reconnect_interval
        self._running          = True

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((self.pi_ip, self.pi_port))
                    s.settimeout(2)
                    log.info("Machine %s connected to %s:%s",
                             self.machine_id, self.pi_ip, self.pi_port)
                    self.status_changed.emit(self.machine_id, "connected")

                    buffer = ""
                    while self._running:
                        try:
                            chunk = s.recv(4096).decode('utf-8', errors='ignore')
                        except socket.timeout:
                            continue
                        if not chunk:
                            log.warning("Machine %s: Pi closed connection", self.machine_id)
                            break
                        buffer += chunk
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            line = line.strip()
                            if line:
                                try:
                                    data = json.loads(line)
                                    self.data_ready.emit(self.machine_id, data)
                                except json.JSONDecodeError as e:
                                    log.debug("Machine %s JSON error: %s", self.machine_id, e)
            except Exception as e:
                log.error("Machine %s connection error: %s", self.machine_id, e)
                if self._running:
                    self.status_changed.emit(self.machine_id, "reconnecting")
                    time.sleep(self.reconnect_interval)

        self.status_changed.emit(self.machine_id, "disconnected")
        self.finished.emit()


# ─────────────────────────────────────────────────────────────────────────────
# MachineMonitor — Orchestrate workers สำหรับทุกเครื่อง
# ─────────────────────────────────────────────────────────────────────────────
class MachineMonitor(QObject):
    machine_updated = Signal(str, dict)   # (machine_id, plc_data)
    machine_status  = Signal(str, str)    # (machine_id, status)

    _DEFECT_TYPES = ["PASS", "OPEN", "SHORT", "BLKM", "SHOT"]
    _DEFECT_WEIGHTS = [92, 3, 2, 2, 1]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._workers: list[tuple[MachineTCPWorker, QThread]] = []
        self._mock_timer: QTimer | None = None
        self._mock_counters: dict = {}
        self._machines: list[dict] = []

    # ── Public API ──────────────────────────────────────────────────────────

    def start(self):
        """อ่าน machines จาก config แล้วเริ่ม workers"""
        machines = config_manager.current_config.get('machines', [])
        self._machines = machines

        if not machines:
            log.warning("No machines configured — add 'machines' array to config.json")
            return

        if config_manager.current_config.get('mock_mode', False):
            self._start_mock(machines)
        else:
            self._start_real(machines)

    def stop(self):
        """หยุด workers ทั้งหมด"""
        if self._mock_timer:
            self._mock_timer.stop()
            self._mock_timer = None

        for worker, thread in self._workers:
            worker.stop()
            thread.quit()
            thread.wait(3000)
        self._workers.clear()
        log.info("MachineMonitor stopped")

    # ── Real TCP mode ────────────────────────────────────────────────────────

    def _start_real(self, machines: list[dict]):
        for m in machines:
            worker = MachineTCPWorker(
                machine_id=m['id'],
                pi_ip=m['pi_ip'],
                pi_port=m.get('pi_port', 9999),
                reconnect_interval=m.get('reconnect_interval', 5),
            )
            thread = QThread()
            worker.moveToThread(thread)
            thread.started.connect(worker.run)
            worker.data_ready.connect(self.machine_updated)
            worker.status_changed.connect(self.machine_status)
            worker.finished.connect(thread.quit)
            thread.start()
            self._workers.append((worker, thread))
            log.info("Worker started: %s @ %s:%s",
                     m['id'], m['pi_ip'], m.get('pi_port', 9999))

    # ── Mock mode ────────────────────────────────────────────────────────────

    def _start_mock(self, machines: list[dict]):
        for m in machines:
            self._mock_counters[m['id']] = {
                'total_shots': random.randint(200, 4000),
                'shot_number': random.randint(4, 16),
                'pcs_number':  random.randint(2, 8),
            }
            self.machine_status.emit(m['id'], "connected")

        self._mock_timer = QTimer()
        self._mock_timer.setInterval(1000)
        self._mock_timer.timeout.connect(self._emit_mock_data)
        self._mock_timer.start()
        log.info("Mock mode: simulating %d machine(s)", len(machines))

    def _emit_mock_data(self):
        for m in self._machines:
            mid = m['id']
            c   = self._mock_counters[mid]
            c['total_shots'] += random.randint(0, 3)

            shots = c['shot_number']
            pcs   = c['pcs_number']

            defect_results: dict[str, list[str]] = {}
            for s in range(1, shots + 1):
                for p in range(1, pcs + 1):
                    chosen = random.choices(
                        self._DEFECT_TYPES, weights=self._DEFECT_WEIGHTS
                    )[0]
                    defect_results[f"S{s}P{p}"] = [chosen]

            data = {
                "lot_number":     m.get('mock_lot',     'TEST001'),
                "product_name":   m.get('mock_product', 'CAW-076W-1A'),
                "shot_number":    shots,
                "pcs_number":     pcs,
                "_total_shots":   c['total_shots'],
                "dm1923": random.randint(0, 1),
                "dm1924": random.randint(0, 1),
                "dm1925": random.randint(0, 500),
                "dm1917": random.randint(0, 10),
                "dm1919": random.randint(0, 10),
                "defect_results": defect_results,
                "shot_per_pcs":   [],
            }
            self.machine_updated.emit(mid, data)
