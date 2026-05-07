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
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QApplication, QMainWindow, 
                              QDialog, QMessageBox, QFrame, QGraphicsView, QGraphicsTextItem, 
                              QGraphicsDropShadowEffect, QScrollArea, QDialogButtonBox, 
                              QLabel, QLineEdit, QPushButton, QComboBox, QSizePolicy, QFileDialog)
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtGui import QColor, QFont, QFontDatabase
from PySide6.QtCore import QEvent, Qt, Signal, QObject
from openpyxl.styles import colors
from sklearn.linear_model import LinearRegression
from src.data_upload import DataUploader
from src.ui_PM import Ui_PM
from src.login_pm import LoginPM
from copy import copy
from src.logout_window import LogoutWindow
from openpyxl.cell.cell import MergedCell
from src.config_manager import config_manager
from src.pm_window import Pmwindow


class ShotCounter(QObject):
    path_changed = Signal(str)
    
    def __init__(self, plc_window, parent_window=None, lot_size_value=1, product_data=None):
        super().__init__()
        self.plc_window = plc_window
        self.parent = parent_window
        self.lot_size_value = lot_size_value
        self.product_data = product_data or {}
        self.main_window = parent_window
        
        # Initialize variables
        self._initialize_variables()
        
        # Load configuration
        self._load_configuration()
        
        # Setup directories
        self._setup_directories()
        
        # Connect signals and setup UI
        self._setup_connections()
        
        # Load initial data
        self._load_initial_data()

    def _initialize_variables(self):
        """Initialize class variables"""
        self._should_stop_for_pm = False
        self.max_shot_limit = 30000
        self.pm_window = None
        self.pm_window_visible = False
        self.pm_triggered = False
        self.old_shot_count = 0
        self.product_name = None
        self.shot_count = 0
        self.last_total_sheet = None
        self.file_path = None
        self.start_lot_shot = 0
        self._just_reset = False
        self._next_pm_pair = None

    def _load_configuration(self):
        """Load configuration from config manager"""
        self.paths_config = config_manager.get_paths_config()

    def _setup_directories(self):
        """Setup and validate required directories"""
        self.base_dir = config_manager.get_full_path(self.paths_config.get('shot_counts', 'shot_counts'))
        self.pm_folder = config_manager.get_full_path(self.paths_config.get('pm_folder', 'PM'))
        self.pm_complete_dir = config_manager.get_full_path(self.paths_config.get('pm_complete', 'PM/PM compleat'))
        self.pm_in_progress_dir = config_manager.get_full_path(self.paths_config.get('pm_in_progress', 'PM/PM in Progress'))
        self.templates_dir = config_manager.get_full_path(self.paths_config.get('templates', 'templat'))
        
        # Create PM directories if they don't exist
        for pm_dir in [self.pm_folder, self.pm_complete_dir, self.pm_in_progress_dir]:
            if not os.path.exists(pm_dir):
                os.makedirs(pm_dir, exist_ok=True)
                print(f"Created PM directory: {pm_dir}")
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir, exist_ok=True)
            print(f"Created templates directory: {self.templates_dir}")
        
        # Check for template files
        template_files = [f for f in os.listdir(self.templates_dir) if f.lower().endswith(".xlsx")]
        if not template_files:
            print(f"No template files found in: {self.templates_dir}")
        else:
            print(f"Found template file: {template_files[0]}")

    def _setup_connections(self):
        """Setup signal connections and UI bindings"""
        # Connect PM Manual button
        if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'pushButton_2'):
            try:
                self.parent.ui.pushButton_2.clicked.connect(self.manual_pm_trigger)
                print("Connected PM Manual button successfully")
            except Exception as e:
                print(f"Failed to connect PM Manual button: {e}")
        
        # Connect finish_lot button
        if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'finish_lot'):
            try:
                self.parent.ui.finish_lot.clicked.connect(self.parent.show_logout_window)
                print("Connected finish_lot button successfully")
            except Exception as e:
                print(f"Failed to connect finish_lot button: {e}")
        
        # Connect other signals
        self.path_changed.connect(self._on_path_changed)
        self.plc_window.data_updated.connect(self.handle_plc_update)

    def _load_initial_data(self):
        """Load initial product data and shot counts"""
        self._check_product_change()
        self._load_product_and_data()
        self._load_last_selected_directory()

    # =========================================================================
    # PATH AND DIRECTORY MANAGEMENT
    # =========================================================================

    def _on_path_changed(self, new_path):
        """Update all related UIs when path changes"""
        if self.pm_window:
            self.pm_window.file_path = new_path

    def _load_last_selected_directory(self):
        """Load last selected directory from config"""
        last_dir = config_manager.current_config.get('user_preferences', {}).get('last_selected_directory', '')
        if last_dir and os.path.exists(last_dir):
            self.custom_base_dir = last_dir
            print(f"Loaded last directory from config: {last_dir}")
        else:
            self.custom_base_dir = self.base_dir
            print("Using default directory from config")

    def select_save_directory(self):
        """Let user select directory for saving and loading data"""
        last_directory = config_manager.current_config.get('user_preferences', {}).get('last_selected_directory', '')
        if not last_directory or not os.path.exists(last_directory):
            last_directory = self.base_dir
        
        directory = QFileDialog.getExistingDirectory(
            self.parent, 
            "Select Directory for Shot Count Data",
            last_directory
        )
        
        if directory:
            # Save selected directory to config
            if 'user_preferences' not in config_manager.current_config:
                config_manager.current_config['user_preferences'] = {}
            config_manager.current_config['user_preferences']['last_selected_directory'] = directory
            config_manager.save_config()
            
            self.custom_base_dir = directory
            print(f"Saved last directory: {directory}")
            
            # Reload data from new directory
            self._reload_data_from_new_directory(directory)
            
            # Emit path changed signal
            self.path_changed.emit(self.file_path)
            
            return directory

    def _reload_data_from_new_directory(self, new_directory):
        """Reload data from newly selected directory"""
        try:
            old_shot_count = self.shot_count
            
            self.custom_base_dir = new_directory
            self._load_product_and_data()
            
            if old_shot_count != self.shot_count:
                print(f"Shot count changed: {old_shot_count} → {self.shot_count}")
                
            # Update UI
            if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                self.parent.ui.shot_cnt.setText(f"{self.shot_count}")
                
            QMessageBox.information(self.parent, "Data Loaded", 
                                   f"Data loaded from new directory\n\n"
                                   f"Directory: {new_directory}\n"
                                   f"Current Shot Count: {self.shot_count}")
                                   
        except Exception as e:
            print(f"Error loading data from new directory: {e}")
            QMessageBox.warning(self.parent, "Error", 
                               f"Cannot load data from new directory: {e}")

    # =========================================================================
    # PRODUCT AND DATA MANAGEMENT
    # =========================================================================

    def _check_product_change(self):
        """Check for product changes and reset data if necessary"""
        try:
            current_data = self.plc_window.get_product_and_shot_count()
            new_product_name = current_data.get("product_name", "")
            
            if new_product_name != self.product_name:
                print(f"Product changed from {self.product_name} to {new_product_name}")
                self._reset_for_new_product(new_product_name)
                
        except Exception as e:
            print(f"Error checking product change: {e}")

    def _reset_for_new_product(self, new_product_name):
        """Reset data for new product"""
        try:
            if not new_product_name or new_product_name.strip() == "":
                print("Cannot reset: new product name is empty")
                return
                
            print(f"Resetting for new product: {new_product_name}")
            
            self.product_name = new_product_name
            self.start_lot_shot = self.shot_count
            self.last_total_sheet = None
            self.old_shot_count = self.shot_count
            
            self.file_path = os.path.join(self.base_dir, f"shotcount_{self.product_name}.txt")
            
            print(f"Reset complete for product: {new_product_name}, shot_count remains {self.shot_count}")
            
        except Exception as e:
            print(f"Error resetting for new product: {e}")

    def _load_product_and_data(self):
        """Load product data and shot counts from file"""
        current_data = self.plc_window.get_product_and_shot_count()
        self.product_name = current_data.get("product_name", "").strip()
        
        if not self.product_name:
            print("No product name found in PLC data")
            return
        
        base_dir = getattr(self, 'custom_base_dir', self.base_dir)
        self.file_path = os.path.join(base_dir, f"shotcount_{self.product_name}.txt")

        print(f"Loading data from: {self.file_path}")
        
        # Load shot count from TXT file
        file_shot_count = None
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\n')
                        file_shot_count = int(lines[0]) if lines[0].strip() else None
                        
                        if len(lines) > 1 and lines[1].strip():
                            self.last_total_sheet = int(lines[1])
                        else:
                            self.last_total_sheet = current_data.get("total_sheet", 0)
                        
                        print(f"Loaded shot_count={file_shot_count}, last_total_sheet={self.last_total_sheet} from TXT file")
                    else:
                        print("TXT file is empty")
                        file_shot_count = None
            except Exception as e:
                print(f"Error loading TXT file: {e}")
                file_shot_count = None
        else:
            print("No existing file found")
            file_shot_count = None
        
        # Use file shot count if available, otherwise keep current
        if file_shot_count is not None:
            self.shot_count = file_shot_count

        self.start_lot_shot = self.shot_count

        print(f"Set shot_count={self.shot_count}, start_lot_shot={self.start_lot_shot}")
        self._save_shot_count()
        
        self._check_pm_condition()

    def _save_shot_count(self):
        """Save shot count and last total sheet to TXT file"""
        try:
            if not self.product_name or self.product_name.strip() == "":
                print("Cannot save: product name is empty")
                return
                
            with open(self.file_path, "w", encoding='utf-8') as f:
                f.write(f"{self.shot_count}\n")
                if self.last_total_sheet is not None:
                    f.write(f"{self.last_total_sheet}\n")
            print(f"Saved shot_count={self.shot_count} to {self.file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    # =========================================================================
    # PLC DATA HANDLING
    # =========================================================================

    def handle_plc_update(self, data):
        """Handle PLC data updates"""
        print("PLC data updated")
        self.update()

    def update(self):
        """Update shot count based on PLC data"""
        current_data = self.plc_window.get_product_and_shot_count()
        product_name_temp = current_data.get("product_name", "")
        total_sheet = current_data.get("total_sheet", 0)
        shot_per_sheet = current_data.get("shot_count", 0)
        pcs_per_shot = current_data.get("pcs_number", 1)
        
        current_shot_count = self.shot_count
        
        # Check predictive PM
        self._check_predictive_pm(current_shot_count, pcs_per_shot)
        
        # Stop counting if PM is needed
        if hasattr(self, '_should_stop_for_pm') and self._should_stop_for_pm:
            print("Stopping shot count due to PM requirement")
            return
        
        # Skip counting after reset
        if hasattr(self, '_just_reset') and self._just_reset:
            self.last_total_sheet = total_sheet
            self._just_reset = False
            print(f"Skipping count after reset, set last_total_sheet to {total_sheet}")
            return

        new_file_path = os.path.join(self.base_dir, f"shotcount_{product_name_temp}.txt")

        # Check for product change
        if product_name_temp != self.product_name:
            self._handle_product_change(product_name_temp, new_file_path)
            return

        # Check for reset condition
        if self.last_total_sheet is not None and total_sheet < self.last_total_sheet:
            print(f"Detected reset: total_sheet decreased from {self.last_total_sheet} to {total_sheet}")
            print("Skipping shot count for this reset")
            self.last_total_sheet = total_sheet
            return
        
        # Count shots when total sheet increases
        if (self.last_total_sheet is not None and 
            self.last_total_sheet != total_sheet and 
            total_sheet > self.last_total_sheet):
            
            old_shot_count = self.shot_count

            sheet_increment = total_sheet - self.last_total_sheet
            actual_shot_increment = sheet_increment * shot_per_sheet
            
            self.shot_count += actual_shot_increment
            self.last_total_sheet = total_sheet
            self._save_shot_count()
            print(f"total_sheet changed (+{sheet_increment}), incremented shot_count by {actual_shot_increment} to {self.shot_count}")

            if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                self.parent.ui.shot_cnt.setText(f"{self.shot_count}")
            
            self._auto_save_excel(old_shot_count)
            self._check_pm_condition()
            
        elif self.last_total_sheet is None:
            # Initial system setup
            self.last_total_sheet = total_sheet
            print(f"Set initial last_total_sheet to {total_sheet}")

    # =========================================================================
    # PM (PREVENTIVE MAINTENANCE) MANAGEMENT
    # =========================================================================

    def _check_pm_condition(self):
        """Check PM conditions"""
        try:
            if self.shot_count >= 30000 and not self.pm_triggered and not self.pm_window_visible:
                print(f"PM condition met: shot_count={self.shot_count} >= 30000")
                print(f"PM triggered: {self.pm_triggered}, PM window visible: {self.pm_window_visible}")
                self._handle_pm_needed()
            else:
                print(f"PM check: shot_count={self.shot_count}, condition not met")
        except Exception as e:
            print(f"Error checking PM condition: {e}")

    def _check_predictive_pm(self, current_shot_count, pcs_per_shot):
        """Predictive PM check"""
        try:
            if (not hasattr(self, 'lot_size_value') or 
                self.lot_size_value is None or 
                self.lot_size_value <= 0 or 
                pcs_per_shot <= 0):
                print(f"Predictive PM: incomplete data (lot_size={getattr(self, 'lot_size_value', 'N/A')}, pcs_per_shot={pcs_per_shot})")
                return
            
            increment_shot = (self.lot_size_value if self.lot_size_value else 1) / pcs_per_shot
            predicted_total_shots = current_shot_count + increment_shot
            
            print(f"Predictive PM:")
            print(f"  - Current Shot: {current_shot_count}")
            print(f"  - Lot size: {self.lot_size_value}")
            print(f"  - PCS/Shot: {pcs_per_shot}")
            print(f"  - Increment: {increment_shot:.2f}")
            print(f"  - Predicted Total: {predicted_total_shots:.2f}")
            print(f"  - Limit: {self.max_shot_limit}")
            
            if predicted_total_shots > self.max_shot_limit:
                print(f"Shot count will exceed {self.max_shot_limit} (current {current_shot_count} + increment {increment_shot:.2f}) - PM required!")
                
                self._should_stop_for_pm = True
                
                if self.parent and hasattr(self.parent, 'ui'):
                    if hasattr(self.parent.ui, 'statusbar'):
                        self.parent.ui.statusbar.showMessage(
                            f"PM required! (predicted: {predicted_total_shots:.0f} shots)", 
                            10000
                        )
                    if hasattr(self.parent.ui, 'shot_cnt'):
                        self.parent.ui.shot_cnt.setStyleSheet("background-color: #ffcccc; color: #cc0000; font-weight: bold;")
                
                if not self.pm_triggered and not self.pm_window_visible:
                    print("Triggering predictive PM process")
                    self._handle_pm_needed()
                else:
                    print("PM already in progress")
                    
            else:
                self._should_stop_for_pm = False
                remaining_shots = self.max_shot_limit - predicted_total_shots
                print(f"Predictive: PM not yet required ({remaining_shots:.2f} shots remaining)")
                
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'shot_cnt'):
                    self.parent.ui.shot_cnt.setStyleSheet("")
                    
        except Exception as e:
            print(f"Error in predictive PM check: {e}")

    def manual_pm_trigger(self):
        """Manual PM trigger by user"""
        try:
            print("User pressed Manual PM button")
            
            if self.pm_triggered or self.pm_window_visible:
                print("PM is already in progress")
                QMessageBox.information(self.parent, "PM in Progress", 
                                      "Preventive Maintenance is already in progress\nPlease wait for the process to complete")
                return
            
            if not self.product_name or self.product_name.strip() == "":
                print("No product name found")
                QMessageBox.warning(self.parent, "Incomplete Data", 
                                  "Product information not found\nPlease wait until machine data is received")
                return
            
            reply = QMessageBox.question(
                self.parent, 
                "Confirm Preventive Maintenance",
                f"Do you want to perform Manual Preventive Maintenance?\n\n"
                f"Product: {self.product_name}\n"
                f"Current Shot Count: {self.shot_count}\n\n"
                f"After PM completion:\n"
                f"• Reset Shot Count to 0\n"
                f"• Save PM data to system\n"
                f"• Generate PM Report file",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                print("User confirmed Manual PM")
                self._handle_pm_needed(is_manual=True)
            else:
                print("User canceled Manual PM")
                
        except Exception as e:
            print(f"Error in manual PM trigger: {e}")
            QMessageBox.critical(self.parent, "Error", 
                               f"Error starting Manual PM: {e}")

    def _handle_pm_needed(self, is_manual=False):
        """Handle PM requirement (both automatic and manual)"""
        if self.pm_triggered or self.pm_window_visible:
            print(f"PM already in progress: triggered={self.pm_triggered}, window_visible={self.pm_window_visible}")
            return
        
        pm_type = "Manual" if is_manual else "Auto"
        print(f"Starting PM process ({pm_type}): shot_count={self.shot_count}")
        self.pm_triggered = True
        print(f"Loading Excel data for PM window ({pm_type})")

        excel_filename = f"shotcount_{self.product_name}.xlsx"
        # ✅ เปลี่ยนมาใช้ pm_in_progress_dir สำหรับไฟล์ที่ยังทำ PM ไม่เสร็จ
        excel_file = os.path.join(self.pm_in_progress_dir, excel_filename)
        
        lot_shot_data, row_3b_value = self.load_excel_data_for_pm(excel_file)
        
        try:
            login_dialog = LoginPM(parent=self.main_window, main_window=self.main_window)
            result = login_dialog.exec()
            
            if result == QDialog.Accepted and login_dialog.login_successful:
                login_data = login_dialog.get_login_data()
                print(f"Login data received for PM ({pm_type}): {login_data}")
                
                self.show_pm_window(
                    lot_shot_data=lot_shot_data, 
                    row_3b_value=row_3b_value, 
                    login_data=login_data,
                    is_manual=is_manual
                )
                print(f"PM window ({pm_type}) opened successfully")
            else:
                self.pm_triggered = False
                self.pm_window_visible = False
                self._should_stop_for_pm = False
                print(f"User canceled PM login ({pm_type})")
                
        except Exception as e:
            print(f"Error in PM login process ({pm_type}): {e}")
            self.pm_triggered = False
            self.pm_window_visible = False

    def show_pm_window(self, lot_shot_data=None, row_3b_value=None, login_data=None, is_manual=False):
        """Show PM window"""
        try:
            pm_type = "Manual" if is_manual else "Auto"
            print(f"Creating PM window ({pm_type})...")
            
            if self.pm_window_visible:
                print("PM window is already visible")
                return
                
            if self.parent is None:
                self.parent = QApplication.activeWindow()
                
            print(f"Creating Pmwindow with login_data: {login_data is not None} ({pm_type})")
            
            self.pm_window = Pmwindow(
                parent=self.parent, 
                login_data=login_data, 
                file_path=self.file_path, 
                shot_counter=self
            )
            self.pm_window_visible = True
            self.pm_window.is_logged_in = True
            
            if is_manual:
                self.pm_window.setWindowTitle(f"Preventive Maintenance (Manual) - {self.product_name}")
            else:
                self.pm_window.setWindowTitle(f"Preventive Maintenance (Auto) - {self.product_name}")
            
            if lot_shot_data is not None:
                self.pm_window.set_excel_data(lot_shot_data)
                print("Excel data set for PM Window")
            
            if row_3b_value is not None:
                self.pm_window.parse_and_set_row_3b_data(row_3b_value)
                print("Row 3B data set for PM Window")
            
            self.pm_window.setAttribute(Qt.WA_DeleteOnClose)
            self.pm_window.destroyed.connect(self._on_pm_window_closed)
            
            print(f"Showing PM window ({pm_type})...")
            self.pm_window.show()
            print(f"PM window ({pm_type}) is now visible")
            
        except Exception as e:
            print(f"Error displaying PM window ({pm_type}): {e}")
            import traceback
            traceback.print_exc()

    def _on_pm_window_closed(self):
        """Handle PM window closure"""
        self.pm_window_visible = False
        self.pm_triggered = False
        self.pm_window = None

    def _handle_product_change(self, new_product_name, new_file_path):
        """Handle product change and load new data"""
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
                    print(f"Loaded shot_count={self.shot_count}, last_total_sheet={self.last_total_sheet} for new product")
                except ValueError:
                    self.shot_count = 0
                    self.last_total_sheet = None
        else:
            self.shot_count = 0
            self.last_total_sheet = None
            print(f"No file for product {self.product_name}, starting at 0")
            
        self.product_name = new_product_name
        self.file_path = new_file_path
        self.start_lot_shot = self.shot_count
        print(f"Reset start_lot_shot to {self.start_lot_shot} for new product")
        self._save_shot_count()

    # =========================================================================
    # EXCEL FILE MANAGEMENT
    # =========================================================================

    def load_excel_data_for_pm(self, file_path):
        """Load Lot and Shot data from Excel file"""
        data_list = []
        row_3b_value = None
        
        if not os.path.exists(file_path):
            print(f"Excel file not found: {file_path}")
            return data_list, row_3b_value

        try:
            wb = load_workbook(file_path)
            ws = wb.active

            # Read row 3, column B
            row_3b_cell = ws.cell(row=3, column=2)
            if row_3b_cell.value:
                row_3b_value = row_3b_cell.value
                print(f"Successfully read row 3B: {row_3b_value}")
            else:
                print("No data found in row 3 column B")

            # Read data from rows 7 to 21
            for row in range(7, 22):
                for col in range(2, 11):  # Columns B to J
                    cell = ws.cell(row=row, column=col)
                    
                    if isinstance(cell.value, str) and 'shot' in cell.value:
                        try:
                            parts = cell.value.split('\n')
                            lot_id = parts[0] if len(parts) > 0 else 'N/A'
                            shot_count = parts[1].split('shot ')[1] if len(parts) > 1 else 'N/A'
                            
                            data_list.append((lot_id, int(shot_count)))
                        except (ValueError, IndexError):
                            print(f"Cannot parse data from cell {cell.coordinate}: {cell.value}")
                            continue
            
            return data_list, row_3b_value

        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return [], None

    def manual_save(self):
        """Manual save to Excel file"""
        try:
            txt_filename = os.path.basename(self.file_path)
            base_filename = os.path.splitext(txt_filename)[0]
            excel_filename = base_filename + ".xlsx"
            
            # ✅ เปลี่ยนมาใช้ pm_in_progress_dir สำหรับไฟล์ที่ยังทำ PM ไม่เสร็จ
            dest_folder = self.pm_in_progress_dir
            dest_path = os.path.join(dest_folder, excel_filename)

            lot_number = self.product_data.get('lot_number', 'N/A')
            shot_count_current = self.shot_count
            
            os.makedirs(dest_folder, exist_ok=True)
            
            # Create Excel file from template if it doesn't exist
            if not os.path.exists(dest_path):
                template_dir = self.templates_dir
                template_files = [f for f in os.listdir(template_dir) if f.lower().endswith(".xlsx")]
                if not template_files:
                    print("No .xlsx files found in templates directory")
                    return
                template_path = os.path.join(template_dir, template_files[0])
                shutil.copy(template_path, dest_path)
                print(f"Copied template: {template_path} → {dest_path}")
                self._save_initial_data(dest_path)
            
            # Open Excel file for editing
            wb = load_workbook(dest_path)
            ws = wb.active

            font_style = Font(name='Angsana New', size=12, bold=True)
            start_row = 7
            end_row = 100
            data_columns = range(2, 11)

            found = False
            columns_to_resize = set()

            current_lot_shots = shot_count_current - self.start_lot_shot
            print(f"Calculating lot shots: {shot_count_current} - {self.start_lot_shot} = {current_lot_shots}")

            if current_lot_shots == 0:
                print("No new shots in this lot, no need to save")
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'statusbar'):
                    self.parent.ui.statusbar.showMessage("No new shots in this lot, no need to save", 5000)
                return

            # Part 1: Update existing lot
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
                        print(f"Updated existing lot at {cell_to_update.coordinate} with total shots {new_total_lot_shots}")
                        
                        self.start_lot_shot = shot_count_current
                        found = True
                        break
                if found:
                    break

            # Part 2: Add new lot by replacing existing number
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
                            print(f"Added new lot at {cell_to_fill.coordinate} by replacing number {cell_value}")
                            
                            self.start_lot_shot = shot_count_current
                            found = True
                            break
                    if found:
                        break

            # Part 3: Add new row if no space available
            if not found:
                new_row = end_row + 1
                new_cell = ws.cell(row=new_row, column=2)
                new_cell.value = f"{lot_number}\nshot {current_lot_shots}"
                new_cell.alignment = Alignment(wrapText=True)
                new_cell.font = font_style
                columns_to_resize.add('B')
                print(f"Added new row for lot at row {new_row}")
                
                self.start_lot_shot = shot_count_current

            # Update prediction and coloring
            predicted_slot = self._predict_next_pm_slot(ws)
            self._update_pm_prediction(ws, predicted_slot)
            
            if predicted_slot and predicted_slot != 'N/A' and predicted_slot != 'Error':
                self._highlight_predicted_slots(ws, predicted_slot)
            
            # Final save
            for column_letter in columns_to_resize:
                ws.column_dimensions[column_letter].width = 8
                print(f"Set column {column_letter} width to 8")

            wb.save(dest_path)
            print("Data saved and columns resized successfully")
            
        except Exception as e:
            print(f"Error during manual save: {str(e)}")

    def _save_initial_data(self, excel_path):
        """Save initial data to cell B3 in single line format"""
        try:
            wb = load_workbook(excel_path)
            ws = wb.active
            
            product_name = self.product_data.get('product_name', 'N/A')
            tooling_code = self.product_data.get('tooling_code', 'N/A')
            lot_number = self.product_data.get('lot_number', 'N/A')
            
            tooling_type = ""
            if tooling_code.startswith('OSTE'):
                tooling_type = "E-FPC"
            elif tooling_code.startswith('OSTM'):
                tooling_type = "SMT"
            else:
                tooling_type = "N/A"
            
            single_line_text = (
                f"Product name:  {product_name}      "
                f"Tooling code:  {tooling_code}      "
                f"Tooling for:   {tooling_type}       "
                f"Next p.m.: {lot_number}"
            )
            
            ws['B3'] = single_line_text
            wb.save(excel_path)
            print(f"Saved initial data in single line: {single_line_text}")
            
        except Exception as e:
            print(f"Cannot save initial data: {str(e)}")

    # =========================================================================
    # AUTO SAVE AND PREDICTION
    # =========================================================================

    def _auto_save_excel(self, old_shot_count):
        """Auto save when conditions are met"""
        try:
            shot_difference = self.shot_count - self.old_shot_count
            print(f"Checking Auto Save: old={self.old_shot_count}, new={self.shot_count}, diff={shot_difference}")
            
            if shot_difference >= 30:
                print(f"Auto Save triggered: increased {shot_difference} shots")
                
                self.manual_save()
                self.old_shot_count = self.shot_count
                
                if self.parent and hasattr(self.parent, 'ui') and hasattr(self.parent.ui, 'statusbar'):
                    self.parent.ui.statusbar.showMessage(f"Auto Save: {self.shot_count} shots", 3000)
                    
            else:
                print(f"Auto Save condition not met: {shot_difference}/50 shots")

        except Exception as e:
            print(f"Error in Auto Save: {e}")

    def _predict_next_pm_slot(self, ws):
        """Calculate next PM slot using Linear Regression"""
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

            self._next_pm_pair = f"{prev_slot}-{predicted_slot}"

            print(f"Predicted PM at slot {predicted_slot} (previous {prev_slot})")
            print(f"PM pair displayed as: {self._next_pm_pair}")

            return predicted_slot

        except Exception as e:
            print(f"Error in prediction: {e}")
            return 'Error'

    def _update_pm_prediction(self, ws, predicted_slot):
        """Update Next P.M. information in Excel"""
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

            print(f"Updated Next PM text in Excel: {next_pm_text}")
            return next_pm_text

        except Exception as e:
            print(f"Error updating PM prediction: {e}")
            return None

    def _highlight_predicted_slots(self, ws, predicted_slot):
        """Highlight predicted PM slots with colors"""
        try:
            START_ROW = 7
            ROW_STEP = 2
            DATA_COLUMNS = list(range(2, 11))

            try:
                pred = int(predicted_slot)
            except Exception:
                print("predicted_slot is not a number")
                return

            yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            # Reset all colors first
            self._reset_table_colors(ws, START_ROW, ROW_STEP, DATA_COLUMNS)

            # Calculate positions
            prev_slot_num = pred - 1
            pred_slot_num = pred

            prev_row = START_ROW + ((prev_slot_num - 1) // 9) * ROW_STEP
            prev_col = 2 + ((prev_slot_num - 1) % 9)
            
            pred_row = START_ROW + ((pred_slot_num - 1) // 9) * ROW_STEP
            pred_col = 2 + ((pred_slot_num - 1) % 9)

            print(f"Calculated positions:")
            print(f"  - Slot {prev_slot_num}: row {prev_row}, column {prev_col} ({chr(64+prev_col)})")
            print(f"  - Slot {pred_slot_num}: row {pred_row}, column {pred_col} ({chr(64+pred_col)})")

            # Highlight previous slot
            prev_cell = ws.cell(row=prev_row, column=prev_col)
            for merged_range in ws.merged_cells.ranges:
                if prev_cell.coordinate in merged_range:
                    prev_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                    break
            prev_cell.fill = yellow_fill
            print(f"Highlighted yellow at {prev_cell.coordinate} (slot {prev_slot_num})")

            # Highlight predicted slot
            pred_cell = ws.cell(row=pred_row, column=pred_col)
            for merged_range in ws.merged_cells.ranges:
                if pred_cell.coordinate in merged_range:
                    pred_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                    break
            pred_cell.fill = red_fill
            print(f"Highlighted red at {pred_cell.coordinate} (slot {pred_slot_num})")

            self._next_pm_pair = f"{prev_slot_num}-{pred_slot_num}"
            print(f"Updated predicted slot pair: {self._next_pm_pair}")

            print("Successfully highlighted previous and predicted slots")

        except Exception as e:
            print(f"Error highlighting slots: {e}")

    def _reset_table_colors(self, ws, start_row, row_step, data_columns):
        """Reset all table cell colors"""
        no_fill = PatternFill(fill_type=None)
        for row in range(start_row, 100, row_step):
            for col in data_columns:
                cell = ws.cell(row=row, column=col)
                for merged_range in ws.merged_cells.ranges:
                    if cell.coordinate in merged_range:
                        main_cell = ws.cell(merged_range.min_row, merged_range.min_col)
                        main_cell.fill = no_fill
                        break
                else:
                    cell.fill = no_fill

    # =========================================================================
    # UI MANAGEMENT
    # =========================================================================

    def show_logout_window(self):
        """Show logout window"""
        try:
            self.logout_window = LogoutWindow(
                parent=self.parent, 
                shot_counter=self,
                theme_settings=getattr(self.parent, 'theme_settings', {})
            )
            self.logout_window.show()
            print("Showing logout window with theme")
            
        except Exception as e:
            print(f"Error showing logout window: {e}")
            self.manual_save()


if __name__ == "__main__":
    window_pm = ShotCounter()
    sys.exit(app.exec())