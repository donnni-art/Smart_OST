from PySide6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PySide6.QtCore import Qt, QSettings, Signal
from PySide6.QtGui import QPixmap, QIcon, QColor
import csv
import os
from functools import lru_cache
import csv
from datetime import datetime
from src.ui_Logout import Ui_Finish
from src.app_logger import get_logger

log = get_logger("logout")
class LogoutWindow(QMainWindow):
    # ✅ เพิ่ม Signal สำหรับแจ้ง MainWindow เมื่อ logout สำเร็จ
    logout_completed = Signal()
    
    def __init__(self, parent=None, shot_counter=None, theme_settings=None, data_uploader=None):
        super().__init__(parent)
        
        # Import UI
        from src.ui_Logout import Ui_Finish
        self.ui = Ui_Finish()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.shot_counter = shot_counter
        self.parent = parent
        self.data_uploader = data_uploader  # ✅ Receive DataUploader
        self._icon_cache = {}  # Cache สำหรับ icon ที่สร้างแล้ว
        
        # ✅ รับ theme settings จาก parent
        self.theme_settings = theme_settings or {}
        
        # ตั้งค่าหน้าต่าง - เอา title bar ออก
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(372, 478)
        
        # เชื่อมต่อสัญญาณ
        self.setup_connections()
        
        # ตั้งค่าข้อมูลเริ่มต้น
        self.setup_initial_data()
        
        # ✅ อัพเดต icon ตามธีม
        self.update_icons()
        
        # ✅ ตัวแปรเก็บข้อมูลที่ operator กรอก
        self.logout_data = {}
        
        log.info("LogoutWindow initialized successfully")
    
    def validate_theme_settings(self, theme_settings):
        """ตรวจสอบความถูกต้องของ theme_settings"""
        if not theme_settings or not isinstance(theme_settings, dict):
            return False
            
        required_keys = ["Icons-color", "Accent-color"]
        return all(key in theme_settings for key in required_keys)
    
    def update_icons(self):
        """อัพเดต icon ทั้งหมดตามธีมปัจจุบัน"""
        try:
            # ✅ ใช้ fallback ถ้าไม่ได้รับ theme_settings
            if not self.theme_settings or not self.validate_theme_settings(self.theme_settings):
                self.theme_settings = self._get_fallback_theme()
                log.warning("Using fallback theme for LogoutWindow")
            
            icons_color = self.theme_settings.get("Icons-color", "#000000")
            accent_color = self.theme_settings.get("Accent-color", "#26bae3")
            
            log.debug("LogoutWindow updating icons with color: %s", icons_color)
            
            # ✅ อัพเดต icon หลัก (log-out)
            logout_icon = self.create_colored_icon(":/feather/icons/feather/log-out.png", icons_color)
            if not logout_icon.isNull():
                self.ui.icon_logout.setPixmap(logout_icon)
            
            # ✅ อัพเดต icon ปุ่ม save
            save_icon = self.create_colored_icon(":/feather/icons/feather/save.png", accent_color)
            if not save_icon.isNull():
                self.ui.save_finish.setIcon(QIcon(save_icon))
            
            # ✅ อัพเดต icon ปุ่ม close
            close_icon = self.create_colored_icon(":/feather/icons/feather/x-circle.png", accent_color)
            if not close_icon.isNull():
                self.ui.close_finish.setIcon(QIcon(close_icon))
            
            log.info("LogoutWindow icons updated successfully")
            
        except Exception as e:
            log.error("Error updating icons in LogoutWindow: %s", e)
            # ✅ แสดง icon ต้นฉบับเป็น fallback
            self._load_default_icons()
    
    def _get_fallback_theme(self):
        """ธีม fallback เมื่อไม่ได้รับ theme_settings"""
        return {
            "Background-color": "#FFFFFF",
            "Text-color": "#000000", 
            "Icons-color": "#666666",
            "Accent-color": "#26bae3",
            "Destructive-color": "#E74C3C",
            "Secondary-text-color": "#666666",
            "Theme-name": "Fallback"
        }
    
    def _load_default_icons(self):
        """โหลด icon ต้นฉบับเมื่อเกิดข้อผิดพลาด"""
        try:
            self.ui.icon_logout.setPixmap(QPixmap(":/feather/icons/feather/log-out.png"))
            self.ui.save_finish.setIcon(QIcon(":/feather/icons/feather/save.png"))
            self.ui.close_finish.setIcon(QIcon(":/feather/icons/feather/x-circle.png"))
            log.info("Loaded default icons as fallback")
        except Exception as e:
            log.warning("Cannot load default icons: %s", e)
    
    @lru_cache(maxsize=32)
    def create_colored_icon(self, icon_path, color):
        """สร้าง icon ที่มีสีตามที่กำหนด (มี caching)"""
        try:
            cache_key = f"{icon_path}_{color}"
            if cache_key in self._icon_cache:
                return self._icon_cache[cache_key]
                
            from PySide6.QtGui import QImage, QPainter
            
            # โหลด icon ดั้งเดิม
            original_pixmap = QPixmap(icon_path)
            if original_pixmap.isNull():
                log.error("Cannot load icon: %s", icon_path)
                return QPixmap()
            
            # สร้าง QImage ใหม่ด้วยสีที่ต้องการ
            colored_image = QImage(original_pixmap.size(), QImage.Format_ARGB32)
            colored_image.fill(Qt.transparent)
            
            painter = QPainter(colored_image)
            painter.setCompositionMode(QPainter.CompositionMode_Source)
            painter.drawPixmap(0, 0, original_pixmap)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            
            # ตั้งค่าสี
            painter.fillRect(colored_image.rect(), QColor(color))
            painter.end()
            
            result = QPixmap.fromImage(colored_image)
            self._icon_cache[cache_key] = result
            return result
            
        except Exception as e:
            log.error("Error creating colored icon: %s", e)
            return QPixmap(icon_path)
    
    def setup_connections(self):
        """เชื่อมต่อสัญญาณปุ่มต่างๆ พร้อม error handling"""
        try:
            self.ui.save_finish.clicked.connect(self.save_and_logout)
            self.ui.close_finish.clicked.connect(self.close)
            
            # Real-time validation
            defect_fields = [
                self.ui.lineEdit_open, self.ui.lineEdit_short, 
                self.ui.lineEdit_blkm, self.ui.lineEdit_mat, 
                self.ui.lineEdit_shot
            ]
            
            for field in defect_fields:
                field.textChanged.connect(self._safe_update_total_ng)
                
            # ✅ เก็บข้อมูลอัตโนมัติพร้อม error handling
            data_fields = [
                self.ui.lineEdit_name, self.ui.lineEdit_id,
                self.ui.lineEdit_open, self.ui.lineEdit_short,
                self.ui.lineEdit_blkm, self.ui.lineEdit_mat,
                self.ui.lineEdit_shot, self.ui.lineEdit_note
            ]
            
            for field in data_fields:
                field.textChanged.connect(self._safe_collect_logout_data)
                
            log.info("LogoutWindow connections established successfully")
            
        except Exception as e:
            log.error("Error setting up connections: %s", e)
    
    def _safe_update_total_ng(self):
        """อัพเดต TOTAL NG แบบ real-time พร้อม error handling"""
        try:
            self.update_total_ng()
        except Exception as e:
            log.warning("Error updating total NG: %s", e)
            self.ui.lineEdit_tatal.setText("0")
    
    def _safe_collect_logout_data(self):
        """เก็บข้อมูลจาก UI Logout พร้อม error handling"""
        try:
            self._collect_logout_data()
        except Exception as e:
            log.warning("Error collecting logout data: %s", e)
    
    def setup_initial_data(self):
        """ตั้งค่าข้อมูลเริ่มต้นใน UI"""
        if self.shot_counter:
            # แสดง shot count ปัจจุบัน
            total_shots = getattr(self.shot_counter, 'shot_count', 0)
            self.ui.lineEdit_tatal.setText(str(total_shots))
        
        # ตั้งค่า placeholder และ tooltip (optional)
        self.ui.lineEdit_name.setPlaceholderText("Enter your name")
        self.ui.lineEdit_id.setPlaceholderText("Enter your ID")
        self.ui.lineEdit_note.setPlaceholderText("Additional notes...")
        
        # Clear defect fields
        self.clear_defect_fields()
    
    def clear_defect_fields(self):
        """ล้างค่าฟิลด์ defects"""
        self.ui.lineEdit_open.clear()
        self.ui.lineEdit_short.clear()
        self.ui.lineEdit_blkm.clear()
        self.ui.lineEdit_mat.clear()
        self.ui.lineEdit_shot.clear()
        self.ui.lineEdit_note.clear()
    
    def update_total_ng(self):
        """อัพเดต TOTAL NG แบบ real-time"""
        try:
            open_val = int(self.ui.lineEdit_open.text() or 0)
            short_val = int(self.ui.lineEdit_short.text() or 0)
            blkm_val = int(self.ui.lineEdit_blkm.text() or 0)
            mat_val = int(self.ui.lineEdit_mat.text() or 0)
            shot_val = int(self.ui.lineEdit_shot.text() or 0)
            
            total_ng = open_val + short_val + blkm_val + mat_val + shot_val
            self.ui.lineEdit_tatal.setText(str(total_ng))
            
        except ValueError:
            # ถ้ามีค่าที่ไม่ใช่ตัวเลข
            self.ui.lineEdit_tatal.setText("0")
    
    def _collect_logout_data(self):
        """เก็บข้อมูลจาก UI Logout แบบ real-time"""
        try:
            self.logout_data = {
                'confirmed_by': self.ui.lineEdit_name.text().strip(),
                'confirmed_id': self.ui.lineEdit_id.text().strip(),
                'total_ng': self.ui.lineEdit_tatal.text().strip(),
                'open_defects': self.ui.lineEdit_open.text().strip(),
                'short_defects': self.ui.lineEdit_short.text().strip(),
                'blkm_defects': self.ui.lineEdit_blkm.text().strip(),
                'mat_defects': self.ui.lineEdit_mat.text().strip(),
                'shot_defects': self.ui.lineEdit_shot.text().strip(),
                'notes': self.ui.lineEdit_note.text().strip(),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ✅ แก้ไขบรรทัดนี้
            }
            log.debug("Collected logout data: %s", self.logout_data)
            
        except Exception as e:
            log.error("Error collecting logout data: %s", e)
    
    def validate_inputs(self):
        """ตรวจสอบความถูกต้องของข้อมูล"""
        errors = []
        
        # ตรวจสอบชื่อและ ID
        if not self.ui.lineEdit_name.text().strip():
            errors.append("กรุณากรอกชื่อผู้ยืนยัน")
        if not self.ui.lineEdit_id.text().strip():
            errors.append("กรุณากรอก ID ผู้ยืนยัน")
        
        # ตรวจสอบว่ามีการกรอก defects อย่างน้อย 1 ช่อง
        open_val = self.ui.lineEdit_open.text().strip()
        short_val = self.ui.lineEdit_short.text().strip()
        blkm_val = self.ui.lineEdit_blkm.text().strip()
        mat_val = self.ui.lineEdit_mat.text().strip()
        shot_val = self.ui.lineEdit_shot.text().strip()
        
        if not any([open_val, short_val, blkm_val, mat_val, shot_val]):
            errors.append("กรุณากรอกจำนวน defects อย่างน้อย 1 รายการ")
        
        return errors
    
    def collect_logout_data(self):
        """รวบรวมข้อมูลจาก UI Logout (เรียกใช้ก่อนบันทึก)"""
        self._collect_logout_data()  # อัปเดตข้อมูลล่าสุด
        return self.logout_data
    
    def save_logout_data(self, product_name, lot_number, data):
        """บันทึกข้อมูล Logout ลงไฟล์ CSV ในโฟลเดอร์เดียวกันกับ defect_data"""
        try:
            # สร้างเส้นทางโฟลเดอร์ตามโครงสร้าง: defec_raw_data/Product_name/Lotnumber
            base_dir = "defect_raw_data"
            product_dir = os.path.join(base_dir, product_name)
            lot_dir = os.path.join(product_dir, lot_number)
            
            # สร้างโฟลเดอร์ถ้ายังไม่มี
            os.makedirs(lot_dir, exist_ok=True)
            
            # สร้าง timestamp สำหรับชื่อไฟล์
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(lot_dir, f"logout_records_{timestamp}.csv")
            
            # ตรวจสอบว่าไฟล์มีอยู่แล้วหรือไม่ (สำหรับการเขียน header)
            file_exists = os.path.exists(filename)
            
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # เขียน header ถ้าไฟล์ใหม่
                if not file_exists:
                    writer.writerow([
                        'Timestamp', 'Confirmed By', 'ID', 'Total NG', 
                        'OPEN', 'SHORT', 'BLKM', 'MAT', 'SHOT', 'Notes'
                    ])
                
                # เขียนข้อมูล
                writer.writerow([
                    data['timestamp'],
                    data['confirmed_by'],
                    data['confirmed_id'],
                    data['total_ng'],
                    data['open_defects'],
                    data['short_defects'],
                    data['blkm_defects'],
                    data['mat_defects'],
                    data['shot_defects'],
                    data['notes']
                ])
            
            log.info("Logout data saved to %s", filename)
            return True
            
        except Exception as e:
            log.error("Error saving logout data: %s", e)
            return False
    
    def save_and_logout(self):
        """บันทึกข้อมูลและออกจากระบบ"""
        try:
            # 1. ตรวจสอบข้อมูล
            errors = self.validate_inputs()
            if errors:
                QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "\n".join(errors))
                return
            
            # 2. รวบรวมข้อมูล
            logout_data = self.collect_logout_data()
            
            # 3. เรียก manual_save เพื่อบันทึก shot count
            if self.shot_counter:
                log.info("Saving shot count data...")
                self.shot_counter.manual_save()
            
            # 4. ดึงข้อมูล product_name และ lot_number จาก shot_counter
            product_name = "Unknown"
            lot_number = "Unknown"
            
            if self.shot_counter and hasattr(self.shot_counter, 'product_data'):
                product_name = self.shot_counter.product_data.get('product_name', 'Unknown')
                lot_number = self.shot_counter.product_data.get('lot_number', 'Unknown')
                log.info("Product data retrieved: %s, lot: %s", product_name, lot_number)
            else:
                log.warning("No product data found in shot_counter")
            
            # 5. บันทึกข้อมูล logout
            log.info("Saving logout data...")
            save_success = self.save_logout_data(product_name, lot_number, logout_data)
            
            # ✅ Save to Database (Localhost)
            if self.data_uploader:
                log.info("Saving logout confirmation to database...")
                # Add lot_number to logout_data for database update
                logout_data['lot_number'] = lot_number
                db_result = self.data_uploader.update_logout_data(logout_data)
                
                if db_result.get('status') == 'success':
                    log.info("Database update successful")
                else:
                    log.warning("Database update failed: %s", db_result.get('message'))
                    # Note: We continue even if DB save fails, as CSV save is done? 
                    # Or should we alert user? Let's print for now.
            else:
                log.warning("No DataUploader instance available")
            
            if save_success:
                # 6. ✅ ส่งสัญญาณว่า logout สำเร็จ
                self.logout_completed.emit()
                
                # 7. แสดงข้อความสำเร็จ
                QMessageBox.information(
                    self, 
                    "Success", 
                    "บันทึกข้อมูลและออกจากระบบเรียบร้อย!\n\n"
                    f"Total NG: {logout_data['total_ng']} pcs\n"
                    f"Confirmed by: {logout_data['confirmed_by']}"
                )
                
                # 8. ✅ ปิดหน้าต่าง logout
                self.close()
                
            else:
                QMessageBox.critical(self, "Error", "บันทึกข้อมูลไม่สำเร็จ")
            
        except Exception as e:
            error_msg = f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}"
            log.error("%s", error_msg)
            QMessageBox.critical(self, "Error", error_msg)
    
    def cleanup_after_logout(self):
        """ทำความสะอาดหลัง logout"""
        try:
            # เคลียร์ข้อมูลใน parent UI ถ้าจำเป็น
            if self.parent and hasattr(self.parent, 'ui'):
                if hasattr(self.parent.ui, 'shot_cnt'):
                    self.parent.ui.shot_cnt.setText("0")
                
                # แสดงสถานะ logout
                if hasattr(self.parent.ui, 'statusbar'):
                    self.parent.ui.statusbar.showMessage("✅ Logged out successfully", 5000)
            
            log.info("Cleanup after logout completed")
            
        except Exception as e:
            log.warning("Error during cleanup: %s", e)
    
    def showEvent(self, event):
        """เรียกเมื่อหน้าต่างแสดงขึ้นมา - อัพเดตธีมล่าสุด"""
        super().showEvent(event)
        
        # ✅ อัพเดต theme settings จาก parent พร้อม validation
        if self.parent and hasattr(self.parent, 'theme_settings'):
            new_theme = self.parent.theme_settings
            if self.validate_theme_settings(new_theme):
                self.theme_settings = new_theme
                self.update_icons()
                log.info("Updated LogoutWindow theme with validation")
            else:
                log.warning("Invalid theme settings from parent, using current theme")