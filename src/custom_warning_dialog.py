import sys
from PySide6.QtWidgets import QDialog, QGraphicsDropShadowEffect, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFrame, QTextEdit
from PySide6.QtGui import QColor, QPainter, QPixmap, QIcon, QMouseEvent, QCursor
from PySide6.QtCore import Qt, QSize, Signal, QEasingCurve, QPoint, QTimer, QPropertyAnimation

from Custom_Widgets import loadJsonStyle
from src.app_logger import get_logger

log = get_logger("warning_dialog")

class CustomWarningDialog(QDialog):
    """
    Custom Dialog ที่ออกแบบมาให้ดูเป็นมืออาชีพ, ยืดหยุ่น, และใช้งานง่าย
    - รองรับ 2 โหมด: Success (ปิดอัตโนมัติ) และ Warning (มีปุ่มดูรายละเอียด)
    - ความสูงปรับตามเนื้อหาอัตโนมัติ
    - มี Animation ตอนเปิดและปิด
    - รองรับการลากหน้าต่างแบบ Frameless
    - สามารถปรับแต่ง Theme ได้
    """

    # ==== ค่าคงที่สำหรับการตั้งค่า ====
    ANIMATION_DURATION = 300
    SHADOW_BLUR_RADIUS = 40
    DEFAULT_WIDTH = 450
    MINIMUM_HEIGHT = 220
    SUCCESS_AUTO_CLOSE_DELAY = 5  # วินาที

    def __init__(self, parent=None, main_window=None, title="Notification", message="", details="", is_success=False):
        """
        Args:
            parent (QWidget, optional): Parent widget.
            main_window (QMainWindow, optional): หน้าต่างหลักเพื่อดึงการตั้งค่า Theme.
            title (str): ข้อความหัวเรื่องหลัก.
            message (str): ข้อความที่ต้องการแสดง.
            details (str, optional): ข้อความรายละเอียดเพิ่มเติม (สำหรับ Warning).
            is_success (bool): True สำหรับ Success Dialog, False สำหรับ Warning Dialog.
        """
        super().__init__(parent)
        self.main_window = main_window
        self.title_text = title
        self.message_text = message
        self.details_text = details
        self.is_success = is_success

        self._drag_active = False
        self._drag_position = QPoint()

        self.setup_ui()
        self.setup_window()
        
        if self.main_window and hasattr(self.main_window, 'theme_changed'):
            self.main_window.theme_changed.connect(self.update_theme)
        
        self.update_theme()
        self._center_on_parent()

        if self.is_success:
            self._start_auto_close_timer()

    def setup_ui(self):
        """ตั้งค่า User Interface ทั้งหมด"""
        self.setObjectName("CustomWarningDialog")
        
        # Layout หลัก
        layout = QVBoxLayout(self)
        layout.setContentsMargins(1, 1, 1, 1) # ลดขอบเพื่อให้เงาแสดงได้เต็มที่
        layout.setSpacing(0)

        # Container หลักสำหรับเนื้อหาและเงา
        self.container_widget = QWidget(self)
        self.container_widget.setObjectName("container_widget")
        main_layout = QVBoxLayout(self.container_widget)
        main_layout.setContentsMargins(30, 30, 30, 25)
        main_layout.setSpacing(20)

        # == Header Section ==
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(48, 48)
        self.icon_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.icon_label)

        text_header_layout = QVBoxLayout()
        text_header_layout.setSpacing(2)
        self.title_label = QLabel(self.title_text)
        self.title_label.setObjectName("title_label")
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle_label")
        text_header_layout.addWidget(self.title_label)
        text_header_layout.addWidget(self.subtitle_label)
        
        header_layout.addLayout(text_header_layout)
        main_layout.addLayout(header_layout)

        # == Separator Line ==
        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # == Content Section ==
        self.message_label = QLabel(self.message_text)
        self.message_label.setObjectName("message_label")
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        main_layout.addWidget(self.message_label)
        
        main_layout.addStretch()

        # == Details Section (สำหรับ Warning) ==
        if not self.is_success and self.details_text:
            self.details_container = QWidget()
            self.details_container.setObjectName("details_container")
            self.details_container.setVisible(False)
            
            details_layout = QVBoxLayout(self.details_container)
            details_layout.setContentsMargins(0, 10, 0, 0)
            
            self.details_text_edit = QTextEdit()
            self.details_text_edit.setReadOnly(True)
            self.details_text_edit.setText(self.details_text)
            self.details_text_edit.setObjectName("details_text_edit")
            self.details_text_edit.setFixedHeight(120)
            details_layout.addWidget(self.details_text_edit)
            
            main_layout.addWidget(self.details_container)
        
        # == Button Section ==
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        
        if not self.is_success and self.details_text:
            self.details_button = QPushButton("ดูรายละเอียด")
            self.details_button.setObjectName("details_button")
            self.details_button.setCursor(QCursor(Qt.PointingHandCursor))
            self.details_button.setCheckable(True)
            self.details_button.toggled.connect(self._toggle_details)
            button_layout.addWidget(self.details_button)

        button_layout.addStretch()
        self.ok_button = QPushButton("ตกลง")
        self.ok_button.setObjectName("ok_button")
        self.ok_button.setMinimumSize(120, 38)
        self.ok_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.ok_button.clicked.connect(self.accept)
        button_layout.addWidget(self.ok_button)

        main_layout.addLayout(button_layout)
        layout.addWidget(self.container_widget)
        
        # ปรับขนาดหน้าต่างให้พอดีกับเนื้อหา
        self.adjustSize()

    def setup_window(self):
        """ตั้งค่าคุณสมบัติของหน้าต่าง"""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(self.DEFAULT_WIDTH, self.MINIMUM_HEIGHT)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(self.SHADOW_BLUR_RADIUS)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.container_widget.setGraphicsEffect(shadow)

    def showEvent(self, event):
        """แสดงหน้าต่างพร้อม Animation"""
        super().showEvent(event)
        self._fade_in_animation()

    def accept(self):
        """ปิดหน้าต่างพร้อม Animation"""
        self._fade_out_animation()

    def _fade_in_animation(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(self.ANIMATION_DURATION)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.start()

    def _fade_out_animation(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(self.ANIMATION_DURATION)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.finished.connect(super(CustomWarningDialog, self).accept)
        self.anim.start()

    def _center_on_parent(self):
        """จัดตำแหน่งกึ่งกลาง Parent Widget"""
        if self.parent():
            self.move(self.parent().geometry().center() - self.rect().center())

    def _toggle_details(self, checked):
        """แสดง/ซ่อน ส่วนของรายละเอียด"""
        self.details_container.setVisible(checked)
        self.details_button.setText("ซ่อนรายละเอียด" if checked else "ดูรายละเอียด")
        # ปรับขนาดหน้าต่างใหม่เมื่อแสดง/ซ่อน
        QTimer.singleShot(10, self.adjustSize)

    def _start_auto_close_timer(self):
        """เริ่มนับเวลาถอยหลังเพื่อปิด Dialog อัตโนมัติ"""
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.accept)
        self.timer.start(self.SUCCESS_AUTO_CLOSE_DELAY * 1000)
        
        # ✅ แสดงข้อความเริ่มต้น (ไม่ต้องอัพเดตทุกวินาที)
        self.ok_button.setText(f"ตกลง")

    def accept(self):
        """ปิดหน้าต่าง"""
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        super().accept()

    def _update_auto_close_timer(self):
        """อัปเดตตัวนับเวลาและปิดเมื่อถึงศูนย์"""
        self.remaining_time -= 1
        self._update_button_text()
        if self.remaining_time <= 0:
            self.timer.stop()
            self.accept()
            
    def _update_button_text(self):
        """อัปเดตข้อความบนปุ่ม OK"""
        if self.is_success and hasattr(self, 'timer') and self.timer.isActive():
            self.ok_button.setText(f"ตกลง ({self.remaining_time})")
        else:
            self.ok_button.setText("ตกลง")

    def update_theme(self):
        """อัปเดต Theme จากไฟล์ JSON และตั้งค่าสีต่างๆ"""
        try:
            loadJsonStyle(self, None, jsonFiles={"json-styles/dialog_style.json"})
            
            if self.main_window and hasattr(self.main_window, "theme_settings"):
                pass  # มีธีมอยู่แล้ว ไม่ต้องทำอะไร
            elif self.main_window and hasattr(self.main_window, "update_theme_settings"):
                self.main_window.update_theme_settings()
            else:
                # ✅ ป้องกันกรณีไม่มี main_window เช่นถูกเรียกจาก popup เดี่ยว
                log.info("CustomWarningDialog: No main_window or theme_settings found, using default style.")

            self.update_content_and_style()
        except Exception as e:
            log.error("Error updating theme in Dialog: %s", e)

    def update_content_and_style(self):
        """อัปเดตเนื้อหาและสไตล์ตามประเภทของ Dialog (Success/Warning)"""
        if not self.main_window or not hasattr(self.main_window, 'theme_settings'):
            theme_settings = {
                "Accent-color": "#FF6B6B", # Warning Color
                "Success-color": "#2ECC71", # Success Color
            }
        else:
            theme_settings = self.main_window.theme_settings

        if self.is_success:
            self.subtitle_label.setText("Operation Successful")
            accent_color = theme_settings.get('Success-color', '#2ECC71')
            icon_path = ":/feather/icons/feather/check-circle.png"
        else:
            self.subtitle_label.setText("An Error Occurred")
            accent_color = theme_settings.get('Accent-color', '#FF6B6B')
            icon_path = ":/feather/icons/feather/alert-circle.png"
        
        # Apply Accent Color to Title
        self.title_label.setStyleSheet(f"color: {accent_color};")
        
        # Create and set colored icon
        main_icon = self._create_colored_pixmap(icon_path, accent_color, QSize(40, 40))
        if not main_icon.isNull():
            self.icon_label.setPixmap(main_icon)

        # Style OK button
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent_color};
            }}
            QPushButton:hover {{
                background-color: {self._adjust_color(accent_color, -20)};
            }}
            QPushButton:pressed {{
                background-color: {self._adjust_color(accent_color, -40)};
            }}
        """)

    def _adjust_color(self, color_hex, adjustment):
        """ปรับความสว่างของสี"""
        color = QColor(color_hex)
        h, s, v, a = color.getHsv()
        new_v = max(0, min(255, v + adjustment))
        return QColor.fromHsv(h, s, new_v, a).name()

    def _create_colored_pixmap(self, icon_path, color_hex, size):
        """สร้าง Pixmap พร้อมเปลี่ยนสี"""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            log.warning("Missing icon: %s", icon_path)
            return QPixmap()
        
        pixmap = pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter = QPainter(pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color_hex))
        painter.end()
        return pixmap

    # ==========================================================
    # 🖱️ Mouse Events for Frameless Window Dragging
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
        event.accept()