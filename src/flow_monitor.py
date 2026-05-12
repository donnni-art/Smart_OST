"""
flow_monitor.py
===============
Real-time monitor ของ data-flow nodes ทั้งหมดใน Smart OST

แสดงสถานะ:
  - PLC Worker       : serial connected / TCP status + last data timestamp
  - ShotCounter      : shot count, product, lot
  - GraphUpdater     : last graph update timing
  - HeatMapDefect    : last shot/defect state
  - DataSync         : last sync timing
  - ProductionCalc   : sheets/hr, pcs/hr, stale/offline detection
  - DB Read/Write    : MySQL connection alive check

การใช้งาน (เปิดจาก MainWindow):
  from src.flow_monitor import FlowMonitorDialog
  dlg = FlowMonitorDialog(main_window, parent=main_window)
  dlg.show()
"""

import time

from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
)

from src.app_logger import get_logger

log = get_logger("monitor")

_DOT = "●"


class FlowMonitorDialog(QDialog):
    """หน้าต่าง real-time monitor ของ data-flow nodes ทั้งหมด"""

    # node rows: (key, display_label)
    _NODES = [
        ("plc",      "PLC Worker"),
        ("shot",     "ShotCounter"),
        ("graph",    "GraphUpdater"),
        ("heatmap",  "HeatMapDefect"),
        ("datasync", "DataSync"),
        ("prodcalc", "ProductionCalc"),
        ("db_read",  "DB Read"),
        ("db_write", "DB Write"),
    ]

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self._main = main_window

        # activity timestamps — updated from signal hooks
        self._ts_plc_data   = None
        self._ts_graph      = None
        self._ts_datasync   = None
        self._ts_prodcalc   = None

        # TCP status string from signal
        self._tcp_status = "unknown"

        self.setWindowTitle("Smart OST — Flow Monitor")
        self.setMinimumWidth(680)
        self.setMinimumHeight(400)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        self._setup_ui()
        self._connect_signals()

        self._timer = QTimer(self)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._refresh)
        self._timer.start()
        self._refresh()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        hdr = QLabel("Real-time Data-flow Monitor")
        hdr.setFont(QFont("Arial", 13, QFont.Bold))
        layout.addWidget(hdr)

        sub = QLabel("Auto refresh: 500 ms  |  กด Ctrl+Shift+M เพื่อเปิด/ปิด")
        sub.setFont(QFont("Arial", 9))
        sub.setStyleSheet("color: #888;")
        layout.addWidget(sub)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #ccc;")
        layout.addWidget(div)

        self._table = QTableWidget(len(self._NODES), 3, self)
        self._table.setHorizontalHeaderLabels(["Node", "Status", "Detail"])
        hh = self._table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        self._table.verticalHeader().setVisible(False)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.setSelectionMode(QTableWidget.NoSelection)
        self._table.setAlternatingRowColors(True)
        self._table.setStyleSheet("""
            QTableWidget          { border: 1px solid #ddd; gridline-color: #eee; }
            QTableWidget::item    { padding: 6px 8px; }
            QHeaderView::section  { background: #f5f5f5; font-weight: bold;
                                    padding: 4px; border: none; }
        """)
        layout.addWidget(self._table)

        bold10 = QFont("Arial", 10, QFont.Bold)
        for row, (_, label) in enumerate(self._NODES):
            item = QTableWidgetItem(label)
            item.setFont(bold10)
            self._table.setItem(row, 0, item)
            self._table.setItem(row, 1, QTableWidgetItem(""))
            self._table.setItem(row, 2, QTableWidgetItem(""))

        btn_bar = QHBoxLayout()
        btn_bar.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.close)
        btn_bar.addWidget(close_btn)
        layout.addLayout(btn_bar)

    # ── signal hooks ──────────────────────────────────────────────────────────

    def _connect_signals(self):
        mw = self._main
        if hasattr(mw, 'plc_window') and mw.plc_window:
            mw.plc_window.data_updated.connect(self._on_plc_data)
            try:
                mw.plc_window.tcp_status_changed.connect(self._on_tcp_status)
            except Exception:
                pass
        if hasattr(mw, 'production_calculator') and mw.production_calculator:
            mw.production_calculator.production_rates_updated.connect(self._on_prodcalc)

    def _disconnect_signals(self):
        mw = self._main
        for attr, slot in [('plc_window', self._on_plc_data)]:
            obj = getattr(mw, attr, None)
            if obj:
                try:
                    obj.data_updated.disconnect(slot)
                except Exception:
                    pass
                try:
                    obj.tcp_status_changed.disconnect(self._on_tcp_status)
                except Exception:
                    pass
        pc = getattr(mw, 'production_calculator', None)
        if pc:
            try:
                pc.production_rates_updated.disconnect(self._on_prodcalc)
            except Exception:
                pass

    @Slot(dict)
    def _on_plc_data(self, _data):
        now = time.time()
        self._ts_plc_data  = now
        self._ts_datasync  = now   # DataSync subscribes to same signal
        self._ts_graph     = now   # GraphUpdater subscribes to same signal

    @Slot(str)
    def _on_tcp_status(self, status: str):
        self._tcp_status = status

    @Slot(dict)
    def _on_prodcalc(self, _rates):
        self._ts_prodcalc = time.time()

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _ago(ts) -> str:
        if ts is None:
            return "ยังไม่มีข้อมูล"
        diff = time.time() - ts
        if diff < 2:
            return "just now"
        return f"{diff:.0f}s ago"

    def _set_row(self, row: int, color: str, status: str, detail: str):
        dot_item = QTableWidgetItem(f"{_DOT}  {status}")
        dot_item.setForeground(QColor(color))
        dot_item.setFont(QFont("Arial", 10))
        self._table.setItem(row, 1, dot_item)

        det_item = QTableWidgetItem(detail)
        det_item.setFont(QFont("Arial", 9))
        det_item.setForeground(QColor("#444"))
        self._table.setItem(row, 2, det_item)

    # ── refresh ───────────────────────────────────────────────────────────────

    def _refresh(self):
        mw    = self._main
        now   = time.time()
        ago   = self._ago
        sr    = self._set_row

        # ── 0: PLC Worker ─────────────────────────────────────────────────────
        plc = getattr(mw, 'plc_window', None)
        if plc:
            cfg  = getattr(plc, 'plc_config', {})
            mode = cfg.get('connection_mode', 'serial')
            if mode == 'tcp':
                tcp_s  = self._tcp_status
                color  = {"connected": "#27ae60", "reconnecting": "#f39c12"}.get(
                    tcp_s, "#e74c3c"
                )
                status = tcp_s.capitalize() if tcp_s not in ("unknown", "") else "Connecting…"
                detail = (
                    f"TCP mode  |  last data: {ago(self._ts_plc_data)}"
                )
            else:
                ok     = getattr(plc, 'serial_connected', False)
                color  = "#27ae60" if ok else "#e74c3c"
                status = "Connected" if ok else "Disconnected"
                port   = cfg.get('port', '?')
                detail = f"Serial {port}  |  last data: {ago(self._ts_plc_data)}"
        else:
            color, status, detail = "#888", "N/A", "PLCWindow ยังไม่ถูก init"
        sr(0, color, status, detail)

        # ── 1: ShotCounter ────────────────────────────────────────────────────
        sc = getattr(mw, 'shot_counter', None)
        if sc:
            shot    = getattr(sc, 'shot_count', 0)
            product = getattr(sc, 'product_name', None) or "—"
            lot     = (sc.product_data.get('lot_number', '—')
                       if hasattr(sc, 'product_data') else '—')
            sr(1, "#27ae60", "Active",
               f"shot: {shot:,}  |  product: {product}  |  lot: {lot}")
        else:
            sr(1, "#888", "N/A", "ยังไม่ถูก init")

        # ── 2: GraphUpdater ───────────────────────────────────────────────────
        gu = getattr(mw, 'graph_updater', None)
        if gu:
            last   = getattr(gu, 'last_data', None)
            lv     = getattr(gu, 'last_values', {}) or {}
            color  = "#27ae60" if last is not None else "#f39c12"
            status = "Active" if last is not None else "Waiting"
            g, n   = lv.get('good_pcs', 0), lv.get('ng_pcs', 0)
            sr(2, color, status,
               f"last update: {ago(self._ts_graph)}  |  good: {g}  ng: {n}")
        else:
            sr(2, "#888", "N/A", "ยังไม่ถูก init")

        # ── 3: HeatMapDefect ──────────────────────────────────────────────────
        hm = getattr(mw, 'heat_map_defect', None)
        if hm:
            ls = getattr(hm, 'last_shot_cnt', None)
            ld = getattr(hm, 'last_dm1923',   None)
            sr(3, "#27ae60", "Active",
               f"last_shot_cnt: {ls}  |  last_dm1923: {ld}")
        else:
            sr(3, "#888", "N/A", "ยังไม่ถูก init")

        # ── 4: DataSync ───────────────────────────────────────────────────────
        ds = getattr(mw, 'update_data_manager', None)
        if ds:
            sr(4, "#27ae60", "Active", f"last sync: {ago(self._ts_datasync)}")
        else:
            sr(4, "#888", "N/A", "ยังไม่ถูก init")

        # ── 5: ProductionCalculator ───────────────────────────────────────────
        pc = getattr(mw, 'production_calculator', None)
        if pc:
            rates  = getattr(pc, 'current_rates', {})
            sph    = rates.get('sheets_per_hour', 0.0)
            pph    = rates.get('pcs_per_hour',    0.0)
            ldr    = getattr(pc, 'last_data_received', None)
            if ldr:
                stale = now - ldr
                if stale > getattr(pc, 'offline_threshold', 600):
                    color, status = "#888888", "Offline"
                elif stale > getattr(pc, 'stale_threshold', 120):
                    color, status = "#3498db", "Stale"
                else:
                    color, status = "#27ae60", "Active"
            else:
                color, status = "#f39c12", "Waiting"
            sr(5, color, status,
               f"sheets/hr: {sph:.1f}  |  pcs/hr: {pph:.1f}  |  last calc: {ago(self._ts_prodcalc)}")
        else:
            sr(5, "#888", "N/A", "ยังไม่ถูก init")

        # ── 6 & 7: DB Read / Write ────────────────────────────────────────────
        du = getattr(mw, 'data_upload', None)
        db = getattr(du, 'db_manager', None) if du else None

        def _db_row(row: int, conn_attr: str, cfg_attr: str):
            if db:
                conn = getattr(db, conn_attr, None)
                try:
                    ok = conn is not None and conn.is_connected()
                except Exception:
                    ok = False
                color  = "#27ae60" if ok else "#e74c3c"
                status = "Connected" if ok else "Disconnected"
                host   = getattr(db, cfg_attr, {}).get('host', '?')
                sr(row, color, status, f"host: {host}")
            else:
                sr(row, "#888", "N/A", "DataUploader ยังไม่ถูก init")

        _db_row(6, '_read_connection',  '_read_config')
        _db_row(7, '_write_connection', '_write_config')

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._timer.stop()
        self._disconnect_signals()
        super().closeEvent(event)
