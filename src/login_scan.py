import sys
import os
import re
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QComboBox, QPushButton, QLineEdit,
                               QVBoxLayout, QFileDialog, QRadioButton, QDialogButtonBox, QMessageBox)
from PySide6.QtCore import Qt, QEvent, Signal
from PySide6.QtGui import QKeyEvent, QIcon
from src.data_upload import DataUploader
from src.PLCdata import PLCWindow
from src.ui_Demo2 import *
from src.ui_PopupScan import *
from src.ui_PopupScanCodeFixture import *
from src.ui_PopupScanPOS import *
from src.config_manager import config_manager
from src.database_manager import database_manager
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QComboBox, QPushButton, QLineEdit,
                               QVBoxLayout, QRadioButton, QDialogButtonBox, QMessageBox, QHBoxLayout, QButtonGroup)

#################################################
# POPUP SCAN OPERATOR
class ScanPopup(QDialog):
    def __init__(self, plc_window ,parent=None):
        super().__init__(parent)
        self.ui = Ui_Scan()
        self.ui.setupUi(self)
        self.setWindowTitle("Scan Operator ID") 
        
        # ช่องกรอก ID ที่สแกน
        self.UserID = self.findChild(QLineEdit, 'UserID')
        self.UserID.setPlaceholderText("Scan the ID here...")
        self.UserID.installEventFilter(self)
        self.UserID.setFocus()

        self.refresh = self.findChild(QPushButton, 'Refresh_scan')
        self.refresh.setFixedSize(20, 20)
        self.refresh.clicked.connect(self.refresh_ports)

        self.confirm = self.findChild(QPushButton, 'confirm')
        self.confirm.clicked.connect(self.complete_scan)

    def complete_scan(self):
        scanned_id = self.UserID.text()
        if scanned_id:
            self.accept()
        else:
            self.UserID.setPlaceholderText("Please scan the ID!")

    def get_scanned_id(self):
        return self.UserID.text()

    def refresh_ports(self):
        self.UserID.clear()
        self.UserID.setPlaceholderText("Scan ID here...")
        self.UserID.setReadOnly(False)
        self.UserID.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.UserID and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                return True
        return super().eventFilter(obj, event)

#################################################
# SCAN POPUP POS
class ScanPOS(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ScanPOS()
        self.ui.setupUi(self)
        self.setWindowTitle("Scan POS")
        
        self.NumberPOS = self.findChild(QLineEdit, 'NumberPOS')
        self.NumberPOS.setPlaceholderText("Scan the POS here...")
        self.NumberPOS.installEventFilter(self)
        self.NumberPOS.setFocus()

        self.refresh = self.findChild(QPushButton, 'Refresh_scanPOS')
        self.refresh.setFixedSize(20, 20)
        self.refresh.clicked.connect(self.refresh_ports)

        self.confirm = self.findChild(QPushButton, 'confirmPOS')
        self.confirm.clicked.connect(self.complete_scan)

    def complete_scan(self):
        scanned_POS = self.NumberPOS.text()
        if scanned_POS:
            self.accept()
        else:
            self.NumberPOS.setPlaceholderText("Please scan the POS!")

    def get_scanned_POS(self):
        return self.NumberPOS.text()

    def refresh_ports(self):
        self.NumberPOS.clear()
        self.NumberPOS.setPlaceholderText("Scan POS here...")
        self.NumberPOS.setReadOnly(False)
        self.NumberPOS.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.NumberPOS and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                return True
        return super().eventFilter(obj, event)

#################################################
# SCAN POPUP FIXTURE
class ScanFixture(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ScanCode()
        self.ui.setupUi(self)
        self.setWindowTitle("Scan Fixture")
        
        self.Code_Fixture = self.findChild(QLineEdit, 'codeFixture')
        self.Code_Fixture.setPlaceholderText("Scan the Fixture here...")
        self.Code_Fixture.installEventFilter(self)
        self.Code_Fixture.setFocus()

        self.refresh = self.findChild(QPushButton, 'Refresh_scanCodeFixture')
        self.refresh.setFixedSize(20, 20)
        self.refresh.clicked.connect(self.refresh_ports)

        self.confirm = self.findChild(QPushButton, 'confirmFixture')
        self.confirm.clicked.connect(self.complete_scan)

    def complete_scan(self):
        scanned_Fixture = self.Code_Fixture.text()
        if scanned_Fixture:
            self.accept()
        else:
            self.Code_Fixture.setPlaceholderText("Please scan the Fixture!")

    def get_scanned_Fixture(self):
        return self.Code_Fixture.text()

    def refresh_ports(self):
        self.Code_Fixture.clear()
        self.Code_Fixture.setPlaceholderText("Scan Fixture here...")
        self.Code_Fixture.setReadOnly(False)
        self.Code_Fixture.setFocus()

    def eventFilter(self, obj, event):
        if obj == self.Code_Fixture and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                return True
        return super().eventFilter(obj, event)

#################################################
# MAIN PROGRAM
#################################################

class MyWindow(QDialog):
    def __init__(self, plc_window ,parent=None):
        super().__init__(parent)
        
        #print("Initializing MyWindow")
        # เก็บค่า total_pcs ล่าสุด

        self.last_total_pcs = None
        
        try:
            self.ui = Ui_Demo1()
            self.ui.setupUi(self)
            self.setWindowTitle("Login & Setup")
            
            #print("UI loaded successfully")
        except Exception as e:
            QMessageBox.critical(self, "UI Error", f"Error loading UI: {e}")
            raise

        # ตั้งค่า DataUploader
        #print("Setting up DataUploader")
        self.data_upload = DataUploader()
        
        # ตั้งค่า PLCWindow
        #print("Setting up PLCWindow")
        try:
            self.plc_window = plc_window
            self.plc_window.hide()
            print("PLCWindow setup completed")
        except Exception as e:
            print(f"Error setting up PLCWindow: {e}")
            self.plc_window = None

        # ตัวแปรเก็บสถานะล็อกอิน
        self.operator_id = None
        self.operator_name = None
        self.process = None
        self.job_title = None
        self.code_training = None
        self.train_topic = None
        self.lot_number = None
        self.product_formatted = None
        self.matched_tooling = None
        self.ost_from_data_base = None
        self.is_fixture_valid = False
        self.timestamp = None
        self.lot_size_value = None

        self.lot_size = self.findChild(QLineEdit,'lineEdit')
        self.lot_size.textChanged.connect(self.on_lotsize_input)

        # Scan ID operator
        self.scannerIdoperator = self.findChild(QPushButton, 'IDoperator')
        self.scannerIdoperator.clicked.connect(self.open_popup_scan_UserID)
        self.scannerIdoperator.installEventFilter(self)
        self.LineLabel = self.findChild(QLabel, 'LicenseUser')

        # Scan POS product
        self.scanPOS = self.findChild(QPushButton, 'NumberPOS')
        self.scanPOS.clicked.connect(self.open_popup_scan_POS)
        self.scanPOS.installEventFilter(self)
        self.LineLabelPOS = self.findChild(QLabel, 'checkPOS')

        # Scan Fixture
        self.scanFixture = self.findChild(QPushButton, 'CodeFixture')
        self.scanFixture.clicked.connect(self.open_popup_scan_Fixture)
        self.scanFixture.installEventFilter(self)
        self.LineLabelscanFixture = self.findChild(QLabel, 'Status_confirm_fixture')
        self.save_result = {'status': 'pending', 'message': ''}

        # Button box setup
        self.button_box = self.findChild(QDialogButtonBox, "buttonBox")
        self.button_box.setStandardButtons(
            QDialogButtonBox.Save |
            QDialogButtonBox.Close |
            QDialogButtonBox.RestoreDefaults
        )
        reset_btn = self.button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        reset_btn.setText("Reset")
        save_btn = self.button_box.button(QDialogButtonBox.StandardButton.Save)
        save_btn.setEnabled(False)
        self.save_button = save_btn
        
        # Radio buttons
        self.clicked_OST1 = self.findChild(QRadioButton, 'FOST')
        self.clicked_OST2 = self.findChild(QRadioButton, 'FOST2')
        self.clicked_OST3 = self.findChild(QRadioButton, 'FOST3')
        
        # เชื่อมต่อสัญญาณ
        self.button_box.accepted.connect(self.save_function)
        self.button_box.rejected.connect(self.close_function)
        reset_btn.clicked.connect(self.reset_function)
        
        for rb in [self.clicked_OST1, self.clicked_OST2, self.clicked_OST3]:
            rb.toggled.connect(self.handle_ost_change)

        # Setup Login Mode (Mass vs FA) using existing UI elements
        self.setup_mode_selection()

    def setup_mode_selection(self):
        """Setup Radio Buttons for Mass/FA mode using existing UI elements"""
        # Bind to existing radio buttons from ui_Demo2.py
        self.rb_mass = self.findChild(QRadioButton, 'mass')
        self.rb_fa = self.findChild(QRadioButton, 'fa')
        
        if not self.rb_mass or not self.rb_fa:
            print("❌ Error: Could not find 'mass' or 'fa' radio buttons in UI")
            return

        # Grouping
        self.mode_group = QButtonGroup(self)
        self.mode_group.addButton(self.rb_mass)
        self.mode_group.addButton(self.rb_fa)
        
        # Connect signals
        self.mode_group.buttonToggled.connect(self.handle_mode_change)
        
        # Load saved mode
        saved_mode = config_manager.get_login_mode()
        self.current_mode = saved_mode
        
        # Block signals to prevent triggering logic during initial setup if desired, 
        # but here we might want to ensure config is correct so we let it trigger or set manually.
        # However, triggering reload on init might be redundant if init already loaded default.
        # Let's set checked state without triggering if we want to avoid double-load, 
        # or just let it handle.
        
        if saved_mode == 'fa':
            self.rb_fa.setChecked(True)
        else:
            self.rb_mass.setChecked(True)
            
        print(f"Login mode initialized to: {self.current_mode}")
        
    def handle_mode_change(self, button, checked):
        """Handle switching between Mass and FA modes"""
        if not checked:
            return
            
        # Determine mode based on which button is checked or passed button
        # The button text might be "M." or "F.", so better check objectName
        mode = "mass" if button.objectName() == "mass" else "fa"
        
        print(f"🔄 Switching login mode to: {mode}")
        
        self.current_mode = mode
        
        # Update Config
        # We need to update read_database config based on mode
        # Mass -> tooling_fix (host 10.17.86.154)
        # FA -> design (host 10.17.86.154)
        
        new_db_name = "tooling_fix" if mode == 'mass' else "design"
        
        # Update config in memory
        config_manager.current_config['read_database']['database'] = new_db_name
        
        # Save persistence
        config_manager.set_login_mode(mode)
        
        # Reload Database Connections
        database_manager.reload_configurations()
        
        # Re-validate Fixture if already scanned
        if hasattr(self, 'scanFixture') and self.scanFixture.text() != "Click to scan Qr code Fixture":
             # Extract fixture code from label "Code fixture: XXXXX"
             current_text = self.scanFixture.text()
             if ":" in current_text:
                 fixture_code = current_text.split(":")[1].strip()
                 print(f"🔄 Re-validating fixture: {fixture_code}")
                 
                 # Re-run validation logic
                 if hasattr(self, 'product_formatted'):
                     self.product_formatted1 = self.product_formatted.replace('\u200c', '')
                     
                     is_valid, fixture_data = self.data_upload.check_fixture_validity(fixture_code, mode=self.current_mode)
                     
                     if fixture_data:
                         self.matched_tooling = fixture_data.get('fpc_code') # Normalized key from data_upload
                         self.ost_from_data_base = fixture_data.get("use_for") # Check if this field exists in 'fa'
                         if not self.ost_from_data_base and mode == 'fa':
                              # Handle case where FA table might not have use_for or different name
                              # For now, assume data_upload handles normalization or we might need adjustment
                              pass
                              
                         print(f"ost_from_data_base : {self.ost_from_data_base}")
                         fpc_pd_name = fixture_data.get("fpc_pd_name", "")
    
                         if self.data_upload.is_product_matching(self.product_formatted1, fpc_pd_name):
                             print("✅ Product matches database (Re-check)")
                             self.is_fixture_valid = True
                             self.LineLabelscanFixture.setText("✅ Fixture Code is valid")
                             self.LineLabelscanFixture.setStyleSheet("color: green; font-weight: bold;")
                             self.update_save_button_status()
                         else:
                             self.is_fixture_valid = False
                             self.LineLabelscanFixture.setText(f"❌ Product does not match Fixture")
                             self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")
                     else:
                         self.is_fixture_valid = False
                         self.LineLabelscanFixture.setText(f"❌ Fixture not found in {mode}")
                         self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")
                 else:
                     pass # No product scanned yet

    def on_lotsize_input(self):
        text = self.lot_size.text()
        # เช็กว่าค่าเป็นตัวเลขหรือไม่
        if text.isdigit():
            self.lot_size_value = int(text)
            print(f"Lot size set to {self.lot_size_value}")
        else:
            print("Invalid input, not a number")
            self.lot_size_value = None
        self.update_save_button_status() 

    ###############################################################################
    
    # POS SCAN FUNCTIONS
    def open_popup_scan_POS(self):
        print("Opening POS scan popup")
        try:
            popupScan = ScanPOS(self)
            if popupScan.exec() == QDialog.Accepted:
                scanned_data = popupScan.get_scanned_POS().strip()
                self.scanPOS.setText(scanned_data)
                self.scanPOS.setEnabled(False)

                parsed = self.parse_scanned_data(scanned_data)
                if not parsed:
                    self.LineLabelPOS.setText("❌ Invalid scan data")
                    self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
                    return

                self.lot_number = parsed['lot_number']
                self.wo_number = parsed['wo_number']
                self.product_code = parsed['product_code']
                self.product_formatted = self.format_product_code(self.product_code)
                self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.update_save_button_status()
                print(f"lot: {self.lot_number}")

                product_name, error = self.data_upload.get_product_name_by_lot(self.lot_number)
                if error:
                    self.LineLabelPOS.setText(f"❌ {error}")
                    self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.LineLabelPOS.setText("✅ Saved successfully")
                    self.LineLabelPOS.setStyleSheet("color: green; font-weight: bold;")
        except Exception as e:
            print(f"Error in open_popup_scan_POS: {e}")

    def parse_scanned_data(self, scanned_str):
        # ตรวจสอบว่าข้อมูลที่ได้รับมีตัวแบ่ง (;) หรือไม่
        if not scanned_str or ";" not in scanned_str:
            self.LineLabelPOS.setText("❌ Invalid scan data (missing ';' separator)")
            self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
            return None  # คืนค่า None หากข้อมูลไม่ถูกต้อง

        parts = scanned_str.split(";")
        
        # ตรวจสอบว่าได้รับข้อมูลครบ 3 ส่วนหรือไม่
        if len(parts) < 3:
            self.LineLabelPOS.setText("❌ Incomplete scan data")
            self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
            return None

        try:
            self.lot_number = parts[0]
            self.wo_number = parts[1]
            product_raw = parts[2]

            # ตรวจสอบให้แน่ใจว่า product_raw มีความยาวพอที่จะแยกได้
            if len(product_raw) < 2:
                self.LineLabelPOS.setText("❌ Invalid product code (must be at least 2 characters)")
                self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
                return None

            product_code = product_raw[2:]  # ตัดตัวอักษรที่ไม่ต้องการ
            self.scanned_pos = product_code 
            self.product_code = product_code
            self.product_formatted = self.format_product_code(product_code)
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return {
                "lot_number": self.lot_number,
                "wo_number": self.wo_number,
                "product_code": self.product_code,
                "product_formatted": self.product_formatted,
                "timestamp": self.timestamp
            }
        except Exception as e:
            # เพิ่มการจัดการข้อผิดพลาดหากเกิดข้อผิดพลาดในการแยกหรือประมวลผลข้อมูล
            self.LineLabelPOS.setText(f"❌ Error: {str(e)}")
            self.LineLabelPOS.setStyleSheet("color: red; font-weight: bold;")
            return None

    def format_product_code(self, product_code):
        match = re.match(r"([A-Za-z]+)(\d+)([A-Za-z]+)(\d+[A-Za-z]+)?", product_code)
        if match:
            part1 = match.group(1)
            part2 = match.group(2)
            part3 = match.group(3)
            part4 = match.group(4) if match.group(4) else ''
            if part4:
                return f"{part1}-{part2}{part3}-{part4}"
            else:
                return f"{part1}-{part2}{part3}"
        else:
            return product_code

    ###########################################################################

    # OPERATOR SCAN FUNCTIONS
    def open_popup_scan_UserID(self):
        popup = ScanPopup(self)
        if popup.exec() == QDialog.Accepted:
            scanned_id = popup.get_scanned_id().strip()
            self.scannerIdoperator.setText(f"User ID : {scanned_id}")
            self.scannerIdoperator.setEnabled(False)
            self.last_user_id = scanned_id

            # ตรวจสอบผู้ใช้ผ่าน DataUploader
            is_allowed, user_data = self.data_upload.check_user_permission(scanned_id)

            if is_allowed:
                self.LineLabel.setText("✅ Authorized")
                self.LineLabel.setStyleSheet("color: green; font-weight: bold;")

                # เก็บข้อมูลผู้ใช้
                self.operator_id = user_data['operator_id']
                self.operator_name = user_data['operator_name']
                self.process = user_data['process']
                self.job_title = user_data['job_title']
                self.code_training = user_data['code_training']
                self.train_topic = user_data['train_topic']
                self.update_save_button_status()

            else:
                self.LineLabel.setText("❌ Not authorized")
                self.LineLabel.setStyleSheet("color: red; font-weight: bold;")


    ###########################################################################
    # FIXTURE SCAN FUNCTIONS
    def open_popup_scan_Fixture(self):
        popup = ScanFixture(self)
        if popup.exec() == QDialog.Accepted:
            scanned_Fixture = popup.get_scanned_Fixture().strip()
            self.scanFixture.setText(f"Code fixture: {scanned_Fixture}")
            self.scanFixture.setEnabled(False)
            self.confirm_Fixture = scanned_Fixture
            # ตรวจสอบ Fixture ผ่าน DataUploader
            if hasattr(self, 'product_formatted'):
                self.product_formatted1 = self.product_formatted.replace('\u200c', '')
                
                # Retrieve current mode, default to 'mass' if not set
                mode = getattr(self, 'current_mode', 'mass')
                is_valid, fixture_data = self.data_upload.check_fixture_validity(scanned_Fixture, mode=mode)
                if fixture_data:
                    self.matched_tooling = fixture_data['fpc_code']
                    self.ost_from_data_base = fixture_data.get("use_for")
                    print(f"ost_from_data_base : {self.ost_from_data_base}")
                    fpc_pd_name = fixture_data.get("fpc_pd_name", "")
                    self.matched_product_name = fpc_pd_name # Store for FOST validation

                    if self.data_upload.is_product_matching(self.product_formatted1, fpc_pd_name):
                        print("✅ Product matches database")
                        self.is_fixture_valid = True
                        self.LineLabelscanFixture.setText("✅ Fixture Code is valid")
                        self.LineLabelscanFixture.setStyleSheet("color: green; font-weight: bold;")
                        self.update_save_button_status()
                    else:
                        self.is_fixture_valid = False
                        self.LineLabelscanFixture.setText(f"❌ Product does not match Fixture")
                        self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.is_fixture_valid = False
                    self.LineLabelscanFixture.setText(f"❌ Fixture not found: {scanned_Fixture}")
                    self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.LineLabelscanFixture.setText("❌ Please scan POS first")
                self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")

    def handle_ost_change(self, checked):
        sender = self.sender()
        if not isinstance(sender, QRadioButton):
            return

        if not getattr(self, 'is_fixture_valid', False):
            print("🚫 Cannot confirm OST - Fixture is invalid")
            self.LineLabelscanFixture.setText("❌ Please scan a valid Fixture before selecting OST")
            self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")
            sender.setChecked(False)
            return

        if checked:
            self.confirm_ost_selection(sender)

    def confirm_ost_selection(self, selected_rb):
        clicked_OST = selected_rb.objectName()
        print(f"🔘 Checking: {clicked_OST}")
        
        # Store selected OST for saving
        self.selected_ost_type = clicked_OST

        # FA Mode: Allow any selection because FA database lacks FOST data
        if getattr(self, 'current_mode', 'mass') == 'fa':
            print("ℹ️ FA Mode detected - Allowing user FOST selection")
            self.show_ost_status(True, clicked_OST)
            return

        if hasattr(self, 'ost_from_data_base') and self.ost_from_data_base:
            db_ost = self.ost_from_data_base.replace('\u200c', '').strip()
            
            # Special case for 'CAW-076W' product family
            # Allow FOST or FOST2 or FOST3 if the product matches "CAW-076W" regardless of strict DB assignment
            is_special_case = False
            if hasattr(self, 'matched_product_name') and "CAW-076W" in self.matched_product_name:
                print("ℹ️ Special Case Detected: CAW-076W - Allowing FOST/FOST2/FOST3 selection")
                if clicked_OST in ["FOST", "FOST2", "FOST3"]:
                    is_special_case = True

            if is_special_case or \
               (clicked_OST == "FOST" and db_ost == "FOST") or \
               (clicked_OST == "FOST2" and db_ost == "FOST2") or \
               (clicked_OST == "FOST2" and db_ost == "FOST3"):
                self.show_ost_status(True, db_ost)
            else:
                self.show_ost_status(False)
        else:
            print("⚠️ Database data not loaded")
            self.show_ost_status(False)

    def show_ost_status(self, is_valid, ost_name=""):
        if is_valid:
            self.LineLabelscanFixture.setText("✅ FOST is correct")
            self.LineLabelscanFixture.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.LineLabelscanFixture.setText("❌ FOST is incorrect")
            self.LineLabelscanFixture.setStyleSheet("color: red; font-weight: bold;")

    ###########################################################################
    # UTILITY FUNCTIONS
    def update_save_button_status(self):
        required_attrs = [
            'operator_id', 
            'product_formatted', 
            'matched_tooling',
            'is_fixture_valid',
            'lot_size_value'
        ]
        
        all_ready = all(
            hasattr(self, attr) and 
            (getattr(self, attr) if attr != 'is_fixture_valid' else getattr(self, attr) is True)
            for attr in required_attrs
        )
        
        self.save_button.setEnabled(all_ready)

    def get_product_scan(self):
        return {
            "product_name": self.product_formatted,
            "lot_number": self.lot_number,
            "tooling_code": self.matched_tooling,
            "operator_name": self.operator_name,
            "operator_id": self.operator_id,
            "start_time": self.timestamp,
        }

    ###########################################################################
    # BUTTON FUNCTIONS
    def close_function(self):
        self.close()

    def reset_after_save(self):
        """รีเซ็ตค่าหลังจากบันทึกสำเร็จ"""
        # รีเซ็ตตัวแปร
        self.operator_id = None
        self.operator_name = None
        self.product_formatted = None
        self.lot_number = None
        self.matched_tooling = None
        self.is_fixture_valid = False
        
        # รีเซ็ต UI
        self.scannerIdoperator.setText("Click to scan user ID")
        self.scannerIdoperator.setEnabled(True)
        self.scanPOS.setText("Click to scan Qr code POS")
        self.scanPOS.setEnabled(True)
        self.scanFixture.setText("Click to scan Qr code Fixture") 
        self.scanFixture.setEnabled(True)
        
        # รีเซ็ตสถานะแสดงผล
        self.LineLabelPOS.setText("")
        self.LineLabel.setText("")
        self.LineLabelscanFixture.setText("")
    
        # รีเซ็ต Radio buttons
        for rb in [self.clicked_OST1, self.clicked_OST2, self.clicked_OST3]:
            rb.setAutoExclusive(False)
            rb.setChecked(False)
            rb.setAutoExclusive(True)
        
        # ปิดปุ่ม Save จนกว่าจะกรอกข้อมูลใหม่
        self.save_button.setEnabled(False)
        print("System reset for new entry")

    def reset_function(self):
        # รีเซ็ตช่องกรอก POS
        self.scanPOS.setText("Click to scan Qr code POS")
        self.LineLabelPOS.setText("")
        self.scanPOS.setEnabled(True)

        # รีเซ็ตข้อมูลของ scanFixture
        self.scanFixture.setText("Click to scan Qr code Fixture")
        self.LineLabelscanFixture.setText("")
        self.scanFixture.setEnabled(True)

        # รีเซ็ตข้อมูลผู้ใช้
        self.scannerIdoperator.setText("Click to scan user ID")
        self.LineLabel.setText("")
        self.scannerIdoperator.setEnabled(True)

        # รีเซ็ต Radio buttons
        self.clicked_OST1.setAutoExclusive(False)
        self.clicked_OST2.setAutoExclusive(False)
        self.clicked_OST3.setAutoExclusive(False)
        
        self.clicked_OST1.setChecked(False)
        self.clicked_OST2.setChecked(False)
        self.clicked_OST3.setChecked(False)
        
        self.clicked_OST1.setAutoExclusive(True)
        self.clicked_OST2.setAutoExclusive(True)
        self.clicked_OST3.setAutoExclusive(True)

        self.lot_size.clear()  # ล้างช่องกรอก
        self.lot_size_value = None  # รีเซ็ตตัวแปร

        # รีเซ็ตตัวแปร
        if hasattr(self, 'matched_tooling'):
            del self.matched_tooling
        if hasattr(self, 'ost_from_data_base'):
            del self.ost_from_data_base
        if hasattr(self, 'confirm_Fixture'):
            del self.confirm_Fixture
        if hasattr(self, 'product_formatted1'):
            del self.product_formatted1
        
        self.LineLabelscanFixture.setStyleSheet("color: black; font-weight: normal;")
        self.save_button.setEnabled(False)

    def save_function(self):
        """บันทึกข้อมูลพื้นฐานและ count รวมกัน"""
        # ตรวจสอบข้อมูลครบถ้วนก่อน
        if not all([self.lot_number, self.product_formatted, self.operator_id, self.matched_tooling, self.is_fixture_valid, self.lot_size_value]):
            self._update_status_label("❌ Incomplete data or invalid Fixture", "red")
            return False

        # ใช้ค่าจาก PLC โดยตรงหากมี หรือใช้ค่าเริ่มต้น
        plc_data = getattr(self, 'latest_plc_data', {})

        # ตรวจสอบว่าได้ข้อมูลจาก PLC หรือไม่ (ถ้าไม่มีให้ดึงข้อมูลใหม่)
        if not plc_data:
            print("No recent PLC data found, fetching new data")
            plc_data = self.plc_window.get_updated_values()  # ดึงข้อมูลใหม่จาก PLC

        # ตรวจสอบว่าได้ข้อมูลจาก PLC หรือไม่
        if not plc_data:
            self._update_status_label("❌ Unable to retrieve PLC data", "red")
            return False

        data_to_save = {
            'lot_number': self.lot_number,
            'product_formatted': self.product_formatted,
            'operator_id': self.operator_id,
            'operator_name': self.operator_name,
            'process': self.process,
            'job_title': self.job_title,
            'code_training': self.code_training,
            'train_topic': self.train_topic,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'matched_tooling': self.matched_tooling,
            'ost_from_data_base': self.ost_from_data_base,
            'ost_type': getattr(self, 'selected_ost_type', self.ost_from_data_base), # Use selected, fallback to DB value
            'is_fixture_valid': self.is_fixture_valid,

            'total_sheet': plc_data.get('dm1923', 0),  # ใช้ค่าโดยตรงจาก PLC
            'good_sheet': plc_data.get('dm1924', 0),
            'reject_sheet': plc_data.get('dm1925', 0),
            'total_pcs': plc_data.get('dm1917', 1),
            'good_pcs': plc_data.get('dm1919', 0),
            'reject_pcs': plc_data.get('dm1917', 1) - plc_data.get('dm1919', 0),

            'defects': {
                'SHORT': plc_data.get('dm1911', 0),
                'OPEN': plc_data.get('dm1912', 0),
                'BLKM': plc_data.get('dm1915', 0),
                'MAT': plc_data.get('dm1914', 0),
                'SHOT': plc_data.get('dm1913', 0),
            }
        }
        print("DEBUG: Calling save_all_data with data:", data_to_save)
        result = self.data_upload.save_all_data(data_to_save)
        print("DEBUG: Result from save_all_data:", result)

        if not result or not isinstance(result, dict):
            self._update_status_label("❌ Unknown error occurred", "red")
            self.save_result = None
            return False

        if result.get('status') == 'success':
            self._update_status_label(f"✅ {'Updated' if result['action'] == 'updated' else 'Saved'} successfully", "green")
            self.save_result = result
            return True
        else:
            self._update_status_label(f"❌ {result.get('message', 'Error occurred')}", "red")
            self.save_result = result
            return False


    def _update_status_label(self, message, color):
        """อัปเดต Label สถานะ"""
        self.LineLabelPOS.setText(message)
        self.LineLabelPOS.setStyleSheet(f"color: {color}; font-weight: bold;")
        QApplication.processEvents()  # บังคับอัปเดต UI ทันที

    def get_product_scan(self):
        """ดึงข้อมูลการสแกนพร้อมตรวจสอบความถูกต้อง"""
        try:
            # ตรวจสอบว่ามีข้อมูลที่จำเป็น
            if not all(hasattr(self, attr) and getattr(self, attr) for attr in [
                'product_formatted', 'lot_number', 'matched_tooling', 'operator_id'
            ]):
                raise ValueError("Scan data incomplete")

            return {
                "product_name": self.product_formatted,
                "lot_number": self.lot_number,
                "tooling_code": self.matched_tooling,
                "operator_name": getattr(self, 'operator_name', 'N/A'),
                "operator_id": self.operator_id,
                "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"Error in get_product_scan: {str(e)}")
            return {
                "error": True,
                "message": str(e)
            }

if __name__ == '__main__':
    try:
        print("Starting application...")
        app = QApplication(sys.argv)
        window = MyWindow()
        window.show()
        print("Main window displayed")
        sys.exit(app.exec())
    except Exception as e:
        print(f"Critical error: {e}")
        sys.exit(1)