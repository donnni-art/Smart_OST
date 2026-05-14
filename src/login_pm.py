import sys, os
import time
from PySide6.QtWidgets import QDialog, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPainter, QPixmap, QIcon, QMouseEvent, QCursor
from PySide6.QtCore import Qt, QSize, Signal, QEasingCurve, QPoint, QTimer, QPropertyAnimation,QEvent

from src.app_logger import get_logger
from src.ui_LoginPM import Ui_PM_SYSTEM
from src.ui_pm_popupScanRepair import Ui_Scanrepair  # ✅ Import popup UI
from src.ui_pm_popupScanLeader import Ui_Scanleader 
from Custom_Widgets import loadJsonStyle
from src.custom_warning_dialog import CustomWarningDialog
from src.data_upload import DataUploader

log = get_logger("login_pm")

class LeaderLoginDialog(QDialog):
    """Popup for scanning Leader ID (no database verification required)"""
    
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.ui = Ui_Scanleader()
        self.ui.setupUi(self)
        self.main_window = main_window
        
        # ✅ Store leader data
        self.name_leader = ""
        self.position_level = ""
        self.leader_id = ""
        self.scanned_data = ""

        # ===== Window settings =====
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_active = False
        self._drag_position = QPoint()

        # ===== Shadow effect =====
        self._apply_shadow_effect()

        # ===== Connect buttons =====
        self.ui.pushButton_D.clicked.connect(self.reject)
        self.ui.confirmID.clicked.connect(self.verify_leader)
        self.ui.Refresh_scanleader.clicked.connect(self.clear_scan)

        # ===== Setup LineEdit =====
        self.leader_input = self.ui.lineEdit
        self.leader_input.setPlaceholderText("Leader Scan ID...")
        self.leader_input.installEventFilter(self)
        self.leader_input.setFocus()

        # ===== Setup ComboBox and name display =====
        self.position_combo = self.ui.comboBox
        self.name_display = self.ui.scan_leader
        self.name_display.setReadOnly(False)  # ✅ Allow name input

        # ===== Connect theme signals from Main =====
        if self.main_window and hasattr(self.main_window, 'theme_changed'):
            self.main_window.theme_changed.connect(self.update_theme)

        # ===== Load initial theme =====
        self.update_theme()

        # ===== Fade-in animation =====
        QTimer.singleShot(50, self._fade_in_animation)

    def _apply_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)

    def _fade_in_animation(self):
        """Fade-in animation when opening Dialog"""
        self.setWindowOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_anim.start()

    def update_theme(self):
        """Automatic theme update"""
        log.debug("LeaderLoginDialog: Theme update triggered.")
        
        # ✅ Load JSON style
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/dialog_style.json"})

        if not hasattr(self.main_window, "theme_settings") or not self.main_window.theme_settings:
            if hasattr(self.main_window, "update_theme_settings"):
                self.main_window.update_theme_settings()

        self.update_all_icons()

    def update_all_icons(self):
        """Update icon colors to match Theme"""
        if not self.main_window or not hasattr(self.main_window, 'theme_settings'):
            log.warning("LeaderLoginDialog: No theme settings found, using default colors")
            theme_settings = {
                "Icons-color": "#4A4A4A",
                "Accent-color": "#26bae3"
            }
        else:
            theme_settings = self.main_window.theme_settings

        icons_color = theme_settings.get('Icons-color', '#4A4A4A')
        accent_color = theme_settings.get('Accent-color', '#26bae3')
        
        # 🟦 Main icon
        self.ui.icon.setPixmap(
            self._create_colored_pixmap(":/feather/icons/feather/user-check.png", 
                                      accent_color, QSize(80, 80))
        )

        # 🟩 Various buttons
        self._update_button_icon(self.ui.Refresh_scanleader, ":/feather/icons/feather/refresh-ccw.png", icons_color)
        self._update_button_icon(self.ui.confirmID, ":/feather/icons/feather/check.png", icons_color)
        self._update_button_icon(self.ui.pushButton_D, ":/feather/icons/feather/x-circle.png", icons_color)

        log.debug("LeaderLoginDialog: Icons recolored -> %s", icons_color)

    def _update_button_icon(self, button, icon_path, color_hex):
        pixmap = self._create_colored_pixmap(icon_path, color_hex, QSize(20, 20))
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(20, 20))

    def _create_colored_pixmap(self, icon_path: str, color_hex: str, size: QSize = None) -> QPixmap:
        """Create QPixmap with recolored theme"""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            log.warning("Missing icon resource: %s", icon_path)
            return QPixmap()

        if size:
            pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(tinted.rect(), QColor(color_hex))
        painter.end()
        return tinted

    def verify_leader(self):
        """Verify that all fields are filled (no database verification required)"""
        leader_id = self.leader_input.text().strip()
        leader_name = self.name_display.text().strip()
        position_level = self.position_combo.currentText()
        
        # ✅ Verify all fields are filled
        if not leader_id:
            self._show_custom_warning("Please enter Leader ID", "Incomplete Information")
            self.leader_input.setFocus()
            return
            
        if not leader_name:
            self._show_custom_warning("Please enter Leader name", "Incomplete Information")
            self.name_display.setFocus()
            return
            
        if not position_level:
            self._show_custom_warning("Please select position", "Incomplete Information")
            self.position_combo.setFocus()
            return

        # ✅ Store entered data
        self.name_leader = leader_name
        self.position_level = position_level
        self.leader_id = leader_id
        self.scanned_data = leader_id
        
        log.info("Leader information collected: %s, Position: %s", self.name_leader, self.position_level)
        
        # ✅ Show success message
        self._show_success_message()

    def _show_success_message(self):
        """Show Custom Warning Dialog for successful entry"""
        success_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=f"Leader login completed!\nName: {self.name_leader}\nPosition: {self.position_level}",
            title="Leader Verification Completed",
            is_success=True  # ✅ Parameter to show as success message
        )
        
        # ✅ Close this dialog when success dialog closes
        success_dialog.finished.connect(lambda: self.accept())
        success_dialog.exec()

    def _show_custom_warning(self, message, title):
        """Show Custom Warning Dialog"""
        warning_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=message,
            title=title
        )
        
        # ✅ Focus back to scan field when warning dialog closes
        warning_dialog.finished.connect(self._on_warning_closed)
        warning_dialog.exec()

    def _on_warning_closed(self):
        """Handle after Warning Dialog closes"""
        self.leader_input.setFocus()

    def clear_scan(self):
        """Clear entered data"""
        self.leader_input.clear()
        self.name_display.clear()
        self.position_combo.setCurrentIndex(0)
        self.leader_input.setPlaceholderText("Leader Scan ID...")
        self.leader_input.setFocus()

    def get_leader_data(self):
        """Return entered data"""
        return {
            'scanned_data': self.scanned_data,
            'name_leader': self.name_leader,
            'position_level': self.position_level,
            'leader_id': self.leader_id
        }

    def eventFilter(self, obj, event):
        """Handle Enter key events"""
        if obj == self.leader_input and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.verify_leader()
                return True
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        """Override showEvent for animation"""
        super().showEvent(event)
        self._fade_in_animation()

    # ==========================================================
    # 🖱️ Support Frameless window dragging
    # ==========================================================
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_active = False


class RepairLoginDialog(QDialog):
    """Popup for scanning Repair Staff ID"""
    
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.ui = Ui_Scanrepair()
        self.ui.setupUi(self)
        self.main_window = main_window
        
        # ✅ Store staff data
        self.name_staff = ""
        self.pm_date = ""
        self.pm_time = ""
        self.scanned_data = ""

        # ===== Window settings =====
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self._drag_active = False
        self._drag_position = QPoint()

        # ===== Shadow effect =====
        self._apply_shadow_effect()

        # ===== Connect buttons =====
        self.ui.pushButton_D.clicked.connect(self.reject)
        self.ui.confirmID.clicked.connect(self.verify_repair_staff)
        self.ui.Refresh_scan.clicked.connect(self.clear_scan)

        # ===== Setup LineEdit =====
        self.id_repair = self.ui.scan_repair  # ✅ Use id_repair from UI
        self.id_repair.setPlaceholderText("Scan the ID here...")
        self.id_repair.installEventFilter(self)
        self.id_repair.setFocus()

        # ===== Connect theme signals from Main =====
        if self.main_window and hasattr(self.main_window, 'theme_changed'):
            self.main_window.theme_changed.connect(self.update_theme)

        # ===== Load initial theme =====
        self.update_theme()

        # ===== Fade-in animation =====
        self.show()
        QTimer.singleShot(50, self._fade_in_animation)

    def _apply_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)

    def _fade_in_animation(self):
        """Fade-in animation when opening Dialog"""
        self.setWindowOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_anim.start()

    def update_theme(self):
        """Automatic theme update"""
        log.debug("RepairLoginDialog: Theme update triggered.")
        
        # ✅ Load JSON style same as LoginPM
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/dialog_style.json"})

        if not hasattr(self.main_window, "theme_settings") or not self.main_window.theme_settings:
            if hasattr(self.main_window, "update_theme_settings"):
                self.main_window.update_theme_settings()

        self.update_all_icons()

    def update_all_icons(self):
        """Update icon colors to match Theme"""
        if not self.main_window or not hasattr(self.main_window, 'theme_settings'):
            log.warning("RepairLoginDialog: No theme settings found, using default colors")
            theme_settings = {
                "Icons-color": "#4A4A4A",
                "Accent-color": "#26bae3"
            }
        else:
            theme_settings = self.main_window.theme_settings

        icons_color = theme_settings.get('Icons-color', '#4A4A4A')
        accent_color = theme_settings.get('Accent-color', '#26bae3')
        
        # 🟦 Main icon (use accent color)
        self.ui.icon.setPixmap(
            self._create_colored_pixmap(":/material_design/icons/material_design/people_outline.png", 
                                      accent_color, QSize(80, 80))
        )

        # 🟩 Various buttons (use icons color)
        self._update_button_icon(self.ui.Refresh_scan, ":/feather/icons/feather/refresh-ccw.png", icons_color)
        self._update_button_icon(self.ui.confirmID, ":/feather/icons/feather/check.png", icons_color)
        self._update_button_icon(self.ui.pushButton_D, ":/feather/icons/feather/x-circle.png", icons_color)

        log.debug("RepairLoginDialog: Icons recolored -> %s", icons_color)

    def _update_button_icon(self, button, icon_path, color_hex):
        pixmap = self._create_colored_pixmap(icon_path, color_hex, QSize(20, 20))
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(20, 20))

    def _create_colored_pixmap(self, icon_path: str, color_hex: str, size: QSize = None) -> QPixmap:
        """Create QPixmap with recolored theme"""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            log.warning("Missing icon resource: %s", icon_path)
            return QPixmap()

        if size:
            pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(tinted.rect(), QColor(color_hex))
        painter.end()
        return tinted

    def verify_repair_staff(self):
        """Verify Repair Staff ID from database"""
        staff_id = self.id_repair.text().strip()
        
        if not staff_id:
            self._show_custom_warning("Please scan staff card", "Incomplete Information")
            return

        # ✅ Validate data_upload connection
        if not self._validate_data_upload_connection():
            return

        try:
            log.debug("Checking staff ID: %s", staff_id)
            
            if hasattr(self.main_window, 'data_upload'):
                data_upload_obj = self.main_window.data_upload
            else:
                log.error("No data_upload available in parent")
                self._show_custom_warning("Database system not available", "System Error")
                return
            
            # ✅ Call ID verification function
            is_allowed, staff_data = data_upload_obj.check_id_staff_employee(staff_id)
            
            log.debug("Verification result - Allowed: %s, Data: %s", is_allowed, staff_data)
            
            if is_allowed and staff_data:
                # ✅ Store verification data
                self.name_staff = staff_data.get('name', '')
                self.pm_date = staff_data.get('scan_date', '')
                self.pm_time = staff_data.get('scan_time', '')
                self.scanned_data = staff_id
                
                log.info("Staff verified: %s, Date: %s, Time: %s", self.name_staff, self.pm_date, self.pm_time)
                self.accept()
            else:
                self._show_custom_warning(
                    f"Staff data not found in system\nID: {staff_id}\nPlease scan staff card again", 
                    "Invalid Data"
                )
                self.clear_scan()
                
        except AttributeError as e:
            log.error("AttributeError in verify_repair_staff: %s", e)
            self._show_custom_warning("ID verification function not available", "System Error")
        except Exception as e:
            log.error("Unexpected error in verify_repair_staff: %s", e)
            self._show_custom_warning("Error occurred during data verification", "System Error")

    def _validate_data_upload_connection(self):
        """Validate data_upload connection"""
        try:
            if not self.main_window:
                log.error("No main_window reference")
                self._show_custom_warning("Cannot connect to main system", "System Error")
                return False

            if not hasattr(self.main_window, 'data_upload'):
                log.error("main_window has no data_upload attribute")
                self._show_custom_warning("Database system not available", "System Error")
                return False

            if not self.main_window.data_upload:
                log.error("data_upload is None")
                self._show_custom_warning("Database system is invalid", "System Error")
                return False

            return True
            
        except Exception as e:
            log.error("Error validating data_upload connection: %s", e)
            self._show_custom_warning("Database connection issue", "System Error")
            return False

    def _show_custom_warning(self, message, title):
        """Show Custom Warning Dialog"""
        warning_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=message,
            title=title
        )
        
        # ✅ Focus back to scan field when warning dialog closes
        warning_dialog.finished.connect(self._on_warning_closed)
        warning_dialog.exec()

    def _on_warning_closed(self):
        """Handle after Warning Dialog closes"""
        # ✅ Focus back to scan field for new input
        self.id_repair.setFocus()
        # ✅ Select all text for easy overwriting
        self.id_repair.selectAll()

    def clear_scan(self):
        """Clear scan data"""
        self.id_repair.clear()
        self.id_repair.setPlaceholderText("Scan the ID here...")
        self.id_repair.setFocus()

    def get_repair_data(self):
        """Return scan data"""
        return {
            'scanned_data': self.scanned_data,
            'name_staff': self.name_staff,
            'pm_date': self.pm_date,
            'pm_time': self.pm_time
        }

    def eventFilter(self, obj, event):
        """Handle Enter key events"""
        if obj == self.id_repair and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                self.verify_repair_staff()
                return True
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        """Override showEvent for animation"""
        super().showEvent(event)
        self._fade_in_animation()

    # ==========================================================
    # 🖱️ Support Frameless window dragging
    # ==========================================================
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_active = False

class LoginPM(QDialog):
    login_completed = Signal(dict)
    request_restart = Signal()  # ✅ New signal for restart request
    restart_requested = Signal()
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.ui = Ui_PM_SYSTEM()
        self.ui.setupUi(self)
        self.main_window = main_window
        self.login_successful = False 


        # ===== Main window settings =====
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.fade_anim = None
        self._drag_active = False
        self._drag_position = QPoint()

        # ===== Login status variables =====
        self.repair_logged_in = False
        self.repair_data = None
        self.leader_logged_in = False
        self.leader_data = None 

        # ===== Shadow effect for depth =====
        self._apply_shadow_effect()

        # ===== Connect buttons =====
        self.ui.id_pm.clicked.connect(self.on_pm_login_clicked)
        self.ui.id_repair.clicked.connect(self.on_repair_login_clicked)
        self.ui.id_leader.clicked.connect(self.on_leader_login_clicked)
        self.ui.pushButton_D.clicked.connect(self.show_close_warning)

        # ===== Connect theme signals from Main =====
        if self.main_window and hasattr(self.main_window, 'theme_changed'):
            self.main_window.theme_changed.connect(self.update_theme)

        # ===== Load initial theme =====
        self.update_theme()

        # ===== Show with Fade-in animation =====
        self.show()
        QTimer.singleShot(150, self._fade_in_animation)
    # ==========================================================
    # ✨ Shadow Effect and Animation
    # ==========================================================
    def _apply_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 10)
        self.setGraphicsEffect(shadow)

    def _fade_in_animation(self):
        """Fade-in animation when opening Dialog"""
        self.setWindowOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(400)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_anim.start()

    # ==========================================================
    # 🖱️ Support Frameless window dragging
    # ==========================================================
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._drag_active and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_active = False

    # ==========================================================
    # 🎨 Load and update theme
    # ==========================================================
    def update_theme(self):
        log.debug("LoginPM: Theme update triggered.")
        loadJsonStyle(self, self.ui, jsonFiles={"json-styles/dialog_style.json"})

        if not hasattr(self.main_window, "theme_settings") or not self.main_window.theme_settings:
            if hasattr(self.main_window, "update_theme_settings"):
                self.main_window.update_theme_settings()

        self.update_all_icons()

    # ==========================================================
    # 🎨 Update all icons in Dialog
    # ==========================================================
    def update_all_icons(self):
        """Update icon colors to match Theme"""
        if not self.main_window or not hasattr(self.main_window, 'theme_settings'):
            log.warning("LoginPM: No theme settings found, using default colors")
            theme_settings = {
                "Icons-color": "#4A4A4A",
                "Background-color": "#FFFFFF"
            }
        else:
            theme_settings = self.main_window.theme_settings

        icons_color = theme_settings.get('Icons-color', '#4A4A4A')
        accent_color = theme_settings.get('Accent-color', '#26bae3')
        
        # 🟦 Main icon
        self.ui.icon.setPixmap(
            self._create_colored_pixmap(":/feather/icons/feather/check-square.png", accent_color, QSize(90, 90))
        )

        # 🟩 Various buttons (slightly different colors based on structure)
        self._update_button_icon(self.ui.id_pm, ":/feather/icons/feather/log-in.png", icons_color)
        
        # ✅ Change repair button color if logged in
        if self.repair_logged_in:
            success_color = "#00AA00"
            self._update_button_icon(self.ui.id_repair, ":/font_awesome_solid/icons/font_awesome/solid/screwdriver-wrench.png", success_color)
            self.ui.id_repair.setText("Staff Verified ✓")
        else:
            self._update_button_icon(self.ui.id_repair, ":/font_awesome_solid/icons/font_awesome/solid/screwdriver-wrench.png", icons_color)
            self.ui.id_repair.setText("Repair Staff")
        
        # ✅ Change leader button color if logged in
        if self.leader_logged_in:
            success_color = "#00AA00"
            self._update_button_icon(self.ui.id_leader, ":/feather/icons/feather/user.png", success_color)
            self.ui.id_leader.setText("Leader Verified ✓")
        else:
            self._update_button_icon(self.ui.id_leader, ":/feather/icons/feather/user.png", icons_color)
            self.ui.id_leader.setText("Leader")
        
        self._update_button_icon(self.ui.pushButton_D, ":/feather/icons/feather/x-circle.png", icons_color)

        log.debug("LoginPM: Icons recolored -> %s", icons_color)

    def show_close_warning(self):
        """Show warning message when Close button is pressed"""
        from src.custom_warning_dialog import CustomWarningDialog
        warning_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message="Please perform fixture PM before starting work\n\nDo you want to reset login and start over?",
            title="Warning"
        )
        warning_dialog.finished.connect(self._on_close_warning_finished)
        warning_dialog.exec()

    def _on_close_warning_finished(self, result):
        """When user responds to warning popup"""
        if result == QDialog.Accepted:
            log.info("User confirmed login reset")
            
            # ✅ Reset all login data
            self._reset_all_login_data()
            
            # ✅ Update UI back to normal state
            self.update_all_icons()
            
            log.info("Login reset completed")
            
        else:
            log.info("User canceled reset")
    def _reset_all_login_data(self):
        """Reset all login data"""
        log.debug("Resetting all login data...")
        
        # ✅ Reset login status
        self.repair_logged_in = False
        self.leader_logged_in = False
        self.login_successful = False
        
        # ✅ Clear stored data
        self.repair_data = None
        self.leader_data = None
        self.name_staff = ""
        self.pm_date = ""
        self.pm_time = ""
        self.scanned_data = ""
        
        # ✅ Reset button text
        self.ui.id_repair.setText("Repair Staff")
        self.ui.id_leader.setText("Leader")
        
        # ✅ Reset button style
        self.ui.id_repair.setStyleSheet("")
        self.ui.id_leader.setStyleSheet("")
        
        # ✅ Close sub-dialogs if any
        if hasattr(self, 'repair_dialog') and self.repair_dialog:
            try:
                self.repair_dialog.close()
                self.repair_dialog.deleteLater()
            except:
                pass
            self.repair_dialog = None
            
        if hasattr(self, 'leader_dialog') and self.leader_dialog:
            try:
                self.leader_dialog.close()
                self.leader_dialog.deleteLater()
            except:
                pass
            self.leader_dialog = None
        
        log.info("All login data reset completed")

    def _safe_close(self):
        """Safely close window"""
        try:
            # ✅ Reset values before closing
            self._reset_all_login_data()
            
            self.reject()
            self.deleteLater()
        except Exception as e:
            log.error("Error closing window: %s", e)

    def _restart_entire_application(self):
        """Restart the entire application"""
        try:
            log.info("Restarting entire application...")

            # ✅ Find actual main.py file
            main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "main.py"))
            python = sys.executable

            log.debug("Launching new program: %s %s", python, main_path)

            # ✅ Launch new program (main.py)
            started = QProcess.startDetached(python, [main_path])

            if started:
                log.info("New program started successfully - closing old program")
                # ✅ Close old event loop and process immediately
                QCoreApplication.exit(0)
                os._exit(0)
            else:
                log.error("Cannot start new program")

        except Exception as e:
            log.error("Cannot restart application: %s", e)


    def _close_and_restart(self):
        """Close LoginPM and send restart request signal"""
        log.info("Closing system and returning to login...")
        
        try:
            # ✅ Send restart request signal first
            self.request_restart.emit()
            
            # ✅ Clear dialog references if any
            if hasattr(self, 'repair_dialog') and self.repair_dialog:
                self.repair_dialog.deleteLater()
                self.repair_dialog = None
                
            if hasattr(self, 'leader_dialog') and self.leader_dialog:
                self.leader_dialog.deleteLater()
                self.leader_dialog = None
            
            # ✅ Close self after delay
            QTimer.singleShot(50, self._safe_close)
                
        except Exception as e:
            log.error("Error closing system: %s", e)
            self._safe_close()

    def closeEvent(self, event):
        """
        This method runs when user clicks 'X' to close window
        """
        log.warning("User closed window, sending restart request...")
        
        # Emit signal
        self.restart_requested.emit() 
        
        # Close window normally
        super().closeEvent(event)

    def _safe_close(self):
        """Safely close window"""
        try:
            self.reject()
            self.deleteLater()
        except Exception as e:
            log.error("Error closing window: %s", e)

    def _restart_login_scan(self):
        """Restart system back to login screen"""
        try:
            # ✅ Import MyWindow (Login Scan) here to prevent circular import
            from src.login_scan import MyWindow
            
            # ✅ Close current MainWindow
            if self.main_window:
                self.main_window.close()
            
            # ✅ Create and show new Login Scan
            QTimer.singleShot(200, self._create_new_login_scan)
            
        except ImportError as e:
            log.error("login_scan module not found: %s", e)
        except Exception as e:
            log.error("Error during restart: %s", e)

    def _create_new_login_scan(self):
        """Create new Login Scan window"""
        try:
            from src.login_scan import MyWindow
            
            self.login_scan = MyWindow()
            self.login_scan.show()
            log.info("New Login Scan window opened successfully")
            
        except Exception as e:
            log.error("Cannot open new Login Scan: %s", e)

    def set_leader_button_success(self):
        """Set leader button to show login success"""
        self.leader_logged_in = True
        self.login_successful = True
        self.update_all_icons()
        
        # ✅ Change button style for clarity
        self.ui.id_leader.setStyleSheet("""
            QPushButton {
                background-color: #E8F5E8;
                border: 2px solid #00AA00;
                border-radius: 10px;
                padding: 10px;
                color: #006600;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D4EDDA;
            }
        """)

    def set_repair_button_success(self):
        """Set repair button to show login success"""
        self.repair_logged_in = True
        self.login_successful = True
        self.update_all_icons()  # Update icons to show green color
        
        # ✅ Change button style for clarity
        self.ui.id_repair.setStyleSheet("""
            QPushButton {
                background-color: #E8F5E8;
                border: 2px solid #00AA00;
                border-radius: 10px;
                padding: 10px;
                color: #006600;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #D4EDDA;
            }
        """)

    def reset_repair_button(self):
        """Reset repair button to normal state"""
        self.repair_logged_in = False
        self.repair_data = None
        self.update_all_icons()  # Update icons back to normal color
        
        # ✅ Reset button style
        self.ui.id_repair.setStyleSheet("")

    # ==========================================================
    # 🧩 Helper functions
    # ==========================================================
    def _update_button_icon(self, button, icon_path, color_hex):
        pixmap = self._create_colored_pixmap(icon_path, color_hex, QSize(24, 24))
        button.setIcon(QIcon(pixmap))
        button.setIconSize(QSize(24, 24))

    def _create_colored_pixmap(self, icon_path: str, color_hex: str, size: QSize = None) -> QPixmap:
        """Create QPixmap with recolored theme"""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            log.warning("Missing icon resource: %s", icon_path)
            return QPixmap()

        if size:
            pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        tinted = QPixmap(pixmap.size())
        tinted.fill(Qt.transparent)

        painter = QPainter(tinted)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(tinted.rect(), QColor(color_hex))
        painter.end()
        return tinted

    # ==========================================================
    # 🔐 Login functions
    # ==========================================================
    def on_pm_login_clicked(self):
        """When PM button is clicked - verify login and return data"""
        # Verify both Repair Staff and Leader are logged in
        if not self.repair_logged_in:
            self._show_custom_warning("Please login as Repair Staff first", "Incomplete Information")
            return
        
        if not self.leader_logged_in:
            self._show_custom_warning("Please login as Leader first", "Incomplete Information")
            return
        
        # Verify complete data
        if not self.repair_data or not self.leader_data:
            self._show_custom_warning("Login information incomplete", "Error")
            return

        # ✅ Collect all data for output
        now = time.localtime()
        self.name_staff = f"{self.leader_data['name_leader']} (PM Staff)"
        self.pm_date = time.strftime("%Y-%m-%d", now)
        self.pm_time = time.strftime("%H:%M:%S", now)
        self.scanned_data = self.leader_data['leader_id']
        
        # ✅ Set login success status
        self.login_successful = True
        
        log.info("PM Login successful - Sending data to PM Window:")
        log.info("  Staff: %s", self.repair_data['name_staff'])
        log.info("  Leader: %s", self.leader_data['name_leader'])
        log.info("  Date: %s Time: %s", self.pm_date, self.pm_time)
        
        # ✅ Close dialog and return to shot_counting
        self.accept()

    def on_repair_login_clicked(self):  
        # ✅ If already logged in, show current status
        if self.repair_logged_in:
            self._show_repair_status()
            return
        
        try:
            # ✅ Create popup and send main_window reference
            self.repair_dialog = RepairLoginDialog(parent=self, main_window=self.main_window)
            
            # ✅ Connect signal when popup closes successfully
            self.repair_dialog.finished.connect(self._on_repair_dialog_finished)
            
            # ✅ Show popup (modal)
            result = self.repair_dialog.exec()
            
        except Exception as e:
            log.error("Error opening repair dialog: %s", e)
            # Fallback: direct login if popup has issues
            self._setup_login_data("Repairing Staff")

    def _show_repair_status(self):
        """Show current staff login status"""
        if self.repair_data:
            message = f"Staff login completed:\nName: {self.repair_data['name_staff']}\nID: {self.repair_data['scanned_data']}"
        else:
            message = "Staff completed"
            
        warning_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=message,
            title="Staff Status"
        )
        warning_dialog.exec()

    def _on_repair_dialog_finished(self, result):
        """Handle after Repair Dialog closes"""
        try:
            if result == QDialog.Accepted:
                # ✅ Get scan data
                repair_data = self.repair_dialog.get_repair_data()
                
                if repair_data and repair_data['name_staff']:
                    log.info("Repair staff verified: %s", repair_data['name_staff'])
                    
                    # ✅ Store repair data
                    self.repair_data = repair_data
                    
                    # ✅ Set button to show success
                    self.set_repair_button_success()
                    
                    # ✅ Show confirmation message
                    self._show_success_message(repair_data['name_staff'])
                    
                else:
                    log.error("Repair login: No valid staff data")

            else:
                log.info("Repair login cancelled")

        except Exception as e:
            log.error("Error in repair dialog finished: %s", e)
            # Fallback
            self._setup_login_data("Repairing Staff")

    def _show_success_message(self, staff_name):
        """Show staff login success confirmation"""
        success_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=f"Staff login completed!\nName: {staff_name}\n\nPlease log in as a Leader to continue.",
            title="Staff Verification Completed",
            is_success=True  # ✅ Parameter to show as success message
        )
        success_dialog.exec()

    def on_leader_login_clicked(self):
        """Show popup for scanning Leader ID"""
        log.debug("Opening Leader Login Dialog...")
        
        # ✅ If already logged in, show current status
        if self.leader_logged_in:
            return
        
        try:
            # ✅ Create popup and send main_window reference
            self.leader_dialog = LeaderLoginDialog(parent=self, main_window=self.main_window)
            
            # ✅ Connect signal when popup closes successfully
            self.leader_dialog.finished.connect(self._on_leader_dialog_finished)
            
            # ✅ Show popup (modal)
            result = self.leader_dialog.exec()
            
        except Exception as e:
            log.error("Error opening leader dialog: %s", e)
            # Fallback
            self._setup_login_data("Leader")

    def _show_leader_status(self):
        """Show current leader login status"""
        if self.leader_data:
            message = f"Leader login completed!:\nName: {self.leader_data['name_leader']}\nPosition: {self.leader_data['position_level']}\nID: {self.leader_data['leader_id']}"
        else:
            message = "Leader Verification completed"
            
        warning_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=message,
            title="Leader Login Status"
        )
        warning_dialog.exec()

    def _on_leader_dialog_finished(self, result):
        """Handle after Leader Dialog closes"""
        try:
            if result == QDialog.Accepted:
                # ✅ Get scan data
                leader_data = self.leader_dialog.get_leader_data()
                
                if leader_data and leader_data['name_leader']:
                    log.info("Leader verified: %s", leader_data['name_leader'])
                    
                    # ✅ Store leader data
                    self.leader_data = leader_data
                    
                    # ✅ Set button to show success
                    self.set_leader_button_success()
                    
                    
                else:
                    log.error("Leader login: No valid leader data")

            else:
                log.info("Leader login cancelled")

        except Exception as e:
            log.error("Error in leader dialog finished: %s", e)

    def _show_leader_success_message(self, leader_name, position):
        """Show leader login success confirmation"""
        success_dialog = CustomWarningDialog(
            parent=self,
            main_window=self.main_window,
            message=f"Leader login completed!\nName: {leader_name}\nPosition: {position}\n\nGo to Preventive Maintenance ",
            title="Leader Verification Completed",
            is_success=True
        )
        success_dialog.exec()

    def _setup_login_data(self, role):
        """Setup login data"""
        now = time.localtime()
        
        if role == "PM Staff" and self.leader_data and self.repair_data:
            # ✅ For PM Staff, use data from logged-in staff and leader
            self.name_staff = f"{self.leader_data['name_leader']} (PM Staff)"
            self.pm_date = time.strftime("%Y-%m-%d", now)
            self.pm_time = time.strftime("%H:%M:%S", now)
            self.scanned_data = self.leader_data['leader_id']
        elif role == "Leader" and self.leader_data:
            # ✅ For Leader
            self.name_staff = f"{self.leader_data['name_leader']} (Leader)"
            self.pm_date = time.strftime("%Y-%m-%d", now)
            self.pm_time = time.strftime("%H:%M:%S", now)
            self.scanned_data = self.leader_data['leader_id']
        else:
            # ✅ For other cases
            self.name_staff = role
            self.pm_date = time.strftime("%Y-%m-%d", now)
            self.pm_time = time.strftime("%H:%M:%S", now)
            self.scanned_data = ""
        
        self.login_successful = True
        self.accept()

    def get_login_data(self):
        """Return all login data"""
        return {
            'staff_data': self.repair_data,      # ✅ Repair Staff data
            'leader_data': self.leader_data      # ✅ Leader data
        }

    def _setup_login_data(self, role):
        """Setup login data"""
        now = time.localtime()
        
        if role == "Leader" and self.repair_data:
            # ✅ For Leader, use data from logged-in staff
            self.name_staff = f"{self.repair_data['name_staff']} (Leader)"
            self.pm_date = self.repair_data['pm_date']
            self.pm_time = self.repair_data['pm_time']
            self.scanned_data = self.repair_data['scanned_data']
        else:
            # ✅ For PM Staff or other cases
            self.name_staff = role
            self.pm_date = time.strftime("%Y-%m-%d", now)
            self.pm_time = time.strftime("%H:%M:%S", now)
            self.scanned_data = ""
        
        self.login_successful = True
        self.accept()