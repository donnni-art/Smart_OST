########################################################################
## IMPORTS
########################################################################
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import shutil
import psutil
########################################################################
# IMPORT GUI FILE
from src.ui_interface import *
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFrame, QGraphicsView, QGraphicsTextItem, QGraphicsDropShadowEffect,QScrollArea
from PySide6.QtCore import Qt, Signal, QObject, QTimer, QMargins, QSettings, QCoreApplication, QLocale
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice, QBarSeries, QBarSet,QLegend
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import patches as mpatches
from matplotlib import colors as mcolors 
import pandas as pd # Add this line
import seaborn as sns # Add this line b
import icons_rc
import hashlib
from matplotlib.colors import LinearSegmentedColormap # Add this line
########################################################################

########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomQToolTip import QCustomQToolTipFilter
########################################################################

########################################################################
# import login
from src.Functions import GuiFunctions
from src.graph_manager import GraphManager
from src.PLCdata import PLCWindow
from src.login_manager import LoginManager
from src.graph_updater import GraphUpdater
from src.update_data_manager import update_sever
from src.data_upload import DataUploader
from src.shot_counting import ShotCounter
from src.login_scan import MyWindow
from src.heat_map_defect import HeatMapDefectPCS
from src.config_manager import config_manager
from src.config_dialog import ConfigDialog
from src.production_calculator import ProductionCalculator
########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    theme_changed = Signal()
    product_info_updated = Signal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # โหลด configuration ก่อนเริ่มต้น UI
        self.config_manager = config_manager
        self.ui_config = self.config_manager.get_ui_config()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # ✅ เพิ่มตัวแปรตรวจสอบสถานะ
        self._is_closing_application = False  # กำลังปิดแอป
        self._logout_for_shutdown = False     # Logout เพื่อปิดแอป
        self.shot_counter = None
        self.theme_settings = None
        # ✅ ตรวจสอบและฆ่ากระบวนการที่ค้างก่อนเริ่ม
        self._kill_zombie_processes()
        
        # ✅ เพิ่มตัวแปรตรวจสอบสถานะ initialization
        self._initialization_complete = False
        
        # ✅ เพิ่มตัวแปรตรวจสอบสถานะ logout
        self.is_logged_out = False
        self.logout_window = None
        self._is_handling_close = False
        try:
            # ✅ สร้าง components หลังจาก Theme พร้อม
            self.plc_window = PLCWindow()
            self.data_upload = DataUploader()
            self.data_uploader = self.data_upload

            self.login_manager = LoginManager(self.plc_window, self)
            if not self.login_manager.login():
                self.close()
                return

            # ✅ โหลด Theme ก่อนสิ่งอื่นใด
            loadJsonStyle(self, self.ui, jsonFiles={"json-styles/style.json"})
            QAppSettings.updateAppSettings(self)
            self.theme = getattr(self, 'theme', None)

            lot_number = self.get_current_lot_number()  
            self.plc_window.set_current_lot_number(lot_number)
            product_data = self.login_manager.get_data_scan()
            
            # ✅ ตรวจสอบว่าข้อมูลผลิตภัณฑ์ถูกต้อง
            if not product_data or not product_data.get('product_name'):
                print("❌ Invalid product data, forcing re-login")
                self._handle_invalid_product_data()
                return
            
            self.shot_counter = ShotCounter(self.plc_window, self, 
                                          lot_size_value=self.login_manager.product_info.get('lot_size_value'), 
                                          product_data=product_data)
            
            self.graph_updater = GraphUpdater(self.plc_window, self)
            self.heat_map_defect = HeatMapDefectPCS(self.plc_window, self)
            self.update_data_manager = update_sever(self.plc_window, self)
            # ✅ สร้าง ProductionCalculator และส่ง reference ของตัวเองไป
            self.production_calculator = ProductionCalculator(self.plc_window, self)
            # ✅ เริ่มการคำนวณ
            self.production_calculator.start_calculation()

            # ✅ เชื่อมต่อ Signal กับ HeatMapDefectPCS
            self.product_info_updated.connect(self.heat_map_defect.set_product_info)
            
            # ✅ อัพเดตข้อมูลผลิตภัณฑ์และรีเซ็ตข้อมูล
            self.update_label_with_product_info()
            
            # ✅ บังคับรีเซ็ตข้อมูล defect เมื่อเริ่มงานใหม่
            self.force_reset_defect_data()

            self.app_functions = GuiFunctions(self)
            self.update_theme_settings()
            self.theme_changed.connect(self.update_theme_settings)
            
            # ✅ ตั้งค่าสถานะ initialization สำเร็จ
            self._initialization_complete = True
            
            # ตั้งค่าให้ลบหน้าต่างเมื่อปิด ก่อนแสดง
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.show()
            
            print("✅ MainWindow initialization completed successfully")
            
        except Exception as e:
            print(f"❌ Error during MainWindow initialization: {e}")
            self._handle_initialization_error(e)

    def force_reset_defect_data(self):
        """บังคับรีเซ็ตข้อมูล defect เมื่อเริ่มงานใหม่"""
        try:
            print("🔄 Force resetting defect data...")
            
            # รีเซ็ตข้อมูลใน memory
            if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                self.heat_map_defect.result_all_by_pcs = {}
                self.heat_map_defect.result_defect_only = {}
                self.heat_map_defect.defect_data_for_heatmap = {}
                self.heat_map_defect.last_dm1923 = None
                self.heat_map_defect.last_shot_cnt = None
                self.heat_map_defect.first_dm1923_checked = False
                
                # ล้างกราฟ
                self.heat_map_defect.clear_heatmap()
                self.heat_map_defect.plot_stacked_bar_defects()
                
            print("✅ Defect data force reset completed")
            
        except Exception as e:
            print(f"❌ Error force resetting defect data: {e}")
            
    def _handle_invalid_product_data(self):
        """จัดการเมื่อข้อมูลผลิตภัณฑ์ไม่ถูกต้อง"""
        QMessageBox.critical(self, "Error", "Invalid product data. Please log in again.")
        self.close()
        # รีสตาร์ทแอป
        self.restart_application()

    def _handle_initialization_error(self, error):
        """จัดการข้อผิดพลาดระหว่าง initialization"""
        print(f"❌ Initialization error: {error}")
        QMessageBox.critical(self, "Initialization Error", 
                            f"An error occurred during program initialization:\n{str(error)}\n\nThe program will close automatically.")
        self._force_quit()

    def update_theme_settings(self):
        """
        ฟังก์ชันนี้จะอ่านค่าธีมปัจจุบันและสร้าง dictionary ของสี
        เพื่อให้ส่วนอื่นๆ ของโปรแกรมนำไปใช้ได้ง่าย        """
        settings = QSettings()
        current_theme_name = settings.value("THEME", "LightBlue")
        current_theme_data = {}
        
        for theme in self.ui.themes:
            if theme.name == current_theme_name:
                # ✅ ใช้ชื่อตัวแปร COLOR_ เป็นหลักเพื่อความสอดคล้องกัน
                current_theme_data = {
                    "Background-color": getattr(theme, 'COLOR_BACKGROUND_1', '#FFFFFF'),
                    "Text-color": getattr(theme, 'COLOR_TEXT_1', '#000000'),
                    "Icons-color": getattr(theme, 'COLOR_ACCENT_3', '#666666'),
                    "Accent-color": getattr(theme, 'COLOR_ACCENT_1', '#26bae3'),
                    "Destructive-color": getattr(theme, 'COLOR_ACCENT_2', '#E74C3C'),
                    "Secondary-text-color": getattr(theme, 'COLOR_TEXT_2', '#666666'),
                    "Theme-name": getattr(theme, 'name', 'Unknown')
                }
                break
        
        self.theme_settings = current_theme_data
        print(f"🎨 Theme settings updated for '{current_theme_name}': {self.theme_settings}")
        
    def show_logout_window(self):
        """แสดงหน้าต่าง Logout จาก MainWindow โดยตรง"""
        try:
            from src.logout_window import LogoutWindow
            
            # สร้าง LogoutWindow และส่ง theme settings ไป
            self.logout_window = LogoutWindow(
                parent=self, 
                shot_counter=self.shot_counter,
                theme_settings=self.theme_settings,
                data_uploader=self.data_uploader # ✅ Pass DataUploader
            )
            
            # ✅ เชื่อมต่อสัญญาณ logout_completed
            self.logout_window.logout_completed.connect(self.handle_logout_completed)
            
            # ✅ เชื่อมต่อสัญญาณ theme_changed ไปยัง LogoutWindow
            self.theme_changed.connect(self.update_logout_window_theme)
            
            self.logout_window.show()
            print("✅ LogoutWindow shown with theme support")
            
        except Exception as e:
            print(f"❌ Error showing logout window: {e}")
    
    @Slot()
    def handle_logout_completed(self):
        """จัดการเมื่อ logout สำเร็จ"""
        try:
            print("✅ Logout completed signal received")
            self.is_logged_out = True
            
            # ปิดหน้าต่าง logout
            if self.logout_window and self.logout_window.isVisible():
                self.logout_window.close()
                self.logout_window = None
            
            # ถ้า logout เพื่อ shutdown ให้ cleanup และจบโปรแกรม (ไม่ restart)
            if self._logout_for_shutdown:
                print("🔄 Logout completed for application shutdown")
                self._logout_for_shutdown = False
                self._is_closing_application = True
                
                # ทำความสะอาดและออกเลย
                self._cleanup_before_exit()
                try:
                    QCoreApplication.quit()
                finally:
                    os._exit(0)
            else:
                print("🔄 Normal logout - restarting application")
                # Logout ปกติ - รีสตาร์ทแอป
                self._cleanup_before_restart()
                self.restart_application()
                
        except Exception as e:
            print(f"❌ Error handling logout completion: {e}")
            # ถ้าเกิดข้อผิดพลาด ให้ปิดแอป
            self._force_quit()

    def _cleanup_before_restart(self):
        """ทำความสะอาดข้อมูลทั้งหมดก่อนรีสตาร์ทแอป"""
        try:
            print("🧹 Cleaning up before restart...")
            
            # 0. หยุด thread และ timer ก่อน
            self._stop_all_threads_and_timers()
            
            # 2. ✅ บันทึกข้อมูล shot count ก่อน cleanup
            if hasattr(self, 'shot_counter') and self.shot_counter:
                print("💾 Saving shot count before cleanup...")
                self.shot_counter._save_shot_count()  # บันทึกค่าปัจจุบัน
            
            if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                try:
                    # หาก HeatMapDefectPCS มีเมธอดหยุด/cleanup ให้เรียกก่อน
                    if hasattr(self.heat_map_defect, 'stop'):
                        try:
                            self.heat_map_defect.stop()
                        except Exception:
                            pass
                    if hasattr(self.heat_map_defect, 'close'):
                        try:
                            self.heat_map_defect.close()
                        except Exception:
                            pass

                    # พยายาม disconnect signal ที่เชื่อมไว้เพื่อลด callback ระหว่าง shutdown
                    try:
                        self.product_info_updated.disconnect(self.heat_map_defect.set_product_info)
                    except Exception:
                        pass

                    # เอา reference ออกให้ GC เก็บ
                    self.heat_map_defect = None
                except Exception as e:
                    print(f"⚠️ Error cleaning up heat map: {e}")
            
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

    def _clean_temp_files(self):
        """ลบไฟล์ชั่วคราว"""
        try:
            print("🗑️ Cleaning temporary files...")
            
            # โฟลเดอร์ที่ต้องการลบไฟล์ชั่วคราว
            temp_folders = [
                "shot_counts",
                "defect_raw_data/temp",
                "PM/temp"
            ]
            
            for folder in temp_folders:
                if os.path.exists(folder):
                    # ระวัง: ไม่ลบโฟลเดอร์หลัก, ลบเฉพาะไฟล์ชั่วคราวเท่านั้น
                    for filename in os.listdir(folder):
                        if filename.endswith('.tmp') or filename.startswith('temp_'):
                            file_path = os.path.join(folder, filename)
                            try:
                                os.remove(file_path)
                                print(f"✅ Deleted temp file: {file_path}")
                            except Exception as e:
                                print(f"⚠️ Cannot delete {file_path}: {e}")
            
            print("✅ Temporary files cleaned")
            
        except Exception as e:
            print(f"❌ Error cleaning temp files: {e}")
            
    def _reset_heat_map_data(self):
        """รีเซ็ตข้อมูลใน Heat Map"""
        try:
            print("🔄 Resetting Heat Map data...")
            
            # รีเซ็ตข้อมูล defect
            self.heat_map_defect.result_all_by_pcs = {}
            self.heat_map_defect.result_defect_only = {}
            self.heat_map_defect.defect_data_for_heatmap = {}
            self.heat_map_defect.last_dm1923 = None
            self.heat_map_defect.last_shot_cnt = None
            self.heat_map_defect.first_dm1923_checked = False
            
            # ล้างกราฟ
            self.heat_map_defect.clear_heatmap()
            self.heat_map_defect.plot_stacked_bar_defects()
            
            print("✅ Heat Map data reset successfully")
            
        except Exception as e:
            print(f"❌ Error resetting Heat Map: {e}")

    def _reset_plc_data(self):
        """รีเซ็ตข้อมูลใน PLC"""
        try:
            print("🔄 Resetting PLC data...")
            
            # รีเซ็ตค่าใน PLC Window
            if hasattr(self.plc_window, 'current_lot_number'):
                self.plc_window.current_lot_number = None
                
            if hasattr(self.plc_window, 'shot_count'):
                self.plc_window.shot_count = 0
                
            # อัพเดต UI ให้แสดงค่าเริ่มต้น
            if hasattr(self.ui, 'shot_cnt'):
                self.ui.shot_cnt.setText("0")
                
            print("✅ PLC data reset successfully")
            
        except Exception as e:
            print(f"❌ Error resetting PLC data: {e}")  

    def _reset_shot_counter_data(self):
        """รีเซ็ตข้อมูลใน Shot Counter - แก้ไขไม่ให้รีเซ็ตไฟล์เป็น 0"""
        try:
            print("🔄 Resetting Shot Counter data...")
            
            # ✅ ไม่รีเซ็ตค่าใน memory เป็น 0 (รักษาค่าเดิมไว้)
            
            # ✅ รีเซ็ตเฉพาะค่าที่จำเป็นจริงๆ
            self.shot_counter.last_total_sheet = None
            
            # ✅ รีเซ็ตข้อมูลผลิตภัณฑ์ (ยังคงทำได้)
            if hasattr(self.shot_counter, 'product_data'):
                self.shot_counter.product_data = {}
                
            print("✅ Shot Counter data reset successfully (file not reset to 0)")
            
        except Exception as e:
            print(f"❌ Error resetting Shot Counter: {e}")   

    def restart_application(self):
        """รีสตาร์ทแอปพลิเคชัน"""
        try:
            print("🔄 Restarting application...")
            
            # ✅ ตั้งค่าสถานะ
            self._is_closing_application = False
            self._logout_for_shutdown = False
            
            # ✅ หยุด thread และ timer
            self._stop_all_threads_and_timers()
            
            # ✅ บันทึกข้อมูลก่อนรีสตาร์ท
            if hasattr(self, 'shot_counter') and self.shot_counter:
                self.shot_counter._save_shot_count()
            
            # ✅ ปิดหน้าต่างหลัก
            self.close()
            
            # ✅ รีสตาร์ทกระบวนการ
            self._safe_restart_process()
            
        except Exception as e:
            print(f"❌ Error restarting application: {e}")
            self._force_quit()

    def _safe_restart_process(self):
        """รีสตาร์ทกระบวนการอย่างปลอดภัย"""
        try:
            python = sys.executable
            script = sys.argv[0]
            
            print(f"🔁 Restarting: {python} {script}")
            
            # ✅ ใช้ os.execv เพื่อแทนที่กระบวนการปัจจุบัน (เหมาะสำหรับ Linux/Unix)
            # หรือใช้ subprocess สำหรับ Windows
            if os.name == 'nt':  # Windows
                import subprocess
                # สร้าง process ใหม่และปิด process เดิม
                subprocess.Popen([python, script] + sys.argv[1:])
                # บังคับปิด process ปัจจุบัน
                os._exit(0)
            else:  # Linux/Unix
                os.execv(python, [python, script] + sys.argv[1:])
                
        except Exception as e:
            print(f"❌ Error in safe restart: {e}")
            os._exit(0)
    def _stop_all_threads_and_timers(self):
        """หยุด thread และ timer ทั้งหมดก่อนปิดแอป"""
        try:
            print("🛑 Stopping all threads and timers...")
            
            # ✅ หยุด PLC thread
            if hasattr(self, 'plc_window') and self.plc_window:
                if hasattr(self.plc_window, 'stop_threads'):
                    self.plc_window.stop_threads()
            
            # ✅ หยุด shot counter timer
            if hasattr(self, 'shot_counter') and self.shot_counter:
                if hasattr(self.shot_counter, '_update_timer') and self.shot_counter._update_timer.isActive():
                    self.shot_counter._update_timer.stop()
            
            # ✅ หยุด heat map timer
            if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                if hasattr(self.heat_map_defect, '_update_timer') and self.heat_map_defect._update_timer.isActive():
                    self.heat_map_defect._update_timer.stop()
            
            # ✅ หยุด main window timer
            if hasattr(self, '_update_timer') and self._update_timer.isActive():
                self._update_timer.stop()
                
            print("✅ All threads and timers stopped")
            
        except Exception as e:
            print(f"⚠️ Error stopping threads and timers: {e}")
            
    def update_logout_window_theme(self):
        """อัพเดตธีมใน LogoutWindow เมื่อธีมเปลี่ยน"""
        if hasattr(self, 'logout_window') and self.logout_window:
            # อัพเดต theme settings
            self.logout_window.theme_settings = self.theme_settings
            # อัพเดต icon
            self.logout_window.update_icons()
            print("✅ Updated LogoutWindow theme")

    def closeEvent(self, event):
        """จัดการการปิดหน้าต่างหลัก"""
        try:
            # ป้องกันการจัดการซ้ำซ้อน
            if self._is_handling_close:
                event.ignore()
                return

            print("🔒 Close event triggered")
            
            # ถ้ายังไม่ได้ Logout (ผู้ใช้อยู่ใน Main หลัง login)
            if not self.is_logged_out:
                # แสดงกล่องข้อความยืนยันแทนการบังคับ Logout
                reply = QMessageBox.question(
                    self, 
                    "Confirm Exit",
                    "Do you want to exit without finishing the Lot?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    print("✅ User confirmed exit without finishing lot")
                    
                    # บันทึกข้อมูล Shot Count ล่าสุดก่อนออก (เพื่อความปลอดภัย)
                    if hasattr(self, 'shot_counter') and self.shot_counter:
                        try:
                            self.shot_counter._save_shot_count()
                            print("💾 Shot count saved before exit")
                        except Exception as e:
                            print(f"⚠️ Error saving shot count: {e}")
                            
                    self._cleanup_before_exit()
                    event.accept()
                else:
                    print("❌ User canceled exit")
                    event.ignore()
                return

            # ถ้าเป็นสถานะ logged out แล้ว ให้ทำ cleanup และยอมปิด
            print("✅ Proceeding with normal shutdown (already logged out)")
            self._cleanup_before_exit()
            event.accept()
            
        except Exception as e:
            print(f"❌ Error in closeEvent: {e}")
            # ในกรณีผิดพลาด ให้ปิดแบบบังคับ
            self._force_quit()


    def _cleanup_before_exit(self):
        """ทำความสะอาดก่อนปิดแอป"""
        try:
            print("🧹 Cleaning up before exit...")
            
            # 1. หยุด thread และ timer
            self._stop_all_threads_and_timers()
            
            # 2. ปิด PLC connection
            if hasattr(self, 'plc_window') and self.plc_window:
                try:
                    if hasattr(self.plc_window, 'close_connection'):
                        self.plc_window.close_connection()
                    self.plc_window.close()
                except Exception as e:
                    print(f"⚠️ Error closing PLC: {e}")
            
            # 3. ลบ reference
            if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                try:
                    # เรียกเมธอด cleanup ถ้ามี
                    if hasattr(self.heat_map_defect, 'stop'):
                        try:
                            self.heat_map_defect.stop()
                        except Exception:
                            pass
                    if hasattr(self.heat_map_defect, 'close'):
                        try:
                            self.heat_map_defect.close()
                        except Exception:
                            pass

                    # พยายาม disconnect สัญญาณที่ผูกไว้
                    try:
                        self.product_info_updated.disconnect(self.heat_map_defect.set_product_info)
                    except Exception:
                        pass

                    # ล้าง reference ให้ GC เก็บ
                    self.heat_map_defect = None
                except Exception as e:
                    print(f"⚠️ Error cleaning up heat map: {e}")
            
            if hasattr(self, 'shot_counter') and self.shot_counter:
                try:
                    self.shot_counter = None
                except Exception as e:
                    print(f"⚠️ Error clearing shot counter: {e}")
            
            # 4. รอให้กระบวนการปิดเสร็จ
            import time
            time.sleep(0.5)
            
            print("✅ Cleanup before exit completed")
            
        except Exception as e:
            print(f"❌ Error during cleanup: {e}")

    def _force_quit(self):
        """บังคับปิดแอปพลิเคชัน"""
        try:
            print("🛑 Force quitting application...")
            QApplication.quit()
            # ✅ ใช้ os._exit เพื่อบังคับปิดทุก thread
            os._exit(0)
        except Exception as e:
            print(f"❌ Error force quitting: {e}")
            os._exit(1)

    def force_logout_before_exit(self):
        """บังคับให้ผู้ใช้ทำการ logout ก่อนออกจากโปรแกรม"""
        try:
            print("🔄 Forcing logout before exit...")

            # ✅ ป้องกันการเปิดซ้ำซ้อน
            if hasattr(self, 'force_logout_dialog') and self.force_logout_dialog:
                self.force_logout_dialog.activateWindow()
                return

            from src.logout_window import LogoutWindow
            
            # ✅ เปลี่ยนเป็น self.force_logout_dialog
            self.force_logout_dialog = LogoutWindow(
                parent=self,
                shot_counter=self.shot_counter,
                theme_settings=self.theme_settings,
                data_uploader=self.data_uploader # ✅ Pass DataUploader
            )
            
            # ✅ ตั้งค่าให้ลบตัวเองเมื่อปิด
            self.force_logout_dialog.setAttribute(Qt.WA_DeleteOnClose)
            
            self.force_logout_dialog.setWindowModality(Qt.ApplicationModal)
            
            self.force_logout_dialog.logout_completed.connect(
                self.handle_forced_logout_completion
            )
            
            # ✅ (เพิ่มใหม่) เชื่อมต่อสัญญาณ destroyed 
            # เพื่อรีเซ็ตสถานะหากหน้าต่างนี้ถูกปิด (โดยไม่ logout)
            self.force_logout_dialog.destroyed.connect(
                self.handle_forced_logout_closed
            )
            
            self.force_logout_dialog.show()

            print("✅ Forced logout window shown")
            
        except Exception as e:
            print(f"❌ Error forcing logout: {e}")
            # ถ้าเกิดข้อผิดพลาด ให้รีเซ็ตสถานะ
            self._is_handling_close = False
            self._logout_for_shutdown = False
            self._force_quit() # หรือ QCoreApplication.quit()
    @Slot()
    def handle_forced_logout_closed(self):
        """
        [เพิ่มใหม่]
        ถูกเรียกเมื่อหน้าต่าง force_logout_dialog ถูกปิด (destroyed)
        """
        print("ℹ️ Forced logout window was closed.")
        
        # ลบ reference
        self.force_logout_dialog = None
        
        # ตรวจสอบว่าเรา *ยังไม่ได้* logout
        # (ถ้า logout สำเร็จ self.is_logged_out จะเป็น True ไปแล้ว)
        if not self.is_logged_out:
            # ถ้าหน้าต่างถูกปิด แต่ยังไม่ได้ logout 
            # หมายความว่าผู้ใช้ "ยกเลิก" การปิด
            print("⚠️ User canceled the forced logout. Resetting close state.")
            self._is_handling_close = False
            self._logout_for_shutdown = False
    def _kill_zombie_processes(self):
        """ฆ่ากระบวนการ Python ที่ค้างอยู่"""
        try:
            current_pid = os.getpid()
            current_script = os.path.basename(sys.argv[0])
            
            print(f"🔍 Checking for zombie processes... Current PID: {current_pid}")
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # ตรวจสอบว่าเป็น Python process และรันสคริปต์เดียวกัน
                    if (proc.info['name'] and 'python' in proc.info['name'].lower() and
                        proc.info['cmdline'] and len(proc.info['cmdline']) > 1 and
                        current_script in proc.info['cmdline'][1] and
                        proc.info['pid'] != current_pid):
                        
                        print(f"🧟 Found zombie process: PID {proc.info['pid']}")
                        proc.terminate()  # ส่ง signal terminate
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                
        except Exception as e:
            print(f"⚠️ Error killing zombie processes: {e}")
    @Slot()
    def handle_forced_logout_completion(self):
        """จัดการเมื่อบังคับ logout สำเร็จ (clean shutdown)"""
        try:
            print("✅ Forced logout completed (clean shutdown start)")
            self.is_logged_out = True
            self._is_handling_close = False

            # stop threads/timers
            try:
                self._stop_all_threads_and_timers()
            except Exception as e:
                print(f"⚠️ Error stopping threads/timers: {e}")

            # cleanup heatmap
            try:
                if hasattr(self, 'heat_map_defect') and self.heat_map_defect:
                    try:
                        if hasattr(self.heat_map_defect, 'stop'):
                            self.heat_map_defect.stop()
                    except Exception as e:
                        print(f"⚠️ heat_map_defect.stop() error: {e}")
                    try:
                        if hasattr(self.heat_map_defect, 'close'):
                            self.heat_map_defect.close()
                    except Exception:
                        pass
                    try:
                        self.product_info_updated.disconnect(self.heat_map_defect.set_product_info)
                    except Exception:
                        pass
                    self.heat_map_defect = None
            except Exception as e:
                print(f"⚠️ Error cleaning heat_map_defect: {e}")

            # cleanup plc
            try:
                if hasattr(self, 'plc_window') and self.plc_window:
                    try:
                        if hasattr(self.plc_window, 'close_connection'):
                            self.plc_window.close_connection()
                    except Exception:
                        pass
                    try:
                        self.plc_window.close()
                    except Exception:
                        pass
                    self.plc_window = None
            except Exception as e:
                print(f"⚠️ Error closing plc_window: {e}")

            # other cleanup
            try:
                self._cleanup_before_exit()
            except Exception as e:
                print(f"⚠️ _cleanup_before_exit error: {e}")

            try:
                QCoreApplication.quit()
            finally:
                os._exit(0)
                        
        except Exception as e:
            print(f"❌ Fatal error in forced logout handler: {e}")
            self._is_handling_close = False
            try:
                QCoreApplication.quit()
            finally:
                os._exit(1)
                
    def get_current_lot_number(self):
        user_info = self.login_manager.get_user_info()
        product_info = self.login_manager.get_data_scan()

        lot_number = None
        if user_info and 'lot_number' in user_info:
            lot_number = user_info['lot_number']
        elif product_info and 'lot_number' in product_info:
            lot_number = product_info['lot_number']

        return lot_number

    def update_label_with_product_info(self):
        try:
            # ใช้ login_manager ที่ถูกต้องในการดึงข้อมูล
            get_data_login = self.login_manager.get_data_scan()  # ตรวจสอบว่า get_data_scan() คืนค่าถูกต้อง

            if get_data_login:
                product_name = get_data_login.get('product_name', 'N/A')
                lot_number   = get_data_login.get('lot_number', 'N/A')
                tooling_code = get_data_login.get('tooling_code', 'N/A')
                operator_name= get_data_login.get('operator_name', 'N/A')
                operator_id  = get_data_login.get('operator_id', 'N/A')

                # อัปเดต UI ด้วยข้อมูลที่ได้รับ
                self.ui.product_name.setText(f": {product_name}")
                self.ui.lot_number.setText(f": {lot_number}")
                self.ui.tooling_code.setText(f": {tooling_code}")
                self.ui.operator_name.setText(f": {operator_name}")
                # ✅ ส่งข้อมูลผ่าน Signal ไปยัง HeatMapDefectPCS
                product_data = {
                    'product_name': product_name,
                    'lot_number': lot_number,
                    'tooling_code': tooling_code,
                    'operator_name': operator_name,
                    'operator_id': operator_id
                }
                self.product_info_updated.emit(product_data)
            else:
                print("Error: No product data found.")
                self.ui.product_name.setText("Error: No data found.")
        except Exception as e:
            error_msg = f"Error retrieving product scan: {str(e)}"
            print(error_msg)
            self.ui.product_name.setText(f"Error: {error_msg}")

    #Get the theme chanfe process
    def sassCompilationProgress(self, n):
        self.ui.activityProgress.setValue(n)

########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    # ✅ Force English Locale to prevent Thai numerals in UI
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    
    app = QApplication(sys.argv)
    
    try:
        ########################################################################
        app_tooltip_filter = QCustomQToolTipFilter(tailPosition= "auto")
        app.installEventFilter(app_tooltip_filter)

       # ✅ ให้แอปพลิเคชันปิดเมื่อหน้าต่างสุดท้ายถูกปิด (ช่วยให้สามารถรันซ้ำจาก VSCode ได้)
        app.setQuitOnLastWindowClosed(True)

        window = MainWindow()
        if window.isVisible():
            window.show()
        
        # ✅ ตรวจสอบว่า initialization สำเร็จ
        if hasattr(window, '_initialization_complete') and window._initialization_complete:
            print("🚀 Application started successfully")
            app_exec = app.exec()
        else:
            print("❌ Application initialization failed")
            app_exec = 1
        
        # ✅ ทำความสะอาดก่อนปิด
        print("🔚 Application is shutting down...")
        
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        app_exec = 1
        
    finally:
        # เอา event filter ออกก่อน interpreter ปิด (ป้องกัน traceback ที่เกิดจาก eventFilter ระหว่าง shutdown)
        try:
            app.removeEventFilter(app_tooltip_filter)
        except Exception:
            pass

        # ✅ บังคับปิด process
        import os
        os._exit(app_exec)