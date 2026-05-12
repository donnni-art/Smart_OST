"""
flow_monitor.py
===============
Real-time monitor ของ data-flow nodes ทั้งหมดใน Smart OST

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
from src.database_manager import database_manager

log = get_logger("monitor")

_DOT  = "●"
_OK   = "#27ae60"
_WARN = "#f39c12"
_ERR  = "#e74c3c"
_STALE = "#3498db"
_OFF  = "#888888"

_TCP_COLOR = {"connected": _OK, "reconnecting": _WARN}


class FlowMonitorDialog(QDialog):
    """หน้าต่าง real-time monitor ของ data-flow nodes ทั้งหมด"""

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

        self._ts_plc_data  = None
        self._ts_prodcalc  = None
        self._tcp_status   = "unknown"

        # cached once at connect-time — stable config values
        self._stale_threshold   = 120
        self._offline_threshold = 600

        self._prev_state: dict = {}
        self._signals_connected = False

        # fonts cached to avoid allocation in hot path
        self._font_status = QFont("Arial", 10)
        self._font_detail = QFont("Arial", 9)
        self._color_detail = QColor("#444")

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
        if self._signals_connected:
            return
        mw = self._main
        if hasattr(mw, 'plc_window') and mw.plc_window:
            mw.plc_window.data_updated.connect(self._on_plc_data)
            try:
                mw.plc_window.tcp_status_changed.connect(self._on_tcp_status)
            except Exception:
                pass
        if hasattr(mw, 'production_calculator') and mw.production_calculator:
            pc = mw.production_calculator
            pc.production_rates_updated.connect(self._on_prodcalc)
            self._stale_threshold   = getattr(pc, 'stale_threshold',   120)
            self._offline_threshold = getattr(pc, 'offline_threshold', 600)
        self._signals_connected = True

    def _disconnect_signals(self):
        if not self._signals_connected:
            return
        mw  = self._main
        plc = getattr(mw, 'plc_window', None)
        if plc:
            try: plc.data_updated.disconnect(self._on_plc_data)
            except Exception: pass
            try: plc.tcp_status_changed.disconnect(self._on_tcp_status)
            except Exception: pass
        pc = getattr(mw, 'production_calculator', None)
        if pc:
            try: pc.production_rates_updated.disconnect(self._on_prodcalc)
            except Exception: pass
        self._signals_connected = False

    @Slot(dict)
    def _on_plc_data(self, _data):
        self._ts_plc_data = time.time()

    @Slot(str)
    def _on_tcp_status(self, status: str):
        self._tcp_status = status

    @Slot(dict)
    def _on_prodcalc(self, _rates):
        self._ts_prodcalc = time.time()

    # ── helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _ago(ts, now: float) -> str:
        if ts is None:
            return "ยังไม่มีข้อมูล"
        diff = now - ts
        if diff < 2:
            return "just now"
        return f"{diff:.0f}s ago"

    def _staleness_status(self, ldr, now: float):
        if ldr is None:
            return _WARN, "Waiting"
        stale = now - ldr
        if stale > self._offline_threshold:
            return _OFF, "Offline"
        if stale > self._stale_threshold:
            return _STALE, "Stale"
        return _OK, "Active"

    def _set_row(self, row: int, color: str, status: str, detail: str):
        state = (color, status, detail)
        if self._prev_state.get(row) == state:
            return
        self._prev_state[row] = state

        s_item = self._table.item(row, 1)
        s_item.setText(f"{_DOT}  {status}")
        s_item.setForeground(QColor(color))
        s_item.setFont(self._font_status)

        d_item = self._table.item(row, 2)
        d_item.setText(detail)
        d_item.setFont(self._font_detail)
        d_item.setForeground(self._color_detail)

    def _db_row(self, row: int, conn_attr: str, cfg_attr: str):
        conn = getattr(database_manager, conn_attr, None)
        try:
            ok = conn is not None and conn.is_connected()
        except Exception:
            ok = False
        host = getattr(database_manager, cfg_attr, {}).get('host', '?')
        self._set_row(row, _OK if ok else _ERR,
                      "Connected" if ok else "Disconnected", f"host: {host}")

    # ── refresh ───────────────────────────────────────────────────────────────

    def _refresh(self):
        mw  = self._main
        now = time.time()
        ago = lambda ts: self._ago(ts, now)

        # ── 0: PLC Worker ─────────────────────────────────────────────────────
        plc = getattr(mw, 'plc_window', None)
        if plc:
            cfg  = getattr(plc, 'plc_config', {})
            mode = cfg.get('connection_mode', 'serial')
            if getattr(plc, 'is_mock_mode', False):
                tcp_s  = self._tcp_status
                color  = _TCP_COLOR.get(tcp_s, _WARN)
                status = f"Simulator ({tcp_s})" if tcp_s not in ("unknown", "") else "Simulator"
                w      = getattr(plc, 'worker', None)
                sheet  = getattr(w, '_total_sheet', 0)
                detail = f"mock_mode  |  sheet: {sheet}  |  last data: {ago(self._ts_plc_data)}"
            elif mode == 'tcp':
                tcp_s  = self._tcp_status
                color  = _TCP_COLOR.get(tcp_s, _ERR)
                status = tcp_s.capitalize() if tcp_s not in ("unknown", "") else "Connecting…"
                detail = f"TCP mode  |  last data: {ago(self._ts_plc_data)}"
            else:
                ok     = getattr(plc, 'serial_connected', False)
                color  = _OK if ok else _ERR
                status = "Connected" if ok else "Disconnected"
                detail = f"Serial {cfg.get('port', '?')}  |  last data: {ago(self._ts_plc_data)}"
        else:
            color, status, detail = _OFF, "N/A", "PLCWindow ยังไม่ถูก init"
        self._set_row(0, color, status, detail)

        # ── 1: ShotCounter ────────────────────────────────────────────────────
        sc = getattr(mw, 'shot_counter', None)
        if sc:
            shot    = getattr(sc, 'shot_count', 0)
            product = getattr(sc, 'product_name', None) or "—"
            lot     = sc.product_data.get('lot_number', '—') if hasattr(sc, 'product_data') else '—'
            self._set_row(1, _OK, "Active",
                          f"shot: {shot:,}  |  product: {product}  |  lot: {lot}")
        else:
            self._set_row(1, _OFF, "N/A", "ยังไม่ถูก init")

        # ── 2: GraphUpdater ───────────────────────────────────────────────────
        gu = getattr(mw, 'graph_updater', None)
        if gu:
            last  = getattr(gu, 'last_data', None)
            lv    = getattr(gu, 'last_values', {}) or {}
            color = _OK if last is not None else _WARN
            g, n  = lv.get('good_pcs', 0), lv.get('ng_pcs', 0)
            self._set_row(2, color, "Active" if last is not None else "Waiting",
                          f"last update: {ago(self._ts_plc_data)}  |  good: {g}  ng: {n}")
        else:
            self._set_row(2, _OFF, "N/A", "ยังไม่ถูก init")

        # ── 3: HeatMapDefect ──────────────────────────────────────────────────
        hm = getattr(mw, 'heat_map_defect', None)
        if hm:
            self._set_row(3, _OK, "Active",
                          f"last_shot_cnt: {getattr(hm,'last_shot_cnt',None)}"
                          f"  |  last_dm1923: {getattr(hm,'last_dm1923',None)}")
        else:
            self._set_row(3, _OFF, "N/A", "ยังไม่ถูก init")

        # ── 4: DataSync ───────────────────────────────────────────────────────
        if getattr(mw, 'update_data_manager', None):
            self._set_row(4, _OK, "Active", f"last sync: {ago(self._ts_plc_data)}")
        else:
            self._set_row(4, _OFF, "N/A", "ยังไม่ถูก init")

        # ── 5: ProductionCalculator ───────────────────────────────────────────
        pc = getattr(mw, 'production_calculator', None)
        if pc:
            rates  = getattr(pc, 'current_rates', {})
            sph    = rates.get('sheets_per_hour', 0.0)
            pph    = rates.get('pcs_per_hour',    0.0)
            color, status = self._staleness_status(
                getattr(pc, 'last_data_received', None), now
            )
            self._set_row(5, color, status,
                          f"sheets/hr: {sph:.1f}  |  pcs/hr: {pph:.1f}"
                          f"  |  last calc: {ago(self._ts_prodcalc)}")
        else:
            self._set_row(5, _OFF, "N/A", "ยังไม่ถูก init")

        # ── 6 & 7: DB Read / Write ────────────────────────────────────────────
        self._db_row(6, '_read_connection',  '_read_config')
        self._db_row(7, '_write_connection', '_write_config')

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._timer.stop()
        self._disconnect_signals()
        super().closeEvent(event)
