"""
Lot Checker Module - ตรวจสอบ Lot Number ก่อน Login

This module checks if a Lot Number has been scanned into the system
by querying a separate "Big Data" database.

Supports two input formats:
1. Plain Lot Number: "LOT123456"
2. POS Scan Format: "LOT123456;WO12345;ABPRODUCT123"

Usage:
    from src.lot_checker import LotChecker
    
    checker = LotChecker()
    result = checker.check_lot("LOT123456")
    # or
    result = checker.check_lot("LOT123456;WO12345;ABPRODUCT123")
    
    if result['status'] == 'VALID':
        # Lot is valid, data is in result['data']
        pass
    elif result['status'] == 'NOT_FOUND':
        # Lot not found in system
        pass
    elif result['status'] == 'INVALID':
        # Lot found but validation failed
        pass
"""

import re
import oracledb
from src.config_manager import config_manager
from src.app_logger import get_logger

log = get_logger("lot_checker")


class LotChecker:
    """
    Class to check Lot Number against Big Data database (Oracle).
    
    Configuration is read from config.json under 'check_lot_database' key.
    """
    
    def __init__(self):
        self.connection = None
        self.config = self._load_config()
        self.parsed_data = {}
        # init Oracle client เฉพาะเมื่อไม่ได้อยู่ใน mock mode และมี path กำหนดไว้
        if not config_manager.current_config.get('mock_mode', False):
            oracle_path = self.config.get('oracle_client_path', '')
            if oracle_path:
                try:
                    oracledb.init_oracle_client(lib_dir=oracle_path)
                except Exception as e:
                    log.warning("Oracle client init skipped: %s", e)
        
    def _load_config(self) -> dict:
        """Load database configuration from config.json"""
        try:
            full_config = config_manager.current_config
            db_config = full_config.get('check_lot_database', {})
            
            if not db_config:
                log.warning("LotChecker: 'check_lot_database' not found in config.json")
                return {}
            
            # Oracle default port is 1521
            service_name = db_config.get('service_name') or db_config.get('database') or 'ORCL'
            
            return {
                'host': db_config.get('host', 'localhost'),
                'port': db_config.get('port', 1521),
                'user': db_config.get('user', 'system'),
                'password': db_config.get('password', ''),
                'service_name': service_name,
            }
        except Exception as e:
            log.error("LotChecker: Error loading config: %s", e)
            return {}
    
    def parse_scanned_input(self, scanned_input: str) -> dict:
        """
        Parse scanned input - supports both plain Lot Number and POS format.
        
        Formats:
        1. Plain Lot Number: "LOT123456"
        2. POS Format: "LOT_NUMBER;WO_NUMBER;PRODUCT_CODE"
           Example: "AA1234567890;WO12345;ABCAW076W1A"
        
        Args:
            scanned_input: Raw scanned string
            
        Returns:
            dict: {
                'lot_number': str,
                'wo_number': str | None,
                'product_code': str | None,
                'product_formatted': str | None,
                'is_pos_format': bool
            }
        """
        if not scanned_input or not scanned_input.strip():
            return {
                'lot_number': '',
                'wo_number': None,
                'product_code': None,
                'product_formatted': None,
                'is_pos_format': False
            }
        
        scanned_input = scanned_input.strip()
        
        # Check if POS format (contains semicolon)
        if ";" in scanned_input:
            parts = scanned_input.split(";")
            
            if len(parts) >= 3:
                lot_number = parts[0].strip()
                wo_number = parts[1].strip()
                product_raw = parts[2].strip()
                
                # Extract product code (skip first 2 characters like in login_scan.py)
                product_code = product_raw[2:] if len(product_raw) >= 2 else product_raw
                product_formatted = self._format_product_code(product_code)
                
                self.parsed_data = {
                    'lot_number': lot_number,
                    'wo_number': wo_number,
                    'product_code': product_code,
                    'product_formatted': product_formatted,
                    'is_pos_format': True
                }
                
                log.debug("Parsed POS format: Lot=%s, WO=%s, Product=%s", lot_number, wo_number, product_formatted)
                return self.parsed_data
            else:
                # Incomplete POS format, use first part as lot number
                lot_number = parts[0].strip()
                log.warning("Incomplete POS format, using first part as Lot: %s", lot_number)
                
                self.parsed_data = {
                    'lot_number': lot_number,
                    'wo_number': parts[1].strip() if len(parts) > 1 else None,
                    'product_code': None,
                    'product_formatted': None,
                    'is_pos_format': True
                }
                return self.parsed_data
        else:
            # Plain lot number
            self.parsed_data = {
                'lot_number': scanned_input,
                'wo_number': None,
                'product_code': None,
                'product_formatted': None,
                'is_pos_format': False
            }
            log.debug("Parsed plain Lot Number: %s", scanned_input)
            return self.parsed_data
    
    def _format_product_code(self, product_code: str) -> str:
        """
        Format product code to standard format.
        Same logic as login_scan.py format_product_code()
        
        Example: "CAW076W1A" -> "CAW-076W-1A"
        """
        if not product_code:
            return product_code
            
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
    
    def connect(self) -> bool:
        """
        Establish connection to the Big Data database (Oracle).
        
        Attempts to connect using Service Name first, then falls back to SID
        if ORA-12514 (Listener does not know of service requested) occurs.
        
        Returns:
            bool: True if connected successfully, False otherwise
        """
        try:
            if not self.config:
                log.error("LotChecker: No configuration available")
                return False
            
            # Clean config values
            host = str(self.config['host']).strip()
            port = str(self.config['port']).strip()
            user = str(self.config['user']).strip()
            password = str(self.config['password']).strip()
            name = str(self.config['service_name']).strip()
            
            # 1. Try "Easy Connect" format for Service Name: host:port/service_name
            dsn_service = f"{host}:{port}/{name}"
            log.info("LotChecker: Connecting to %s (Service Name mode)...", dsn_service)

            try:
                self.connection = oracledb.connect(user=user, password=password, dsn=dsn_service)
                log.info("LotChecker: Connected!")
                return True
            except oracledb.Error as e:
                # If Service Name fails, try SID format: host:port:sid
                # Note: 'DPY-6001' is 'ORA-12514' (Service missing)
                #       'DPY-6005' can be generic connection failure but often implies name resolution
                log.warning("Service Name connection failed (%s). Retrying as SID...", e)
                
                dsn_sid = oracledb.makedsn(host, port, sid=name)
                log.info("LotChecker: Connecting to %s:%s:%s (SID mode)...", host, port, name)
                
                try:
                    self.connection = oracledb.connect(user=user, password=password, dsn=dsn_sid)
                    log.info("LotChecker: Connected via SID!")
                    return True
                except oracledb.Error as e_sid:
                    # Report the original error if SID also fails, or just the last one
                    log.error("LotChecker: SID connection also failed - %s", e_sid)
                    if "DPY-6001" in str(e) or "ORA-12514" in str(e):
                        log.warning("LotChecker: The database name seems incorrect. Please check 'service_name' in config.json")

            self.connection = None
            
        except Exception as e:
            log.error("LotChecker: Unexpected error during connect - %s", e)
            self.connection = None
            
        return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                log.info("LotChecker: Disconnected")
            except oracledb.Error:
                pass
            self.connection = None
    
    def check_lot(self, scanned_input: str) -> dict:
        """
        Check if the Lot Number exists and is valid in the Big Data database.
        
        Supports both plain Lot Number and POS scan format.
        
        Args:
            scanned_input: The scanned input (Lot Number or POS format)
            
        Returns:
            dict: result dictionary
        """
        if not scanned_input or not scanned_input.strip():
            return {
                'status': 'ERROR',
                'message': 'Lot Number is empty',
                'data': None,
                'parsed_input': {}
            }
        
        # Parse the scanned input (handles both formats)
        parsed = self.parse_scanned_input(scanned_input.strip())
        lot_number = parsed.get('lot_number', '')
        
        if not lot_number:
            return {
                'status': 'ERROR',
                'message': 'ไม่สามารถแยก Lot Number จากข้อมูลที่ scan ได้',
                'data': None,
                'parsed_input': parsed
            }
        
        # ─── mock mode ────────────────────────────────────────────────
        if config_manager.current_config.get('mock_mode', False):
            from src.mock_database import get_mock_oracle_connection
            log.info("MOCK: LotChecker using mock Oracle data for lot '%s'", lot_number)
            self.connection = get_mock_oracle_connection()

        # Try to connect if not already connected
        elif not self.connection:
            if not self.connect():
                return {
                    'status': 'ERROR',
                    'message': 'Cannot connect to check lot database',
                    'data': None,
                    'parsed_input': parsed
                }

        try:
            cursor = self.connection.cursor()
            
            # Using dictionary cursor equivalent for easier data handling
            # Note: oracledb default cursor returns tuples, we will map columns later
            
            # ========================================================
            # ORACLE QUERY
            # Use :lot_number for bind variable instead of %s
            # ========================================================
            
            query = """
                SELECT
                       fp.PROC_DISP,
                       fttt.TTT_TOOLS_TYPE_NAME,
                       TTL_SCAN_TYPE,
                       TTL_PRD_ITEM_CODE,
                       TTL_LOT_MOS,
                       TTL_PROCESS,
                       TTL_MC_NO,
                       TTL_TOOLS_TYPE,
                       TTL_TOOLS_CODE,
                       TTL_TOOLS_REV,
                       TTL_SCAN_STATION,
                       TTL_SCAN_BY,
                       TTL_SCAN_DATE,
                       TTL_CHANGE_TIME
                FROM FPC.FPCT_TRACE_TOOLS_LOT ft
                INNER JOIN FPC.FPC_PROCESS fp 
                       ON ft.TTL_PROCESS = fp.PROC_ID
                INNER JOIN FPC.FPCT_TRACE_TOOLS_TYPE fttt 
                       ON ft.TTL_TOOLS_TYPE = fttt.TTT_TOOLS_TYPE
                WHERE ft.TTL_LOT_MOS = :lot_number
                    AND ft.TTL_SCAN_STATION LIKE '%10.17.86%'
            """
            
            log.debug("LotChecker: Executing query for Lot %s", lot_number)
            cursor.execute(query, lot_number=lot_number)
            
            # Fetch all rows
            # oracledb returns list of tuples
            rows = cursor.fetchall()
            cursor.close()

            if not rows:
                return {
                    'status': 'NOT_FOUND',
                    'message': f'Lot "{lot_number}" ไม่พบในระบบ หรือไม่ได้ Scan ผ่าน Station ที่กำหนด (10.17.86%)',
                    'data': None,
                    'parsed_input': parsed
                }

            # Get column names to create dictionary rows
            columns = [col[0] for col in cursor.description]
            
            # Convert tuples to dictionary
            results = [dict(zip(columns, row)) for row in rows]

            
            # Process results to extract required information
            processed_data = self._process_lot_results(results, lot_number)
            
            if processed_data['is_valid']:
                # Merge parsed data with processed result
                processed_data['data']['_parsed_input'] = parsed
                return {
                    'status': 'VALID',
                    'message': 'Lot ถูกต้อง สามารถเข้าใช้งานได้',
                    'data': processed_data['data'],
                    'parsed_input': parsed
                }
            else:
                return {
                    'status': 'INVALID',
                    'message': processed_data['message'],
                    'data': None,
                    'parsed_input': parsed
                }
                
        except oracledb.Error as e:
            log.error("LotChecker: Query error - %s", e)
            return {
                'status': 'ERROR',
                'message': f'Database error: {e}',
                'data': None,
                'parsed_input': parsed
            }
    
    def _process_lot_results(self, results: list, lot_number: str) -> dict:
        """
        Process database results to extract Fixture and Operator info.
        
        Logic:
        1. Find row where TTT_TOOLS_TYPE_NAME == 'FIXTURE'
           -> Extract product_name (TTL_PRD_ITEM_CODE), tooling_code (TTL_TOOLS_CODE), ost_type (PROC_DISP)
        2. Find row where TTT_TOOLS_TYPE_NAME == 'OPERATOR' AND same PROC_DISP as Fixture
           -> Extract operator_id (TTL_TOOLS_CODE)
        
        Args:
            results: List of dictionary rows from database
            lot_number: The lot number being checked
            
        Returns:
            dict: {
                'is_valid': bool,
                'message': str,
                'data': dict  # Extracted data
            }
        """
        fixture_row = None
        operator_row = None
        all_operators = []  # เก็บ Operator ทั้งหมดไว้ fallback
        
        # Step 1: Find FIXTURE row first
        for row in results:
            tools_type_name = row.get('TTT_TOOLS_TYPE_NAME', '').upper()
            if tools_type_name == 'FIXTURE':
                fixture_row = row
                break  # ใช้ Fixture แรกที่เจอ
        
        # Validation: Must have Fixture scan
        if not fixture_row:
            return {
                'is_valid': False,
                'message': 'ไม่พบข้อมูลการ Scan Fixture (TTT_TOOLS_TYPE_NAME = FIXTURE)',
                'data': None
            }
        
        # Get the Process of the Fixture (e.g., FOST, FOST2)
        fixture_process = fixture_row.get('PROC_DISP', '').upper()
        log.debug("LotChecker: Fixture found at Process: %s", fixture_process)
        
        # Step 2: Find OPERATOR row that matches the same PROC_DISP as Fixture
        for row in results:
            tools_type_name = row.get('TTT_TOOLS_TYPE_NAME', '').upper()
            if tools_type_name == 'OPERATOR':
                all_operators.append(row)
                row_process = row.get('PROC_DISP', '').upper()
                if row_process == fixture_process:
                    operator_row = row
                    log.info("LotChecker: Matched Operator at same Process: %s", row_process)
                    break
        
        # Fallback: If no matching process, use any Operator
        if not operator_row and all_operators:
            operator_row = all_operators[0]
            fallback_process = operator_row.get('PROC_DISP', '')
            log.warning("LotChecker: No Operator at %s, fallback to first Operator at %s", fixture_process, fallback_process)
            
        if not operator_row:
            return {
                'is_valid': False,
                'message': 'ไม่พบข้อมูลการ Scan Operator (TTT_TOOLS_TYPE_NAME = OPERATOR)',
                'data': None
            }
            
        # Extract data
        data = {
            'lot_number': lot_number,
            'product_name': fixture_row.get('TTL_PRD_ITEM_CODE', ''),
            'product_code': fixture_row.get('TTL_PRD_ITEM_CODE', ''), # Alias
            'tooling_code': fixture_row.get('TTL_TOOLS_CODE', ''),
            'ost_type': fixture_row.get('PROC_DISP', ''),  # e.g., FOST2
            'operator_id': operator_row.get('TTL_TOOLS_CODE', ''),
            'scan_date': fixture_row.get('TTL_SCAN_DATE', ''),
            'scan_station': fixture_row.get('TTL_SCAN_STATION', ''),
            # Include raw rows for debugging if needed
            '_raw_fixture': fixture_row,
            '_raw_operator': operator_row
        }
        
        log.info("LotChecker: Processed Data -> Product: %s, Tooling: %s, Operator: %s", data['product_name'], data['tooling_code'], data['operator_id'])
        
        return {
            'is_valid': True,
            'message': 'Success',
            'data': data
        }
    
    def get_lot_info_for_login(self, lot_data: dict) -> dict:
        """
        Extract login-relevant information from processed lot data.
        """
        return {
            'lot_number': lot_data.get('lot_number', ''),
            'product_name': lot_data.get('product_name', ''),
            'product_formatted': self._format_product_code(lot_data.get('product_code', '')),
            'operator_id': lot_data.get('operator_id', ''),
            'operator_name': '', # Validation doesn't provide name, might need secondary lookup or empty
            'tooling_code': lot_data.get('tooling_code', ''),
            'ost_type': lot_data.get('ost_type', ''),
        }


# Singleton instance for easy importing
lot_checker = LotChecker()
