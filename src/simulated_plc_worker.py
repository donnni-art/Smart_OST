"""
simulated_plc_worker.py
=======================
จำลอง PLC data เมื่อ mock_mode = true ใน config.json

Interface เหมือน TCPWorker:
  data_ready        = Signal(dict)   — emits ทุก shot_interval_ms
  finished          = Signal()
  connection_status = Signal(str)    — "connected" | "reconnecting" | "disconnected"

Attributes ที่ปรับได้จาก SimulatorControlPanel (thread-safe ผ่าน Python GIL):
  shot_interval_ms  : ms ต่อ 1 sheet (100–10000)
  defect_rate       : สัดส่วน defect 0.0–1.0
  shot_number       : shots per sheet (dm1251)
  pcs_number        : pcs per shot
  is_paused         : หยุดชั่วคราว (ไม่ increment sheet)
  is_disconnected   : จำลอง PLC offline (ไม่ emit data)

Scenarios:
  inject_high_defect(duration_s) : raise defect_rate → 0.5 ชั่วคราว
  trigger_jump_to_pm(target, current): เพิ่ม sheet ก้าวกระโดดให้ถึง PM threshold
"""

import random
import time

from PySide6.QtCore import QObject, Signal

from src.app_logger import get_logger

log = get_logger("sim_plc")

_DEFECT_ENCODE = {
    "OPEN":  0x05,
    "SHORT": 0x03,
    "BLKM":  0x21,
    "SHOT":  0x09,
    "MAT":   0x11,
}
_DEFECT_NAMES = list(_DEFECT_ENCODE.keys())

_PM_SHOT_LIMIT = 30_000   # ต้องตรงกับ pm_manager._PM_SHOT_LIMIT


class SimulatedPLCWorker(QObject):
    """จำลอง PLC worker — ใช้แทน PLCWorker/TCPWorker เมื่อ mock_mode=true"""

    finished          = Signal()
    data_ready        = Signal(dict)
    connection_status = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True

        # — ปรับได้จาก SimulatorControlPanel —
        self.shot_interval_ms = 1000
        self.defect_rate      = 0.05
        self.shot_number      = 4
        self.pcs_number       = 2
        self.is_paused        = False
        self.is_disconnected  = False

        # สถานะภายใน — สะสมตลอด session
        self._total_sheet  = 0
        self._good_sheet   = 0
        self._ng_sheet     = 0
        self._total_pcs    = 0
        self._good_pcs     = 0
        self._defect_accum = {k: 0 for k in _DEFECT_NAMES}

        self._lot_number   = None
        self._product_name = ""

        # pending actions (set by control panel, consumed each cycle)
        self._jump_sheets    = 0
        self._temp_defect    = None   # (rate, until_time)

    def stop(self):
        self._running = False

    def set_lot_number(self, lot: str):
        self._lot_number = lot

    def set_product_name(self, name: str):
        self._product_name = name

    # ── scenarios ─────────────────────────────────────────────────────────────

    def inject_high_defect(self, duration_s: float = 10.0):
        """ตั้ง defect_rate = 0.5 เป็นเวลา duration_s วินาที"""
        self._temp_defect = (0.5, time.time() + duration_s)
        log.info("SIM: inject high defect for %.0fs", duration_s)

    def trigger_jump_to_pm(self, current_shot_count: int):
        """เพิ่ม sheet ก้าวกระโดดให้ shot_count ไปถึง PM threshold - 50"""
        target    = _PM_SHOT_LIMIT - 50
        needed    = max(0, target - current_shot_count)
        sn        = max(1, self.shot_number)
        self._jump_sheets = (needed + sn - 1) // sn
        log.info("SIM: jump %d sheets to reach PM (current=%d)", self._jump_sheets, current_shot_count)

    # ── run loop ──────────────────────────────────────────────────────────────

    def run(self):
        self.connection_status.emit("connected")
        log.info("SIM: SimulatedPLCWorker started")

        while self._running:
            interval = self.shot_interval_ms / 1000.0

            if self.is_disconnected:
                self.connection_status.emit("reconnecting")
                time.sleep(interval)
                continue

            if not self.is_paused:
                sheets = 1 + self._jump_sheets
                self._jump_sheets = 0

                eff_rate = self._effective_defect_rate()
                for _ in range(sheets):
                    self._produce_sheet(eff_rate)

                self.data_ready.emit(self._build_data())

            time.sleep(interval)

        self.connection_status.emit("disconnected")
        self.finished.emit()
        log.info("SIM: SimulatedPLCWorker stopped")

    # ── internal ──────────────────────────────────────────────────────────────

    def _effective_defect_rate(self) -> float:
        if self._temp_defect:
            rate, until = self._temp_defect
            if time.time() < until:
                return rate
            self._temp_defect = None
        return self.defect_rate

    def _produce_sheet(self, defect_rate: float):
        self._total_sheet += 1
        sheet_pcs  = self.shot_number * self.pcs_number
        ng_count   = sum(1 for _ in range(sheet_pcs) if random.random() < defect_rate)
        self._total_pcs += sheet_pcs
        self._good_pcs  += sheet_pcs - ng_count
        if ng_count:
            self._ng_sheet  += 1
        else:
            self._good_sheet += 1

    def _build_data(self) -> dict:
        defect_results, shot_per_pcs, counts = self._generate_defects(
            self._effective_defect_rate()
        )
        for k, v in counts.items():
            self._defect_accum[k] += v

        return {
            # ── cumulative PLC registers ──────────────────────────────────
            "dm1923": self._total_sheet,
            "dm1924": self._good_sheet,
            "dm1925": self._ng_sheet,
            "dm1917": self._total_pcs,
            "dm1919": self._good_pcs,
            # ── defect type counters ──────────────────────────────────────
            "dm1911": self._defect_accum["SHORT"],
            "dm1912": self._defect_accum["OPEN"],
            "dm1913": self._defect_accum["SHOT"],
            "dm1914": self._defect_accum["MAT"],
            "dm1915": self._defect_accum["BLKM"],
            # ── config / metadata ─────────────────────────────────────────
            "dm1251":       self.shot_number,   # shots per sheet
            "lot_number":   self._lot_number,
            "shot_number":  self.shot_number,
            "pcs_number":   self.pcs_number,
            "shot_per_pcs": shot_per_pcs,
            "defect_results": defect_results,
            "product_name": self._product_name,
        }

    def _generate_defects(self, defect_rate: float):
        results   = {}
        raw_list  = []
        counts    = {k: 0 for k in _DEFECT_NAMES}

        for s in range(1, self.shot_number + 1):
            for p in range(1, self.pcs_number + 1):
                key = f"S{s}P{p}"
                if random.random() < defect_rate:
                    name           = random.choice(_DEFECT_NAMES)
                    results[key]   = [name]
                    raw_list.append(_DEFECT_ENCODE[name])
                    counts[name]  += 1
                else:
                    results[key]   = ["PASS"]
                    raw_list.append(0)

        return results, raw_list, counts
