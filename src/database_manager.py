"""
Database Manager
=================
จัดการการเชื่อมต่อ database แบบแยกส่วน:
- Read Database: ดึงข้อมูลจาก remote server (10.17.86.154) - tooling_fix
- Write Database: บันทึกข้อมูลไปยัง local server (localhost) - tooling_fix
- Read Database Staff: ดึงข้อมูล Staff จาก remote server (10.17.86.154) - design

Author: System
Date: 2025-12-08
"""

import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any
import threading
from src.config_manager import config_manager


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
        print("🔄 Reloading database configurations...")
        
        # ปิด connections เดิมก่อน
        self.close_all_connections()
        
        # โหลด config ใหม่
        self._load_configurations()
        
        print("✅ Database configurations reloaded")
    
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
                print("✅ Database configurations loaded successfully")
                print(f"   📖 Read DB: {self._read_config['host']}/{self._read_config['database']}")
                print(f"   📝 Write DB: {self._write_config['host']}/{self._write_config['database']}")
                print(f"   👥 Staff DB: {self._staff_config['host']}/{self._staff_config['database']}")
            
        except Exception as e:
            if not silent:
                print(f"❌ Error loading database configurations: {e}")
    
    def get_read_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        รับการเชื่อมต่อสำหรับอ่านข้อมูล
        
        Returns:
            mysql.connector.MySQLConnection: การเชื่อมต่อ database หรือ None ถ้าเชื่อมต่อไม่สำเร็จ
        """
        try:
            # ตรวจสอบว่าการเชื่อมต่อยังใช้งานได้อยู่หรือไม่
            if self._read_connection and self._read_connection.is_connected():
                return self._read_connection
            
            # สร้างการเชื่อมต่อใหม่
            print(f"🔌 Connecting to READ database: {self._read_config['host']}")
            self._read_connection = mysql.connector.connect(**self._read_config)
            
            if self._read_connection.is_connected():
                print(f"✅ Connected to READ database: {self._read_config['database']}")
                return self._read_connection
            
        except Error as e:
            print(f"❌ Error connecting to READ database: {e}")
            self._read_connection = None
        
        return None
    
    def get_write_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        รับการเชื่อมต่อสำหรับเขียนข้อมูล
        
        Returns:
            mysql.connector.MySQLConnection: การเชื่อมต่อ database หรือ None ถ้าเชื่อมต่อไม่สำเร็จ
        """
        try:
            # ตรวจสอบว่าการเชื่อมต่อยังใช้งานได้อยู่หรือไม่
            if self._write_connection and self._write_connection.is_connected():
                return self._write_connection
            
            # สร้างการเชื่อมต่อใหม่
            print(f"🔌 Connecting to WRITE database: {self._write_config['host']}")
            self._write_connection = mysql.connector.connect(**self._write_config)
            
            if self._write_connection.is_connected():
                print(f"✅ Connected to WRITE database: {self._write_config['database']}")
                return self._write_connection
            
        except Error as e:
            print(f"❌ Error connecting to WRITE database: {e}")
            self._write_connection = None
        
        return None
    
    def get_staff_connection(self) -> Optional[mysql.connector.MySQLConnection]:
        """
        รับการเชื่อมต่อสำหรับอ่านข้อมูล Staff
        
        Returns:
            mysql.connector.MySQLConnection: การเชื่อมต่อ database หรือ None ถ้าเชื่อมต่อไม่สำเร็จ
        """
        try:
            # ตรวจสอบว่าการเชื่อมต่อยังใช้งานได้อยู่หรือไม่
            if self._staff_connection and self._staff_connection.is_connected():
                return self._staff_connection
            
            # สร้างการเชื่อมต่อใหม่
            print(f"🔌 Connecting to STAFF database: {self._staff_config['host']}")
            self._staff_connection = mysql.connector.connect(**self._staff_config)
            
            if self._staff_connection.is_connected():
                print(f"✅ Connected to STAFF database: {self._staff_config['database']}")
                return self._staff_connection
            
        except Error as e:
            print(f"❌ Error connecting to STAFF database: {e}")
            self._staff_connection = None
        
        return None
    
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
                print("❌ No READ database connection available")
                return None
            
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            
            return results
            
        except Error as e:
            print(f"❌ Error executing READ query: {e}")
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
        try:
            connection = self.get_write_connection()
            if not connection:
                print("❌ No WRITE database connection available")
                return False
            
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if commit:
                connection.commit()
            
            cursor.close()
            print(f"✅ Write query executed successfully")
            return True
            
        except Error as e:
            print(f"❌ Error executing WRITE query: {e}")
            if connection:
                connection.rollback()
            return False
    
    def close_read_connection(self):
        """ปิดการเชื่อมต่อ read database"""
        try:
            if self._read_connection and self._read_connection.is_connected():
                self._read_connection.close()
                print("✅ READ database connection closed")
        except Error as e:
            print(f"❌ Error closing READ connection: {e}")
        finally:
            self._read_connection = None
    
    def close_write_connection(self):
        """ปิดการเชื่อมต่อ write database"""
        try:
            if self._write_connection and self._write_connection.is_connected():
                self._write_connection.close()
                print("✅ WRITE database connection closed")
        except Error as e:
            print(f"❌ Error closing WRITE connection: {e}")
        finally:
            self._write_connection = None
    
    def close_staff_connection(self):
        """ปิดการเชื่อมต่อ staff database"""
        try:
            if self._staff_connection and self._staff_connection.is_connected():
                self._staff_connection.close()
                print("✅ STAFF database connection closed")
        except Error as e:
            print(f"❌ Error closing STAFF connection: {e}")
        finally:
            self._staff_connection = None
    
    def close_all_connections(self):
        """ปิดการเชื่อมต่อ database ทั้งหมด"""
        print("🔌 Closing all database connections...")
        self.close_read_connection()
        self.close_write_connection()
        self.close_staff_connection()
        print("✅ All database connections closed")
    
    def test_connections(self) -> Dict[str, bool]:
        """
        ทดสอบการเชื่อมต่อทั้ง 3 databases
        
        Returns:
            dict: สถานะการเชื่อมต่อ {'read': bool, 'write': bool, 'staff': bool}
        """
        results = {
            'read': False,
            'write': False,
            'staff': False
        }
        
        # ทดสอบ read connection
        read_conn = self.get_read_connection()
        if read_conn and read_conn.is_connected():
            results['read'] = True
            print("✅ READ database connection: OK")
        else:
            print("❌ READ database connection: FAILED")
        
        # ทดสอบ write connection
        write_conn = self.get_write_connection()
        if write_conn and write_conn.is_connected():
            results['write'] = True
            print("✅ WRITE database connection: OK")
        else:
            print("❌ WRITE database connection: FAILED")
        
        # ทดสอบ staff connection
        staff_conn = self.get_staff_connection()
        if staff_conn and staff_conn.is_connected():
            results['staff'] = True
            print("✅ STAFF database connection: OK")
        else:
            print("❌ STAFF database connection: FAILED")
        
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
