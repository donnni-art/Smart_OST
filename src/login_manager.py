"""
login_manager.py
================
จัดการกระบวนการ Login และการตรวจสอบ Lot Number ก่อนเข้า Dashboard

หน้าที่หลัก:
  - แสดง login scan dialog (MyWindow) เพื่อรับข้อมูล operator + product
  - ตรวจสอบ Lot Number ซ้ำผ่าน lot_checker ก่อน login สำเร็จ
  - ดึงข้อมูล product_name จาก DB ด้วย DataUploader
  - retry login สูงสุด 3 ครั้งเมื่อข้อมูลไม่ครบ

การใช้งาน:
  - สร้างโดย MainWindow ใน __init__:
      self.login_manager = LoginManager(self.plc_window, self)
  - เรียก:
      success = self.login_manager.login()
      data    = self.login_manager.get_data_scan()   → dict
      user    = self.login_manager.get_user_info()   → dict

ความสัมพันธ์กับโมดูลอื่น:
  - login_scan  : MyWindow dialog รับ scan barcode
  - lot_checker : ตรวจสอบสถานะ Lot ใน database
  - DataUploader: ดึง product_name จาก lot_number
"""
import re
import logging
from datetime import datetime
from PySide6.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PySide6.QtCore import QCoreApplication
from src.login_scan import MyWindow
from src.lot_checker import lot_checker
from src.data_upload import DataUploader

class LoginManager:
    def __init__(self, plc_window, parent=None):
        self.parent = parent
        self.logged_in_user = {}
        self.plc_window = plc_window
        self.product_info = {}
        self.data_uploader = DataUploader()  # เพิ่ม DataUploader
        self._is_logging_in = False
        
    def setup_logging(self):
        import sys
        import logging

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        # Clear previous handlers (to prevent duplicates)
        if root.hasHandlers():
            root.handlers.clear()

        # File handler (UTF-8)
        file_handler = logging.FileHandler('login_manager.log', encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        root.addHandler(file_handler)

        # Console handler (UTF-8)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        root.addHandler(console_handler)

        logging.debug("LoginManager initialized with UTF-8 logging")


    def login(self, retry_count=0, max_retries=3, is_after_reset=False):
        """Execute login process with Lot Number pre-check"""
        # ✅ Prevent duplicate login attempts
        if self._is_logging_in:
            print("⚠️ Login process already in progress")
            return False
            
        self._is_logging_in = True
        
        try:
            # ========================================================
            # STEP 1: Pre-check Lot Number
            # ========================================================
            lot_check_result = self._perform_lot_pre_check()
            
            if lot_check_result == 'DIRECT_LOGIN':
                # Lot is valid, data loaded - go directly to dashboard
                print("✅ Lot pre-check passed - Direct login")
                self._is_logging_in = False
                return True
            elif lot_check_result == 'CANCEL':
                # User cancelled - exit application
                self._is_logging_in = False
                QCoreApplication.quit()
                return False
            # else: lot_check_result == 'MANUAL_LOGIN' -> proceed to normal scan
            
            # ========================================================
            # STEP 2: Normal Login via Scanning (Original Flow)
            # ========================================================
            while retry_count < max_retries:
                login_dialog = MyWindow(self.plc_window) #Start Login_scan.py
                result = login_dialog.exec()

                if result == QDialog.DialogCode.Accepted:
                    try:
                        self._process_successful_login(login_dialog)
                        logging.debug("Login accepted and processed successfully")
                        self._is_logging_in = False
                        return True
                    except Exception as e:
                        logging.error(f"Login error: {str(e)}", exc_info=True)
                        if not self._handle_login_error(e, retry_count, max_retries):
                            self._is_logging_in = False
                            return False
                        retry_count += 1
                else:
                    logging.info("Login cancelled by user")
                    if not self._handle_login_cancellation(is_after_reset):
                        self._is_logging_in = False
                        return False

            logging.warning("Maximum login attempts exceeded")
            QMessageBox.warning(
                self.parent,
                "Attempts Exceeded",
                "You have exceeded the maximum number of attempts. Please try again later."
            )
            self._is_logging_in = False
            return False
            
        except Exception as e:
            logging.error(f"Unexpected login error: {str(e)}", exc_info=True)
            self._is_logging_in = False
            return False

    def _perform_lot_pre_check(self) -> str:
        """
        Perform Lot Number pre-check before manual login.
        
        Returns:
            'DIRECT_LOGIN': Lot valid, data loaded - skip manual login
            'MANUAL_LOGIN': Need to proceed with manual scan login
            'CANCEL': User cancelled the process
        """
        # Show input dialog for Lot Number
        lot_number, ok = QInputDialog.getText(
            self.parent,
            "Lot Number Check",
            "กรุณา Scan หรือกรอก Lot Number:",
            QLineEdit.Normal,
            ""
        )
        
        if not ok:
            # User clicked Cancel
            reply = QMessageBox.question(
                self.parent,
                "ยืนยันการยกเลิก",
                "ต้องการ Login แบบ Manual (Scan) หรือออกจากโปรแกรม?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            if reply == QMessageBox.StandardButton.Yes:
                return 'MANUAL_LOGIN'
            else:
                return 'CANCEL'
        
        if not lot_number.strip():
            QMessageBox.warning(
                self.parent,
                "Lot Number ว่าง",
                "กรุณากรอก Lot Number หรือใช้การ Login แบบ Manual"
            )
            return 'MANUAL_LOGIN'
        
        # Check Lot in Big Data database
        print(f"🔍 Checking Lot Number: {lot_number}")
        result = lot_checker.check_lot(lot_number.strip())
        
        status = result.get('status', 'ERROR')
        message = result.get('message', '')
        lot_data = result.get('data')
        parsed_input = result.get('parsed_input', {})
        
        if status == 'VALID':
            # Lot is valid - now verify Fixture and Operator
            print(f"✅ Lot {lot_number} is valid - verifying Fixture and Operator...")
            
            tooling_code = lot_data.get('tooling_code', '')
            operator_id = lot_data.get('operator_id', '')
            product_name = lot_data.get('product_name', '')
            
            # ========================================================
            # VERIFY FIXTURE
            # ========================================================
            print(f"🔍 Verifying Fixture: {tooling_code}")
            is_fixture_valid, fixture_data = self.data_uploader.check_fixture_validity(tooling_code, mode='mass')
            
            if not is_fixture_valid:
                print(f"⚠️ Fixture not found in local DB: {tooling_code}")
                # ลองค้นหาใน FA mode
                is_fixture_valid, fixture_data = self.data_uploader.check_fixture_validity(tooling_code, mode='fa')
            
            if is_fixture_valid and fixture_data:
                fpc_pd_name = fixture_data.get('fpc_pd_name', '') or fixture_data.get('Product_Name', '')
                print(f"✅ Fixture valid - fpc_pd_name: {fpc_pd_name}")
                
                # ตรวจสอบ Product Matching
                if not self.data_uploader.is_product_matching(product_name, fpc_pd_name):
                    print(f"⚠️ Product mismatch: {product_name} vs {fpc_pd_name}")
                    QMessageBox.warning(
                        self.parent,
                        "Product ไม่ตรงกับ Fixture",
                        f"Product จาก Oracle: {product_name}\nProduct จาก Fixture DB: {fpc_pd_name}\n\nกรุณาใช้การ Login แบบ Manual"
                    )
                    return 'MANUAL_LOGIN'
                    
                # เก็บ fixture data สำหรับ upload
                lot_data['_fixture_data'] = fixture_data
                lot_data['is_fixture_valid'] = True
            else:
                # ❌ Block if Fixture not found - redirect to manual login
                print(f"❌ Fixture not found: {tooling_code} - redirecting to manual login")
                QMessageBox.warning(
                    self.parent,
                    "Fixture ไม่พบในระบบ",
                    f"ไม่พบ Fixture Code: {tooling_code} ในฐานข้อมูล\n\nกรุณาใช้การ Login แบบ Manual"
                )
                return 'MANUAL_LOGIN'
            
            # ========================================================
            # VERIFY OPERATOR
            # ========================================================
            print(f"🔍 Verifying Operator: {operator_id}")
            is_operator_valid, operator_data = self.data_uploader.check_user_permission(operator_id)
            
            if is_operator_valid and operator_data:
                print(f"✅ Operator valid: {operator_data.get('operator_name', '')}")
                lot_data['_operator_data'] = operator_data
            else:
                # ❌ Block if Operator not found or not authorized - redirect to manual login
                print(f"❌ Operator not authorized: {operator_id} - redirecting to manual login")
                QMessageBox.warning(
                    self.parent,
                    "Operator ไม่ผ่านการตรวจสอบ",
                    f"Operator ID: {operator_id} ไม่พบในระบบ หรือไม่มีสิทธิ์ใช้งาน\n\n" +
                    "ต้องมี Training Code: F4/1 หรือ F4/2\n\nกรุณาใช้การ Login แบบ Manual"
                )
                return 'MANUAL_LOGIN'
            
            # Load data และ Upload to server
            self._load_lot_data_for_login(lot_data, parsed_input)
            self._upload_to_server(lot_data)
            return 'DIRECT_LOGIN'
            
        elif status == 'NOT_FOUND':
            # Lot not found - alert user to scan in-process first
            QMessageBox.warning(
                self.parent,
                "ไม่พบ Lot Number",
                f"{message}\n\nกรุณาไป Scan In Process ให้เสร็จก่อนแล้วค่อยกลับมา Login"
            )
            return 'MANUAL_LOGIN'
            
        elif status == 'INVALID':
            # Lot found but validation failed - show error details
            QMessageBox.critical(
                self.parent,
                "Lot Number ไม่ผ่านการตรวจสอบ",
                f"พบปัญหา: {message}\n\nกรุณาตรวจสอบข้อมูลและดำเนินการ Login แบบ Manual"
            )
            return 'MANUAL_LOGIN'
            
        else:
            # Error case
            QMessageBox.critical(
                self.parent,
                "เกิดข้อผิดพลาด",
                f"ไม่สามารถตรวจสอบ Lot Number ได้:\n{message}\n\nกรุณาใช้การ Login แบบ Manual"
            )
            return 'MANUAL_LOGIN'

    def _load_lot_data_for_login(self, lot_data: dict, parsed_input: dict = None):
        """
        Load data from Lot check result into login manager.
        
        This prepares the data so MainWindow can use it directly
        without requiring manual scan.
        
        Args:
            lot_data: Data from database
            parsed_input: Parsed input from scan (may contain product_formatted from POS)
        """
        try:
            parsed_input = parsed_input or {}
            
            # Get formatted data from lot_checker
            formatted_data = lot_checker.get_lot_info_for_login(lot_data)
            
            # Use product_formatted from POS scan if available, otherwise format from database
            raw_product = parsed_input.get('product_formatted') or formatted_data.get('product_name', '')
            # Format the product code like login_scan does
            product_name = self._format_product_code(raw_product)
            lot_number = parsed_input.get('lot_number') or formatted_data.get('lot_number', '')
            
            # Get operator data if available (from verification step)
            operator_data = lot_data.get('_operator_data', {}) or {}
            
            # Set start_time to current datetime
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Populate product_info (used by MainWindow)
            self.product_info = {
                'product_name': product_name,
                'lot_number': lot_number,
                'tooling_code': formatted_data.get('tooling_code', ''),
                'operator_name': operator_data.get('operator_name', '') if operator_data else '',
                'operator_id': formatted_data.get('operator_id', ''),
                'start_time': start_time,
                'lot_size_value': lot_data.get('lot_size', lot_data.get('LOT_SIZE', 0)),
            }
            
            # Populate logged_in_user with extra info for upload
            self.logged_in_user = {
                'lot_number': lot_number,
                'operator_id': formatted_data.get('operator_id', ''),
                'operator_name': operator_data.get('operator_name', '') if operator_data else '',
                'product_formatted': product_name,
                'matched_tooling': formatted_data.get('tooling_code', ''),
                'from_lot_check': True,  # Flag to indicate data came from lot check
                'wo_number': parsed_input.get('wo_number', ''),  # WO from POS scan
                'ost_type': lot_data.get('ost_type', ''),
                'is_fixture_valid': lot_data.get('is_fixture_valid', False),
                # Operator extra data
                'process': operator_data.get('process', '') if operator_data else '',
                'job_title': operator_data.get('job_title', '') if operator_data else '',
                'code_training': operator_data.get('code_training', '') if operator_data else '',
                'train_topic': operator_data.get('train_topic', '') if operator_data else '',
                'timestamp': start_time,
            }
            
            print(f"✅ Lot data loaded: {self.product_info}")
            logging.info(f"Loaded lot data for direct login: {self.product_info.get('lot_number')}")
            
        except Exception as e:
            print(f"❌ Error loading lot data: {e}")
            logging.error(f"Error loading lot data: {e}")
            raise
    
    def _format_product_code(self, product_code: str) -> str:
        """
        Format product code to standard format.
        Same logic as login_scan.py format_product_code()
        
        Example: "CAW076W1A" -> "CAW-076W-1A"
        Example: "95SUSZ018MW1B" -> "SUS-Z018M-W1B" (skip leading digits)
        """
        if not product_code:
            return product_code
        
        # Remove any invisible characters
        product_code = product_code.replace('\u200c', '').strip()
        
        # Skip leading digits (like "95" in "95SUSZ018MW1B")
        clean_code = re.sub(r'^[\d]+', '', product_code)
        
        match = re.match(r"([A-Za-z]+)(\d+)([A-Za-z]+)(\d+[A-Za-z]+)?", clean_code)
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
            # If pattern doesn't match, return the cleaned code
            return clean_code if clean_code else product_code

    def _upload_to_server(self, lot_data: dict):
        """
        Upload login data to server (tbl_result_test).
        
        Args:
            lot_data: Data from lot_checker including verification results
        """
        try:
            # ตรวจสอบว่า fixture valid หรือไม่
            if not lot_data.get('is_fixture_valid', False):
                print("⚠️ Fixture not validated - skipping server upload")
                return
            
            operator_data = lot_data.get('_operator_data', {}) or {}
            
            # Prepare data for save_all_data
            upload_data = {
                'lot_number': self.logged_in_user.get('lot_number', ''),
                'product_formatted': self.logged_in_user.get('product_formatted', ''),
                'matched_tooling': self.logged_in_user.get('matched_tooling', ''),
                'operator_id': self.logged_in_user.get('operator_id', ''),
                'operator_name': operator_data.get('operator_name', ''),
                'process': operator_data.get('process', ''),
                'job_title': operator_data.get('job_title', ''),
                'code_training': operator_data.get('code_training', ''),
                'train_topic': operator_data.get('train_topic', ''),
                'ost_type': lot_data.get('ost_type', ''),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'is_fixture_valid': True,
                # Initial counts (will be updated later)
                'total_sheet': 0,
                'good_sheet': 0,
                'reject_sheet': 0,
                'total_pcs': 0,
                'good_pcs': 0,
                'reject_pcs': 0,
                'defects': {'SHORT': 0, 'OPEN': 0, 'BLKM': 0, 'MAT': 0, 'SHOT': 0}
            }
            
            print(f"📤 Uploading to server: Lot={upload_data['lot_number']}, Product={upload_data['product_formatted']}")
            
            result = self.data_uploader.save_all_data(upload_data)
            
            if result.get('status') == 'success':
                print("✅ Data uploaded to server successfully")
                logging.info(f"Uploaded login data for lot: {upload_data['lot_number']}")
            else:
                print(f"⚠️ Upload failed: {result.get('message', 'Unknown error')}")
                logging.warning(f"Failed to upload login data: {result.get('message')}")
                
        except Exception as e:
            print(f"❌ Error uploading to server: {e}")
            logging.error(f"Error uploading to server: {e}")

    def _process_successful_login(self, login_dialog):
        logging.debug("Processing successful login")
        if not hasattr(login_dialog, 'save_result') or 'data' not in login_dialog.save_result:
            logging.error("No save_result data found in login dialog")
            raise ValueError("Save result data not found.") 

        self.product_info = login_dialog.get_product_scan()
        logging.debug(f"Product info obtained: {self.product_info}")

        if not self.product_info:
            logging.error("Product info is empty or invalid")
            raise ValueError("Product information is incomplete.")

        self.logged_in_user = login_dialog.save_result['data']
        logging.debug(f"User logged in: {self.logged_in_user}")

        # Assume lot_number is in user data or product_info
        lot_number = self.logged_in_user.get('lot_number') or self.product_info.get('lot_number')
        logging.debug(f"Lot number extracted: {lot_number}")

        lot_size_value = getattr(login_dialog, 'lot_size_value', None)
        print(f"lot_size_value: {lot_size_value}")
        if lot_size_value is not None:
            logging.debug(f"Lot size value obtained: {lot_size_value}")
            self.product_info['lot_size_value'] = lot_size_value
        else:
            logging.warning("Lot size value is None.")

        if hasattr(self.parent, 'update_label_with_product_info'):
            self.parent.update_label_with_product_info()

        logging.info(f"User {self.logged_in_user.get('operator_id', 'unknown')} logged in successfully")

    def _handle_login_error(self, error, retry_count, max_retries):
        remaining_attempts = max_retries - retry_count - 1
        error_msg = f"{str(error)}\n\n{remaining_attempts} attempts remaining.\nDo you want to try again?"

        retry = QMessageBox.critical(
            self.parent,
            "Error",
            error_msg,
            QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel
        )

        logging.debug(f"User chose {'Retry' if retry == QMessageBox.StandardButton.Retry else 'Cancel'} on login error")
        return retry == QMessageBox.StandardButton.Retry

    def _handle_login_cancellation(self, is_after_reset=False):
        """Handle user cancellation
        Args:
            is_after_reset: True if logging in after a reset
        """
        # ✅ When user cancels login, exit immediately without asking again
        # The MainWindow closeEvent will handle the confirmation if needed
        logging.debug("Login cancelled by user - closing application")
        QCoreApplication.quit()
        return False

    def get_data_scan(self):
        logging.debug(f"Returning product info: {self.product_info}")
        return self.product_info

    def get_user_info(self):
        logging.debug(f"Returning logged in user info: {self.logged_in_user}")
        return self.logged_in_user

    def is_logged_in(self):
        status = bool(self.logged_in_user)
        logging.debug(f"is_logged_in check: {status}")
        return status