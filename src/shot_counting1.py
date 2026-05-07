import os
import re
import sys
import time
import numpy as np
import math
import shutil
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import column_index_from_string
from openpyxl.cell.rich_text import TextBlock, CellRichText
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFrame, QGraphicsView, QGraphicsTextItem, QGraphicsDropShadowEffect,QScrollArea,QDialogButtonBox, QLabel,QLineEdit, QPushButton, QComboBox,QSizePolicy
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtCore import QEvent, Qt,Signal, QObject
from openpyxl.styles import colors
from sklearn.linear_model import LinearRegression
from src.data_upload import DataUploader
from src.ui_PM import Ui_PM
from src.login_pm import LoginPM
from copy import copy
from src.logout_window import LogoutWindow
from openpyxl.cell.cell import MergedCell
from src.config_manager import config_manager

class Pmwindow(QMainWindow):
    def __init__(self, parent=None, login_data=None, file_path=None, shot_counter=None):
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
            shot_counter.path_changed.connect(self._update_file_path)
        else:
            # ✅ ใช้ค่า default ถ้าไม่มี shot_counter
            self.paths_config = config_manager.get_paths_config()
            self.templates_dir = config_manager.get_full_path(self.paths_config.get('templates', 'templat'))

        self.ui = Ui_PM()
        self.ui.setupUi(self)
        self.ui.save.clicked.connect(self._save_login_info_to_excel)
        self.setStyleSheet("")

        self.file_path = file_path
        self.tab_data = {}
        self.paths_config = config_manager.get_paths_config()
        self.pm_folder = config_manager.get_full_path(self.paths_config.get('pm_folder', 'PM'))

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
            print("[PM UI] ✅ Connected tab signals successfully")

        except Exception as e:
            print(f"[PM UI] ❌ Error connecting signals: {e}")

    def _update_file_path(self, new_path):
        """อัปเดต file_path เมื่อ ShotCounter เปลี่ยน"""
        self.file_path = new_path
        print(f"🔄 Pmwindow อัปเดต path เป็น: {new_path}")
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
            print(f"[PM UI] ❌ Error collecting all tab data: {e}")

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
                print("⚠️ ข้อมูลไม่ครบ ไม่สามารถบันทึกได้")
                return

            if not self.file_path:
                print("[PM UI] ❌ ไม่มี file_path")
                return

            txt_filename = os.path.basename(self.file_path)
            base_filename = os.path.splitext(txt_filename)[0]
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_excel_filename = f"{base_filename}_PM_{timestamp}.xlsx"
            original_excel_filename = base_filename + ".xlsx"
            dest_folder = self.pm_folder
            original_path = os.path.join(dest_folder, original_excel_filename)
            new_path = os.path.join(dest_folder, new_excel_filename)

            if not os.path.exists(original_path):
                print(f"[PM UI] ❌ ไม่พบไฟล์ Excel: {original_path}")
                return

            shutil.copy(original_path, new_path)
            print(f"[PM UI] 📄 สร้างไฟล์ใหม่สำหรับบันทึก PM: {new_path}")

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
            print(f"[PM UI] 💾 บันทึกข้อมูล PM และชื่อผู้ตรวจสอบเรียบร้อยที่: {new_path}")

            # ✅ ✅ ✅ เพิ่มส่วนนี้: รีเซ็ตไฟล์ต้นฉบับและไฟล์นับ shot
            self._reset_after_pm_completion(original_path)

            # ✅ แสดงข้อความสำเร็จ
            QMessageBox.information(self, "บันทึกสำเร็จ",
                f"บันทึกข้อมูล PM เรียบร้อยที่:\n{new_excel_filename}")

            print("[PM UI] 🔒 ปิดหน้าต่าง PM และกลับสู่หน้าหลัก")
            self.close()

        except Exception as e:
            print(f"[PM UI] ❌ เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")
            QMessageBox.critical(self, "ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการบันทึก: {e}")

    def _reset_after_pm_completion(self, original_excel_path):
        """รีเซ็ตไฟล์หลังจากทำ PM เสร็จสิ้น"""
        try:
            print("[PM UI] 🔄 เริ่มกระบวนการรีเซ็ตหลังทำ PM...")
            
            # ✅ ตรวจสอบว่า original_excel_path มีอยู่จริง
            if not os.path.exists(original_excel_path):
                print(f"[PM UI] ⚠️ ไม่พบไฟล์ Excel ต้นฉบับ: {original_excel_path}")
                excel_reset_success = False
            else:
                # 1. รีเซ็ตไฟล์ Excel ต้นฉบับ
                excel_reset_success = self._reset_original_excel_file(original_excel_path)
            
            # 2. รีเซ็ตไฟล์ TXT นับ shot
            txt_reset_success = self._reset_shot_count_file()
            
            # 3. รีเซ็ตค่าใน memory ของ Shot Counter
            print(f"[PM UI] กำลังรีเซ็ต memory... self.shot_counter = {self.shot_counter}")
            memory_reset_success = self._reset_shot_counter_memory()
            
            # ✅ อ่านค่าไฟล์ TXT หลังรีเซ็ตเพื่อยืนยัน
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    file_content = f.read().strip()
                    print(f"[PM UI] ไฟล์ TXT หลังรีเซ็ต: '{file_content}'")
            
            # ✅ ตรวจสอบผลลัพธ์การรีเซ็ตทุกส่วน
            if excel_reset_success and txt_reset_success and memory_reset_success:
                print("[PM UI] 🔄 รีเซ็ตไฟล์ Excel, TXT และ Memory เรียบร้อย")
            else:
                print(f"[PM UI] ⚠️ การรีเซ็ตไฟล์มีบางอย่างผิดพลาด: excel={excel_reset_success}, txt={txt_reset_success}, memory={memory_reset_success}")
                
        except Exception as e:
            print(f"[PM UI] ❌ เกิดข้อผิดพลาดในการรีเซ็ตไฟล์: {e}")
            import traceback
            traceback.print_exc()

    def _reset_shot_counter_memory(self):
        """รีเซ็ตค่าใน memory ของ Shot Counter"""
        try:
            # ✅ ใช้ shot_counter ที่ส่งผ่าน parameter โดยตรง
            if self.shot_counter is not None:
                shot_counter = self.shot_counter
                print(f"[PM UI] 🔄 รีเซ็ต Shot Counter โดยตรงจาก parameter")
            elif hasattr(self.parent, 'shot_counter'):
                shot_counter = self.parent.shot_counter
                print(f"[PM UI] 🔄 รีเซ็ต Shot Counter ผ่าน parent")
            else:
                print("[PM UI] ❌ ไม่พบ shot_counter ใน parameter หรือ parent")
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
            
            print(f"[PM UI] 🔄 รีเซ็ต Shot Counter memory เรียบร้อย: shot_count=0, last_total_sheet=0")
            return True
            
        except Exception as e:
            print(f"[PM UI] ❌ ไม่สามารถรีเซ็ต Shot Counter memory: {e}")
            return False

    def _reset_original_excel_file(self, original_excel_path):
        """รีเซ็ตไฟล์ Excel เดิมโดยคัดลอกจาก template"""
        try:
            # ✅ ใช้ self.templates_dir ที่ตั้งค่าใน __init__
            template_dir = self.templates_dir
            
            # ตรวจสอบว่า template_dir มีอยู่จริง
            if not os.path.exists(template_dir):
                print(f"[PM UI] ❌ ไม่พบโฟลเดอร์ template: {template_dir}")
                return False
                
            template_files = [f for f in os.listdir(template_dir) if f.lower().endswith(".xlsx")]
            
            if not template_files:
                print(f"[PM UI] ❌ ไม่พบไฟล์ template ในโฟลเดอร์: {template_dir}")
                return False
                
            template_path = os.path.join(template_dir, template_files[0])
            
            # ตรวจสอบว่า template file มีอยู่จริง
            if not os.path.exists(template_path):
                print(f"[PM UI] ❌ ไม่พบไฟล์ template: {template_path}")
                return False
            
            # คัดลอก template ไปทับไฟล์เดิม
            shutil.copy(template_path, original_excel_path)
            print(f"[PM UI] 🔄 รีเซ็ตไฟล์ Excel เดิมเรียบร้อย: {original_excel_path}")
            
            return True  # ✅ return True เมื่อสำเร็จ
            
        except Exception as e:
            print(f"[PM UI] ❌ เกิดข้อผิดพลาดในการรีเซ็ตไฟล์ Excel: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _reset_shot_count_file(self):
        """รีเซ็ตไฟล์ TXT ที่เก็บค่า shot count เป็น 0"""
        try:
            if self.file_path and os.path.exists(self.file_path):
                with open(self.file_path, "w") as f:
                    f.write("0\n")
                print(f"[PM UI] 🔄 รีเซ็ตไฟล์ TXT เรียบร้อย: {self.file_path}")
                return True  # ✅ return True เมื่อสำเร็จ
            else:
                print(f"[PM UI] ⚠️ ไม่พบไฟล์ TXT ที่จะรีเซ็ต: {self.file_path}")
                return False
                
        except Exception as e:
            print(f"[PM UI] ❌ เกิดข้อผิดพลาดในการรีเซ็ตไฟล์ TXT: {e}")
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

            print(f"[PM UI] ✅ Display login info: {staff_name} / {leader_name}")

        except Exception as e:
            print(f"[PM UI] ❌ Display login info error: {e}")

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
                print(f"📦 Product: {data_dict['product_name']}")
            else:
                print("⚠️ ไม่พบข้อมูล Product name")
            
            if 'tooling_code' in data_dict:
                self.ui.lineEdit_2.setText(data_dict['tooling_code'])
                self.ui.lineEdit_2.setReadOnly(True)
                self.ui.lineEdit_2.setStyleSheet("background-color: #f0f0f0;")
                print(f"🔧 Tooling: {data_dict['tooling_code']}")
            else:
                print("⚠️ ไม่พบข้อมูล Tooling code")
            
            if 'tooling_for' in data_dict:
                tooling_for = data_dict['tooling_for']
                if tooling_for.upper() == 'E-FPC':
                    self.ui.efpc.setChecked(True)
                    self.ui.smt.setChecked(False)
                    self.ui.efpc.setEnabled(False)
                    self.ui.smt.setEnabled(False)
                    print("🏷️ Tooling for: E-FPC")
                elif tooling_for.upper() == 'SMT':
                    self.ui.smt.setChecked(True)
                    self.ui.efpc.setChecked(False)
                    self.ui.efpc.setEnabled(False)
                    self.ui.smt.setEnabled(False)
                    print("🏷️ Tooling for: SMT")
                else:
                    print(f"⚠️ ไม่รู้จัก Tooling for: {tooling_for}")
            else:
                print("⚠️ ไม่พบข้อมูล Tooling for")
            
            if 'next_pm' in data_dict:
                next_pm_value = data_dict['next_pm']
                self.ui.lineEdit_3.setText(next_pm_value)
                self.ui.lineEdit_3.setReadOnly(True)
                self.ui.lineEdit_3.setStyleSheet("background-color: #f0f0f0;")
                print(f"⏭️ Next PM: {next_pm_value}")
                
                # 🔥 ล้างสีเดิมและเติมสีใหม่
                self._clear_table_highlight()
                self._highlight_table_by_next_pm(next_pm_value)
            else:
                print("⚠️ ไม่พบข้อมูล Next PM")
                
            print(f"✅ แยกข้อมูลจาก B3 สำเร็จ")
            
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการแยกข้อมูลจาก B3: {e}")
            # แสดงข้อความ row_3b_text เพื่อ debugging
            print(f"📄 ข้อความที่กำลังแยก: {row_3b_text}")

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
                    print(f"⚠️ ไม่สามารถแปลงค่า Next PM เป็นตัวเลข: {next_pm_text}")
                    return
            else:
                try:
                    pm_numbers = [int(next_pm_text.strip())]
                except ValueError:
                    print(f"⚠️ ไม่สามารถแปลงค่า Next PM เป็นตัวเลข: {next_pm_text}")
                    return
            
            if not pm_numbers:
                print("⚠️ ไม่พบตัวเลขในค่า Next PM")
                return
            
            print(f"🎨 เติมสีตารางสำหรับตัวเลข: {pm_numbers}")
            
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
                    print(f"✅ เติมสีเซลล์ ({row}, {col}) สำหรับหมายเลข {pm_num} ด้วยสี {colors[color_index]}")
                else:
                    print(f"⚠️ ตำแหน่ง ({row}, {col}) สำหรับหมายเลข {pm_num} อยู่นอกขอบเขตตาราง")
            
            print(f"🎯 เติมสี {found_count} เซลล์จาก {len(pm_numbers)} ตัวเลขที่ต้องการ")
                
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการเติมสีตาราง: {e}")

    def _clear_table_highlight(self):
        """
        ล้างสีทั้งหมดในตาราง
        """
        try:
            table = self.ui.tableWidget
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setBackground(QColor("#FFFFFF"))  # สีขาว
                        item.setForeground(QColor("#000000"))  # สีดำ
                        font = item.font()
                        font.setBold(False)
                        item.setFont(font)
            print("🧹 ล้างสีตารางเรียบร้อย")
        except Exception as e:
            print(f"⚠️ ไม่สามารถล้างสีตาราง: {e}")
    

class ShotCounter(QObject):
    path_changed = Signal(str)
    def __init__(self, plc_window, parent_window=None, lot_size_value=1, product_data=None):
        super().__init__()
        self.plc_window = plc_window
        self.parent = parent_window
        self.lot_size_value = lot_size_value
        self.product_data = product_data or {}
        self.main_window = parent_window
        self._should_stop_for_pm = False  # ✅ สถานะหยุดสำหรับ PM
        self.max_shot_limit = 30000  # ✅ กำหนดค่า limit
        # โหลด configuration
        self.paths_config = config_manager.get_paths_config()
        
        # ใช้ paths จาก config
        self.base_dir = config_manager.get_full_path(self.paths_config.get('shot_counts', 'shot_counts'))
        self.pm_folder = config_manager.get_full_path(self.paths_config.get('pm_folder', 'PM'))
        self.templates_dir = config_manager.get_full_path(self.paths_config.get('templates', 'templat'))
        # ✅ ตรวจสอบและสร้างโฟลเดอร์ถ้ายังไม่มี
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            print(f"📁 สร้างโฟลเดอร์ templates: {self.templates_dir}")
        
        # ✅ ตรวจสอบว่า templates_dir มีไฟล์ template
        template_files = [f for f in os.listdir(self.templates_dir) if f.lower().endswith(".xlsx")]
        if not template_files:
            print(f"⚠️ ไม่พบไฟล์ template (.xlsx) ในโฟลเดอร์: {self.templates_dir}")
        else:
            print(f"✅ พบไฟล์ template: {template_files[0]}")



        product_name = self.product_data.get('product_name', 'N/A')
        tooling_code = self.product_data.get('tooling_code', 'N/A')
        #print(f"Product Name PM: {product_name}")
        #print(f"tooling_code PM: {tooling_code}")
        self.pm_window = None  # เก็บ reference หน้าต่าง PM
        self.pm_window_visible = False  # สถานะการแสดงหน้าต่าง
        self.pm_triggered = False  # สถานะการ triggered PM
        self.old_shot_count = 0
        self.product_name = None
        self.shot_count = 0
        self.last_total_sheet = None
        self.file_path = None
        self.start_lot_shot = 0
        self._check_product_change()
        self._load_product_and_data()
         # โหลดโฟลเดอร์ล่าสุดจาก config
        self._load_last_selected_directory()
        self.path_changed.connect(self._on_path_changed)
        self.plc_window.data_updated.connect(self.handle_plc_update)

        # เชื่อมต่อปุ่ม finish_lot กับฟังก์ชันแสดง Logout UI
        if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'finish_lot'):
            try:
                # ✅ เปลี่ยนเป็นเรียก show_logout_window ของ MainWindow โดยตรง
                self.parent.ui.finish_lot.clicked.connect(self.parent.show_logout_window)
                print("[ShotCounter] ✔ เชื่อมปุ่ม finish กับ parent.show_logout_window สำเร็จ")
            except Exception as e:
                print(f"[ShotCounter] ❌ เชื่อมปุ่ม finish ไม่สำเร็จ: {e}")
        else:
            print("[ShotCounter] ⚠️ ไม่พบ parent.ui.finish — เชื่อมปุ่มไม่สำเร็จ")

    def _on_path_changed(self, new_path):
        """อัปเดตทุก UI ที่เกี่ยวข้อง"""
        if self.pm_window:
            self.pm_window.file_path = new_path

    def _check_product_change(self):
        """ตรวจสอบการเปลี่ยนผลิตภัณฑ์และรีเซ็ตข้อมูลถ้าจำเป็น"""
        try:
            current_data = self.plc_window.get_product_and_shot_count()
            new_product_name = current_data.get("product_name", "")
            
            # ถ้าเป็นผลิตภัณฑ์ใหม่ หรือเป็นครั้งแรกที่เริ่ม
            if new_product_name != self.product_name:
                print(f"🔄 Product changed from {self.product_name} to {new_product_name}")
                self._reset_for_new_product(new_product_name)
                
        except Exception as e:
            print(f"❌ Error checking product change: {e}")

    def _reset_for_new_product(self, new_product_name):
        """รีเซ็ตข้อมูลสำหรับผลิตภัณฑ์ใหม่"""
        try:
            # ✅ ตรวจสอบว่า new_product_name ไม่ว่าง
            if not new_product_name or new_product_name.strip() == "":
                print("⚠️ ไม่สามารถรีเซ็ตได้: product_name ใหม่ว่าง")
                return
                
            print(f"🔄 Resetting for new product: {new_product_name}")
            
            # รีเซ็ตค่าใน memory
            self.product_name = new_product_name
            # ❌ ไม่รีเซ็ต shot_count เป็น 0
            # self.shot_count = 0  # ลบบรรทัดนี้
            self.start_lot_shot = self.shot_count  # ใช้ค่าเดิม
            self.last_total_sheet = None
            self.old_shot_count = self.shot_count  # ใช้ค่าเดิม
            
            # อัพเดต file_path
            self.file_path = os.path.join(self.base_dir, f"shotcount_{self.product_name}.txt")
            
            # ✅ ไม่สร้างไฟล์ใหม่หรือรีเซ็ตค่าเป็น 0
            # with open(self.file_path, 'w') as f:
            #     f.write("0\n")  # ลบบรรทัดนี้
                
            print(f"✅ Reset complete for product: {new_product_name}, shot_count ยังคงเป็น {self.shot_count}")
            
        except Exception as e:
            print(f"❌ Error resetting for new product: {e}")


    def _load_product_and_data(self):
        """โหลดข้อมูลจากโฟลเดอร์ล่าสุดที่ผู้ใช้เลือก และดึง shot_count จากไฟล์ TXT"""
        current_data = self.plc_window.get_product_and_shot_count()
        self.product_name = current_data.get("product_name", "").strip()
        
        # ✅ ตรวจสอบว่า product_name ไม่ว่าง
        if not self.product_name:
            print("⚠️ ไม่พบ product_name จาก PLC data")
            # ใช้ค่า default หรือรอจนกว่าจะได้ product_name ที่ถูกต้อง
            return
        
        # ใช้โฟลเดอร์ล่าสุดที่ผู้ใช้เลือก
        base_dir = getattr(self, 'custom_base_dir', self.base_dir)
        self.file_path = os.path.join(base_dir, f"shotcount_{self.product_name}.txt")

        print(f"🔍 กำลังโหลดข้อมูลจาก: {self.file_path}")
        
        # ✅ โหลด shot_count จากไฟล์ TXT
        file_shot_count = None
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\n')
                        # ✅ ดึง shot_count จากไฟล์ TXT
                        file_shot_count = int(lines[0]) if lines[0].strip() else None  # ❌ เปลี่ยนจาก 0 เป็น None
                        
                        # ✅ โหลด last_total_sheet (ถ้ามี)
                        if len(lines) > 1 and lines[1].strip():
                            self.last_total_sheet = int(lines[1])
                        else:
                            self.last_total_sheet = current_data.get("total_sheet", 0)
                        
                        print(f"✅ โหลด shot_count={file_shot_count}, last_total_sheet={self.last_total_sheet} จากไฟล์ TXT")
                    else:
                        # ❌ ไม่ตั้งค่าเป็น 0 ถ้าไฟล์ว่าง
                        print("⚠️ ไฟล์ TXT ว่าง")
                        file_shot_count = None
            except Exception as e:
                print(f"❌ ข้อผิดพลาดในการโหลดไฟล์ TXT: {e}")
                file_shot_count = None  # ❌ เปลี่ยนจาก 0 เป็น None
        else:
            print("📝 ไม่พบไฟล์เดิม")
            file_shot_count = None  # ❌ เปลี่ยนจาก 0 เป็น None
        
        # ✅ ใช้ค่า shot_count จากไฟล์ TXT ถ้ามีค่า, ไม่ใช่ตั้งเป็น 0
        if file_shot_count is not None:
            self.shot_count = file_shot_count
        else:
            # ถ้าไม่สามารถโหลดค่าได้ ให้ใช้ค่าปัจจุบัน (ไม่รีเซ็ตเป็น 0)
            print("ℹ️ ใช้ค่า shot_count ปัจจุบัน")
            # self.shot_count = self.shot_count  # ค่าเดิม

        # ✅ ตั้งค่า start_lot_shot
        self.start_lot_shot = self.shot_count

        print(f"[ShotCounter] Set shot_count={self.shot_count}, start_lot_shot={self.start_lot_shot}")
        # ✅ บันทึกค่าเริ่มต้น (กรณีสร้างไฟล์ใหม่)
        self._save_shot_count()
        
        # ✅ ตรวจสอบ PM หลังจากโหลดข้อมูล
        self._check_pm_condition()

    def _check_pm_condition(self):
        """ตรวจสอบเงื่อนไขการทำ PM"""
        try:
            # ตรวจสอบว่า shot_count ถึง 30,000 หรือไม่
            if self.shot_count >= 30000 and not self.pm_triggered and not self.pm_window_visible:
                print(f"🚨 ตรวจสอบเงื่อนไข PM: shot_count={self.shot_count} >= 30000")
                print(f"🚨 PM triggered: {self.pm_triggered}, PM window visible: {self.pm_window_visible}")
                self._handle_pm_needed()
            else:
                print(f"🔍 ตรวจสอบ PM: shot_count={self.shot_count}, เงื่อนไขไม่ถึง")
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการตรวจสอบ PM: {e}")

    def _load_last_selected_directory(self):
        """โหลดโฟลเดอร์ที่ผู้ใช้เลือกล่าสุดจาก config"""
        last_dir = config_manager.current_config.get('user_preferences', {}).get('last_selected_directory', '')
        if last_dir and os.path.exists(last_dir):
            self.custom_base_dir = last_dir
            print(f"📁 โหลดโฟลเดอร์ล่าสุดจาก config: {last_dir}")
        else:
            self.custom_base_dir = self.base_dir
            print("📁 ใช้โฟลเดอร์ default จาก config")

    def select_save_directory(self):
        """ให้ผู้ใช้เลือกโฟลเดอร์สำหรับบันทึกและโหลดข้อมูล"""
        # โหลดโฟลเดอร์ล่าสุดจาก config
        last_directory = config_manager.current_config.get('user_preferences', {}).get('last_selected_directory', '')
        if not last_directory or not os.path.exists(last_directory):
            last_directory = self.base_dir
        
        directory = QFileDialog.getExistingDirectory(
            self.parent, 
            "เลือกโฟลเดอร์สำหรับบันทึกและโหลดข้อมูล Shot Count",
            last_directory
        )
        
        if directory:
            # บันทึกโฟลเดอร์ล่าสุดใน config
            if 'user_preferences' not in config_manager.current_config:
                config_manager.current_config['user_preferences'] = {}
            config_manager.current_config['user_preferences']['last_selected_directory'] = directory
            config_manager.save_config()
            
            self.custom_base_dir = directory
            print(f"✅ บันทึกโฟลเดอร์ล่าสุด: {directory}")
            
            # โหลดข้อมูลเดิมจากโฟลเดอร์ใหม่
            self._reload_data_from_new_directory(directory)
            
            # ✅ ส่ง signal หลังจากอัปเดต file_path แล้ว
            self.path_changed.emit(self.file_path)
            
            return directory

    def _reload_data_from_new_directory(self, new_directory):
        """โหลดข้อมูลเดิมจากโฟลเดอร์ใหม่ที่ผู้ใช้เลือก"""
        try:
            old_shot_count = self.shot_count
            
            # อัปเดต base_dir
            self.custom_base_dir = new_directory
            
            # โหลดข้อมูลใหม่
            self._load_product_and_data()
            
            # แจ้งเตือนการเปลี่ยนแปลง
            if old_shot_count != self.shot_count:
                print(f"🔄 ข้อมูล shot_count เปลี่ยนแปลง: {old_shot_count} → {self.shot_count}")
                
            # อัปเดต UI
            if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                self.parent.ui.shot_cnt.setText(f"{self.shot_count}")
                
            QMessageBox.information(self.parent, "โหลดข้อมูลสำเร็จ", 
                                   f"โหลดข้อมูลจากโฟลเดอร์ใหม่เรียบร้อย\n\n"
                                   f"โฟลเดอร์: {new_directory}\n"
                                   f"Shot Count ปัจจุบัน: {self.shot_count}")
                                   
        except Exception as e:
            print(f"❌ ข้อผิดพลาดในการโหลดข้อมูลจากโฟลเดอร์ใหม่: {e}")
            QMessageBox.warning(self.parent, "ข้อผิดพลาด", 
                               f"ไม่สามารถโหลดข้อมูลจากโฟลเดอร์ใหม่ได้: {e}")
    def _save_shot_count(self):
        """บันทึก shot_count และ last_total_sheet ลงไฟล์ TXT"""
        try:
            # ✅ ตรวจสอบว่า product_name ไม่ว่าง
            if not self.product_name or self.product_name.strip() == "":
                print("⚠️ ไม่สามารถบันทึกได้: product_name ว่าง")
                return
                
            with open(self.file_path, "w", encoding='utf-8') as f:
                f.write(f"{self.shot_count}\n")
                if self.last_total_sheet is not None:
                    f.write(f"{self.last_total_sheet}\n")
            print(f"[ShotCounter] ✅ บันทึก shot_count={self.shot_count} ไปยัง {self.file_path}")
        except Exception as e:
            print(f"[ShotCounter] ❌ เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}")

    def handle_plc_update(self, data):
        print(f"[ShotCounter] ⏸️ ")
        self.update()

    def update(self):
        current_data = self.plc_window.get_product_and_shot_count()
        product_name_temp = current_data.get("product_name", "")
        total_sheet = current_data.get("total_sheet", 0)
        shot_per_sheet = current_data.get("shot_count", 0)
        pcs_per_shot = current_data.get("pcs_number", 1)
        
        # ✅ ใช้ self.shot_count โดยตรง (ค่าที่โหลดจากไฟล์ TXT แล้ว)
        current_shot_count = self.shot_count
        
        # ✅ ตรวจสอบเงื่อนไข PM แบบพยากรณ์ก่อน
        self._check_predictive_pm(current_shot_count, pcs_per_shot)
        
        # ✅ ถ้าต้องหยุดสำหรับ PM ให้ไม่นับ shot เพิ่ม
        if hasattr(self, '_should_stop_for_pm') and self._should_stop_for_pm:
            print(f"[ShotCounter] ⏹️ หยุดการนับ shot เนื่องจากถึงเวลา PM")
            return
        
        # ✅ เพิ่ม: ตรวจสอบว่าพึ่งรีเซ็ตมาและยังไม่ควรนับ shot ใหม่
        if hasattr(self, '_just_reset') and self._just_reset:
            self.last_total_sheet = total_sheet
            self._just_reset = False
            print(f"[ShotCounter] ⏸️ ข้ามการนับ shot หลังรีเซ็ต, ตั้งค่า last_total_sheet เป็น {total_sheet}")
            return

        new_file_path = os.path.join(self.base_dir, f"shotcount_{product_name_temp}.txt")

        # ตรวจสอบการเปลี่ยนผลิตภัณฑ์
        if product_name_temp != self.product_name:
            self._handle_product_change(product_name_temp, new_file_path)
            return

        # ✅ แก้ไข: ตรวจสอบว่า last_total_sheet ไม่ใช่ None ก่อนเปรียบเทียบ
        if self.last_total_sheet is not None and total_sheet < self.last_total_sheet:
            print(f"[ShotCounter] 🔄 พบการ reset: total_sheet ลดลงจาก {self.last_total_sheet} เป็น {total_sheet}")
            print(f"[ShotCounter] ⏸️ ไม่นับ shot ในการ reset นี้")
            self.last_total_sheet = total_sheet  # อัปเดตค่าใหม่
            return
        
        # ✅ แก้ไข: ตรวจสอบว่า last_total_sheet ไม่ใช่ None และ total_sheet เพิ่มขึ้นจริงๆ
        if (self.last_total_sheet is not None and 
            self.last_total_sheet != total_sheet and 
            total_sheet > self.last_total_sheet):
            
            old_shot_count = self.shot_count  # ✅ เก็บค่าเดิมเพื่อตรวจสอบการเปลี่ยนแปลง

            # ✅ แก้ไข: คำนวณจำนวน sheet ที่เพิ่มขึ้นจริง
            sheet_increment = total_sheet - self.last_total_sheet
            actual_shot_increment = sheet_increment * shot_per_sheet
            
            self.shot_count += actual_shot_increment
            self.last_total_sheet = total_sheet
            self._save_shot_count()
            print(f"[ShotCounter] total_sheet changed (+{sheet_increment}), incremented shot_count by {actual_shot_increment} to {self.shot_count}")

            if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                self.parent.ui.shot_cnt.setText(f"{self.shot_count}")
            
            # ✅ เพิ่ม: บันทึกอัตโนมัติเมื่อ shot count เปลี่ยนแปลง
            self._auto_save_excel(old_shot_count)
            
            # ✅ เพิ่ม: ตรวจสอบเงื่อนไข PM หลังจากอัปเดต shot_count
            self._check_pm_condition()
            
        elif self.last_total_sheet is None:
            # กรณีเริ่มต้นระบบ
            self.last_total_sheet = total_sheet
            print(f"[ShotCounter] 🔄 ตั้งค่าเริ่มต้น last_total_sheet เป็น {total_sheet}")

    def _check_predictive_pm(self, current_shot_count, pcs_per_shot):
        """
        ตรวจสอบแบบพยากรณ์ว่าถ้ารัน lot นี้ครบจะเกิน limit หรือไม่
        ใช้ current_shot_count ที่ส่งมาจากฟังก์ชันเรียก
        """
        try:
            # ✅ ตรวจสอบว่ามีข้อมูลครบถ้วน
            if (not hasattr(self, 'lot_size_value') or 
                self.lot_size_value is None or 
                self.lot_size_value <= 0 or 
                pcs_per_shot <= 0):
                print(f"[ShotCounter] 🔍 การพยากรณ์ PM: ข้อมูลไม่ครบ (lot_size={getattr(self, 'lot_size_value', 'N/A')}, pcs_per_shot={pcs_per_shot})")
                return  # ข้ามการตรวจสอบถ้าข้อมูลไม่ครบ
            
            # ✅ คำนวณจำนวน shot ที่จะเพิ่มในรอบปัจจุบัน
            increment_shot = (self.lot_size_value if self.lot_size_value else 1) / pcs_per_shot
            
            # ✅ คำนวณ shot_total ที่คาดการณ์
            predicted_total_shots = current_shot_count + increment_shot
            
            print(f"[ShotCounter] 🔮 การพยากรณ์ PM:")
            print(f"  - Shot ปัจจุบัน: {current_shot_count}")
            print(f"  - Lot size: {self.lot_size_value}")
            print(f"  - PCS/Shot: {pcs_per_shot}")
            print(f"  - Shot ที่จะเพิ่ม: {increment_shot:.2f}")
            print(f"  - Shot รวมที่คาดการณ์: {predicted_total_shots:.2f}")
            print(f"  - Limit: {self.max_shot_limit}")
            
            # ✅ ตรวจสอบเงื่อนไข PM
            if predicted_total_shots > self.max_shot_limit:
                print(f"[ShotCounter] ⚠️ จำนวน Shot จะเกิน {self.max_shot_limit} (ปัจจุบัน {current_shot_count} + เพิ่ม {increment_shot:.2f}) ถึงเวลา PM แล้ว!")
                
                # ✅ ตั้งค่าสถานะเพื่อป้องกันการนับ shot เพิ่ม
                self._should_stop_for_pm = True
                
                # ✅ อัปเดต UI เพื่อแจ้งเตือน
                if self.parent and hasattr(self.parent, 'ui'):
                    if hasattr(self.parent.ui, 'statusbar'):
                        self.parent.ui.statusbar.showMessage(
                            f"⚠️ ถึงเวลา PM แล้ว! (พยากรณ์: {predicted_total_shots:.0f} shots)", 
                            10000
                        )
                    if hasattr(self.parent.ui, 'shot_cnt'):
                        self.parent.ui.shot_cnt.setStyleSheet("background-color: #ffcccc; color: #cc0000; font-weight: bold;")
                
                # ✅ เรียกกระบวนการ PM
                if not self.pm_triggered and not self.pm_window_visible:
                    print(f"[ShotCounter] 🚨 เรียกกระบวนการ PM แบบพยากรณ์")
                    self._handle_pm_needed()
                else:
                    print(f"[ShotCounter] ⏸️ PM กำลังดำเนินการอยู่แล้ว")
                    
            else:
                self._should_stop_for_pm = False
                remaining_shots = self.max_shot_limit - predicted_total_shots
                print(f"[ShotCounter] ✅ การพยากรณ์: ยังไม่ถึงเวลา PM (เหลืออีก {remaining_shots:.2f} shots)")
                
                # ✅ คืนค่าสไตล์ปกติถ้าไม่ถึง PM
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                    self.parent.ui.shot_cnt.setStyleSheet("")  # ล้างสไตล์
                    
        except Exception as e:
            print(f"[ShotCounter] ❌ ข้อผิดพลาดในการตรวจสอบ PM แบบพยากรณ์: {e}")

    def show_logout_window(self):
        """แสดงหน้าต่าง Logout"""
        try:
            # สร้างและแสดงหน้าต่าง Logout
            self.logout_window = LogoutWindow(
                parent=self.parent, 
                shot_counter=self,
                theme_settings=getattr(self.parent, 'theme_settings', {})  # ✅ ส่ง theme settings
            )
            self.logout_window.show()
            print("[ShotCounter] 📋 แสดงหน้าต่าง Logout พร้อมธีม")
            
        except Exception as e:
            print(f"[ShotCounter] ❌ เกิดข้อผิดพลาดในการแสดงหน้าต่าง Logout: {e}")
            # ถ้าเกิดข้อผิดพลาด ให้เรียก manual_save โดยตรงเป็น fallback
            self.manual_save()
    def _auto_save_excel(self, old_shot_count):
        """เรียกใช้ manual_save() โดยตรงเมื่อถึงเงื่อนไข auto-save"""
        try:
            # ตรวจสอบเกณฑ์ auto-save (เพิ่มขึ้นจากรอบที่บันทึกล่าสุด >= 50)
            shot_difference = self.shot_count - self.old_shot_count
            print(f"[ShotCounter] 🔍 ตรวจสอบ Auto Save: old={self.old_shot_count}, new={self.shot_count}, diff={shot_difference}")
            
            if shot_difference >= 30:
                print(f"[ShotCounter] 🔄 Auto Save ถูก触发: เพิ่มขึ้น {shot_difference} shots")
                
                # ✅ เรียกใช้ manual_save() โดยตรง
                self.manual_save()
                
                # ✅ อัปเดต old_shot_count เป็นค่าปัจจุบันหลัง save เสร็จ
                self.old_shot_count = self.shot_count
                
                # ✅ แสดงสถานะใน UI ถ้ามี
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'statusbar'):
                    self.parent.ui.statusbar.showMessage(f"✅ Auto Save: {self.shot_count} shots", 3000)
                    
            else:
                print(f"[ShotCounter] ⏸️ Auto Save ยังไม่ถึงเงื่อนไข: {shot_difference}/50 shots")

        except Exception as e:
            print(f"[ShotCounter] ❌ ข้อผิดพลาดในการ Auto Save: {e}")
    
    # --- Function แยกสำหรับการจัดการ PM ---
    def _handle_product_change(self, new_product_name, new_file_path):
        """จัดการการเปลี่ยนผลิตภัณฑ์และโหลดข้อมูลใหม่"""
        # รีเซ็ตสถานะ PM เมื่อเปลี่ยนผลิตภัณฑ์
        self.pm_triggered = False
        self.pm_window_visible = False
        self.product_name = new_product_name
        self.file_path = new_file_path
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                lines = f.read().splitlines()
                try:
                    self.shot_count = int(lines[0])
                    self.last_total_sheet = int(lines[1]) if len(lines) > 1 else None
                    print(f"[ShotCounter] Loaded shot_count={self.shot_count}, last_total_sheet={self.last_total_sheet} for new product")
                except ValueError:
                    self.shot_count = 0
                    self.last_total_sheet = None
        else:
            self.shot_count = 0
            self.last_total_sheet = None
            print(f"[ShotCounter] No file for product {self.product_name}, starting at 0")
        self.product_name = new_product_name
        self.file_path = new_file_path
        self.start_lot_shot = self.shot_count
        print(f"[ShotCounter] Reset start_lot_shot to {self.start_lot_shot} for new product")
        self._save_shot_count()

    def _handle_pm_needed(self):
        """จัดการเหตุการณ์เมื่อถึงเวลา PM"""
        if self.pm_triggered or self.pm_window_visible:
            print(f"⏸️ PM กำลังดำเนินการอยู่แล้ว: triggered={self.pm_triggered}, window_visible={self.pm_window_visible}")
            return
        
        print(f"🚨 เริ่มกระบวนการ PM: shot_count={self.shot_count}")
        self.pm_triggered = True
        print("[ShotCounter] 🔴 เตรียมโหลดข้อมูล Excel เพื่อแสดงบนหน้าต่าง PM")

        # สร้าง path สำหรับไฟล์ Excel
        excel_filename = f"shotcount_{self.product_name}.xlsx"
        
        # ✅ ใช้โฟลเดอร์ล่าสุดที่ผู้ใช้เลือก (ถ้ามี)
        dest_folder = getattr(self, 'custom_base_dir', self.pm_folder)
        excel_file = os.path.join(dest_folder, excel_filename)
        
        # โหลดข้อมูลจากไฟล์ Excel
        lot_shot_data, row_3b_value = self.load_excel_data_for_pm(excel_file)
        
        # ✅ สร้าง LoginPM Dialog
        try:
            login_dialog = LoginPM(parent=self.main_window, main_window=self.main_window)
            result = login_dialog.exec()
            
            # ตรวจสอบผลลัพธ์
            if result == QDialog.Accepted and login_dialog.login_successful:
                # ✅ รับข้อมูลจากการล็อกอิน
                login_data = login_dialog.get_login_data()
                print(f"✅ ได้รับข้อมูลล็อกอิน: {login_data}")
                
                # ✅ แสดงหน้าต่าง PM พร้อมข้อมูล
                self.show_pm_window(
                    lot_shot_data=lot_shot_data, 
                    row_3b_value=row_3b_value, 
                    login_data=login_data,
                )
                print("🚀 เรียกแสดงหน้าต่าง PM สำเร็จ")
            else:
                self.pm_triggered = False
                self.pm_window_visible = False
                self._should_stop_for_pm = False
                print("[ShotCounter] ❌ ผู้ใช้ยกเลิกการล็อกอิน PM")
                
        except Exception as e:
            print(f"[ShotCounter] ❌ ข้อผิดพลาดในกระบวนการล็อกอิน PM: {e}")
            self.pm_triggered = False
            self.pm_window_visible = False

    def show_pm_window(self, lot_shot_data=None, row_3b_value=None, login_data=None):
        """แสดงหน้าต่าง PM"""
        try:
            print(f"[ShotCounter] 🚀 เริ่มสร้างหน้าต่าง PM...")
            
            if self.pm_window_visible:
                print("⚠️ หน้าต่าง PM กำลังแสดงอยู่แล้ว")
                return
                
            # สร้างหน้าต่างใหม่
            if self.parent is None:
                self.parent = QApplication.activeWindow()
                
            print(f"[ShotCounter] 📝 สร้าง Pmwindow ด้วย login_data: {login_data is not None}")
            
            self.pm_window = Pmwindow(
                parent=self.parent, 
                login_data=login_data, 
                file_path=self.file_path, 
                shot_counter=self
            )
            self.pm_window_visible = True
            
            # ตั้งค่าสถานะล็อกอิน
            self.pm_window.is_logged_in = True
            
            if lot_shot_data is not None:
                self.pm_window.set_excel_data(lot_shot_data)
                print("✅ ตั้งค่าข้อมูล Excel ให้ PM Window")
            
            if row_3b_value is not None:
                self.pm_window.parse_and_set_row_3b_data(row_3b_value)
                print("✅ ตั้งค่าข้อมูลแถว 3B ให้ PM Window")
            
            # ตั้งค่าให้หน้าต่างปิด时ทำลายวัตถุจริงๆ
            self.pm_window.setAttribute(Qt.WA_DeleteOnClose)
            
            # เชื่อมสัญญาณการปิดหน้าต่างเพื่ออัปเดตสถานะ
            self.pm_window.destroyed.connect(self._on_pm_window_closed)
            
            print("🎯 แสดงหน้าต่าง PM...")
            self.pm_window.show()
            print("✅ หน้าต่าง PM แสดงแล้ว")
            
        except Exception as e:
            print(f"[ShotCounter] ❌ ข้อผิดพลาดในการแสดงหน้าต่าง PM: {e}")
            import traceback
            traceback.print_exc()

    def _on_pm_window_closed(self):
        """จัดการเมื่อหน้าต่าง PM ถูกปิด"""
        self.pm_window_visible = False
        self.pm_triggered = False
        self.pm_window = None

    def load_excel_data_for_pm(self, file_path):
        """
        โหลดข้อมูล Lot และ Shot จากไฟล์ Excel
        โดยจะแยกค่า Lot และ Shot ที่อยู่ในเซลล์เดียวกัน
        และอ่านค่าเพิ่มเติมจากแถว 3 คอลัมน์ B
        """
        data_list = []
        row_3b_value = None  # เก็บค่าจากแถว 3 คอลัมน์ B
        
        if not os.path.exists(file_path):
            print(f"⚠️ ไม่พบไฟล์ Excel ที่: {file_path}")
            return data_list, row_3b_value

        try:
            # โหลด workbook และเลือก worksheet ที่ใช้งาน
            wb = load_workbook(file_path)
            ws = wb.active

            # อ่านค่าในแถวที่ 3 คอลัมน์ B (row=3, column=2)
            row_3b_cell = ws.cell(row=3, column=2)
            if row_3b_cell.value:
                row_3b_value = row_3b_cell.value
                print(f"📖 อ่านค่าแถว 3B สำเร็จ: {row_3b_value}")
            else:
                print("⚠️ ไม่พบข้อมูลในแถว 3 คอลัมน์ B")

            # วนลูปอ่านข้อมูลในแถวที่ 7 ถึง 21
            for row in range(7, 22):
                for col in range(2, 11): # คอลัมน์ B ถึง J
                    cell = ws.cell(row=row, column=col)
                    
                    # ตรวจสอบว่าเซลล์มีข้อมูลหรือไม่ และเป็นข้อความที่รวม Lot และ Shot
                    if isinstance(cell.value, str) and 'shot' in cell.value:
                        try:
                            # แยกค่า Lot และ Shot ออกจากข้อความ
                            parts = cell.value.split('\n')
                            lot_id = parts[0] if len(parts) > 0 else 'N/A'
                            shot_count = parts[1].split('shot ')[1] if len(parts) > 1 else 'N/A'
                            
                            # เพิ่มข้อมูลเป็น tuple (Lot ID, Shot Count)
                            data_list.append((lot_id, int(shot_count)))
                        except (ValueError, IndexError):
                            print(f"❌ ไม่สามารถแยกข้อมูลจากเซลล์ {cell.coordinate}: {cell.value}")
                            continue
            
            return data_list, row_3b_value  # คืนค่าทั้งสองอย่าง

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในการโหลดไฟล์ Excel: {e}")
            return [], None

    def manual_save(self):
        try:
            txt_filename = os.path.basename(self.file_path)
            base_filename = os.path.splitext(txt_filename)[0]
            excel_filename = base_filename + ".xlsx"
            
            # ✅ ใช้โฟลเดอร์ล่าสุดที่ผู้ใช้เลือก (ถ้ามี)
            dest_folder = getattr(self, 'custom_base_dir', self.pm_folder)
            dest_path = os.path.join(dest_folder, excel_filename)

            lot_number = self.product_data.get('lot_number', 'N/A')
            shot_count_current = self.shot_count
            
            os.makedirs(dest_folder, exist_ok=True)
            
            # --- สร้างไฟล์ Excel จาก Template ถ้ายังไม่มี ---
            if not os.path.exists(dest_path):
                template_dir = self.templates_dir
                template_files = [f for f in os.listdir(template_dir) if f.lower().endswith(".xlsx")]
                if not template_files:
                    print("[ShotCounter] ❌ ไม่พบไฟล์ .xlsx ในโฟลเดอร์ templat/")
                    return
                template_path = os.path.join(template_dir, template_files[0])
                shutil.copy(template_path, dest_path)
                print(f"[ShotCounter] ✅ คัดลอก template: {template_path} → {dest_path}")
                self._save_initial_data(dest_path)
            
            # --- เปิดไฟล์ Excel เพื่อแก้ไขข้อมูล ---
            wb = load_workbook(dest_path)
            ws = wb.active

            font_style = Font(name='Angsana New', size=12, bold=True)
            start_row = 7
            end_row = 100
            data_columns = range(2, 11)

            found = False
            columns_to_resize = set()

            current_lot_shots = shot_count_current - self.start_lot_shot
            print(f"[ShotCounter] Calculating lot shots: {shot_count_current} - {self.start_lot_shot} = {current_lot_shots}")

            if current_lot_shots == 0:
                print("[ShotCounter] ⚠️ ไม่มี shot ใหม่ใน lot นี้ ไม่จำเป็นต้องบันทึก")
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'statusbar'):
                    self.parent.ui.statusbar.showMessage("⚠️ ไม่มี shot ใหม่ใน lot นี้ ไม่จำเป็นต้องบันทึก", 5000)
                return

            # --- 🔁 ส่วนที่ 1: ตรวจสอบและอัปเดต Lot เดิมที่มีอยู่แล้ว ---
            for row in range(start_row, end_row + 1):
                if (row - start_row) % 3 != 0:
                    continue
                for col_index in data_columns:
                    data_cell = ws.cell(row=row, column=col_index)
                    cell_to_update = data_cell
                    for merged_range in ws.merged_cells.ranges:
                        if data_cell.coordinate in merged_range:
                            cell_to_update = ws.cell(merged_range.min_row, merged_range.min_col)
                            break
                    label_text = str(cell_to_update.value).strip() if cell_to_update.value else ""
                    
                    if lot_number in label_text: 
                        old_shot_count = 0
                        try:
                            old_shot_text = label_text.split('shot ')[-1]
                            old_shot_count = int(old_shot_text)
                        except (ValueError, IndexError):
                            pass
                        
                        new_total_lot_shots = old_shot_count + current_lot_shots
                        
                        cell_to_update.value = f"{lot_number}\nshot {new_total_lot_shots}"
                        cell_to_update.alignment = Alignment(wrapText=True)
                        cell_to_update.font = font_style
                        columns_to_resize.add(ws.cell(row=1, column=col_index).column_letter)
                        print(f"[ShotCounter] ✏️ อัปเดต Lot เดิมที่ {cell_to_update.coordinate} รวม shot เป็น {new_total_lot_shots}")
                        
                        self.start_lot_shot = shot_count_current
                        found = True
                        break
                if found:
                    break

            # --- ➕ ส่วนที่ 2: เพิ่ม Lot ใหม่โดยการแทนที่หมายเลขเดิม ---
            if not found:
                for row in range(start_row, end_row + 1):
                    if (row - start_row) % 3 != 0:
                        continue
                    for col_index in data_columns:
                        data_cell = ws.cell(row=row, column=col_index)
                        cell_to_fill = data_cell
                        for merged_range in ws.merged_cells.ranges:
                            if data_cell.coordinate in merged_range:
                                cell_to_fill = ws.cell(merged_range.min_row, merged_range.min_col)
                                break
                        
                        cell_value = cell_to_fill.value
                        if isinstance(cell_value, int):
                            cell_to_fill.value = f"{lot_number}\nshot {current_lot_shots}"
                            cell_to_fill.alignment = Alignment(wrapText=True)
                            cell_to_fill.font = font_style
                            columns_to_resize.add(ws.cell(row=1, column=col_index).column_letter)
                            print(f"[ShotCounter] ➕ เพิ่ม Lot ใหม่ที่ {cell_to_fill.coordinate} โดยแทนที่หมายเลข {cell_value}")
                            
                            self.start_lot_shot = shot_count_current
                            found = True
                            break
                    if found:
                        break

            # --- ➕ ส่วนที่ 3: ถ้าไม่มีช่องว่างเลย ให้เพิ่มแถวใหม่ ---
            if not found:
                new_row = end_row + 1
                new_cell = ws.cell(row=new_row, column=2)
                new_cell.value = f"{lot_number}\nshot {current_lot_shots}"
                new_cell.alignment = Alignment(wrapText=True)
                new_cell.font = font_style
                columns_to_resize.add('B')
                print(f"[ShotCounter] ➕ เพิ่มแถวใหม่สำหรับ Lot ที่แถว {new_row}")
                
                self.start_lot_shot = shot_count_current

            # --- อัปเดตการคาดการณ์และเติมสีในคราวเดียว ---
            predicted_slot = self._predict_next_pm_slot(ws)
            self._update_pm_prediction(ws, predicted_slot)
            
            if predicted_slot and predicted_slot != 'N/A' and predicted_slot != 'Error':
                self._highlight_predicted_slots(ws, predicted_slot)
            
            # --- บันทึกไฟล์ Excel ครั้งสุดท้าย ---
            for column_letter in columns_to_resize:
                ws.column_dimensions[column_letter].width = 8
                print(f"[ShotCounter] กำหนดความกว้างคอลัมน์ {column_letter} เป็น 8")

            wb.save(dest_path)
            print(f"[ShotCounter] ✅ บันทึกข้อมูลและปรับขนาดคอลัมน์เรียบร้อย")
            
        except Exception as e:
            print(f"[ShotCounter] ❌ เกิดข้อผิดพลาด: {str(e)}")

    def _highlight_predicted_slots(self, ws, predicted_slot):
        """เติมสีแจ้งเตือนในช่องที่คาดการณ์และช่องก่อนหน้า"""
        try:
            START_ROW = 7  # แถวเริ่มต้น
            ROW_STEP = 2   # แต่ละช่องใช้ 2 แถว (merge แนวตั้ง)
            DATA_COLUMNS = list(range(2, 11))  # B to J (9 คอลัมน์)

            try:
                pred = int(predicted_slot)
            except Exception:
                print("[ShotCounter] ⚠️ predicted_slot ไม่ใช่ตัวเลข")
                return

            yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            # รีเซ็ตสีทั้งหมดก่อน
            self._reset_table_colors(ws, START_ROW, ROW_STEP, DATA_COLUMNS)

            # คำนวณตำแหน่งที่ถูกต้องตามโครงสร้างตารางจริง
            # แต่ละช่องใช้ 2 แถว (merge แนวตั้ง), มี 9 คอลัมน์ (B-J)
            
            # คำนวณช่องก่อนหน้า (186) และช่องคาดการณ์ (187)
            prev_slot_num = pred - 1  # ช่องก่อนหน้า (186)
            pred_slot_num = pred      # ช่องคาดการณ์ (187)

            # คำนวณตำแหน่งสำหรับช่องก่อนหน้า (186)
            prev_row = START_ROW + ((prev_slot_num - 1) // 9) * ROW_STEP
            prev_col = 2 + ((prev_slot_num - 1) % 9)  # 2 = คอลัมน์ B
            
            # คำนวณตำแหน่งสำหรับช่องคาดการณ์ (187)
            pred_row = START_ROW + ((pred_slot_num - 1) // 9) * ROW_STEP
            pred_col = 2 + ((pred_slot_num - 1) % 9)  # 2 = คอลัมน์ B

            print(f"[ShotCounter] 🔍 คำนวณตำแหน่ง:")
            print(f"  - ช่อง {prev_slot_num}: แถว {prev_row}, คอลัมน์ {prev_col} ({chr(64+prev_col)})")
            print(f"  - ช่อง {pred_slot_num}: แถว {pred_row}, คอลัมน์ {pred_col} ({chr(64+pred_col)})")

            # เติมสีช่องก่อนหน้า (186)
            prev_cell = ws.cell(row=prev_row, column=prev_col)
            # เนื่องจากมีการ merge ในแนวตั้ง ให้ตรวจสอบว่าเซลล์เป็นส่วนหนึ่งของ merged range หรือไม่
            for merged_range in ws.merged_cells.ranges:
                if prev_cell.coordinate in merged_range:
                    # ใช้เซลล์หลักของ merged range
                    prev_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                    break
            prev_cell.fill = yellow_fill
            print(f"[ShotCounter] 🟡 เติมสีเหลืองที่ {prev_cell.coordinate} (ช่อง {prev_slot_num})")

            # เติมสีช่องคาดการณ์ (187)
            pred_cell = ws.cell(row=pred_row, column=pred_col)
            # ตรวจสอบ merged cells
            for merged_range in ws.merged_cells.ranges:
                if pred_cell.coordinate in merged_range:
                    # ใช้เซลล์หลักของ merged range
                    pred_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                    break
            pred_cell.fill = red_fill
            print(f"[ShotCounter] 🔴 เติมสีแดงที่ {pred_cell.coordinate} (ช่อง {pred_slot_num})")

            # ✅ อัปเดตค่าคู่ช่องล่าสุด
            self._next_pm_pair = f"{prev_slot_num}-{pred_slot_num}"
            print(f"[ShotCounter] 🔢 อัปเดตคู่ช่องคาดการณ์: {self._next_pm_pair}")

            print(f"[ShotCounter] ✅ เติมสีช่องก่อนหน้าและช่องคาดการณ์เรียบร้อย")

        except Exception as e:
            print(f"[ShotCounter] ❌ เกิดข้อผิดพลาดในการเติมสี: {e}")

    def _reset_table_colors(self, ws, start_row, row_step, data_columns):
        """รีเซ็ตสีเติมทั้งหมดในตาราง"""
        no_fill = PatternFill(fill_type=None)
        # วนลูปตามโครงสร้างตารางจริง (ทุก 2 แถว)
        for row in range(start_row, 100, row_step):  # แถว 7, 9, 11, 13, ...
            for col in data_columns:
                cell = ws.cell(row=row, column=col)
                # ตรวจสอบ merged cells
                for merged_range in ws.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        # รีเซ็ตสีเฉพาะเซลล์หลักของ merged range
                        main_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                        main_cell.fill = no_fill
                        break
                else:
                    cell.fill = no_fill

    def _update_pm_prediction(self, ws, predicted_slot):
        """อัปเดตข้อมูล Next P.M. ให้ตรงกับค่าที่คำนวณได้จริง (เฉพาะใน Excel)"""
        try:
            product_name = self.product_data.get('product_name', 'N/A')
            tooling_code = self.product_data.get('tooling_code', 'N/A')

            tooling_type = "E-FPC" if tooling_code.startswith("OSTE") else \
                           "SMT" if tooling_code.startswith("OSTM") else "N/A"

            next_pm_text = getattr(self, "_next_pm_pair", "N/A")

            cell_b3 = ws["B3"]
            old_fill = copy(cell_b3.fill)
            cell_b3.value = (
                f"Product name:  {product_name}      "
                f"Tooling code:  {tooling_code}      "
                f"Tooling for:   {tooling_type}       "
                f"Next p.m.: {next_pm_text}"
            )
            cell_b3.fill = old_fill

            print(f"[ShotCounter] ✅ Updated Next PM text in Excel: {next_pm_text}")

            # ✅ คืนค่าผลลัพธ์กลับไปให้ Pmwindow ใช้ต่อ
            return next_pm_text

        except Exception as e:
            print(f"[ShotCounter] ❌ Error updating PM prediction: {e}")
            return None
    def _predict_next_pm_slot(self, ws):
        """คำนวณช่องที่คาดว่าจะถึง 30,000 shot โดยใช้ Linear Regression"""
        try:
            START_ROW = 7
            END_ROW = 100
            DATA_COLUMNS = range(2, 11)

            shot_data = []
            slot_indices_for_shots = []
            slot_index = 0

            for row in range(START_ROW, END_ROW + 1):
                if (row - START_ROW) % 3 != 0:
                    continue
                for col in DATA_COLUMNS:
                    slot_index += 1
                    cell = ws.cell(row=row, column=col)
                    if cell.value and isinstance(cell.value, str) and 'shot' in cell.value:
                        try:
                            shot_text = cell.value.split('shot')[-1].strip()
                            shot_value = int(shot_text)
                            shot_data.append(shot_value)
                            slot_indices_for_shots.append(slot_index)
                        except (ValueError, IndexError):
                            continue

            if len(shot_data) < 2:
                return 'N/A'

            cumulative_shots = []
            current_cum = 0
            for s in shot_data:
                current_cum += s
                cumulative_shots.append(current_cum)

            X = np.array(slot_indices_for_shots).reshape(-1, 1)
            y = np.array(cumulative_shots)
            model = LinearRegression()
            model.fit(X, y)

            intercept = model.intercept_
            slope = model.coef_[0]

            if abs(slope) < 1e-6:
                return 'N/A'

            predicted_slot = math.ceil((30000 - intercept) / slope)

            total_slots = 0
            for row in range(START_ROW, END_ROW + 1):
                if (row - START_ROW) % 2 != 0:
                    continue
                for col in DATA_COLUMNS:
                    total_slots += 1

            predicted_slot = max(1, min(predicted_slot, total_slots))
            prev_slot = max(predicted_slot - 1, 1)

            # 🔹 เก็บค่าไว้ใช้ต่อ
            self._next_pm_pair = f"{prev_slot}-{predicted_slot}"

            print(f"[ShotCounter] 📊 คาดการณ์ถึงรอบ PM ที่ช่อง {predicted_slot} (ก่อนหน้า {prev_slot})")
            print(f"[ShotCounter] แสดงคู่ PM เป็น: {self._next_pm_pair}")

            return predicted_slot

        except Exception as e:
            print(f"[ShotCounter] ❌ เกิดข้อผิดพลาดในการคาดการณ์: {e}")
            return 'Error'

       
    def _save_initial_data(self, excel_path):
        """บันทึกข้อมูลในเซลล์ B3 ในรูปแบบบรรทัดเดียว"""
        try:
            wb = load_workbook(excel_path)
            ws = wb.active
            
            # ดึงข้อมูลจาก product_data
            product_name = self.product_data.get('product_name', 'N/A')
            tooling_code = self.product_data.get('tooling_code', 'N/A')
            lot_number = self.product_data.get('lot_number', 'N/A')
            
            # กำหนด Tooling Type ตามโค้ด
            tooling_type = ""
            if tooling_code.startswith('OSTE'):
                tooling_type = "E-FPC"
            elif tooling_code.startswith('OSTM'):
                tooling_type = "SMT"
            else:
                tooling_type = "N/A"
            
            # ✅ เปลี่ยนเป็นรูปแบบบรรทัดเดียว
            single_line_text = (
                f"Product name:  {product_name}      "
                f"Tooling code:  {tooling_code}      "
                f"Tooling for:   {tooling_type}       "
                f"Next p.m.: {lot_number}"
            )
            
            # เขียนข้อมูลลงเซลล์ B3 ในรูปแบบบรรทัดเดียว
            ws['B3'] = single_line_text
            
            wb.save(excel_path)
            print(f"[ShotCounter] ✅ บันทึกข้อมูลเริ่มต้นแบบบรรทัดเดียวเรียบร้อย: {single_line_text}")
            
        except Exception as e:
            print(f"[ShotCounter] ❌ ไม่สามารถบันทึกข้อมูล: {str(e)}")
if __name__ == "__main__":
    window_pm = ShotCounter()
    sys.exit(app.exec())