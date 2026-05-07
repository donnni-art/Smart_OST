# [file content begin]
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                              QGroupBox, QLineEdit, QSpinBox, QComboBox, 
                              QPushButton, QFileDialog, QMessageBox, QTabWidget,
                              QLabel, QCheckBox, QWidget)
from PySide6.QtCore import Qt
import serial.tools.list_ports
from src.config_manager import config_manager

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Configuration")
        self.resize(700, 600)
        
        self.setup_ui()
        self.load_config_to_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create tabs
        tab_widget = QTabWidget()
        
        # PLC Settings Tab
        plc_tab = self.create_plc_tab()
        tab_widget.addTab(plc_tab, "PLC Settings")
        
        # Database Settings Tab
        db_tab = self.create_database_tab()
        tab_widget.addTab(db_tab, "Database Settings")
        
        # Paths Settings Tab
        paths_tab = self.create_paths_tab()
        tab_widget.addTab(paths_tab, "Paths Settings")
        
        # UI Settings Tab
        ui_tab = self.create_ui_tab()
        tab_widget.addTab(ui_tab, "UI Settings")
        
        # Application Settings Tab
        app_tab = self.create_application_tab()
        tab_widget.addTab(app_tab, "Application Settings")
        
        # Buttons
        button_layout = QHBoxLayout()
        self.test_plc_btn = QPushButton("TPC.")
        self.test_db_btn = QPushButton("TDC.")
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        # ------------------------
        button_layout.addWidget(self.test_plc_btn)
        button_layout.addWidget(self.test_db_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        # Connect signals
        self.save_btn.clicked.connect(self.save_config)
        self.cancel_btn.clicked.connect(self.reject)
        self.test_plc_btn.clicked.connect(self.test_plc_connection)
        self.test_db_btn.clicked.connect(self.test_database_connection)
        
        # Add to main layout
        layout.addWidget(tab_widget)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_plc_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # COM Port
        self.plc_port = QComboBox()
        self.refresh_com_ports()
        self.refresh_ports_btn = QPushButton("Refresh Ports")
        self.refresh_ports_btn.clicked.connect(self.refresh_com_ports)
        
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.plc_port)
        port_layout.addWidget(self.refresh_ports_btn)
        
        # Other PLC settings
        self.plc_baudrate = QComboBox()
        self.plc_baudrate.addItems(["9600", "19200", "38400", "57600", "115200"])
        
        self.plc_bytesize = QComboBox()
        self.plc_bytesize.addItems(["5", "6", "7", "8"])
        
        self.plc_parity = QComboBox()
        self.plc_parity.addItems(["N", "E", "O", "M", "S"])
        
        self.plc_stopbits = QComboBox()
        self.plc_stopbits.addItems(["1", "1.5", "2"])
        
        self.plc_timeout = QSpinBox()
        self.plc_timeout.setRange(1, 10)
        self.plc_timeout.setSuffix(" seconds")
        
        # Auto-reconnect settings
        self.plc_auto_reconnect = QCheckBox("Enable Auto Reconnect")
        self.plc_reconnect_interval = QSpinBox()
        self.plc_reconnect_interval.setRange(1, 60)
        self.plc_reconnect_interval.setSuffix(" seconds")
        
        layout.addRow("COM Port:", port_layout)
        layout.addRow("Baud Rate:", self.plc_baudrate)
        layout.addRow("Data Bits:", self.plc_bytesize)
        layout.addRow("Parity:", self.plc_parity)
        layout.addRow("Stop Bits:", self.plc_stopbits)
        layout.addRow("Timeout:", self.plc_timeout)
        layout.addRow(self.plc_auto_reconnect)
        layout.addRow("Reconnect Interval:", self.plc_reconnect_interval)
        
        widget.setLayout(layout)
        return widget
    
    def create_database_tab(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        
        # ========== READ DATABASE (tooling_fix) ==========
        read_group = QGroupBox("📖 Read Database (tooling_fix)")
        read_layout = QFormLayout()
        
        self.read_db_host = QLineEdit()
        self.read_db_user = QLineEdit()
        self.read_db_password = QLineEdit()
        self.read_db_password.setEchoMode(QLineEdit.Password)
        self.read_db_name = QLineEdit()
        self.read_db_timeout = QSpinBox()
        self.read_db_timeout.setRange(1, 30)
        self.read_db_timeout.setSuffix(" seconds")
        
        read_layout.addRow("Host:", self.read_db_host)
        read_layout.addRow("Username:", self.read_db_user)
        read_layout.addRow("Password:", self.read_db_password)
        read_layout.addRow("Database:", self.read_db_name)
        read_layout.addRow("Timeout:", self.read_db_timeout)
        
        self.test_read_db_btn = QPushButton("Test Read DB Connection")
        self.test_read_db_btn.clicked.connect(lambda: self.test_specific_database('read'))
        read_layout.addRow(self.test_read_db_btn)
        
        read_group.setLayout(read_layout)
        
        # ========== WRITE DATABASE (tooling_fix) ==========
        write_group = QGroupBox("📝 Write Database (tooling_fix)")
        write_layout = QFormLayout()
        
        self.write_db_host = QLineEdit()
        self.write_db_user = QLineEdit()
        self.write_db_password = QLineEdit()
        self.write_db_password.setEchoMode(QLineEdit.Password)
        self.write_db_name = QLineEdit()
        self.write_db_timeout = QSpinBox()
        self.write_db_timeout.setRange(1, 30)
        self.write_db_timeout.setSuffix(" seconds")
        
        write_layout.addRow("Host:", self.write_db_host)
        write_layout.addRow("Username:", self.write_db_user)
        write_layout.addRow("Password:", self.write_db_password)
        write_layout.addRow("Database:", self.write_db_name)
        write_layout.addRow("Timeout:", self.write_db_timeout)
        
        self.test_write_db_btn = QPushButton("Test Write DB Connection")
        self.test_write_db_btn.clicked.connect(lambda: self.test_specific_database('write'))
        write_layout.addRow(self.test_write_db_btn)
        
        write_group.setLayout(write_layout)
        
        # ========== STAFF DATABASE (design) ==========
        staff_group = QGroupBox("👥 Staff Database (design)")
        staff_layout = QFormLayout()
        
        self.staff_db_host = QLineEdit()
        self.staff_db_user = QLineEdit()
        self.staff_db_password = QLineEdit()
        self.staff_db_password.setEchoMode(QLineEdit.Password)
        self.staff_db_name = QLineEdit()
        self.staff_db_timeout = QSpinBox()
        self.staff_db_timeout.setRange(1, 30)
        self.staff_db_timeout.setSuffix(" seconds")
        
        staff_layout.addRow("Host:", self.staff_db_host)
        staff_layout.addRow("Username:", self.staff_db_user)
        staff_layout.addRow("Password:", self.staff_db_password)
        staff_layout.addRow("Database:", self.staff_db_name)
        staff_layout.addRow("Timeout:", self.staff_db_timeout)
        
        self.test_staff_db_btn = QPushButton("Test Staff DB Connection")
        self.test_staff_db_btn.clicked.connect(lambda: self.test_specific_database('staff'))
        staff_layout.addRow(self.test_staff_db_btn)
        
        staff_group.setLayout(staff_layout)
        
        # Add all groups to main layout
        main_layout.addWidget(read_group)
        main_layout.addWidget(write_group)
        main_layout.addWidget(staff_group)
        main_layout.addStretch()
        
        widget.setLayout(main_layout)
        return widget
    
    def create_paths_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        # Shot counts path
        shot_path_layout = QHBoxLayout()
        self.shot_counts_path = QLineEdit()
        self.shot_browse_btn = QPushButton("Browse...")
        self.shot_browse_btn.clicked.connect(lambda: self.browse_folder(self.shot_counts_path))
        shot_path_layout.addWidget(self.shot_counts_path)
        shot_path_layout.addWidget(self.shot_browse_btn)
        
        # Defect data path
        defect_path_layout = QHBoxLayout()
        self.defect_data_path = QLineEdit()
        self.defect_browse_btn = QPushButton("Browse...")
        self.defect_browse_btn.clicked.connect(lambda: self.browse_folder(self.defect_data_path))
        defect_path_layout.addWidget(self.defect_data_path)
        defect_path_layout.addWidget(self.defect_browse_btn)
        
        # PM folder path
        pm_path_layout = QHBoxLayout()
        self.pm_folder_path = QLineEdit()
        self.pm_browse_btn = QPushButton("Browse...")
        self.pm_browse_btn.clicked.connect(lambda: self.browse_folder(self.pm_folder_path))
        pm_path_layout.addWidget(self.pm_folder_path)
        pm_path_layout.addWidget(self.pm_browse_btn)
        
        # PM Complete path
        pm_complete_layout = QHBoxLayout()
        self.pm_complete_path = QLineEdit()
        self.pm_complete_browse_btn = QPushButton("Browse...")
        self.pm_complete_browse_btn.clicked.connect(lambda: self.browse_folder(self.pm_complete_path))
        pm_complete_layout.addWidget(self.pm_complete_path)
        pm_complete_layout.addWidget(self.pm_complete_browse_btn)
        
        # PM In Progress path
        pm_in_progress_layout = QHBoxLayout()
        self.pm_in_progress_path = QLineEdit()
        self.pm_in_progress_browse_btn = QPushButton("Browse...")
        self.pm_in_progress_browse_btn.clicked.connect(lambda: self.browse_folder(self.pm_in_progress_path))
        pm_in_progress_layout.addWidget(self.pm_in_progress_path)
        pm_in_progress_layout.addWidget(self.pm_in_progress_browse_btn)
        
        # Templates path
        template_path_layout = QHBoxLayout()
        self.templates_path = QLineEdit()
        self.template_browse_btn = QPushButton("Browse...")
        self.template_browse_btn.clicked.connect(lambda: self.browse_folder(self.templates_path))
        template_path_layout.addWidget(self.templates_path)
        template_path_layout.addWidget(self.template_browse_btn)
        
        # Logs path
        logs_path_layout = QHBoxLayout()
        self.logs_path = QLineEdit()
        self.logs_browse_btn = QPushButton("Browse...")
        self.logs_browse_btn.clicked.connect(lambda: self.browse_folder(self.logs_path))
        logs_path_layout.addWidget(self.logs_path)
        logs_path_layout.addWidget(self.logs_browse_btn)
        
        layout.addRow("Shot Counts Folder:", shot_path_layout)
        layout.addRow("Defect Data Folder:", defect_path_layout)
        layout.addRow("PM Folder:", pm_path_layout)
        layout.addRow("PM Complete Folder:", pm_complete_layout)
        layout.addRow("PM In Progress Folder:", pm_in_progress_layout)
        layout.addRow("Templates Folder:", template_path_layout)
        layout.addRow("Logs Folder:", logs_path_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_ui_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        self.ui_theme = QComboBox()
        self.ui_theme.addItems(["LightBlue", "DarkBlue", "Light", "Dark"])
        
        self.ui_font_size = QSpinBox()
        self.ui_font_size.setRange(8, 20)
        
        self.ui_language = QComboBox()
        self.ui_language.addItems(["th", "en"])
        
        layout.addRow("Theme:", self.ui_theme)
        layout.addRow("Font Size:", self.ui_font_size)
        layout.addRow("Language:", self.ui_language)
        
        widget.setLayout(layout)
        return widget
    
    def create_application_tab(self):
        widget = QWidget()
        layout = QFormLayout()
        
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(10, 300)
        self.auto_save_interval.setSuffix(" seconds")
        
        self.max_log_files = QSpinBox()
        self.max_log_files.setRange(5, 50)
        
        self.enable_debug = QCheckBox("Enable Debug Mode")
        
        layout.addRow("Auto Save Interval:", self.auto_save_interval)
        layout.addRow("Max Log Files:", self.max_log_files)
        layout.addRow(self.enable_debug)
        
        widget.setLayout(layout)
        return widget
    
    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit.setText(folder)
    
    def refresh_com_ports(self):
        """Refresh available COM ports"""
        self.plc_port.clear()
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.plc_port.addItems(ports)
    
    def load_config_to_ui(self):
        """Load current configuration to UI elements"""
        config = config_manager.current_config
        
        # PLC Settings
        plc_config = config['plc']
        self.plc_port.setCurrentText(plc_config.get('port', 'COM4'))
        self.plc_baudrate.setCurrentText(str(plc_config.get('baudrate', 9600)))
        self.plc_bytesize.setCurrentText(str(plc_config.get('bytesize', 8)))
        self.plc_parity.setCurrentText(plc_config.get('parity', 'E'))
        self.plc_stopbits.setCurrentText(str(plc_config.get('stopbits', 1)))
        self.plc_timeout.setValue(plc_config.get('timeout', 0.3))
        self.plc_auto_reconnect.setChecked(plc_config.get('auto_reconnect', True))
        self.plc_reconnect_interval.setValue(plc_config.get('reconnect_interval', 5))
        
        # Database Settings - Read Database
        read_db_config = config.get('read_database', {})
        self.read_db_host.setText(read_db_config.get('host', '10.17.86.154'))
        self.read_db_user.setText(read_db_config.get('user', 'root'))
        self.read_db_password.setText(read_db_config.get('password', ''))
        self.read_db_name.setText(read_db_config.get('database', 'tooling_fix'))
        self.read_db_timeout.setValue(read_db_config.get('timeout', 5))
        
        # Database Settings - Write Database
        write_db_config = config.get('write_database', {})
        self.write_db_host.setText(write_db_config.get('host', 'localhost'))
        self.write_db_user.setText(write_db_config.get('user', 'root'))
        self.write_db_password.setText(write_db_config.get('password', ''))
        self.write_db_name.setText(write_db_config.get('database', 'tooling_fix'))
        self.write_db_timeout.setValue(write_db_config.get('timeout', 5))
        
        # Database Settings - Staff Database
        staff_db_config = config.get('read_database_staff', {})
        self.staff_db_host.setText(staff_db_config.get('host', '10.17.86.154'))
        self.staff_db_user.setText(staff_db_config.get('user', 'root'))
        self.staff_db_password.setText(staff_db_config.get('password', ''))
        self.staff_db_name.setText(staff_db_config.get('database', 'design'))
        self.staff_db_timeout.setValue(staff_db_config.get('timeout', 5))
        
        # Paths Settings
        paths_config = config['paths']
        self.shot_counts_path.setText(paths_config.get('shot_counts', 'shot_counts'))
        self.defect_data_path.setText(paths_config.get('defect_data', 'defect_raw_data'))
        self.pm_folder_path.setText(paths_config.get('pm_folder', 'PM'))
        self.pm_complete_path.setText(paths_config.get('pm_complete', 'PM/PM compleat'))
        self.pm_in_progress_path.setText(paths_config.get('pm_in_progress', 'PM/PM in Progress'))
        self.templates_path.setText(paths_config.get('templates', 'templat'))
        self.logs_path.setText(paths_config.get('logs', 'logs'))
        
        # UI Settings
        ui_config = config['ui']
        self.ui_theme.setCurrentText(ui_config.get('theme', 'LightBlue'))
        self.ui_font_size.setValue(ui_config.get('font_size', 12))
        self.ui_language.setCurrentText(ui_config.get('language', 'th'))
        
        # Application Settings
        app_config = config['application']
        self.auto_save_interval.setValue(app_config.get('auto_save_interval', 30))
        self.max_log_files.setValue(app_config.get('max_log_files', 10))
        self.enable_debug.setChecked(app_config.get('enable_debug', False))
    
    def save_config(self):
        """Save configuration to file"""
        try:
            new_config = {
                "plc": {
                    "port": self.plc_port.currentText(),
                    "baudrate": int(self.plc_baudrate.currentText()),
                    "bytesize": int(self.plc_bytesize.currentText()),
                    "parity": self.plc_parity.currentText(),
                    "stopbits": float(self.plc_stopbits.currentText()),
                    "timeout": self.plc_timeout.value(),
                    "auto_reconnect": self.plc_auto_reconnect.isChecked(),
                    "reconnect_interval": self.plc_reconnect_interval.value()
                },
                "read_database": {
                    "host": self.read_db_host.text(),
                    "user": self.read_db_user.text(),
                    "password": self.read_db_password.text(),
                    "database": self.read_db_name.text(),
                    "connect_timeout": self.read_db_timeout.value(),
                    "timeout": self.read_db_timeout.value()
                },
                "write_database": {
                    "host": self.write_db_host.text(),
                    "user": self.write_db_user.text(),
                    "password": self.write_db_password.text(),
                    "database": self.write_db_name.text(),
                    "connect_timeout": self.write_db_timeout.value(),
                    "timeout": self.write_db_timeout.value()
                },
                "read_database_staff": {
                    "host": self.staff_db_host.text(),
                    "user": self.staff_db_user.text(),
                    "password": self.staff_db_password.text(),
                    "database": self.staff_db_name.text(),
                    "connect_timeout": self.staff_db_timeout.value(),
                    "timeout": self.staff_db_timeout.value()
                },
                "paths": {
                    "shot_counts": self.shot_counts_path.text(),
                    "defect_data": self.defect_data_path.text(),
                    "pm_folder": self.pm_folder_path.text(),
                    "pm_complete": self.pm_complete_path.text(),
                    "pm_in_progress": self.pm_in_progress_path.text(),
                    "templates": self.templates_path.text(),
                    "logs": self.logs_path.text()
                },
                "ui": {
                    "theme": self.ui_theme.currentText(),
                    "font_size": self.ui_font_size.value(),
                    "language": self.ui_language.currentText()
                },
                "application": {
                    "auto_save_interval": self.auto_save_interval.value(),
                    "max_log_files": self.max_log_files.value(),
                    "enable_debug": self.enable_debug.isChecked()
                }
            }
            
            if config_manager.save_config(new_config):
                QMessageBox.information(self, "Success", 
                                      "Configuration saved successfully!\n\n"
                                      "Some changes may require application restart.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to save configuration!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration:\n{str(e)}")
    
    def test_plc_connection(self):
        """Test PLC connection with current settings"""
        try:
            import serial
            import serial.tools.list_ports
            
            port = self.plc_port.currentText()
            baudrate = int(self.plc_baudrate.currentText())
            
            if not port:
                QMessageBox.warning(self, "PLC Test", "Please select a COM port first")
                return
            
            # ตรวจสอบว่าพอร์ตมีอยู่จริง
            available_ports = [port.device for port in serial.tools.list_ports.comports()]
            if port not in available_ports:
                QMessageBox.critical(self, "PLC Test", 
                                   f"Port {port} not found!\n\nAvailable ports: {', '.join(available_ports)}")
                return
            
            # พยายามเปิดพอร์ตด้วยการจัดการ error ที่ดีขึ้น
            try:
                ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    bytesize=8,
                    parity='N',
                    stopbits=1,
                    timeout=2
                )
                
                if ser.is_open:
                    ser.close()
                    QMessageBox.information(self, "PLC Test", f"✅ Successfully connected to {port}")
                else:
                    QMessageBox.warning(self, "PLC Test", f"Failed to connect to {port}")
                    
            except serial.SerialException as e:
                if "Access is denied" in str(e):
                    QMessageBox.critical(self, "PLC Test", 
                                       f"❌ Access denied to {port}\n\n"
                                       "Possible solutions:\n"
                                       "• Run program as Administrator\n"
                                       "• Close other programs using this port\n"
                                       "• Restart the computer\n"
                                       "• Check device manager")
                else:
                    QMessageBox.critical(self, "PLC Test", f"Connection failed:\n{str(e)}")
                    
        except Exception as e:
            QMessageBox.critical(self, "PLC Test", f"Error:\n{str(e)}")
    def test_specific_database(self, db_type):
        """Test specific database connection (read/write/staff)"""
        try:
            import mysql.connector
            
            # Select the appropriate database config based on type
            if db_type == 'read':
                db_config = {
                    'host': self.read_db_host.text(),
                    'user': self.read_db_user.text(),
                    'password': self.read_db_password.text(),
                    'database': self.read_db_name.text(),
                    'connect_timeout': self.read_db_timeout.value()
                }
                title = "Read Database Test"
                db_label = f"Read DB ({self.read_db_name.text()})"
            elif db_type == 'write':
                db_config = {
                    'host': self.write_db_host.text(),
                    'user': self.write_db_user.text(),
                    'password': self.write_db_password.text(),
                    'database': self.write_db_name.text(),
                    'connect_timeout': self.write_db_timeout.value()
                }
                title = "Write Database Test"
                db_label = f"Write DB ({self.write_db_name.text()})"
            elif db_type == 'staff':
                db_config = {
                    'host': self.staff_db_host.text(),
                    'user': self.staff_db_user.text(),
                    'password': self.staff_db_password.text(),
                    'database': self.staff_db_name.text(),
                    'connect_timeout': self.staff_db_timeout.value()
                }
                title = "Staff Database Test"
                db_label = f"Staff DB ({self.staff_db_name.text()})"
            else:
                QMessageBox.warning(self, "Error", "Invalid database type")
                return
            
            connection = mysql.connector.connect(**db_config)
            if connection.is_connected():
                connection.close()
                QMessageBox.information(self, title, f"✅ {db_label} connection successful!")
            else:
                QMessageBox.warning(self, title, f"❌ {db_label} connection failed!")
                
        except Exception as e:
            QMessageBox.critical(self, title, f"❌ {db_label} connection failed:\n{str(e)}")
    
    def test_database_connection(self):
        """Test all database connections"""
        try:
            from src.database_manager import database_manager
            
            # Reload configurations first
            database_manager.reload_configurations()
            
            # Test all connections
            results = database_manager.test_connections()
            
            # Build result message
            message = "Database Connection Test Results:\n\n"
            message += f"📖 Read Database: {'✅ Connected' if results.get('read') else '❌ Failed'}\n"
            message += f"📝 Write Database: {'✅ Connected' if results.get('write') else '❌ Failed'}\n"
            message += f"👥 Staff Database: {'✅ Connected' if results.get('staff') else '❌ Failed'}"
            
            # Determine message type
            all_connected = all(results.values())
            if all_connected:
                QMessageBox.information(self, "Database Test", message)
            else:
                QMessageBox.warning(self, "Database Test", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Database Test", f"Error testing connections:\n{str(e)}")