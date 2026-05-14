# src/pm_window.py
import os
import re
import shutil
import time
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from src.app_logger import get_logger
from src.ui_PM import Ui_PM
from src.config_manager import config_manager

log = get_logger("pm_window")

class Pmwindow(QMainWindow):
    def __init__(self, parent=None, login_data=None, file_path=None, shot_counter=None, is_manual=False):
        super().__init__(parent)
        self.setObjectName("Pmwindow")
        self.name_staff = None
        self.pm_date = None
        self.pm_time = None
        self.is_logged_in = False
        self.shot_counter = shot_counter
        
        # ✅ รับ templates_dir จาก shot_counter
        if shot_counter:
            self.templates_dir = shot_counter.templates_dir
            self.pm_complete_dir = shot_counter.pm_complete_dir
            self.pm_in_progress_dir = shot_counter.pm_in_progress_dir
            shot_counter.path_changed.connect(self._update_file_path)
        else:
            # ✅ ใช้ค่า default ถ้าไม่มี shot_counter
            self.paths_config = config_manager.get_paths_config()
            self.templates_dir = config_manager.get_full_path(self.paths_config.get('templates', 'templat'))
            self.pm_complete_dir = config_manager.get_full_path(self.paths_config.get('pm_complete', 'PM/PM compleat'))
            self.pm_in_progress_dir = config_manager.get_full_path(self.paths_config.get('pm_in_progress', 'PM/PM in Progress'))

        self._current_login_info = {}

        self.ui = Ui_PM()
        self.ui.setupUi(self)
        self.ui.save.clicked.connect(self._save_login_info_to_excel)
        self.setStyleSheet("")
        # ✅ ตั้งชื่อหน้าต่างตามประเภท PM
        pm_type = "Manual" if is_manual else "Auto"
        self.setWindowTitle(f"Preventive Maintenance ({pm_type})")
        self.file_path = file_path
        self.tab_data = {}
        self.paths_config = config_manager.get_paths_config()

        # ✅ ใช้ข้อมูลจาก login_data
        if login_data:
            self.name_staff = login_data.get("name_staff")
            self.pm_date = login_data.get("pm_date")
            self.pm_time = login_data.get("pm_time")
            self.is_logged_in = True
            self._display_login_info(login_data)

        # ✅ เชื่อมต่อสัญญาณแบบ real-time
        self._connect_tab_signals()

    # ============================================================
    # ✅ เชื่อมสัญญาณ ComboBox และ LineEdit
    # ============================================================
    def _connect_tab_signals(self):
        """เชื่อมต่อสัญญาณ comboBox / lineEdit เพื่อเก็บข้อมูลอัตโนมัติ"""
        try:
            # Tab1
            self.ui.comboBox.currentTextChanged.connect(self._collect_tab1_data)
            self.ui.comboBox_2.currentTextChanged.connect(self._collect_tab1_data)
            self.ui.lineEdit_4.textChanged.connect(self._collect_tab1_data)
            self.ui.lineEdit_5.textChanged.connect(self._collect_tab1_data)

            # Tab2
            self.ui.comboBox_3.currentTextChanged.connect(self._collect_tab2_data)
            self.ui.lineEdit_6.textChanged.connect(self._collect_tab2_data)

            # Tab3
            self.ui.comboBox_4.currentTextChanged.connect(self._collect_tab3_data)
            self.ui.comboBox_5.currentTextChanged.connect(self._collect_tab3_data)
            self.ui.comboBox_6.currentTextChanged.connect(self._collect_tab3_data)
            self.ui.lineEdit_9.textChanged.connect(self._collect_tab3_data)
            self.ui.lineEdit_8.textChanged.connect(self._collect_tab3_data)
            self.ui.lineEdit_7.textChanged.connect(self._collect_tab3_data)

            # Tab4
            self.ui.comboBox_7.currentTextChanged.connect(self._collect_tab4_data)
            self.ui.lineEdit_10.textChanged.connect(self._collect_tab4_data)

            # Tab5
            self.ui.comboBox_8.currentTextChanged.connect(self._collect_tab5_data)
            self.ui.lineEdit_11.textChanged.connect(self._collect_tab5_data)

            # Tab6
            self.ui.comboBox_9.currentTextChanged.connect(self._collect_tab6_data)
            self.ui.comboBox_10.currentTextChanged.connect(self._collect_tab6_data)
            self.ui.comboBox_11.currentTextChanged.connect(self._collect_tab6_data)
            self.ui.lineEdit_12.textChanged.connect(self._collect_tab6_data)
            self.ui.lineEdit_14.textChanged.connect(self._collect_tab6_data)
            self.ui.lineEdit_15.textChanged.connect(self._collect_tab6_data)

            self._collect_all_tab_data()
            log.info("Connected tab signals successfully")

        except Exception as e:
            log.error("Error connecting signals: %s", e)

    def _update_file_path(self, new_path):
        """อัปเดต file_path เมื่อ ShotCounter เปลี่ยน"""
        self.file_path = new_path
        log.info("Pmwindow อัปเดต path เป็น: %s", new_path)
    
    # ============================================================
    # ✅ เก็บข้อมูลจากแต่ละ Tab
    # ============================================================
    def _collect_all_tab_data(self):
        try:
            self._collect_tab1_data()
            self._collect_tab2_data()
            self._collect_tab3_data()
            self._collect_tab4_data()
            self._collect_tab5_data()
            self._collect_tab6_data()
        except Exception as e:
            log.error("Error collecting all tab data: %s", e)

    def _collect_tab1_data(self):
        self.tab_data["tab1"] = {
            "frame_5": {
                "comboBox": self.ui.comboBox.currentText(),
                "lineEdit_4": self.ui.lineEdit_4.text(),
            },
            "frame_6": {
                "comboBox_2": self.ui.comboBox_2.currentText(),
                "lineEdit_5": self.ui.lineEdit_5.text(),
            },
        }

    def _collect_tab2_data(self):
        self.tab_data["tab2"] = {
            "frame_7": {
                "comboBox_3": self.ui.comboBox_3.currentText(),
                "lineEdit_6": self.ui.lineEdit_6.text(),
            }
        }

    def _collect_tab3_data(self):
        self.tab_data["tab3"] = {
            "frame_4": {
                "comboBox_4": self.ui.comboBox_4.currentText(),
                "lineEdit_9": self.ui.lineEdit_9.text(),
            },
            "frame_8": {
                "comboBox_5": self.ui.comboBox_5.currentText(),
                "lineEdit_8": self.ui.lineEdit_8.text(),
            },
            "frame_10": {
                "comboBox_6": self.ui.comboBox_6.currentText(),
                "lineEdit_7": self.ui.lineEdit_7.text(),
            },
        }

    def _collect_tab4_data(self):
        self.tab_data["tab4"] = {
            "frame_11": {
                "comboBox_7": self.ui.comboBox_7.currentText(),
                "lineEdit_10": self.ui.lineEdit_10.text(),
            }
        }

    def _collect_tab5_data(self):
        self.tab_data["tab5"] = {
            "frame_12": {
                "comboBox_8": self.ui.comboBox_8.currentText(),
                "lineEdit_11": self.ui.lineEdit_11.text(),
            }
        }

    def _collect_tab6_data(self):
        self.tab_data["tab6"] = {
            "frame_14": {
                "comboBox_11": self.ui.comboBox_11.currentText(),
                "lineEdit_14": self.ui.lineEdit_14.text(),
            },
            "frame_15": {
                "comboBox_10": self.ui.comboBox_10.currentText(),
                "lineEdit_15": self.ui.lineEdit_15.text(),
            },
            "frame_18": {
                "comboBox_9": self.ui.comboBox_9.currentText(),
                "lineEdit_12": self.ui.lineEdit_12.text(),
            },
        }

    # ============================================================
    # ✅ ตรวจสอบว่ากรอกข้อมูลครบหรือยัง (comboBox + หมายเหตุ)
    # ============================================================
    def _is_all_tab_filled(self):
        """
        ตรวจสอบข้อมูลก่อนบันทึก:
        - comboBox ต้องเลือกค่า
        - ถ้าเลือก Not Pass หรือ Not Check → ต้องกรอกหมายเหตุ
        """
        missing_fields = []

        for tab_name, frames in self.tab_data.items():
            for frame_name, data in frames.items():
                combo_value = ""
                line_value = ""

                for key, val in data.items():
                    if key.startswith("comboBox"):
                        combo_value = val.strip()
                    elif key.startswith("lineEdit"):
                        line_value = val.strip()

                if not combo_value:
                    missing_fields.append(f"{tab_name} → {frame_name}: ยังไม่ได้เลือกค่า")
                elif combo_value.lower() in ["not pass", "not check"] and not line_value:
                    missing_fields.append(
                        f"{tab_name} → {frame_name}: โปรดกรอกหมายเหตุสำหรับ '{combo_value}'"
                    )

        if missing_fields:
            msg = "\n".join(missing_fields)
            QMessageBox.warning(self, "Incomplete Data", f"กรุณากรอกข้อมูลให้ครบ:\n\n{msg}")
            return False

        return True

    # ============================================================
    # ✅ บันทึกข้อมูลลง Excel
    # ============================================================
    def _save_login_info_to_excel(self):
        """บันทึกข้อมูลลง Excel ตามค่าใน comboBox และ lineEdit"""
        try:
            self._collect_all_tab_data()

            if not self._is_all_tab_filled():
                log.warning("ข้อมูลไม่ครบ ไม่สามารถบันทึกได้")
                return

            if not self.file_path:
                log.error("ไม่มี file_path")
                return

            # ดึงข้อมูล product_name จาก file_path
            txt_filename = os.path.basename(self.file_path)
            base_filename = os.path.splitext(txt_filename)[0]
            # เอา 'shotcount_' ออกเพื่อได้ชื่อ product จริง
            product_name = base_filename.replace('shotcount_', '')
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            # ✅ ตั้งชื่อไฟล์ใหม่โดยไม่มี 'shotcount_' และมี timestamp
            new_excel_filename = f"{product_name}_PM_{timestamp}.xlsx"
            original_excel_filename = base_filename + ".xlsx"
            
            # ✅ เส้นทางไฟล์ต้นฉบับ (ใน PM in Progress)
            original_path = os.path.join(self.pm_in_progress_dir, original_excel_filename)
            
            # ✅ สร้างโฟลเดอร์ย่อยตาม product ใน PM compleat
            product_complete_dir = os.path.join(self.pm_complete_dir, product_name)
            os.makedirs(product_complete_dir, exist_ok=True)
            
            # ✅ เส้นทางไฟล์ใหม่ (ใน PM compleat/product_name/)
            new_path = os.path.join(product_complete_dir, new_excel_filename)

            if not os.path.exists(original_path):
                log.error("ไม่พบไฟล์ Excel: %s", original_path)
                return

            # ✅ คัดลอกไฟล์จาก PM in Progress ไปยัง PM compleat
            shutil.copy(original_path, new_path)
            log.info("สร้างไฟล์ใหม่สำหรับบันทึก PM: %s", new_path)

            wb = load_workbook(new_path)
            ws = wb.active

            # ============================================================
            # ✅ Mapping แถวตาม tab/frame
            # ============================================================
            mapping = {
                "tab1": {"frame_5": 10, "frame_6": 11},
                "tab2": {"frame_7": 13},
                "tab3": {"frame_4": 15, "frame_8": 16, "frame_10": 19},
                "tab4": {"frame_11": 21},
                "tab5": {"frame_12": 23},
                "tab6": {"frame_14": 26, "frame_15": 27, "frame_18": 29},
            }

            bold_center = Font(bold=True)
            center_align = Alignment(horizontal="center", vertical="center")

            # ✅ เขียนค่าจาก comboBox + lineEdit
            for tab_name, frames in self.tab_data.items():
                for frame_name, data in frames.items():
                    row = mapping.get(tab_name, {}).get(frame_name)
                    if not row:
                        continue

                    combo_value = ""
                    line_value = ""
                    for key, val in data.items():
                        if key.startswith("comboBox"):
                            combo_value = val.strip()
                        elif key.startswith("lineEdit"):
                            line_value = val.strip()

                    # ล้างค่าก่อนเขียน
                    for col in ["N", "O", "P", "Q"]:
                        ws[f"{col}{row}"] = ""

                    cell = None
                    if combo_value.lower() == "pass":
                        cell = ws[f"N{row}"]
                    elif combo_value.lower() == "not pass":
                        cell = ws[f"O{row}"]
                    elif combo_value.lower() == "not check":
                        cell = ws[f"P{row}"]

                    if cell:
                        cell.value = "✓"
                        cell.font = bold_center
                        cell.alignment = center_align

                    if line_value:
                        note_cell = ws[f"Q{row}"]
                        note_cell.value = line_value
                        note_cell.font = Font(name='Angsana New', size=12, bold=True)
                        note_cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

            # ✅ เพิ่มข้อมูลผู้ตรวจสอบ (Staff / Leader)
            staff_name = self._current_login_info.get("staff_name", "")
            staff_id   = self._current_login_info.get("staff_scan", "")
            staff_date = self._current_login_info.get("staff_date", "")
            leader_name = self._current_login_info.get("leader_name", "")
            leader_id   = self._current_login_info.get("leader_scan", "")
            leader_date = self._current_login_info.get("leader_date", "")

            ws["L66"] = f"Check by Fixture room :  {staff_name} ({staff_id})     Date : {staff_date}"
            ws["L67"] = f"Checked and Approved by :  {leader_name} ({leader_id})     Date : {leader_date}"

            # ✅ บันทึกไฟล์จริง
            wb.save(new_path)
            log.info("บันทึกข้อมูล PM และชื่อผู้ตรวจสอบเรียบร้อยที่: %s", new_path)

            # ✅ ✅ ✅ เพิ่มส่วนนี้: รีเซ็ตไฟล์ต้นฉบับและไฟล์นับ shot
            self._reset_after_pm_completion(original_path)

            # ✅ แสดงข้อความสำเร็จ
            QMessageBox.information(self, "บันทึกสำเร็จ",
                f"บันทึกข้อมูล PM เรียบร้อยที่:\n{new_excel_filename}\n\n"
                f"ไฟล์ถูกบันทึกในโฟลเดอร์:\n{product_complete_dir}")

            log.info("ปิดหน้าต่าง PM และกลับสู่หน้าหลัก")
            self.close()

        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการบันทึกข้อมูล: %s", e)
            QMessageBox.critical(self, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการบันทึก: {e}")

    def _reset_after_pm_completion(self, original_excel_path):
        """รีเซ็ตไฟล์หลังจากทำ PM เสร็จสิ้น"""
        try:
            log.info("เริ่มกระบวนการรีเซ็ตหลังทำ PM...")
            
            # ✅ ตรวจสอบว่า original_excel_path มีอยู่จริง
            if not os.path.exists(original_excel_path):
                log.warning("ไม่พบไฟล์ Excel ต้นฉบับ: %s", original_excel_path)
                excel_reset_success = False
            else:
                # 1. รีเซ็ตไฟล์ Excel ต้นฉบับ
                excel_reset_success = self._reset_original_excel_file(original_excel_path)
            
            # 2. รีเซ็ตไฟล์ TXT นับ shot
            txt_reset_success = self._reset_shot_count_file()
            
            # 3. รีเซ็ตค่าใน memory ของ Shot Counter
            log.debug("กำลังรีเซ็ต memory... self.shot_counter = %s", self.shot_counter)
            memory_reset_success = self._reset_shot_counter_memory()
            
            # ✅ อ่านค่าไฟล์ TXT หลังรีเซ็ตเพื่อยืนยัน
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    file_content = f.read().strip()
                    log.debug("ไฟล์ TXT หลังรีเซ็ต: '%s'", file_content)
            
            # ✅ ตรวจสอบผลลัพธ์การรีเซ็ตทุกส่วน
            if excel_reset_success and txt_reset_success and memory_reset_success:
                log.info("รีเซ็ตไฟล์ Excel, TXT และ Memory เรียบร้อย")
            else:
                log.warning("การรีเซ็ตไฟล์มีบางอย่างผิดพลาด: excel=%s, txt=%s, memory=%s", excel_reset_success, txt_reset_success, memory_reset_success)
                
        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการรีเซ็ตไฟล์: %s", e)
            import traceback
            traceback.print_exc()

    def _reset_shot_counter_memory(self):
        """รีเซ็ตค่าใน memory ของ Shot Counter"""
        try:
            # ✅ ใช้ shot_counter ที่ส่งผ่าน parameter โดยตรง
            if self.shot_counter is not None:
                shot_counter = self.shot_counter
                log.debug("รีเซ็ต Shot Counter โดยตรงจาก parameter")
            elif hasattr(self.parent, 'shot_counter'):
                shot_counter = self.parent.shot_counter
                log.debug("รีเซ็ต Shot Counter ผ่าน parent")
            else:
                log.error("ไม่พบ shot_counter ใน parameter หรือ parent")
                return False

            # ✅ รีเซ็ตค่าทั้งหมด
            shot_counter.shot_count = 0
            shot_counter.start_lot_shot = 0
            shot_counter.last_total_sheet = 0  # ✅ เปลี่ยนจาก None เป็น 0
            shot_counter.pm_triggered = False
            shot_counter.pm_window_visible = False
            shot_counter._should_stop_for_pm = False  # ✅ รีเซ็ตสถานะหยุด PM
            
            # ✅ เพิ่ม: ตั้งค่าสถานะ "พึ่งรีเซ็ต"
            shot_counter._just_reset = True
            
            # ✅ อัปเดต UI
            if hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                self.parent.ui.shot_cnt.setText("0")
                self.parent.ui.shot_cnt.setStyleSheet("")  # ✅ คืนค่าสไตล์ปกติ
            
            log.info("รีเซ็ต Shot Counter memory เรียบร้อย: shot_count=0, last_total_sheet=0")
            return True
            
        except Exception as e:
            log.error("ไม่สามารถรีเซ็ต Shot Counter memory: %s", e)
            return False

    def _reset_original_excel_file(self, original_excel_path):
        """รีเซ็ตไฟล์ Excel เดิมโดยคัดลอกจาก template"""
        try:
            # ✅ ใช้ self.templates_dir ที่ตั้งค่าใน __init__
            template_dir = self.templates_dir
            
            # ตรวจสอบว่า template_dir มีอยู่จริง
            if not os.path.exists(template_dir):
                log.error("ไม่พบโฟลเดอร์ template: %s", template_dir)
                return False
                
            template_files = [f for f in os.listdir(template_dir) if f.lower().endswith(".xlsx")]
            
            if not template_files:
                log.error("ไม่พบไฟล์ template ในโฟลเดอร์: %s", template_dir)
                return False
                
            template_path = os.path.join(template_dir, template_files[0])
            
            # ตรวจสอบว่า template file มีอยู่จริง
            if not os.path.exists(template_path):
                log.error("ไม่พบไฟล์ template: %s", template_path)
                return False
            
            # คัดลอก template ไปทับไฟล์เดิม
            shutil.copy(template_path, original_excel_path)
            log.info("รีเซ็ตไฟล์ Excel เดิมเรียบร้อย: %s", original_excel_path)
            
            return True  # ✅ return True เมื่อสำเร็จ
            
        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการรีเซ็ตไฟล์ Excel: %s", e)
            import traceback
            traceback.print_exc()
            return False

    def _reset_shot_count_file(self):
        """รีเซ็ตไฟล์ TXT ที่เก็บค่า shot count เป็น 0"""
        try:
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, "w") as f:
                    f.write("0\n")
                log.info("รีเซ็ตไฟล์ TXT เรียบร้อย: %s", self.file_path)
                return True  # ✅ return True เมื่อสำเร็จ
            else:
                log.warning("ไม่พบไฟล์ TXT ที่จะรีเซ็ต: %s", self.file_path)
                return False
                
        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการรีเซ็ตไฟล์ TXT: %s", e)
            return False

    # ============================================================
    # ✅ แสดงข้อมูลล็อกอิน
    # ============================================================
    def _display_login_info(self, login_data):
        try:
            staff = login_data.get("staff_data", {})
            leader = login_data.get("leader_data", {})
            staff_scan = staff.get("scanned_data", "")
            staff_date = staff.get("pm_date", "")
            leader_scan = leader.get("scanned_data", "")
            leader_date = leader.get("pm_date", "") or login_data.get("pm_date", "") or staff_date
            staff_name = staff.get("name_staff", "")
            leader_name = leader.get("name_leader", "")

            self.ui.lineEdit_17.setText(f"{staff_name} ({staff_scan})")
            self.ui.lineEdit_13.setText(f"{leader_name} ({leader_scan})")
            self.ui.lineEdit_18.setText(str(staff_date))
            self.ui.lineEdit_16.setText(str(leader_date))

            self._current_login_info = {
                "staff_scan": staff_scan,
                "leader_scan": leader_scan,
                "staff_date": staff_date,
                "leader_date": leader_date,
                "staff_name": staff_name,
                "leader_name": leader_name,
            }

            log.info("Display login info: %s / %s", staff_name, leader_name)

        except Exception as e:
            log.error("Display login info error: %s", e)

    def set_excel_data(self, excel_data):
        """ตั้งค่าข้อมูลจาก Excel ให้กับ UI"""
        table = self.ui.tableWidget
        for col, (lot_id, shot_count) in enumerate(excel_data):
            if col >= table.columnCount():
                break

            # รวม Lot + Shot ไว้ใน cell เดียว แยกด้วย \n
            text = f"{lot_id}\n{shot_count}"
            item = QTableWidgetItem(text)
            item.setTextAlignment(Qt.AlignCenter)   # จัดกลาง
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # ป้องกันแก้ไข

            # ใส่ข้อมูลลงในคอลัมน์เดียว (เช่น column 0)
            table.setItem(0, col, item)

    def parse_and_set_row_3b_data(self, row_3b_text):
        """
        แยกข้อมูลจากข้อความในแถว 3B และตั้งค่าใน UI
        """
        try:
            # ประกาศ data_dict ก่อนใช้งาน
            data_dict = {}
            
            # ใช้ regex เพื่อแยกข้อมูล (จัดการกับช่องว่างไม่แน่นอน)
            patterns = {
                'product_name': r'Product name:\s*([^\n]+?)\s*(?=Tooling code:|$)',
                'tooling_code': r'Tooling code:\s*([^\n]+?)\s*(?=Tooling for:|$)',
                'tooling_for': r'Tooling for:\s*([^\n]+?)\s*(?=Next p\.m\.:|$)',
                'next_pm': r'Next p\.m\.:\s*([^\n]+)'
            }
            
            for key, pattern in patterns.items():
                match = re.search(pattern, row_3b_text, re.DOTALL)
                if match:
                    data_dict[key] = match.group(1).strip()
            
            # ตั้งค่าใน UI ตาม key ที่พบ (แบบ read-only)
            if 'product_name' in data_dict:
                self.ui.lineEdit.setText(data_dict['product_name'])
                self.ui.lineEdit.setReadOnly(True)
                self.ui.lineEdit.setStyleSheet("background-color: #f0f0f0;")
                log.debug("Product: %s", data_dict['product_name'])
            else:
                log.warning("ไม่พบข้อมูล Product name")
            
            if 'tooling_code' in data_dict:
                self.ui.lineEdit_2.setText(data_dict['tooling_code'])
                self.ui.lineEdit_2.setReadOnly(True)
                self.ui.lineEdit_2.setStyleSheet("background-color: #f0f0f0;")
                log.debug("Tooling: %s", data_dict['tooling_code'])
            else:
                log.warning("ไม่พบข้อมูล Tooling code")
            
            if 'tooling_for' in data_dict:
                tooling_for = data_dict['tooling_for']
                if tooling_for.upper() == 'E-FPC':
                    self.ui.efpc.setChecked(True)
                    self.ui.smt.setChecked(False)
                    self.ui.efpc.setEnabled(False)
                    self.ui.smt.setEnabled(False)
                    log.debug("Tooling for: E-FPC")
                elif tooling_for.upper() == 'SMT':
                    self.ui.smt.setChecked(True)
                    self.ui.efpc.setChecked(False)
                    self.ui.efpc.setEnabled(False)
                    self.ui.smt.setEnabled(False)
                    log.debug("Tooling for: SMT")
                else:
                    log.warning("ไม่รู้จัก Tooling for: %s", tooling_for)
            else:
                log.warning("ไม่พบข้อมูล Tooling for")
            
            if 'next_pm' in data_dict:
                next_pm_value = data_dict['next_pm']
                self.ui.lineEdit_3.setText(next_pm_value)
                self.ui.lineEdit_3.setReadOnly(True)
                self.ui.lineEdit_3.setStyleSheet("background-color: #f0f0f0;")
                log.debug("Next PM: %s", next_pm_value)
                
                # 🔥 ล้างสีเดิมและเติมสีใหม่
                self._clear_table_highlight()
                self._highlight_table_by_next_pm(next_pm_value)
            else:
                log.warning("ไม่พบข้อมูล Next PM")

            log.info("แยกข้อมูลจาก B3 สำเร็จ")

        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการแยกข้อมูลจาก B3: %s", e)
            log.debug("ข้อความที่กำลังแยก: %s", row_3b_text)

    def _highlight_table_by_next_pm(self, next_pm_text):
        """
        เติมสีในตาราง tableWidget ตามค่า Next PM โดยคำนวณตำแหน่งจากโครงสร้างตาราง
        ตารางมีโครงสร้าง: 
        - แถว 0: 1-10
        - แถว 1: 11-20  
        - แถว 2: 21-30
        - ไปเรื่อยๆ...
        """
        try:
            # แยกค่า Next PM
            pm_numbers = []
            if '-' in next_pm_text:
                parts = next_pm_text.split('-')
                try:
                    pm_numbers = [int(part.strip()) for part in parts if part.strip().isdigit()]
                except ValueError:
                    log.warning("ไม่สามารถแปลงค่า Next PM เป็นตัวเลข: %s", next_pm_text)
                    return
            else:
                try:
                    pm_numbers = [int(next_pm_text.strip())]
                except ValueError:
                    log.warning("ไม่สามารถแปลงค่า Next PM เป็นตัวเลข: %s", next_pm_text)
                    return

            if not pm_numbers:
                log.warning("ไม่พบตัวเลขในค่า Next PM")
                return

            log.debug("เติมสีตารางสำหรับตัวเลข: %s", pm_numbers)
            
            # สีสำหรับการเน้น (สีเหลืองสำหรับตัวเลขแรก, สีแดงสำหรับตัวเลขที่สอง)
            colors = ["#FFFF00", "#FF0000"]  # สีเหลือง, สีแดง
            
            table = self.ui.tableWidget
            found_count = 0
            
            # คำนวณตำแหน่งและเติมสี
            for i, pm_num in enumerate(pm_numbers):
                # คำนวณแถวและคอลัมน์จากตัวเลข
                # สูตร: 
                # - row = (number - 1) // 10  (เพราะ 10 คอลัมน์ต่อแถว)
                # - col = (number - 1) % 10
                
                row = (pm_num - 1) // 10
                col = (pm_num - 1) % 10
                
                # ตรวจสอบว่าตำแหน่งอยู่ในขอบเขตของตาราง
                if 0 <= row < table.rowCount() and 0 <= col < table.columnCount():
                    item = table.item(row, col)
                    if item is None:
                        # ถ้าเซลล์ว่าง ให้สร้าง item ใหม่
                        item = QTableWidgetItem(str(pm_num))
                        item.setTextAlignment(Qt.AlignCenter)
                        table.setItem(row, col, item)
                    else:
                        # อัปเดตข้อความให้แน่ใจว่าแสดงตัวเลขที่ถูกต้อง
                        item.setText(str(pm_num))
                    
                    # เติมสี
                    color_index = min(i, len(colors) - 1)
                    item.setBackground(QColor(colors[color_index]))
                    
                    # ตั้งค่าสไตล์ตัวอักษรให้เด่นชัด
                    item.setForeground(QColor("#000000"))  # สีตัวอักษรดำ
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                    
                    # ตั้งค่าให้ไม่สามารถแก้ไขได้
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    
                    found_count += 1
                    log.debug("เติมสีเซลล์ (%s, %s) สำหรับหมายเลข %s ด้วยสี %s", row, col, pm_num, colors[color_index])
                else:
                    log.warning("ตำแหน่ง (%s, %s) สำหรับหมายเลข %s อยู่นอกขอบเขตตาราง", row, col, pm_num)

            log.debug("เติมสี %s เซลล์จาก %s ตัวเลขที่ต้องการ", found_count, len(pm_numbers))

        except Exception as e:
            log.error("เกิดข้อผิดพลาดในการเติมสีตาราง: %s", e)

    def _clear_table_highlight(self):
        """ล้างสีทั้งหมดในตาราง"""
        try:
            table = self.ui.tableWidget
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setBackground(QColor("#FFFFFF"))
                        item.setForeground(QColor("#000000"))
                        font = item.font()
                        font.setBold(False)
                        item.setFont(font)
            log.debug("ล้างสีตารางเรียบร้อย")
        except Exception as e:
            log.warning("ไม่สามารถล้างสีตาราง: %s", e)