"""
database_manager.py
===================
จัดการการเชื่อมต่อ MySQL แบบ Singleton พร้อม retry logic

หน้าที่หลัก:
  - Read connection  : remote server (10.17.86.154) — ดึงข้อมูล product/tooling
  - Write connection : local server (localhost) — บันทึกผลการผลิต
  - Staff connection : remote server (10.17.86.154) — ข้อมูล staff/permission
  - retry ทุก connection สูงสุด 3 ครั้ง + exponential backoff (1s → 2s → 4s)

การใช้งาน:
  - import Singleton: from src.database_manager import database_manager
  - เรียก:
      conn = database_manager.get_read_connection()
      conn = database_manager.get_write_connection()
      conn = database_manager.get_staff_connection()

ความสัมพันธ์กับโมดูลอื่น:
  - config_manager : อ่าน host/port/credentials จาก config.json
  - app_logger     : log connection attempt, retry, failure
  - DataUploader, LoginManager : ใช้ connection จาก module นี้
"""

import time
import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any
import threading
from src.config_manager import config_manager
from src.app_logger import get_logger

log = get_logger("db")

_MAX_RETRIES = 3
_RETRY_DELAY = 1.0  # seconds, doubles each attempt


class DatabaseManager:
    """
    จัดการการเชื่อมต่อ database แบบแยกส่วน
    
    Attributes:
        _read_connection: การเชื่อมต่อสำหรับอ่านข้อมูล (tooling_fix)
        _write_connection: การเชื่อมต่อสำหรับเขียนข้อมูล (tooling_fix)
        _staff_connection: การเชื่อมต่อสำหรับอ่านข้อมูล Staff (design)
        _lock: Thread lock สำหรับ thread-safe operations
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern เพื่อให้มี instance เดียวในระบบ"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize database manager"""
        if not hasattr(self, '_initialized'):
            self._read_connection: Optional[mysql.connector.MySQLConnection] = None
            self._write_connection: Optional[mysql.connector.MySQLConnection] = None
            self._staff_connection: Optional[mysql.connector.MySQLConnection] = None
            self._read_config: Dict[str, Any] = {}
            self._write_config: Dict[str, Any] = {}
            self._staff_config: Dict[str, Any] = {}
            self._initialized = True
            self._load_configurations()
    
    def reload_configurations(self):
        """
        โหลด configuration ใหม่จาก config.json และปิด connections เดิม
        ใช้เมื่อมีการเปลี่ยนแปลง database settings
        """
        log.info("Reloading database configurations")
        self.close_all_connections()
        self._load_configurations()
        log.info("Database configurations reloaded")
    
    def _load_configurations(self, silent: bool = False):
        """
        โหลด configuration จาก config.json
        
        Args:
            silent: ถ้าเป็น True จะไม่แสดง print messages
        """
        try:
            # โหลด config ใหม่จาก file
            config_manager.load_config()
            
            # โหลด read database config
            read_db = config_manager.current_config.get('read_database', {})
            self._read_config = {
                'host': read_db.get('host', '10.17.86.154'),
                'user': read_db.get('user', 'root'),
                'password': read_db.get('password', ''),
                'database': read_db.get('database', 'tooling_fix'),
                'connect_timeout': read_db.get('connect_timeout', 5),
            }
            
            # โหลด write database config
            write_db = config_manager.current_config.get('write_database', {})
            self._write_config = {
                'host': write_db.get('host', 'localhost'),
                'user': write_db.get('user', 'root'),
                'password': write_db.get('password', ''),
                'database': write_db.get('database', 'tooling_fix'),
                'connect_timeout': write_db.get('connect_timeout', 5),
            }
            
            # โหลด staff database config
            staff_db = config_manager.current_config.get('read_database_staff', {})
            self._staff_config = {
                'host': staff_db.get('host', '10.17.86.154'),
                'user': staff_db.get('user', 'root'),
                'password': staff_db.get('password', ''),
                'database': staff_db.get('database', 'design'),
                'connect_timeout': staff_db.get('connect_timeout', 5),
            }
            
            if not silent:
                log.info(
                    "DB configs — read: %s/%s  write: %s/%s  staff: %s/%s",
                    self._read_config['host'], self._read_config['database'],
                    self._write_config['host'], self._write_config['database'],
                    self._staff_config['host'], self._staff_config['database'],
                )
            
        except Exception as e:
            if not silent:
                log.error(f"Error loading database configurations: {e}")
    
    def _connect_with_retry(
        self,
        config: Dict[str, Any],
        label: str,
    ) -> Optional[mysql.connector.MySQLConnection]:
        """เชื่อมต่อ database พร้อม exponential-backoff retry"""
        delay = _RETRY_DELAY
        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                conn = mysql.connector.connect(**config)
                if conn.is_connected():
                    log.info("Connected to %s database: %s", label, config['database'])
                    return conn
            except Error as e:
                log.warning(
                    "%s connection attempt %d/%d failed: %s",
                    label, attempt, _MAX_RETRIES, e,
                )
                if attempt < _MAX_RETRIES:
                    time.sleep(delay)
                    delay *= 2
                else:
                    log.error("%s database unavailable after %d attempts", label, _MAX_RETRIES)
        return None

    def _is_mock_mode(self) -> bool:
        return bool(config_manager.current_config.get('mock_mode', False))

    def get_read_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """รับการเชื่อมต่อสำหรับอ่านข้อมูล"""
        if self._is_mock_mode():
            from src.mock_database import get_mock_read_connection
            log.info("MOCK: returning mock READ connection")
            return get_mock_read_connection()
        if self._read_connection and self._read_connection.is_connected():
            return self._read_connection
        log.info("Connecting to READ database: %s", self._read_config['host'])
        self._read_connection = self._connect_with_retry(self._read_config, "READ")
        return self._read_connection

    def get_write_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """รับการเชื่อมต่อสำหรับเขียนข้อมูล"""
        if self._is_mock_mode():
            from src.mock_database import get_mock_write_connection
            log.info("MOCK: returning mock WRITE connection")
            return get_mock_write_connection()
        if self._write_connection and self._write_connection.is_connected():
            return self._write_connection
        log.info("Connecting to WRITE database: %s", self._write_config['host'])
        self._write_connection = self._connect_with_retry(self._write_config, "WRITE")
        return self._write_connection

    def get_staff_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """รับการเชื่อมต่อสำหรับอ่านข้อมูล Staff"""
        if self._is_mock_mode():
            from src.mock_database import get_mock_staff_connection
            log.info("MOCK: returning mock STAFF connection")
            return get_mock_staff_connection()
        if self._staff_connection and self._staff_connection.is_connected():
            return self._staff_connection
        log.info("Connecting to STAFF database: %s", self._staff_config['host'])
        self._staff_connection = self._connect_with_retry(self._staff_config, "STAFF")
        return self._staff_connection
    
    def execute_read_query(self, query: str, params: tuple = None) -> Optional[list]:
        """
        ดำเนินการ SELECT query บน read database
        
        Args:
            query: SQL query string
            params: Parameters สำหรับ query (optional)
            
        Returns:
            list: ผลลัพธ์จาก query หรือ None ถ้าเกิดข้อผิดพลาด
        """
        try:
            connection = self.get_read_connection()
            if not connection:
                log.error("No READ database connection available")
                return None

            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()

            return results

        except Error as e:
            log.error("Error executing READ query: %s", e)
            return None

    def execute_write_query(self, query: str, params: tuple = None, commit: bool = True) -> bool:
        """
        ดำเนินการ INSERT/UPDATE/DELETE query บน write database

        Args:
            query: SQL query string
            params: Parameters สำหรับ query (optional)
            commit: ทำการ commit หรือไม่ (default: True)

        Returns:
            bool: True ถ้าสำเร็จ, False ถ้าเกิดข้อผิดพลาด
        """
        connection = None
        try:
            connection = self.get_write_connection()
            if not connection:
                log.error("No WRITE database connection available")
                return False

            cursor = connection.cursor()
            cursor.execute(query, params or ())

            if commit:
                connection.commit()

            cursor.close()
            log.debug("Write query executed successfully")
            return True

        except Error as e:
            log.error("Error executing WRITE query: %s", e)
            if connection:
                connection.rollback()
            return False
    
    def close_read_connection(self):
        """ปิดการเชื่อมต่อ read database"""
        try:
            if self._read_connection and self._read_connection.is_connected():
                self._read_connection.close()
                log.info("READ database connection closed")
        except Error as e:
            log.error("Error closing READ connection: %s", e)
        finally:
            self._read_connection = None

    def close_write_connection(self):
        """ปิดการเชื่อมต่อ write database"""
        try:
            if self._write_connection and self._write_connection.is_connected():
                self._write_connection.close()
                log.info("WRITE database connection closed")
        except Error as e:
            log.error("Error closing WRITE connection: %s", e)
        finally:
            self._write_connection = None

    def close_staff_connection(self):
        """ปิดการเชื่อมต่อ staff database"""
        try:
            if self._staff_connection and self._staff_connection.is_connected():
                self._staff_connection.close()
                log.info("STAFF database connection closed")
        except Error as e:
            log.error("Error closing STAFF connection: %s", e)
        finally:
            self._staff_connection = None

    def close_all_connections(self):
        """ปิดการเชื่อมต่อ database ทั้งหมด"""
        log.info("Closing all database connections")
        self.close_read_connection()
        self.close_write_connection()
        self.close_staff_connection()
        log.info("All database connections closed")

    def test_connections(self) -> Dict[str, bool]:
        """
        ทดสอบการเชื่อมต่อทั้ง 3 databases

        Returns:
            dict: สถานะการเชื่อมต่อ {'read': bool, 'write': bool, 'staff': bool}
        """
        results = {'read': False, 'write': False, 'staff': False}

        for name, getter in (
            ('read', self.get_read_connection),
            ('write', self.get_write_connection),
            ('staff', self.get_staff_connection),
        ):
            conn = getter()
            ok = bool(conn and conn.is_connected())
            results[name] = ok
            level = log.info if ok else log.error
            level("%s database connection: %s", name.upper(), "OK" if ok else "FAILED")
        
        return results


# สร้าง singleton instance
database_manager = DatabaseManager()


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    print("=" * 60)
    print("Database Manager - Connection Test")
    print("=" * 60)
    
    # ทดสอบการเชื่อมต่อ
    db_manager = DatabaseManager()
    test_results = db_manager.test_connections()
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print(f"  READ Database:  {'✅ Connected' if test_results['read'] else '❌ Failed'}")
    print(f"  WRITE Database: {'✅ Connected' if test_results['write'] else '❌ Failed'}")
    print(f"  STAFF Database: {'✅ Connected' if test_results['staff'] else '❌ Failed'}")
    print("=" * 60)
    
    # ปิดการเชื่อมต่อ
    db_manager.close_all_connections()
