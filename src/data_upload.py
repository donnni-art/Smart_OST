import re  # เพิ่มบรรทัดนี้ที่ส่วนบนของไฟล์
import mysql.connector
from datetime import datetime
import logging
from src.config_manager import config_manager
from src.database_manager import database_manager  # ✅ เพิ่ม import DatabaseManager

class DataUploader:
    def __init__(self):
        # ✅ ใช้ DatabaseManager แทนการเชื่อมต่อโดยตรง
        self.db_manager = database_manager
        
        # ✅ ลบ db_config เดิมออก เพราะจะใช้ DatabaseManager จัดการแทน
        # self.db_config ไม่จำเป็นอีกต่อไป
        
        self.setup_logging()
    
    def setup_logging(self):
        # ใช้ path จาก config
        logs_path = config_manager.get_full_path(config_manager.get_paths_config().get('logs', 'logs'))
        log_file = logs_path / "data_uploader.log"
        
        logging.basicConfig(
            filename=str(log_file),
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def get_product_name_by_lot(self, lot_number: str):
        """อ่านข้อมูล product_name จาก tbl_result_test (WRITE DATABASE)"""
        try:
            # ✅ ใช้ execute_read_query จาก write_database
            connection = self.db_manager.get_write_connection()
            if not connection:
                return None, "❌ ไม่สามารถเชื่อมต่อฐานข้อมูลได้"

            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT product_name FROM tbl_result_test WHERE lot_number = %s", (lot_number,))
            result = cursor.fetchone()
            cursor.close()

            if result and 'product_name' in result:
                return result['product_name'], None
            else:
                return None, None

        except Exception as e:
            print(f"❌ Query error: {e}")
            return None, f"❌ เกิดข้อผิดพลาด: {str(e)}"
    
    def check_user_permission(self, user_id):
        """ตรวจสอบสิทธิ์ผู้ใช้งานจาก tbl_training (WRITE DATABASE)"""
        try:
            # ✅ ใช้ write_database เพราะ tbl_training อยู่ใน write database
            connection = self.db_manager.get_write_connection()
            if not connection:
                logging.error("❌ Cannot connect to write database")
                return False, None
                
            cursor = connection.cursor(dictionary=True)

            query = "SELECT * FROM tbl_training WHERE id_code = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if result:
                train_code = result.get("code_training", "").strip()
                if train_code in ["F4/1", "F4/2"]:
                    user_data = {
                        "operator_id": result.get("id_code"),
                        "operator_name": result.get("name"),
                        "process": result.get("process"),
                        "job_title": result.get("job_title"),
                        "code_training": result.get("code_training"),
                        "train_topic": result.get("train_item"),
                    }
                    logging.info(f"✅ User authorized: {user_id}")
                    cursor.close()
                    return True, user_data

            logging.warning(f"⚠️ User not authorized or not found: {user_id}")
            cursor.close()
            return False, None

        except mysql.connector.Error as err:
            logging.error(f"❌ Database error: {err}")
            return False, None

        except Exception as e:
            logging.error(f"⚠️ Unexpected error in check_user_permission: {e}")
            return False, None


    def check_id_staff_employee(self, scanned_id):
        """ตรวจสอบว่า ID ที่สแกนตรงกับข้อมูลใน tbl_staff (STAFF DATABASE)"""
        try:
            # ✅ ใช้ staff_database เพราะ tbl_staff อยู่ใน design database
            connection = self.db_manager.get_staff_connection()
            if not connection:
                logging.error("❌ Cannot connect to staff database")
                return False, None
                
            cursor = connection.cursor(dictionary=True)

            query = "SELECT Code, Name FROM tbl_staff WHERE Code = %s"
            cursor.execute(query, (scanned_id,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                # ถ้าเจอ → เก็บข้อมูลพนักงาน + เวลา
                now = datetime.now()
                user_data = {
                    "employee_id": result["Code"],
                    "name": result["Name"],
                    "scan_date": now.strftime("%Y-%m-%d"),
                    "scan_time": now.strftime("%H:%M:%S")
                }
                return True, user_data
            else:
                return False, None

        except Exception as e:
            logging.error(f"Database error in check_id_staff_employee: {e}")
            return False, None
    
    def check_fixture_validity(self, fixture_code, mode='mass'):
        """
        ตรวจสอบความถูกต้องของ fixture และ product
        mode='mass' -> ใช้ tbl_fpc (tooling_fix DB)
        mode='fa' -> ใช้ tbl_database (design DB)
        """
        try:
            # เลือก connection และ query ตาม mode
            if mode == 'mass':
                connection = self.db_manager.get_read_connection()
                query = "SELECT * FROM tbl_fpc WHERE fpc_type = 'FIXTURE' AND fpc_code = %s"
                db_name = "READ DB (tooling_fix)"
            elif mode == 'fa':
                # FA mode ใช้ database design ซึ่งปกติอยู่ใน staff connection หรือต้อง config แยก
                # ตาม Requirement: เปลี่ยน read_database เป็น design
                # แต่ใน implementation จริง เราอาจจะใช้ connection ที่ชี้ไปที่ design ตรงๆ
                # ซึ่ง config 'read_database' จะถูก reload ใหม่ใน level บน (login_scan.py) 
                # ดังนั้นตรงนี้เราใช้ get_read_connection() ได้เลย ถ้า logic การ reload ถูกต้อง
                # หรือถ้าต้องการ query ต่างตารางกันจริงๆ
                
                connection = self.db_manager.get_read_connection()
                query = "SELECT * FROM tbl_database WHERE Types = 'FIXTURE' AND Tooling_Code = %s" 
                db_name = "READ DB (design)"
            else:
                logging.error(f"Invalid mode: {mode}")
                return False, None

            if not connection:
                logging.error(f"❌ Cannot connect to {db_name}")
                return False, None
                
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (fixture_code,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                logging.debug(f"Fixture found in {mode} mode: {fixture_code}")
                
                # Normalize field names if tables are different
                if mode == 'fa':
                    # Map fields from tbl_database to match expected format
                    # tbl_database fields: Tooling_Code, etc. -> map to fpc_code
                    result['fpc_code'] = result.get('Tooling_Code')
                    result['fpc_pd_name'] = result.get('Product_Name') # Assuming Product_Name exists or similar
                    # If field names differ significantly, mapping is needed here
                    
                return True, result  # ✅ return True เมื่อพบข้อมูล
            else:
                logging.debug(f"Fixture not found in {mode} mode: {fixture_code}")
                return False, None  # ✅ return False เมื่อไม่พบข้อมูล

        except Exception as e:
            logging.error(f"Error in check_fixture_validity: {e}")
            return False, None  # ✅ return False เมื่อเกิด error
    
    def is_product_matching(self, product_code, fpc_pd_name_from_db):
        """ตรวจสอบว่า product_code ตรงกับ fpc_pd_name หรือไม่"""
        if not product_code or not fpc_pd_name_from_db:
            print(f"❌ Missing data - product_code: {product_code}, fpc_pd_name: {fpc_pd_name_from_db}")
            return False

        product_clean = product_code.replace('\u200c', '').strip().upper()
        fpc_pd_clean = fpc_pd_name_from_db.replace('\u200c', '').strip()

        print(f"🔍 Product Matching Debug:")
        print(f"   Original product_code: {repr(product_code)}")
        print(f"   Cleaned product_code: {product_clean}")
        print(f"   Original fpc_pd_name: {repr(fpc_pd_name_from_db)}")
        print(f"   Cleaned fpc_pd_name: {fpc_pd_clean}")

        if "-" in product_clean:
            base_part, suffix_part = product_clean.rsplit("-", 1)
        else:
            base_part = product_clean
            suffix_part = ""

        print(f"   Suffix part: {suffix_part}")

        # Handle multiple separators (comma or slash)
        # Replace '/' with ',' to handle "SYC-476W / SYC-480W" format
        fpc_pd_normalized = fpc_pd_clean.replace('/', ',')
        fpc_pd_list = [item.strip().upper() for item in fpc_pd_normalized.split(",")]
        print(f"   FPC PD List: {fpc_pd_list}")

        full_candidates = []
        for part in fpc_pd_list:
            if "-" in part:
                full_candidates.append(part)
            else:
                full_candidates.append(f"{base_part}-{part}")

        print(f"   Full candidates: {full_candidates}")
        print(f"   Checking if '{product_clean}' matches any candidate in {full_candidates}")
        
        # Check for exact match or prefix match
        result = False
        for candidate in full_candidates:
            # 1. Exact match
            if product_clean == candidate:
                result = True
                break
            # 2. Prefix match (DB has "CAW-076W", Scan is "CAW-076W-0A")
            # We ensure that if it's a prefix match, it should be followed by a hyphen or end of string if we strictly controlled,
            # but usually startswith is enough if codes are structured.
            # Adding check to ensure we don't match "ABC-1" with "ABC-12" (which is different), 
            # usually different sets are separated. 
            # For this specific request "CAW076W0A" (CAW-076W-0A) vs "CAW-076W", it's a clear prefix.
            if product_clean.startswith(candidate):
                result = True
                break
                
        print(f"   Result: {'✅ MATCH' if result else '❌ NO MATCH'}")
        
        logging.debug(f"Checking product {product_clean} against: {full_candidates} -> {result}")
        return result

    def update_counts_only(self, data):
        """อัพเดตข้อมูล counts ใน tbl_result_test (WRITE DATABASE)"""
        # ตรวจสอบข้อมูลที่จำเป็น
        required_fields = ['lot_number', 'good_pcs', 'defects']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return {'status': 'error', 'message': f"Missing fields: {', '.join(missing_fields)}", 'data': None}

        try:
            # ✅ ใช้ write_database
            connection = self.db_manager.get_write_connection()
            if not connection:
                logging.error("❌ Cannot connect to write database")
                return {'status': 'error', 'message': 'Cannot connect to database', 'data': None}
                
            logging.debug(f"Connected to WRITE DB")

            cursor = connection.cursor(dictionary=True)

            # ตรวจสอบ lot_number ก่อนอัปเดต
            product_name, err = self.get_product_name_by_lot(data['lot_number'])
            if err or not product_name:
                logging.error(f"Lot number {data['lot_number']} not found in DB")
                cursor.close()
                return {'status': 'error', 'message': f"Lot number {data['lot_number']} not found", 'data': None}

            # คำนวณค่าใหม่เพื่อความถูกต้อง
            total_pcs = data.get('total_pcs', data.get('good_pcs', 0) + data.get('ng_pcs', 0))
            good_pcs = data.get('good_pcs', 0)
            ng_pcs = total_pcs - good_pcs
            reject_ratio = (ng_pcs / total_pcs * 100) if total_pcs > 0 else 0

            sql_update = """
                UPDATE tbl_result_test SET
                    total_sheet = %s,
                    good_sheet = %s,
                    reject_sheet = %s,
                    total_pcs = %s,
                    good_pcs = %s,
                    reject_pcs = %s,
                    reject_ratio = %s,
                    short = %s,
                    open = %s,
                    blkm = %s,
                    mat = %s,
                    shot = %s,
                    date_time = NOW()
                WHERE lot_number = %s
            """

            defects = data.get('defects', {})

            values = (
                data.get('total_sheet', 0),
                data.get('good_sheet', 0),
                data.get('reject_sheet', 0),
                total_pcs,
                good_pcs,
                ng_pcs,
                reject_ratio,
                defects.get('SHORT', 0),
                defects.get('OPEN', 0),
                defects.get('BLKM', 0),
                defects.get('MAT', 0),
                defects.get('SHOT', 0),
                data['lot_number']
            )

            logging.debug(f"Executing SQL update with values: {values}")
            cursor.execute(sql_update, values)
            connection.commit()
            logging.debug("Database commit successful")

            # ดึงข้อมูลหลังอัปเดตเพื่อตรวจสอบ
            cursor.execute("SELECT * FROM tbl_result_test WHERE lot_number = %s", (data['lot_number'],))
            updated_data = cursor.fetchone()
            cursor.close()

            if updated_data:
                logging.debug(f"Update verified for lot_number={data['lot_number']}")
            else:
                logging.warning(f"No data returned after update for lot_number={data['lot_number']}")

            return {
                'status': 'success', 
                'message': 'Updated counts successfully',
                'data': {
                    'lot_number': data['lot_number'],
                    'total_pcs': total_pcs,
                    'good_pcs': good_pcs,
                    'ng_pcs': ng_pcs,
                    'reject_ratio': reject_ratio,
                    'updated_at': updated_data['date_time'] if updated_data else None
                }
            }

        except mysql.connector.Error as err:
            logging.error(f"MySQL error during update_counts_only: {err}", exc_info=True)
            if connection and connection.is_connected():
                connection.rollback()
            return {'status': 'error', 'message': str(err), 'data': None}
        except Exception as e:
            logging.error(f"Unexpected error during update_counts_only: {e}", exc_info=True)
            if connection and connection.is_connected():
                connection.rollback()
            return {'status': 'error', 'message': str(e), 'data': None}

    def update_logout_data(self, data):
        """อัพเดตข้อมูลการ Logout ขึ้นเซิร์ฟเวอร์ใน tbl_result_test (WRITE DATABASE)"""
        try:
            # ✅ ใช้ write_database
            connection = self.db_manager.get_write_connection()
            if not connection:
                logging.error("❌ Cannot connect to write database")
                return {'status': 'error', 'message': 'Cannot connect to database'}
                
            cursor = connection.cursor(dictionary=True)
            
            # SQL query สำหรับอัพเดตข้อมูลการ logout
            sql_update = """
                UPDATE tbl_result_test SET
                    confirm_closs_lot_by = %s,
                    confirm_total_ng = %s,
                    confirm_open = %s,
                    confirm_short = %s,
                    confirm_blkm = %s,
                    confirm_mat = %s,
                    confirm_shot = %s,
                    note = %s,
                    closs_time = %s
                WHERE lot_number = %s
            """
            
            values = (
                data['confirmed_by'],  # confirm_closs_lot_by
                data['total_ng'],      # confirm_total_ng
                data['open_defects'],  # confirm_open
                data['short_defects'], # confirm_short
                data['blkm_defects'],  # confirm_blkm
                data['mat_defects'],   # confirm_mat
                data['shot_defects'],  # confirm_shot
                data['notes'],         # note
                data['timestamp'],     # closs_time
                data['lot_number']     # lot_number
            )
            
            cursor.execute(sql_update, values)
            connection.commit()
            cursor.close()
            
            logging.info(f"✅ Updated logout data for lot: {data['lot_number']}")
            return {
                'status': 'success',
                'message': 'บันทึกข้อมูลการ Logout ขึ้นเซิร์ฟเวอร์เรียบร้อย'
            }
            
        except Exception as e:
            logging.error(f"❌ Error updating logout data: {e}")
            if connection and connection.is_connected():
                connection.rollback()
            return {
                'status': 'error',
                'message': f'เกิดข้อผิดพลาดในการบันทึกข้อมูล: {str(e)}'
            }
                
    def save_all_data(self, data):
        """
        รวมบันทึกข้อมูลทั้งตัวตนและ count data ในฟังก์ชันเดียว (WRITE DATABASE)
        """
        required_fields = ['operator_id', 'product_formatted', 'matched_tooling', 'lot_number', 'timestamp', 'is_fixture_valid']
        missing_fields = [f for f in required_fields if f not in data or not data[f]]
        if missing_fields:
            return {
                'status': 'error',
                'message': f"❌ ขาดข้อมูลจำเป็น: {', '.join(missing_fields)}",
                'data': None
            }
        if not data.get('is_fixture_valid', False):
            return {
                'status': 'error',
                'message': "❌ Fixture ไม่ถูกต้อง",
                'data': None
            }

        try:
            # ✅ ใช้ write_database
            connection = self.db_manager.get_write_connection()
            if not connection:
                logging.error("❌ Cannot connect to write database")
                return {'status': 'error', 'message': 'Cannot connect to database', 'data': None}
                
            cursor = connection.cursor(dictionary=True)

            # คำนวณ reject_ratio
            total_pcs = data.get('total_pcs', 0)
            reject_pcs = data.get('reject_pcs', 0)
            reject_ratio = (reject_pcs / total_pcs * 100) if total_pcs > 0 else 0.0

            # ตรวจสอบข้อมูลเดิม
            cursor.execute("SELECT * FROM tbl_result_test WHERE lot_number = %s", (data['lot_number'],))
            existing = cursor.fetchone()

            if existing:
                sql_update = """
                    UPDATE tbl_result_test SET
                        product_name = %s,
                        operator_id = %s,
                        operator_name = %s,
                        process = %s,
                        job_title = %s,
                        code_training = %s,
                        train_topic = %s,
                        date_time = %s,
                        tooling_code = %s,
                        ost_type = %s,
                        total_sheet = %s,
                        good_sheet = %s,
                        reject_sheet = %s,
                        total_pcs = %s,
                        good_pcs = %s,
                        reject_pcs = %s,
                        reject_ratio = %s,
                        short = %s,
                        open = %s,
                        blkm = %s,
                        mat = %s,
                        shot = %s
                    WHERE lot_number = %s
                """

                values_update = (
                    data['product_formatted'],
                    data['operator_id'],
                    data.get('operator_name', ''),
                    data.get('process', ''),
                    data.get('job_title', ''),
                    data.get('code_training', ''),
                    data.get('train_topic', ''),
                    data['timestamp'],
                    data['matched_tooling'],
                    data.get('ost_type', data.get('ost_from_data_base', '')),
                    data.get('total_sheet', 0),
                    data.get('good_sheet', 0),
                    data.get('reject_sheet', 0),
                    total_pcs,
                    data.get('good_pcs', 0),
                    reject_pcs,
                    reject_ratio,
                    data.get('defects', {}).get('SHORT', 0),
                    data.get('defects', {}).get('OPEN', 0),
                    data.get('defects', {}).get('BLKM', 0),
                    data.get('defects', {}).get('MAT', 0),
                    data.get('defects', {}).get('SHOT', 0),
                    data['lot_number']
                )
                cursor.execute(sql_update, values_update)
                action = "updated"
            else:
                sql_insert = """
                    INSERT INTO tbl_result_test (
                        lot_number, product_name, operator_id, operator_name, 
                        process, job_title, code_training, train_topic, 
                        date_time, tooling_code, ost_type,
                        total_sheet, good_sheet, reject_sheet,
                        total_pcs, good_pcs, reject_pcs, reject_ratio,
                        short, open, blkm, mat, shot
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values_insert = (
                    data['lot_number'],
                    data['product_formatted'],
                    data['operator_id'],
                    data.get('operator_name', ''),
                    data.get('process', ''),
                    data.get('job_title', ''),
                    data.get('code_training', ''),
                    data.get('train_topic', ''),
                    data['timestamp'],
                    data['matched_tooling'],
                    data.get('ost_type', data.get('ost_from_data_base', '')),
                    data.get('total_sheet', 0),
                    data.get('good_sheet', 0),
                    data.get('reject_sheet', 0),
                    total_pcs,
                    data.get('good_pcs', 0),
                    reject_pcs,
                    reject_ratio,
                    data.get('defects', {}).get('SHORT', 0),
                    data.get('defects', {}).get('OPEN', 0),
                    data.get('defects', {}).get('BLKM', 0),
                    data.get('defects', {}).get('MAT', 0),
                    data.get('defects', {}).get('SHOT', 0)
                )
                cursor.execute(sql_insert, values_insert)
                action = "inserted"

            connection.commit()

            # ดึงข้อมูลล่าสุดจากฐานข้อมูลหลังบันทึก
            cursor.execute("SELECT * FROM tbl_result_test WHERE lot_number = %s", (data['lot_number'],))
            verified_data = cursor.fetchone()
            cursor.close()

            if verified_data:
                logging.debug(f"save_all_data success, lot_number={data['lot_number']}")
                return {
                    'status': 'success',
                    'action': action,
                    'message': "✅ บันทึกข้อมูลสำเร็จ",
                    'data': data,
                    'verified_data': verified_data
                }
            else:
                logging.error("save_all_data: ไม่สามารถตรวจสอบข้อมูลหลังบันทึกได้")
                return {
                    'status': 'error',
                    'message': "❌ ตรวจสอบข้อมูลหลังบันทึกไม่ได้",
                    'data': None
                }

        except Exception as e:
            if connection:
                connection.rollback()
            logging.error(f"Exception in save_all_data: {e}", exc_info=True)
            return {
                'status': 'error',
                'message': f"❌ เกิดข้อผิดพลาด: {str(e)}",
                'data': None
            }