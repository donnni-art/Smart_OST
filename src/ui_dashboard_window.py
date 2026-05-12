"""
ui_dashboard_window.py
======================
Dashboard ภาพรวมสำหรับ Supervisor/Monitoring PC บน LAN

แสดงสถานะแบบ real-time ของ OST ทุกเครื่องพร้อมกัน
ข้อมูลมาจาก MachineMonitor ผ่าน TCP → Raspberry Pi → PLC

Layout:
  ┌─ Header ─────────────────────────────────────────────────┐
  │  SMART OST Dashboard   ●Online:3  ●Offline:0   14:30:25 │
  └──────────────────────────────────────────────────────────┘
  ┌─ Scroll area: grid ของ MachineCard ──────────────────────┐
  │  ┌───────────┐  ┌───────────┐  ┌───────────┐            │
  │  │ Machine 1 │  │ Machine 2 │  │ Machine 3 │  ...       │
  │  └───────────┘  └───────────┘  └───────────┘            │
  └──────────────────────────────────────────────────────────┘

การใช้งาน:
  from src.ui_dashboard_window import DashboardWindow
  win = DashboardWindow()
  win.show()
"""

from __future__ import annotations

import math
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QScrollArea, QPushButton, QSizePolicy, QSpacerItem,
)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QFont, QColor

from src.config_manager import config_manager
from src.machine_monitor import MachineMonitor
from src.app_logger import get_logger

log = get_logger("dashboard")

# ─────────────────────────────────────────────────────────────────────────────
# Color palette (dark industrial theme)
# ─────────────────────────────────────────────────────────────────────────────
_C = {
    "bg":            "#0d1117",   # main background
    "header_bg":     "#161b22",   # top bar
    "card_bg":       "#161b22",   # card background
    "card_border":   "#30363d",   # card border
    "connected":     "#238636",   # green
    "reconnecting":  "#d29922",   # yellow/orange
    "disconnected":  "#da3633",   # red
    "text_primary":  "#f0f6fc",   # white
    "text_secondary":"#8b949e",   # grey
    "accent":        "#58a6ff",   # blue accent (numbers)
    "accent2":       "#3fb950",   # green (pass rate)
    "accent3":       "#f85149",   # red (defect)
    "divider":       "#21262d",   # section divider
}

_CARD_MIN_W = 290
_CARD_MIN_H = 260
_GRID_COLS  = 4    # max columns in grid


# ─────────────────────────────────────────────────────────────────────────────
# MachineCard — แสดงสถานะ PLC เครื่องเดียว
# ─────────────────────────────────────────────────────────────────────────────
class MachineCard(QFrame):
    """Card ใน dashboard แต่ละใบ = เครื่อง OST หนึ่งเครื่อง"""

    def __init__(self, machine_cfg: dict, parent=None):
        super().__init__(parent)
        self.machine_id   = machine_cfg['id']
        self.machine_name = machine_cfg.get('name', machine_cfg['id'])
        self._status = "disconnected"

        self.setMinimumSize(_CARD_MIN_W, _CARD_MIN_H)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setObjectName("MachineCard")
        self._setup_ui()
        self._apply_style()
        self._set_status("disconnected")

    # ── Build widget tree ────────────────────────────────────────────────────

    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Card header ──────────────────────────────────────────────────────
        self.header_frame = QFrame()
        self.header_frame.setObjectName("CardHeader")
        self.header_frame.setFixedHeight(44)
        h_layout = QHBoxLayout(self.header_frame)
        h_layout.setContentsMargins(12, 0, 12, 0)

        self.status_dot = QLabel("●")
        self.status_dot.setFixedWidth(16)

        self.name_lbl = QLabel(self.machine_name)
        self.name_lbl.setObjectName("CardMachineName")

        self.badge_lbl = QLabel("DISCONNECTED")
        self.badge_lbl.setObjectName("CardBadge")
        self.badge_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        h_layout.addWidget(self.status_dot)
        h_layout.addWidget(self.name_lbl)
        h_layout.addStretch()
        h_layout.addWidget(self.badge_lbl)

        outer.addWidget(self.header_frame)

        # ── Body ─────────────────────────────────────────────────────────────
        body = QFrame()
        body.setObjectName("CardBody")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(14, 10, 14, 10)
        body_layout.setSpacing(6)

        # Lot + Product row
        info_grid = QGridLayout()
        info_grid.setHorizontalSpacing(8)
        info_grid.setVerticalSpacing(4)

        info_grid.addWidget(self._label("LOT", secondary=True),     0, 0)
        self.lot_val = self._value("—")
        info_grid.addWidget(self.lot_val, 0, 1)

        info_grid.addWidget(self._label("PRODUCT", secondary=True), 1, 0)
        self.product_val = self._value("—")
        info_grid.addWidget(self.product_val, 1, 1)

        body_layout.addLayout(info_grid)

        # Divider
        body_layout.addWidget(self._divider())

        # Stats row
        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(4)
        stats_grid.setVerticalSpacing(4)

        self.shot_val  = self._big_number("—")
        self.pcs_val   = self._big_number("—")
        self.total_val = self._big_number("—")
        self.defect_val = self._big_number("—")

        stats_grid.addWidget(self._label("SHOT TYPE", secondary=True), 0, 0)
        stats_grid.addWidget(self._label("PCS/SHOT",  secondary=True), 0, 1)
        stats_grid.addWidget(self._label("TOTAL",     secondary=True), 0, 2)
        stats_grid.addWidget(self._label("DEFECT",    secondary=True), 0, 3)

        stats_grid.addWidget(self.shot_val,  1, 0)
        stats_grid.addWidget(self.pcs_val,   1, 1)
        stats_grid.addWidget(self.total_val, 1, 2)
        stats_grid.addWidget(self.defect_val,1, 3)

        body_layout.addLayout(stats_grid)

        # Divider
        body_layout.addWidget(self._divider())

        # Pass rate bar label
        rate_row = QHBoxLayout()
        self.rate_lbl = QLabel("PASS RATE")
        self.rate_lbl.setObjectName("SecondaryLabel")
        self.rate_val = QLabel("—")
        self.rate_val.setObjectName("RateLabel")
        self.rate_val.setAlignment(Qt.AlignmentFlag.AlignRight)
        rate_row.addWidget(self.rate_lbl)
        rate_row.addWidget(self.rate_val)
        body_layout.addLayout(rate_row)

        # Footer: last update time
        body_layout.addStretch()
        self.time_lbl = QLabel("—")
        self.time_lbl.setObjectName("FooterLabel")
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        body_layout.addWidget(self.time_lbl)

        outer.addWidget(body)

    # ── Update methods (called by DashboardWindow) ───────────────────────────

    @Slot(dict)
    def update_data(self, data: dict):
        """อัพเดตข้อมูล PLC บนการ์ด"""
        lot     = data.get("lot_number",   "—") or "—"
        product = data.get("product_name", "—") or "—"
        shots   = data.get("shot_number",   0)
        pcs     = data.get("pcs_number",    0)
        total   = data.get("_total_shots",  0)
        defects = data.get("defect_results", {})

        # defect analysis
        n_total  = len(defects)
        n_failed = sum(1 for v in defects.values() if v != ["PASS"])
        pass_pct = (n_total - n_failed) / n_total * 100 if n_total > 0 else 100.0

        self.lot_val.setText(lot[:20])
        self.product_val.setText(product[:22])
        self.shot_val.setText(str(shots))
        self.pcs_val.setText(str(pcs))
        self.total_val.setText(f"{total:,}")
        self.defect_val.setText(str(n_failed))

        rate_text = f"{pass_pct:.1f}%"
        self.rate_val.setText(rate_text)
        # color pass rate label
        if pass_pct >= 99.0:
            self.rate_val.setStyleSheet(f"color: {_C['accent2']}; font-weight: bold;")
            self.defect_val.setStyleSheet(f"color: {_C['accent2']}; font-size: 18px; font-weight: bold;")
        elif pass_pct >= 95.0:
            self.rate_val.setStyleSheet(f"color: {_C['reconnecting']}; font-weight: bold;")
            self.defect_val.setStyleSheet(f"color: {_C['reconnecting']}; font-size: 18px; font-weight: bold;")
        else:
            self.rate_val.setStyleSheet(f"color: {_C['accent3']}; font-weight: bold;")
            self.defect_val.setStyleSheet(f"color: {_C['accent3']}; font-size: 18px; font-weight: bold;")

        self.time_lbl.setText(datetime.now().strftime("%H:%M:%S"))

    @Slot(str)
    def set_status(self, status: str):
        """อัพเดตสี header ตาม status: connected / reconnecting / disconnected"""
        self._status = status
        self._set_status(status)

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _set_status(self, status: str):
        color_map = {
            "connected":    _C["connected"],
            "reconnecting": _C["reconnecting"],
            "disconnected": _C["disconnected"],
        }
        badge_map = {
            "connected":    "● ONLINE",
            "reconnecting": "⟳ RECONNECTING",
            "disconnected": "✕ OFFLINE",
        }
        color = color_map.get(status, _C["disconnected"])
        badge = badge_map.get(status, "✕ OFFLINE")

        self.header_frame.setStyleSheet(
            f"QFrame#CardHeader {{ background-color: {color}; border-radius: 6px 6px 0 0; }}"
        )
        self.status_dot.setStyleSheet(f"color: white; font-size: 10px;")
        self.badge_lbl.setText(badge)
        self.badge_lbl.setStyleSheet("color: rgba(255,255,255,0.85); font-size: 11px;")
        self.name_lbl.setStyleSheet(
            "color: white; font-weight: bold; font-size: 13px;"
        )

        if status == "disconnected":
            for w in (self.lot_val, self.product_val, self.shot_val,
                      self.pcs_val, self.total_val, self.defect_val,
                      self.rate_val, self.time_lbl):
                w.setText("—")

    def _apply_style(self):
        self.setStyleSheet(f"""
            QFrame#MachineCard {{
                background-color: {_C['card_bg']};
                border: 1px solid {_C['card_border']};
                border-radius: 6px;
            }}
            QFrame#CardBody {{
                background-color: {_C['card_bg']};
            }}
            QLabel#SecondaryLabel {{
                color: {_C['text_secondary']};
                font-size: 10px;
                font-weight: bold;
            }}
            QLabel#FooterLabel {{
                color: {_C['text_secondary']};
                font-size: 10px;
            }}
            QLabel#RateLabel {{
                font-size: 13px;
                font-weight: bold;
            }}
        """)

    @staticmethod
    def _label(text: str, secondary: bool = False) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("SecondaryLabel" if secondary else "")
        if secondary:
            lbl.setStyleSheet(
                f"color: {_C['text_secondary']}; font-size: 10px; font-weight: bold;"
            )
        return lbl

    @staticmethod
    def _value(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(
            f"color: {_C['text_primary']}; font-size: 12px;"
        )
        return lbl

    @staticmethod
    def _big_number(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet(
            f"color: {_C['accent']}; font-size: 18px; font-weight: bold;"
        )
        return lbl

    @staticmethod
    def _divider() -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"border: 1px solid {_C['divider']};")
        line.setFixedHeight(1)
        return line


# ─────────────────────────────────────────────────────────────────────────────
# DashboardWindow — หน้าต่างหลักของ Monitoring Dashboard
# ─────────────────────────────────────────────────────────────────────────────
class DashboardWindow(QMainWindow):
    """หน้าต่าง dashboard แสดงภาพรวม OST ทุกเครื่องบน LAN"""

    closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SMART OST — Production Dashboard")
        self.resize(1280, 760)
        self.setMinimumSize(800, 500)

        self._cards: dict[str, MachineCard] = {}
        self._online_count  = 0
        self._offline_count = 0

        self._setup_ui()
        self._apply_global_style()

        # Clock timer
        self._clock_timer = QTimer(self)
        self._clock_timer.setInterval(1000)
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start()
        self._tick_clock()

        # Machine monitor
        self._monitor = MachineMonitor(self)
        self._monitor.machine_updated.connect(self._on_machine_data)
        self._monitor.machine_status.connect(self._on_machine_status)

        # Build cards for all configured machines
        machines = config_manager.current_config.get('machines', [])
        for m in machines:
            self._add_card(m)

        self._relayout_cards()
        self._monitor.start()

        log.info("DashboardWindow started with %d machine(s)", len(machines))

    # ── Build UI ─────────────────────────────────────────────────────────────

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top header bar ───────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("TopHeader")
        header.setFixedHeight(56)
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(20, 0, 20, 0)

        title = QLabel("⚙  SMART OST  —  Production Dashboard")
        title.setObjectName("DashTitle")

        self.stats_lbl = QLabel()
        self.stats_lbl.setObjectName("StatsLabel")

        self.clock_lbl = QLabel()
        self.clock_lbl.setObjectName("ClockLabel")

        h_lay.addWidget(title)
        h_lay.addStretch()
        h_lay.addWidget(self.stats_lbl)
        h_lay.addSpacing(24)
        h_lay.addWidget(self.clock_lbl)

        root.addWidget(header)

        # ── Sub-header: machine count row ────────────────────────────────────
        sub = QFrame()
        sub.setObjectName("SubHeader")
        sub.setFixedHeight(32)
        sub_lay = QHBoxLayout(sub)
        sub_lay.setContentsMargins(20, 0, 20, 0)

        self.online_lbl  = QLabel("● Online: 0")
        self.online_lbl.setObjectName("OnlineLabel")
        self.offline_lbl = QLabel("✕ Offline: 0")
        self.offline_lbl.setObjectName("OfflineLabel")
        self.recon_lbl   = QLabel()
        self.recon_lbl.setObjectName("ReconLabel")

        sub_lay.addWidget(self.online_lbl)
        sub_lay.addSpacing(20)
        sub_lay.addWidget(self.offline_lbl)
        sub_lay.addSpacing(20)
        sub_lay.addWidget(self.recon_lbl)
        sub_lay.addStretch()

        root.addWidget(sub)

        # ── Scroll area: card grid ────────────────────────────────────────────
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setObjectName("CardScroll")
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._grid_widget = QWidget()
        self._grid_widget.setObjectName("GridWidget")
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setContentsMargins(16, 16, 16, 16)
        self._grid.setSpacing(14)

        self._scroll.setWidget(self._grid_widget)
        root.addWidget(self._scroll)

    def _apply_global_style(self):
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {_C['bg']};
                font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
            }}
            QFrame#TopHeader {{
                background-color: {_C['header_bg']};
                border-bottom: 1px solid {_C['card_border']};
            }}
            QLabel#DashTitle {{
                color: {_C['text_primary']};
                font-size: 16px;
                font-weight: bold;
            }}
            QLabel#StatsLabel {{
                color: {_C['text_secondary']};
                font-size: 13px;
            }}
            QLabel#ClockLabel {{
                color: {_C['accent']};
                font-size: 15px;
                font-weight: bold;
                font-family: monospace;
            }}
            QFrame#SubHeader {{
                background-color: {_C['bg']};
                border-bottom: 1px solid {_C['divider']};
            }}
            QLabel#OnlineLabel {{
                color: {_C['connected']};
                font-size: 12px;
                font-weight: bold;
            }}
            QLabel#OfflineLabel {{
                color: {_C['disconnected']};
                font-size: 12px;
                font-weight: bold;
            }}
            QLabel#ReconLabel {{
                color: {_C['reconnecting']};
                font-size: 12px;
                font-weight: bold;
            }}
            QWidget#GridWidget {{
                background-color: {_C['bg']};
            }}
            QScrollArea#CardScroll {{
                background-color: {_C['bg']};
                border: none;
            }}
            QScrollBar:vertical {{
                background: {_C['divider']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {_C['card_border']};
                border-radius: 4px;
            }}
        """)

    # ── Card management ──────────────────────────────────────────────────────

    def _add_card(self, machine_cfg: dict):
        card = MachineCard(machine_cfg)
        self._cards[machine_cfg['id']] = card

    def _relayout_cards(self):
        """วาง card ลง grid โดยคำนวณจำนวน column อัตโนมัติ"""
        # ล้าง grid ก่อน
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        n = len(self._cards)
        if n == 0:
            no_machine = QLabel("ไม่มีเครื่องที่กำหนดใน config.json\nกรุณาเพิ่ม 'machines' array")
            no_machine.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_machine.setStyleSheet(f"color: {_C['text_secondary']}; font-size: 14px;")
            self._grid.addWidget(no_machine, 0, 0)
            return

        cols = min(_GRID_COLS, n)
        for i, card in enumerate(self._cards.values()):
            row = i // cols
            col = i % cols
            self._grid.addWidget(card, row, col)

        # ยืด column ให้เท่ากัน
        for c in range(cols):
            self._grid.setColumnStretch(c, 1)

        # เพิ่ม row spacer ด้านล่าง
        self._grid.setRowStretch(math.ceil(n / cols), 1)

        total = len(self._cards)
        self.stats_lbl.setText(f"เครื่องทั้งหมด: {total}")

    # ── Slots ────────────────────────────────────────────────────────────────

    @Slot(str, dict)
    def _on_machine_data(self, machine_id: str, data: dict):
        card = self._cards.get(machine_id)
        if card:
            card.update_data(data)

    @Slot(str, str)
    def _on_machine_status(self, machine_id: str, status: str):
        card = self._cards.get(machine_id)
        if card:
            card.set_status(status)
        self._update_status_counts()

    def _update_status_counts(self):
        online = recon = offline = 0
        for card in self._cards.values():
            s = card._status
            if s == "connected":
                online += 1
            elif s == "reconnecting":
                recon += 1
            else:
                offline += 1

        self.online_lbl.setText(f"● Online: {online}")
        self.offline_lbl.setText(f"✕ Offline: {offline}")
        if recon > 0:
            self.recon_lbl.setText(f"⟳ Reconnecting: {recon}")
        else:
            self.recon_lbl.setText("")

    def _tick_clock(self):
        now = datetime.now()
        self.clock_lbl.setText(now.strftime("%H:%M:%S   %d/%m/%Y"))

    # ── Lifecycle ────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._monitor.stop()
        self._clock_timer.stop()
        self.closed.emit()
        super().closeEvent(event)
