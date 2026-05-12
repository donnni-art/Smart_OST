"""
config_manager.py
=================
อ่านและจัดการ config.json สำหรับการตั้งค่าทั้งหมดของแอปพลิเคชัน

หน้าที่หลัก:
  - โหลด config.json จาก root directory (รองรับทั้ง script และ compiled executable)
  - ให้ getter แยกตาม section: PLC, TCP, database, paths, UI
  - fallback ไปยัง default config เมื่อไฟล์ไม่มีหรือ parse ผิดพลาด
  - แปลง relative path เป็น absolute path ด้วย get_full_path()

การใช้งาน:
  - import Singleton: from src.config_manager import config_manager
  - เรียก:
      config_manager.get_plc_config()     → dict
      config_manager.get_tcp_config()     → dict
      config_manager.get_db_config()      → dict
      config_manager.get_paths_config()   → dict
      config_manager.get_ui_config()      → dict
      config_manager.get_full_path(rel)   → Path

ความสัมพันธ์กับโมดูลอื่น:
  - ไม่ import จาก src/ เพื่อหลีกเลี่ยง circular import
  - ถูก import โดยทุก module ที่ต้องการ config (PLCdata, database_manager, ฯลฯ)
"""

import json
import os
import logging
import sys
from pathlib import Path
class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.logger = logging.getLogger(__name__)
        self.config_file = self.get_config_path()
        self.current_config = self.load_default_config()
        self.load_config()
        
        self._initialized = True
        
    #################################################################################   
    def get_config_path(self):
        """Get config file path based on execution environment หาที่อยู่ (Path) ของไฟล์ """
        '''Project_Root/           <-- (2) ถอยครั้งที่ 2 (base_path คือตรงนี้)
                ├── config.json         <-- ไฟล์ config อยู่ตรงนี้
                └── src/                <-- (1) ถอยครั้งที่ 1
                    └── utils/
                        └── this_file.py  <-- ไฟล์ปัจจุบันที่มีโค้ดนี้ (__file__)'''
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = Path(sys.executable).parent
        else:
            # Running as script
            base_path = Path(__file__).parent.parent
        
        return base_path / "config.json"

    #################################################################################
    
    def load_default_config(self):
        """Load default configuration"""
        return {
            "mock_mode": False,
            "plc": {
                "connection_mode": "serial",
                "port": "COM4",
                "baudrate": 9600,
                "bytesize": 8,
                "parity": "E",
                "stopbits": 1,
                "timeout": 0.3,
                "auto_reconnect": True,
                "reconnect_interval": 5
            },
            "tcp": {
                "pi_ip": "192.168.1.10",
                "pi_port": 9999,
                "reconnect_interval": 5
            },
            "read_database": {
                "host": "10.17.86.154",
                "user": "root",
                "password": "",
                "database": "tooling_fix",
                "connect_timeout": 5
            },
            "write_database": {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "tooling_fix",
                "connect_timeout": 5
            },
            "read_database_staff": {
                "host": "10.17.86.154",
                "user": "root",
                "password": "",
                "database": "design",
                "connect_timeout": 5
            },
            "check_lot_database": {
                "host": "10.17.86.154",
                "port": 1521,
                "user": "fpc_user",
                "password": "",
                "service_name": "ORCL",
                "oracle_client_path": ""
            },
            "database": {
                "host": "10.17.84.186",
                "user": "root",
                "password": "",
                "database": "tooling_fix",
                "connect_timeout": 5
            },
            "paths": {
                "shot_counts": "shot_counts",
                "defect_data": "defect_raw_data",
                "pm_folder": "PM",
                "pm_complete": "PM/PM compleat",
                "pm_in_progress": "PM/PM in Progress",
                "templates": "templat",
                "logs": "logs",
                "generated_files": "generated-files"
            },
            "ui": {
                "theme": "LightBlue",
                "font_size": 12,
                "language": "th"
            },
            "application": {
                "auto_save_interval": 30,
                "max_log_files": 10,
                "enable_debug": False
            },
            "user_preferences": {
                "last_selected_directory": ""
        }
        }
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.current_config = self.merge_configs(self.current_config, loaded_config)
                self.logger.info(f"✅ Configuration loaded from {self.config_file}")
            else:
                self.create_default_config()
                
        except Exception as e:
            self.logger.error(f"❌ Error loading config: {e}")
            self.create_default_config()
    
    def merge_configs(self, default, loaded):
        """Recursively merge configurations"""
        merged = default.copy()
        for key, value in loaded.items():
            if isinstance(value, dict) and key in merged:
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def save_config(self, config_data=None):
        """Save configuration to file"""
        try:
            if config_data:
                self.current_config = self.merge_configs(self.current_config, config_data)
            
            # Create directories if they don't exist
            self.create_directories()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_config, f, indent=4, ensure_ascii=False)
            
            self.logger.info("✅ Configuration saved successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving config: {e}")
            return False
    
    def create_default_config(self):
        """Create default configuration file"""
        try:
            self.create_directories()
            self.save_config()
            self.logger.info("✅ Default configuration created")
        except Exception as e:
            self.logger.error(f"❌ Error creating default config: {e}")
    
    def create_directories(self):
        """Create all necessary directories"""
        paths_config = self.current_config['paths']
        
        for key, path in paths_config.items():
            full_path = Path(path)
            if not full_path.is_absolute():
                full_path = self.config_file.parent / path
            
            if not os.path.exists(full_path):
                os.makedirs(full_path, exist_ok=True)
                self.logger.info(f"📁 Created directory: {full_path}")
    
    def get_plc_config(self):
        return self.current_config.get('plc', {})

    def get_tcp_config(self):
        return self.current_config.get('tcp', {})
    
    def get_database_config(self):
        return self.current_config.get('database', {})
    
    def get_paths_config(self):
        return self.current_config.get('paths', {})
    
    def get_ui_config(self):
        return self.current_config.get('ui', {})
    
    def get_application_config(self):
        return self.current_config.get('application', {})
    
    def get_full_path(self, relative_path):
        """Convert relative path to absolute path"""
        if Path(relative_path).is_absolute():
            return relative_path
        return self.config_file.parent / relative_path
    
    def get_last_selected_directory(self):
        """ดึงโฟลเดอร์ล่าสุดที่ผู้ใช้เลือก"""
        return self.current_config.get('user_preferences', {}).get('last_selected_directory', '')

    def set_last_selected_directory(self, directory):
        """บันทึกโฟลเดอร์ล่าสุดที่ผู้ใช้เลือก"""
        if 'user_preferences' not in self.current_config:
            self.current_config['user_preferences'] = {}
        self.current_config['user_preferences']['last_selected_directory'] = directory
        self.save_config()

    def get_login_mode(self):
        """ดึงโหมดการเข้าสู่ระบบล่าสุด (mass/fa)"""
        return self.current_config.get('user_preferences', {}).get('login_mode', 'mass')

    def set_login_mode(self, mode):
        """บันทึกโหมดการเข้าสู่ระบบ (mass/fa)"""
        if 'user_preferences' not in self.current_config:
            self.current_config['user_preferences'] = {}
        self.current_config['user_preferences']['login_mode'] = mode
        self.save_config()

# Singleton instance
config_manager = ConfigManager()