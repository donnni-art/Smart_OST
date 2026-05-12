"""
simulator_control.py
====================
Control Panel สำหรับ SimulatedPLCWorker — ใช้เมื่อ mock_mode = true

เปิดจาก MainWindow ด้วย Ctrl+Shift+S

UI:
  ┌─────────────────────────────────────────────────────┐
  │  [⚙ SIMULATOR MODE]  mock_mode = true               │
  ├────────────────────────┬────────────────────────────┤
  │  Configuration         │  Scenarios                 │
  │  Shot interval  [────] │  [▶ Resume / ⏸ Pause]     │
  │  1000 ms               │  [📶 Disconnect (5s)]      │
  │  Defect rate   [────]  │  [⚡ High Defect (10s)]    │
  │  5 %                   │  [🔧 Jump to PM]           │
  │  Shots/sheet   [4  ↕]  ├────────────────────────────┤
  │  PCS/shot      [2  ↕]  │  Live Status               │
  │                        │  Sheet : 0                  │
  │                        │  Shot  : 0                  │
  │                        │  PLC   : ● Connected        │
  └────────────────────────┴────────────────────────────┘
"""

from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSlider, QSpinBox, QVBoxLayout,
)

from src.app_logger import get_logger
from src.config_manager import config_manager

log = get_logger("sim_ctrl")


class SimulatorControlPanel(QDialog):
    """UI ควบคุม SimulatedPLCWorker แบบ real-time"""

    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self._main = main_window

        # ดึง worker จาก plc_window (ต้องเป็น SimulatedPLCWorker)
        plc = getattr(main_window, 'plc_window', None)
        self._worker = getattr(plc, 'worker', None)

        self.setWindowTitle("Smart OST — Simulator Control")
        self.setMinimumWidth(560)
        self.setMinimumHeight(380)
        self.setAttribute(Qt.WA_DeleteOnClose, False)

        self._setup_ui()

        self._status_timer = QTimer(self)
        self._status_timer.setInterval(500)
        self._status_timer.timeout.connect(self._refresh_status)
        self._status_timer.start()
        self._refresh_status()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        # ── banner ────────────────────────────────────────────────────────────
        banner = QLabel("⚙  SIMULATOR MODE  —  mock_mode = true")
        banner.setFont(QFont("Arial", 12, QFont.Bold))
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet(
            "background: #f39c12; color: white; border-radius: 6px; padding: 6px 12px;"
        )
        root.addWidget(banner)

        # ── body: config left | scenarios+status right ────────────────────────
        body = QHBoxLayout()
        body.setSpacing(10)
        root.addLayout(body)

        body.addWidget(self._build_config_group(),   stretch=5)
        body.addWidget(self._build_right_column(),   stretch=4)

        # ── close ─────────────────────────────────────────────────────────────
        btn_bar = QHBoxLayout()
        btn_bar.addStretch()
        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(80)
        close_btn.clicked.connect(self.close)
        btn_bar.addWidget(close_btn)
        root.addLayout(btn_bar)

    # ── config group ──────────────────────────────────────────────────────────

    def _build_config_group(self) -> QGroupBox:
        grp = QGroupBox("Configuration")
        g   = QGridLayout(grp)
        g.setVerticalSpacing(10)
        g.setHorizontalSpacing(8)

        # shot interval
        g.addWidget(QLabel("Shot interval"), 0, 0)
        self._interval_slider = QSlider(Qt.Horizontal)
        self._interval_slider.setRange(100, 10000)
        self._interval_slider.setSingleStep(100)
        initial_ms = getattr(self._worker, 'shot_interval_ms', 1000)
        self._interval_slider.setValue(initial_ms)
        self._interval_slider.valueChanged.connect(self._on_interval_changed)
        g.addWidget(self._interval_slider, 1, 0, 1, 2)

        self._interval_label = QLabel(f"{initial_ms} ms")
        self._interval_label.setAlignment(Qt.AlignRight)
        g.addWidget(self._interval_label, 0, 1)

        g.addWidget(_divider(), 2, 0, 1, 2)

        # defect rate
        g.addWidget(QLabel("Defect rate"), 3, 0)
        self._defect_slider = QSlider(Qt.Horizontal)
        self._defect_slider.setRange(0, 50)
        initial_pct = int(getattr(self._worker, 'defect_rate', 0.05) * 100)
        self._defect_slider.setValue(initial_pct)
        self._defect_slider.valueChanged.connect(self._on_defect_changed)
        g.addWidget(self._defect_slider, 4, 0, 1, 2)

        self._defect_label = QLabel(f"{initial_pct} %")
        self._defect_label.setAlignment(Qt.AlignRight)
        g.addWidget(self._defect_label, 3, 1)

        g.addWidget(_divider(), 5, 0, 1, 2)

        # shots per sheet
        g.addWidget(QLabel("Shots / sheet"), 6, 0)
        self._shot_spin = QSpinBox()
        self._shot_spin.setRange(1, 16)
        self._shot_spin.setValue(getattr(self._worker, 'shot_number', 4))
        self._shot_spin.valueChanged.connect(self._on_shot_number_changed)
        g.addWidget(self._shot_spin, 6, 1)

        # pcs per shot
        g.addWidget(QLabel("PCS / shot"), 7, 0)
        self._pcs_spin = QSpinBox()
        self._pcs_spin.setRange(1, 8)
        self._pcs_spin.setValue(getattr(self._worker, 'pcs_number', 2))
        self._pcs_spin.valueChanged.connect(self._on_pcs_number_changed)
        g.addWidget(self._pcs_spin, 7, 1)

        return grp

    # ── right column ──────────────────────────────────────────────────────────

    def _build_right_column(self) -> QVBoxLayout:
        col = QVBoxLayout()
        col.setSpacing(8)

        col.addWidget(self._build_scenarios_group())
        col.addWidget(self._build_status_group())

        wrapper = QFrame()
        wrapper.setLayout(col)
        return wrapper

    def _build_scenarios_group(self) -> QGroupBox:
        grp = QGroupBox("Scenarios")
        v   = QVBoxLayout(grp)
        v.setSpacing(6)

        self._pause_btn = QPushButton("⏸  Pause")
        self._pause_btn.setCheckable(True)
        self._pause_btn.clicked.connect(self._on_pause_toggled)
        v.addWidget(self._pause_btn)

        disc_btn = QPushButton("📶  Disconnect PLC (5 s)")
        disc_btn.clicked.connect(self._on_disconnect)
        v.addWidget(disc_btn)

        defect_btn = QPushButton("⚡  High Defect (10 s)")
        defect_btn.clicked.connect(self._on_inject_defect)
        v.addWidget(defect_btn)

        pm_btn = QPushButton("🔧  Jump to PM")
        pm_btn.clicked.connect(self._on_jump_to_pm)
        v.addWidget(pm_btn)

        return grp

    def _build_status_group(self) -> QGroupBox:
        grp = QGroupBox("Live Status")
        g   = QGridLayout(grp)
        g.setVerticalSpacing(6)

        g.addWidget(QLabel("Total sheet :"), 0, 0)
        self._lbl_sheet = QLabel("0")
        self._lbl_sheet.setFont(QFont("Arial", 10, QFont.Bold))
        g.addWidget(self._lbl_sheet, 0, 1)

        g.addWidget(QLabel("Shot count  :"), 1, 0)
        self._lbl_shot = QLabel("0")
        self._lbl_shot.setFont(QFont("Arial", 10, QFont.Bold))
        g.addWidget(self._lbl_shot, 1, 1)

        g.addWidget(QLabel("PLC status  :"), 2, 0)
        self._lbl_plc = QLabel("—")
        self._lbl_plc.setFont(QFont("Arial", 10, QFont.Bold))
        g.addWidget(self._lbl_plc, 2, 1)

        g.addWidget(QLabel("Defect total:"), 3, 0)
        self._lbl_defect = QLabel("0")
        self._lbl_defect.setFont(QFont("Arial", 10, QFont.Bold))
        g.addWidget(self._lbl_defect, 3, 1)

        return grp

    # ── config callbacks ──────────────────────────────────────────────────────

    @Slot(int)
    def _on_interval_changed(self, value: int):
        self._interval_label.setText(f"{value} ms")
        if self._worker:
            self._worker.shot_interval_ms = value

    @Slot(int)
    def _on_defect_changed(self, value: int):
        self._defect_label.setText(f"{value} %")
        if self._worker:
            self._worker.defect_rate = value / 100.0

    @Slot(int)
    def _on_shot_number_changed(self, value: int):
        if self._worker:
            self._worker.shot_number = value

    @Slot(int)
    def _on_pcs_number_changed(self, value: int):
        if self._worker:
            self._worker.pcs_number = value

    # ── scenario callbacks ────────────────────────────────────────────────────

    @Slot(bool)
    def _on_pause_toggled(self, checked: bool):
        if self._worker:
            self._worker.is_paused = checked
        self._pause_btn.setText("▶  Resume" if checked else "⏸  Pause")
        log.info("SIM: %s", "paused" if checked else "resumed")

    @Slot()
    def _on_disconnect(self):
        if not self._worker:
            return
        self._worker.is_disconnected = True
        log.info("SIM: PLC disconnected for 5s")
        QTimer.singleShot(5000, self._reconnect)

    def _reconnect(self):
        if self._worker:
            self._worker.is_disconnected = False
        log.info("SIM: PLC reconnected")

    @Slot()
    def _on_inject_defect(self):
        if self._worker:
            self._worker.inject_high_defect(duration_s=10.0)

    @Slot()
    def _on_jump_to_pm(self):
        if not self._worker:
            return
        sc = getattr(self._main, 'shot_counter', None)
        current = getattr(sc, 'shot_count', 0) if sc else 0
        self._worker.trigger_jump_to_pm(current_shot_count=current)

    # ── status refresh ────────────────────────────────────────────────────────

    @Slot()
    def _refresh_status(self):
        if not self._worker:
            return

        plc = getattr(self._main, 'plc_window', None)
        sc  = getattr(self._main, 'shot_counter', None)

        self._lbl_sheet.setText(str(getattr(self._worker, '_total_sheet', 0)))
        self._lbl_shot.setText(
            f"{getattr(sc, 'shot_count', 0):,}" if sc else "—"
        )

        # PLC connection dot
        disconnected = getattr(self._worker, 'is_disconnected', False)
        paused       = getattr(self._worker, 'is_paused',       False)
        if disconnected:
            dot, color = "● Disconnected", "#e74c3c"
        elif paused:
            dot, color = "⏸ Paused",       "#f39c12"
        else:
            dot, color = "● Connected",    "#27ae60"
        self._lbl_plc.setText(dot)
        self._lbl_plc.setStyleSheet(f"color: {color};")

        # defect total
        accum = getattr(self._worker, '_defect_accum', {})
        self._lbl_defect.setText(str(sum(accum.values())))

    # ── lifecycle ─────────────────────────────────────────────────────────────

    def closeEvent(self, event):
        self._status_timer.stop()
        super().closeEvent(event)


# ── helpers ───────────────────────────────────────────────────────────────────

def _divider() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.HLine)
    f.setStyleSheet("color: #ddd;")
    return f
