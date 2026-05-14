"""
main.py
=======
จุดเริ่มต้นของแอปพลิเคชัน Smart OST

หน้าที่ของ MainWindow:
  - Orchestrate การสร้าง component ทั้งหมด (PLC, Login, ShotCounter, ฯลฯ)
  - จัดการ lifecycle: login → ทำงาน → logout / exit
  - ดูแล theme และ TCP status indicator
  - เชื่อม Signal ระหว่าง component

โครงสร้าง component:
  MainWindow
    ├── plc_window          : PLCWindow          — อ่านข้อมูลจาก PLC/Pi
    ├── login_manager       : LoginManager        — Login + Lot pre-check
    ├── shot_counter        : ShotCounter         — นับ shot count
    │     ├── excel_mgr     : ExcelManager        — บันทึก Excel + PM prediction
    │     └── pm_mgr        : PMManager           — PM workflow
    ├── graph_updater       : GraphUpdater        — อัพเดตกราฟ real-time
    ├── heat_map_defect     : HeatMapDefectPCS    — แผนที่ defect
    ├── update_data_manager : update_sever        — sync ข้อมูลไปยัง server
    ├── production_calculator: ProductionCalculator — คำนวณ production rate
    ├── data_uploader       : DataUploader        — อัพโหลดผลลัพธ์ไป DB
    └── sys_mgr             : SystemManager       — process/thread management
"""

# ─── Standard library ────────────────────────────────────────────────────────
import os
import sys
import time

# ─── Third-party ─────────────────────────────────────────────────────────────
import icons_rc

# ─── Qt ──────────────────────────────────────────────────────────────────────
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QLabel,
)
from PySide6.QtCore import Qt, Signal, QSettings, QCoreApplication, QLocale, Slot
from PySide6.QtGui import QFont, QKeySequence, QShortcut

# ─── Custom widgets ───────────────────────────────────────────────────────────
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomQToolTip import QCustomQToolTipFilter

# ─── UI file (auto-generated) ────────────────────────────────────────────────
from src.ui_interface import *

# ─── Application modules ─────────────────────────────────────────────────────
from src.config_manager import config_manager
from src.app_logger import get_logger
from src.PLCdata import PLCWindow
from src.login_manager import LoginManager
from src.shot_counting import ShotCounter
from src.heat_map_defect import HeatMapDefectPCS
from src.graph_updater import GraphUpdater
from src.update_data_manager import update_sever
from src.data_upload import DataUploader
from src.production_calculator import ProductionCalculator
from src.system_manager import SystemManager
from src.Functions import GuiFunctions
from src.flow_monitor import FlowMonitorDialog

log = get_logger("main")

# ─── MainWindow ──────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    theme_changed = Signal()
    product_info_updated = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.ui_config = self.config_manager.get_ui_config()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._is_closing_application = False
        self._logout_for_shutdown = False
        self.shot_counter = None
        self.theme_settings = None

        # ─── SystemManager — process/thread lifecycle ────────────────────
        self.sys_mgr = SystemManager(self)
        self.sys_mgr.kill_zombie_processes()

        self._initialization_complete = False
        self.is_logged_out = False
        self.logout_window = None
        self._is_handling_close = False

        try:
            self.plc_window = PLCWindow()
            self.data_upload = DataUploader()
            self.data_uploader = self.data_upload

            self.login_manager = LoginManager(self.plc_window, self)
            if not self.login_manager.login():
                self.close()
                return

            loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})
            QAppSettings.updateAppSettings(self)
            self.theme = getattr(self, 'theme', None)

            lot_number = self.get_current_lot_number()
            self.plc_window.set_current_lot_number(lot_number)
            product_data = self.login_manager.get_data_scan()

            if not product_data or not product_data.get('product_name'):
                log.error("Invalid product data — forcing re-login")
                self._handle_invalid_product_data()
                return

            self.shot_counter = ShotCounter(
                self.plc_window, self,
                lot_size_value=self.login_manager.product_info.get('lot_size_value'),
                product_data=product_data,
            )

            self.graph_updater = GraphUpdater(self.plc_window, self)
            self.heat_map_defect = HeatMapDefectPCS(self.plc_window, self)
            self.update_data_manager = update_sever(self.plc_window, self)
            self.production_calculator = ProductionCalculator(self.plc_window, self)
            self.production_calculator.start_calculation()

            self.product_info_updated.connect(self.heat_map_defect.set_product_info)

            self.update_label_with_product_info()
            self.force_reset_defect_data()

            self.app_functions = GuiFunctions(self)
            self.update_theme_settings()
            self.theme_changed.connect(self.update_theme_settings)

            self._setup_tcp_status_indicator()

            self._initialization_complete = True
            self._monitor_dialog    = None
            self._simulator_dialog  = None
            self._setup_flow_monitor_shortcut()
            self._setup_simulator_shortcut()
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.show()
            log.info("MainWindow initialization completed successfully")

        except Exception as e:
            log.exception("Error during MainWindow initialization: %s", e)
            self._handle_initialization_error(e)

    # ─── Defect data reset ────────────────────────────────────────────────────

    def force_reset_defect_data(self):
        """บังคับรีเซ็ตข้อมูล defect เมื่อเริ่มงานใหม่"""
        try:
            if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                self.heat_map_defect.result_all_by_pcs = {}
                self.heat_map_defect.result_defect_only = {}
                self.heat_map_defect.defect_data_for_heatmap = {}
                self.heat_map_defect.last_dm1923 = None
                self.heat_map_defect.last_shot_cnt = None
                self.heat_map_defect.first_dm1923_checked = False
                self.heat_map_defect.clear_heatmap()
                self.heat_map_defect.plot_stacked_bar_defects()
        except Exception as e:
            log.warning("Error force resetting defect data: %s", e)

    # ─── Error handlers ───────────────────────────────────────────────────────

    def _handle_invalid_product_data(self):
        """จัดการเมื่อข้อมูลผลิตภัณฑ์ไม่ถูกต้อง"""
        QMessageBox.critical(self, "Error", "Invalid product data. Please log in again.")
        self.close()
        self.sys_mgr.safe_restart()

    def _handle_initialization_error(self, error):
        """จัดการข้อผิดพลาดระหว่าง initialization"""
        QMessageBox.critical(
            self, "Initialization Error",
            f"An error occurred during program initialization:\n{error}\n\n"
            "The program will close automatically.",
        )
        self.sys_mgr.force_quit(1)

    # ─── Theme ────────────────────────────────────────────────────────────────

    def update_theme_settings(self):
        """อ่านค่าธีมปัจจุบันและสร้าง dict ของสีสำหรับ component อื่น"""
        settings = QSettings()
        current_theme_name = settings.value("THEME", "LightBlue")
        current_theme_data = {}

        for theme in self.ui.themes:
            if theme.name == current_theme_name:
                current_theme_data = {
                    "Background-color": getattr(theme, 'COLOR_BACKGROUND_1', '#FFFFFF'),
                    "Text-color":       getattr(theme, 'COLOR_TEXT_1',       '#000000'),
                    "Icons-color":      getattr(theme, 'COLOR_ACCENT_3',     '#666666'),
                    "Accent-color":     getattr(theme, 'COLOR_ACCENT_1',     '#26bae3'),
                    "Destructive-color":getattr(theme, 'COLOR_ACCENT_2',     '#E74C3C'),
                    "Secondary-text-color": getattr(theme, 'COLOR_TEXT_2',   '#666666'),
                    "Theme-name":       getattr(theme, 'name',               'Unknown'),
                }
                break

        self.theme_settings = current_theme_data
        log.debug("Theme settings updated: %s", current_theme_name)

    # ─── TCP status indicator ─────────────────────────────────────────────────

    def _setup_tcp_status_indicator(self):
        """เพิ่ม label แสดงสถานะ TCP ใน header (เฉพาะ TCP mode)"""
        from src.config_manager import config_manager as cm
        if cm.get_plc_config().get('connection_mode', 'serial') != 'tcp':
            self._tcp_status_label = None
            return

        self._tcp_status_label = QLabel("PLC: connecting…", self.ui.header)
        self._tcp_status_label.setFont(QFont("Arial", 9))
        self._tcp_status_label.setMinimumWidth(140)
        self._tcp_status_label.setAlignment(Qt.AlignCenter)
        self.ui.horizontalLayout_7.insertWidget(1, self._tcp_status_label)
        self.plc_window.tcp_status_changed.connect(self._on_tcp_status_changed)
        self._on_tcp_status_changed("reconnecting")

    # ─── Flow Monitor ─────────────────────────────────────────────────────────

    def _setup_flow_monitor_shortcut(self):
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+M"), self)
        shortcut.activated.connect(self._open_flow_monitor)

    @Slot()
    def _open_flow_monitor(self):
        if self._monitor_dialog and self._monitor_dialog.isVisible():
            self._monitor_dialog.raise_()
            self._monitor_dialog.activateWindow()
            return
        self._monitor_dialog = FlowMonitorDialog(self, parent=self)
        self._monitor_dialog.finished.connect(self._on_monitor_closed)
        self._monitor_dialog.show()

    @Slot()
    def _on_monitor_closed(self):
        self._monitor_dialog = None

    # ─── Simulator Control ────────────────────────────────────────────────────

    def _setup_simulator_shortcut(self):
        if not config_manager.current_config.get('mock_mode', False):
            return
        shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        shortcut.activated.connect(self._open_simulator_control)

    @Slot()
    def _open_simulator_control(self):
        if self._simulator_dialog and self._simulator_dialog.isVisible():
            self._simulator_dialog.raise_()
            self._simulator_dialog.activateWindow()
            return
        from src.simulator_control import SimulatorControlPanel
        self._simulator_dialog = SimulatorControlPanel(self, parent=self)
        self._simulator_dialog.finished.connect(self._on_simulator_closed)
        self._simulator_dialog.show()

    @Slot()
    def _on_simulator_closed(self):
        self._simulator_dialog = None

    @Slot(str)
    def _on_tcp_status_changed(self, status: str):
        """อัพเดตสี/ข้อความ TCP status label"""
        if not self._tcp_status_label:
            return
        mapping = {
            "connected":    ("PLC: connected",    "#27ae60"),
            "disconnected": ("PLC: disconnected",  "#e74c3c"),
            "reconnecting": ("PLC: reconnecting…", "#f39c12"),
        }
        text, color = mapping.get(status, ("PLC: unknown", "#888888"))
        self._tcp_status_label.setText(text)
        self._tcp_status_label.setStyleSheet(
            f"color: white; background: {color}; border-radius: 4px; padding: 2px 6px;"
        )

    # ─── Logout ───────────────────────────────────────────────────────────────

    def show_logout_window(self):
        """แสดงหน้าต่าง Logout"""
        try:
            from src.logout_window import LogoutWindow
            self.logout_window = LogoutWindow(
                parent=self,
                shot_counter=self.shot_counter,
                theme_settings=self.theme_settings,
                data_uploader=self.data_uploader,
            )
            self.logout_window.logout_completed.connect(self.handle_logout_completed)
            self.theme_changed.connect(self.update_logout_window_theme)
            self.logout_window.show()
        except Exception as e:
            log.exception("Error showing logout window: %s", e)

    @Slot()
    def handle_logout_completed(self):
        """จัดการเมื่อ logout สำเร็จ"""
        try:
            log.info("Logout completed signal received")
            self.is_logged_out = True

            if self.logout_window and self.logout_window.isVisible():
                self.logout_window.close()
                self.logout_window = None

            if self._logout_for_shutdown:
                log.info("Logout completed for application shutdown")
                self._logout_for_shutdown = False
                self._is_closing_application = True
                self._cleanup_before_exit()
                try:
                    QCoreApplication.quit()
                finally:
                    os._exit(0)
            else:
                log.info("Normal logout — restarting application")
                self._cleanup_heatmap()
                self.sys_mgr.safe_restart()

        except Exception as e:
            log.exception("Error handling logout completion: %s", e)
            self.sys_mgr.force_quit(1)

    def update_logout_window_theme(self):
        """อัพเดตธีมใน LogoutWindow เมื่อธีมเปลี่ยน"""
        if hasattr(self, 'logout_window') and self.logout_window:
            self.logout_window.theme_settings = self.theme_settings
            self.logout_window.update_icons()

    # ─── Heatmap cleanup ─────────────────────────────────────────────────────

    def _cleanup_heatmap(self):
        """ปล่อย HeatMapDefectPCS และ disconnect signals"""
        if not (hasattr(self, 'heat_map_defect') and self.heat_map_defect):
            return
        try:
            if hasattr(self.heat_map_defect, 'stop'):
                try:
                    self.heat_map_defect.stop()
                except Exception:
                    pass
            if hasattr(self.heat_map_defect, 'close'):
                try:
                    self.heat_map_defect.close()
                except Exception:
                    pass
            try:
                self.product_info_updated.disconnect(self.heat_map_defect.set_product_info)
            except Exception:
                pass
            self.heat_map_defect = None
        except Exception as e:
            log.warning("Error cleaning up heat map: %s", e)

    # ─── Cleanup / exit ───────────────────────────────────────────────────────

    def _cleanup_before_exit(self):
        """ทำความสะอาดก่อนปิดแอป"""
        try:
            log.info("Cleaning up before exit")
            self.sys_mgr.stop_all_threads_and_timers()
            if hasattr(self, 'plc_window') and self.plc_window:
                try:
                    if hasattr(self.plc_window, 'close_connection'):
                        self.plc_window.close_connection()
                    self.plc_window.close()
                except Exception as e:
                    log.warning("Error closing PLC: %s", e)
            self._cleanup_heatmap()
            if hasattr(self, 'shot_counter') and self.shot_counter:
                self.shot_counter = None
            time.sleep(0.5)
        except Exception as e:
            log.warning("Error during cleanup before exit: %s", e)

    def closeEvent(self, event):
        """จัดการการปิดหน้าต่างหลัก"""
        try:
            if self._is_handling_close:
                event.ignore()
                return

            if not self.is_logged_out:
                reply = QMessageBox.question(
                    self,
                    "Confirm Exit",
                    "Do you want to exit without finishing the Lot?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.Yes:
                    log.info("User confirmed exit without finishing lot")
                    if hasattr(self, 'shot_counter') and self.shot_counter:
                        try:
                            self.shot_counter._save_shot_count()
                        except Exception as e:
                            log.warning("Error saving shot count: %s", e)
                    self._cleanup_before_exit()
                    event.accept()
                else:
                    event.ignore()
                return

            self._cleanup_before_exit()
            event.accept()

        except Exception as e:
            log.exception("Error in closeEvent: %s", e)
            self.sys_mgr.force_quit(1)

    # ─── Forced logout ────────────────────────────────────────────────────────

    def force_logout_before_exit(self):
        """บังคับให้ผู้ใช้ทำการ logout ก่อนออกจากโปรแกรม"""
        try:
            if hasattr(self, 'force_logout_dialog') and self.force_logout_dialog:
                self.force_logout_dialog.activateWindow()
                return

            from src.logout_window import LogoutWindow
            self.force_logout_dialog = LogoutWindow(
                parent=self,
                shot_counter=self.shot_counter,
                theme_settings=self.theme_settings,
                data_uploader=self.data_uploader,
            )
            self.force_logout_dialog.setAttribute(Qt.WA_DeleteOnClose)
            self.force_logout_dialog.setWindowModality(Qt.ApplicationModal)
            self.force_logout_dialog.logout_completed.connect(
                self.handle_forced_logout_completion
            )
            self.force_logout_dialog.destroyed.connect(
                self.handle_forced_logout_closed
            )
            self.force_logout_dialog.show()

        except Exception as e:
            log.exception("Error forcing logout: %s", e)
            self._is_handling_close = False
            self._logout_for_shutdown = False
            self.sys_mgr.force_quit()

    @Slot()
    def handle_forced_logout_closed(self):
        """ถูกเรียกเมื่อหน้าต่าง force_logout_dialog ถูกปิดโดยไม่ได้ logout"""
        self.force_logout_dialog = None
        if not self.is_logged_out:
            log.info("User canceled forced logout — resetting close state")
            self._is_handling_close = False
            self._logout_for_shutdown = False

    @Slot()
    def handle_forced_logout_completion(self):
        """จัดการเมื่อบังคับ logout สำเร็จ (clean shutdown)"""
        try:
            log.info("Forced logout completed — clean shutdown start")
            self.is_logged_out = True
            self._is_handling_close = False

            try:
                self.sys_mgr.stop_all_threads_and_timers()
            except Exception as e:
                log.warning("Error stopping threads/timers: %s", e)

            try:
                self._cleanup_heatmap()
            except Exception as e:
                log.warning("Error cleaning heat_map_defect: %s", e)

            try:
                if hasattr(self, 'plc_window') and self.plc_window:
                    if hasattr(self.plc_window, 'close_connection'):
                        try:
                            self.plc_window.close_connection()
                        except Exception:
                            pass
                    try:
                        self.plc_window.close()
                    except Exception:
                        pass
                    self.plc_window = None
            except Exception as e:
                log.warning("Error closing plc_window: %s", e)

            try:
                self._cleanup_before_exit()
            except Exception as e:
                log.warning("_cleanup_before_exit error: %s", e)

            try:
                QCoreApplication.quit()
            finally:
                os._exit(0)

        except Exception as e:
            log.exception("Fatal error in forced logout handler: %s", e)
            self._is_handling_close = False
            try:
                QCoreApplication.quit()
            finally:
                os._exit(1)

    # ─── Product / Lot info ───────────────────────────────────────────────────

    def get_current_lot_number(self):
        user_info = self.login_manager.get_user_info()
        product_info = self.login_manager.get_data_scan()

        lot_number = None
        if user_info and 'lot_number' in user_info:
            lot_number = user_info['lot_number']
        elif product_info and 'lot_number' in product_info:
            lot_number = product_info['lot_number']
        return lot_number

    def update_label_with_product_info(self):
        try:
            get_data_login = self.login_manager.get_data_scan()
            if get_data_login:
                product_name  = get_data_login.get('product_name',  'N/A')
                lot_number    = get_data_login.get('lot_number',    'N/A')
                tooling_code  = get_data_login.get('tooling_code',  'N/A')
                operator_name = get_data_login.get('operator_name', 'N/A')
                operator_id   = get_data_login.get('operator_id',   'N/A')

                self.ui.product_name.setText(f": {product_name}")
                self.ui.lot_number.setText(f": {lot_number}")
                self.ui.tooling_code.setText(f": {tooling_code}")
                self.ui.operator_name.setText(f": {operator_name}")

                self.product_info_updated.emit({
                    'product_name': product_name,
                    'lot_number':   lot_number,
                    'tooling_code': tooling_code,
                    'operator_name':operator_name,
                    'operator_id':  operator_id,
                })
            else:
                log.error("No product data found")
                self.ui.product_name.setText("Error: No data found.")
        except Exception as e:
            log.exception("Error retrieving product scan: %s", e)
            self.ui.product_name.setText(f"Error: {e}")

    # ─── Misc ─────────────────────────────────────────────────────────────────

    def sassCompilationProgress(self, n):
        self.ui.activityProgress.setValue(n)


########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))

    app = QApplication(sys.argv)

    try:
        app_tooltip_filter = QCustomQToolTipFilter(tailPosition="auto")
        app.installEventFilter(app_tooltip_filter)
        app.setQuitOnLastWindowClosed(True)

        window = MainWindow()
        if window.isVisible():
            window.show()

        if hasattr(window, '_initialization_complete') and window._initialization_complete:
            log.info("Application started successfully")
            app_exec = app.exec()
        else:
            log.error("Application initialization failed")
            app_exec = 1

        log.info("Application is shutting down")

    except Exception as e:
        log.exception("Fatal error: %s", e)
        app_exec = 1

    finally:
        try:
            app.removeEventFilter(app_tooltip_filter)
        except Exception:
            pass
        os._exit(app_exec)
