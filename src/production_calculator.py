"""
production_calculator.py
========================
คำนวณ production rate แบบ real-time และแสดงผลใน UI

หน้าที่หลัก:
  - คำนวณ sheets/hour, pcs/hour, shots/hour, time/sheet ทุก 3 วินาที
  - ตรวจสอบ stale data (>120s) และ offline (>600s) จาก PLC
  - แสดงสีต่างๆ ใน UI ตามสถานะการเชื่อมต่อ

การใช้งาน:
  - สร้างโดย MainWindow ใน __init__:
      self.production_calculator = ProductionCalculator(self.plc_window, self)
      self.production_calculator.start_calculation()
  - หยุด: self.production_calculator.stop_calculation()

Signals:
  - production_rates_updated: Signal(dict) — ส่งค่า rate ล่าสุดไปยัง UI

ความสัมพันธ์กับโมดูลอื่น:
  - PLCWindow : subscribe data_updated signal เพื่อรับ shot count ล่าสุด
  - MainWindow: อัพเดต label ใน ui ผ่าน update_ui_directly()
"""

import time
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import logging

class ProductionCalculator(QObject):
    production_rates_updated = Signal(dict)  # Signal to update UI with rates
    
    def __init__(self, plc_window, main_window=None):
        super().__init__()
        self.plc_window = plc_window
        self.main_window = main_window
        self.logger = logging.getLogger(__name__)
        
        # Production tracking variables
        self.start_time = None
        self.last_sheet_count = 0
        self.last_data_received = None
        self.last_calc_time = None  # ✅ เพิ่มตัวแปรเก็บเวลาคำนวณล่าสุด
        
        # Configuration from PLC - ตั้งค่า default เป็น 0 ตามที่ต้องการ
        self.pcs_per_shot = 1      # ✅ ตั้งค่า default เป็น 0
        self.shots_per_sheet = 1   # ✅ ตั้งค่า default เป็น 0
        self.pcs_per_sheet = 1     # ✅ ตั้งค่า default เป็น 0
        
        # Current production rates - ตั้งค่าเริ่มต้นเป็น 0
        self.current_rates = {
            'sheets_per_hour': 0.0,
            'pcs_per_hour': 0.0,
            'shots_per_hour': 0.0,
            'time_per_sheet': 0.0,
            'time_per_piece': 0.0,
            'time_per_shot': 0.0,
            'pcs_per_shot': 0,
            'shots_per_sheet': 0,
            'pcs_per_sheet': 0,
            'total_sheets': 0
        }
        
        # Connection monitoring
        self.stale_threshold = 120    # >120s = stale (show blue)
        self.offline_threshold = 600  # >600s = offline (show gray)
        
        # Timer for periodic calculation
        self.calc_timer = QTimer()
        self.calc_timer.setInterval(3000)  # คำนวณทุก 3 วินาที
        self.calc_timer.timeout.connect(self.calculate_production_rates)
        
        # ✅ เชื่อมต่อ signal กับ internal method
        self.production_rates_updated.connect(self.update_ui_directly)
        
        self.logger.info("ProductionCalculator initialized with zero default configuration")
    
    def setup_ui_styling(self):
        """ตั้งค่าการแสดงผล UI สำหรับตัวเลข生产率"""
        try:
            if self.main_window and hasattr(self.main_window, 'ui'):
                ui = self.main_window.ui
                
                # ✅ กำหนดฟอนต์และสไตล์
                font = QFont()
                font.setPointSize(17)  # ขนาด 11pt
                font.setBold(True)     # ตัวหนา
                
                # ✅ ตั้งค่าสำหรับแต่ละ label
                rate_labels = ['sheet_per_ht', 'pcs_per_hr', 'shot_per_hr']
                
                for label_name in rate_labels:
                    if hasattr(ui, label_name):
                        label = getattr(ui, label_name)
                        
                        # ตั้งค่าฟอนต์
                        label.setFont(font)
                        
                        # ตั้งค่าสีดำ (ปกติ)
                        label.setStyleSheet("color: black; background-color: transparent;")
                        
                        # ตั้งค่าการจัดตำแหน่งให้อยู่กึ่งกลาง
                        label.setAlignment(Qt.AlignCenter)
                        
                        # ตั้งค่าเริ่มต้นเป็น "0"
                        label.setText("0")
                        label.setVisible(True)  # ✅ บังคับให้แสดงผล
                        
                        self.logger.info(f"Styled {label_name} with black, 11pt, bold, center alignment")
                
                # ✅ บังคับอัพเดต UI ทันทีหลังจากตั้งสไตล์
                self.update_ui_directly(self.current_rates)
                
        except Exception as e:
            self.logger.error(f"Error setting up UI styling: {e}")
    
    def update_configuration(self, plc_data):
        """อัพเดตการตั้งค่าจาก PLC data - ป้องกันค่าเป็น 0 และเพิ่ม fallback"""
        try:
            product_config = self.plc_window.get_updated_production_calculator()
            
            # ใช้ค่าจาก product_config เป็นหลัก
            new_pcs_per_shot = product_config.get('pcs_number', 0)
            new_shots_per_sheet = product_config.get('shot_number', 0)
            
            # ✅ ตรวจสอบค่าจาก PLC โดยตรงถ้าจาก product_config เป็น 0
            if new_pcs_per_shot <= 0:
                new_pcs_per_shot = plc_data.get('pcs_number', self.pcs_per_shot)
            
            if new_shots_per_sheet <= 0:
                new_shots_per_sheet = plc_data.get('shot_number', self.shots_per_sheet)
            
            # ✅ Fallback สุดท้าย: ใช้ค่าปัจจุบันถ้าทั้งหมดเป็น 0
            if new_pcs_per_shot <= 0:
                new_pcs_per_shot = self.pcs_per_shot if self.pcs_per_shot > 0 else 1  # default 1
            
            if new_shots_per_sheet <= 0:
                new_shots_per_sheet = self.shots_per_sheet if self.shots_per_sheet > 0 else 1  # default 1
            
            # คำนวณ PCS ต่อ sheet
            new_pcs_per_sheet = new_pcs_per_shot * new_shots_per_sheet
            
            # ตรวจสอบว่าการตั้งค่าเปลี่ยนไปหรือไม่
            config_changed = (
                new_pcs_per_shot != self.pcs_per_shot or
                new_shots_per_sheet != self.shots_per_sheet
            )
            
            if config_changed:
                self.pcs_per_shot = new_pcs_per_shot
                self.shots_per_sheet = new_shots_per_sheet
                self.pcs_per_sheet = new_pcs_per_sheet
                
                self.current_rates.update({
                    'pcs_per_shot': self.pcs_per_shot,
                    'shots_per_sheet': self.shots_per_sheet,
                    'pcs_per_sheet': self.pcs_per_sheet
                })
                
                self.logger.info(f"⚙️ Configuration updated: {self.pcs_per_shot} PCS/shot, {self.shots_per_sheet} shots/sheet, {self.pcs_per_sheet} PCS/sheet")
                
            return config_changed
            
        except Exception as e:
            self.logger.error(f"❌ Error updating configuration: {e}")
            return False

    def update_ui_directly(self, rates):
        """อัพเดต UI โดยตรง - ปรับปรุงให้ทำงานเสถียร"""
        try:
            if self.main_window and hasattr(self.main_window, 'ui'):
                ui = self.main_window.ui

                # --- คำนวณสถานะการเชื่อมต่อตามเวลา last_data_received ---
                current_time = time.time()
                elapsed = None
                if self.last_data_received:
                    elapsed = current_time - self.last_data_received
                else:
                    # ถ้าไม่มีการรับข้อมูลเลย ให้ถือว่า stale (แต่ยังไม่ offline)
                    elapsed = float('inf')

                # สถานะ: normal / stale / offline (ใช้ชุดสี S5)
                if elapsed <= self.stale_threshold:
                    color = "#000000"  # normal (black)
                    status = "normal"
                elif elapsed <= self.offline_threshold:
                    color = "#1E90FF"  # stale (blue)
                    status = "stale"
                else:
                    color = "#808080"  # offline (gray)
                    status = "offline"

                # ✅ อัพเดต sheets_per_hour
                sheets_per_hour = rates.get('sheets_per_hour', 0.0)
                if hasattr(ui, 'sheet_per_ht'):
                    formatted_sheets = self.format_rate_value(sheets_per_hour)
                    ui.sheet_per_ht.setText(formatted_sheets)
                    ui.sheet_per_ht.setStyleSheet(f"color: {color}; background-color: transparent;")
                    ui.sheet_per_ht.setVisible(True)

                # ✅ อัพเดต pcs_per_hour
                pcs_per_hour = rates.get('pcs_per_hour', 0.0)
                if hasattr(ui, 'pcs_per_hr'):
                    formatted_pcs = self.format_rate_value(pcs_per_hour)
                    ui.pcs_per_hr.setText(formatted_pcs)
                    ui.pcs_per_hr.setStyleSheet(f"color: {color}; background-color: transparent;")
                    ui.pcs_per_hr.setVisible(True)

                # ✅ อัพเดต shots_per_hour
                shots_per_hour = rates.get('shots_per_hour', 0.0)
                if hasattr(ui, 'shot_per_hr'):
                    formatted_shots = self.format_rate_value(shots_per_hour)
                    ui.shot_per_hr.setText(formatted_shots)
                    ui.shot_per_hr.setStyleSheet(f"color: {color}; background-color: transparent;")
                    ui.shot_per_hr.setVisible(True)

                # ✅ บังคับอัพเดต UI ทันที
                if hasattr(ui, 'sheet_per_ht'):
                    ui.sheet_per_ht.repaint()
                if hasattr(ui, 'pcs_per_hr'):
                    ui.pcs_per_hr.repaint()
                if hasattr(ui, 'shot_per_hr'):
                    ui.shot_per_hr.repaint()

                # log for debug
                self.logger.debug(f"UI Updated - Sheets: {sheets_per_hour}/h, PCS: {pcs_per_hour}/h, Shots: {shots_per_hour}/h, Status: {status}")

        except Exception as e:
            self.logger.error(f"Error updating UI directly: {e}")
    
    def format_rate_value(self, value):
        """จัดรูปแบบตัวเลขให้แสดงผลสวยงาม"""
        try:
            if value == 0:
                return "0"
            elif value < 1:
                return f"{value:.2f}"  # แสดงทศนิยม 2 ตำแหน่งสำหรับค่าต่ำมาก
            elif value < 10:
                return f"{value:.2f}"  # แสดงทศนิยม 2 ตำแหน่งสำหรับค่าต่ำ
            elif value < 100:
                return f"{value:.1f}"  # แสดงทศนิยม 1 ตำแหน่ง
            else:
                return f"{int(value)}"  # แสดงเป็นจำนวนเต็มสำหรับค่าสูง
        except:
            return "0"
    
    def start_calculation(self):
        """Start production rate calculation - ปรับปรุงการเริ่มต้น"""
        try:
            # ✅ ตั้งค่าสไตล์ UI ก่อนเริ่มคำนวณ
            self.setup_ui_styling()
            
            # Reset tracking variables
            self.start_time = time.time()
            self.last_data_received = time.time()
            self.last_calc_time = time.time()  # ✅ เริ่มต้นเวลาคำนวณ
            
            # Get initial values from PLC
            plc_data = self.plc_window.get_updated_production_calculator()
            if plc_data:
                # อัพเดตการตั้งค่าจาก PLC
                self.update_configuration(plc_data)
                
                # ✅ ตั้งค่าจำนวนแผ่นเริ่มต้น (สำคัญ!)
                self.last_sheet_count = plc_data.get('dm1923', 0)
                self.last_data_received = time.time()
                
                self.logger.info(f"Initial sheet count: {self.last_sheet_count}")
                
                # ✅ อัพเดต rates เริ่มต้นด้วย
                self.current_rates.update({
                    'total_sheets': self.last_sheet_count
                })
            
            # Start calculation timer
            self.calc_timer.start()
            self.logger.info("Production rate calculation started and timer running")
            
            # ✅ อัพเดต UI ทันทีด้วยค่าเริ่มต้น
            self.update_ui_directly(self.current_rates)
            
            # ✅ บังคับคำนวณครั้งแรกทันที
            QTimer.singleShot(1000, self.calculate_production_rates)
            
        except Exception as e:
            self.logger.error(f"❌ Error starting production calculation: {e}")
        
    def stop_calculation(self):
        """Stop production rate calculation"""
        try:
            if self.calc_timer.isActive():
                self.calc_timer.stop()
                self.logger.info("Production rate calculation stopped")
        except Exception as e:
            self.logger.error(f"Error stopping production calculation: {e}")
    
    def reset_calculation(self):
        """Reset calculation for new lot - ป้องกันการรีเซ็ตค่าเป็น 0"""
        try:
            # ไม่รีเซ็ต start_time และ last_data_received
            # คงค่า rates ไว้ ยกเว้นจะมีการเปลี่ยน product จริงๆ
            
            # อัพเดตค่าปัจจุบันจาก PLC เท่านั้น
            plc_data = self.plc_window.get_updated_production_calculator()
            if plc_data:
                self.last_sheet_count = plc_data.get('dm1923', self.last_sheet_count)  # ใช้ค่าเดิมเป็น fallback
                self.last_data_received = time.time()
                
            self.logger.info(f"Production calculation updated, sheet count: {self.last_sheet_count}")
            
        except Exception as e:
            self.logger.error(f"Error resetting production calculation: {e}")
    
    def calculate_production_rates(self):
        """Calculate current production rates - แก้ไข logic การคำนวณ"""
        try:
            current_time = time.time()
            
            self.logger.debug(f"Calculation triggered at {current_time}")
            
            if not self.start_time:
                self.start_time = current_time
                
            # Get current values from PLC
            plc_data = self.plc_window.get_updated_production_calculator()
            
            if plc_data:
                self.logger.debug(f"PLC data received: {plc_data.get('dm1923', 0)} sheets")
                
                # ✅ อัพเดตการตั้งค่าจาก PLC data
                config_changed = self.update_configuration(plc_data)
                
                # ✅ อัพเดตเวลาที่ได้รับข้อมูลล่าสุด
                self.last_data_received = time.time()
                
                # ✅ ดึงค่าจำนวนแผ่นปัจจุบัน
                current_sheet_count = plc_data.get('dm1923', 0)
                
                print(f"🔄 Calculation: current={current_sheet_count}, last={self.last_sheet_count}")
                
                # ✅ คำนวณผลต่างที่แท้จริง
                sheets_produced = current_sheet_count - self.last_sheet_count
                print(f"📊 Sheets produced this cycle: {sheets_produced}")
                
                # Calculate time elapsed (Incremental time)
                # ✅ ใช้เวลาจากรอบที่แล้ว (3 วินาที) แทนเวลาทั้งหมด
                if self.last_calc_time is None:
                    self.last_calc_time = self.start_time
                
                time_elapsed = current_time - self.last_calc_time
                
                if time_elapsed > 0 and sheets_produced > 0:  # ✅ เฉพาะเมื่อมี production
                    # ✅ คำนวณ PCS และ shots ที่ผลิตได้
                    pcs_produced = sheets_produced * self.pcs_per_sheet
                    shots_produced = sheets_produced * self.shots_per_sheet
                    
                    # Calculate rates per hour
                    time_per_sheet = time_elapsed / sheets_produced
                    sheets_per_hour = 3600 / time_per_sheet
                    
                    time_per_piece = time_elapsed / pcs_produced if pcs_produced > 0 else 0
                    pcs_per_hour = 3600 / time_per_piece if time_per_piece > 0 else 0
                    
                    time_per_shot = time_elapsed / shots_produced if shots_produced > 0 else 0
                    shots_per_hour = 3600 / time_per_shot if time_per_shot > 0 else 0
                    
                    # Update current rates
                    self.current_rates.update({
                        'sheets_per_hour': round(sheets_per_hour, 2),
                        'pcs_per_hour': round(pcs_per_hour, 2),
                        'shots_per_hour': round(shots_per_hour, 2),
                        'time_per_sheet': round(time_per_sheet, 2),
                        'time_per_piece': round(time_per_piece, 2),
                        'time_per_shot': round(time_per_shot, 2),
                        'total_sheets': current_sheet_count
                    })
                    
                    # ✅ อัพเดต last_sheet_count และ last_calc_time หลังจากคำนวณเสร็จแล้ว
                    self.last_sheet_count = current_sheet_count
                    self.last_calc_time = current_time
                    
                    self.logger.info(f"✅ Calculated rates - Sheets: {sheets_per_hour:.1f}/h, PCS: {pcs_per_hour:.1f}/h, Shots: {shots_per_hour:.1f}/h")
                    
                elif sheets_produced == 0:
                    # ✅ ไม่มี production ใหม่ แต่ยังคงแสดงค่าล่าสุด
                    self.logger.debug(" No new production, maintaining current rates")
                    # อัพเดตเวลาคำนวณล่าสุดแม้ไม่มีการผลิต เพื่อให้รอบถัดไปคำนวณจากช่วงเวลาที่ถูกต้อง
                    self.last_calc_time = current_time
                    
            else:
                self.logger.debug("❌ No PLC data received")
                
            # ✅ อัพเดต UI เสมอ (รักษาค่าล่าสุดไว้)
            self.production_rates_updated.emit(self.current_rates)
                
        except Exception as e:
            self.logger.error(f"❌ Error calculating production rates: {e}")
            self.production_rates_updated.emit(self.current_rates)
    
    def get_current_rates(self):
        """Get current production rates"""
        return self.current_rates
    
    def get_configuration(self):
        """Get current configuration"""
        return {
            'pcs_per_shot': self.pcs_per_shot,
            'shots_per_sheet': self.shots_per_sheet,
            'pcs_per_sheet': self.pcs_per_sheet
        }
    
    def print_debug_info(self):
        """พิมพ์ข้อมูล debug ไปที่ console"""
        config = self.get_configuration()
        current_time = time.time()
        elapsed = current_time - self.last_data_received if self.last_data_received else float('inf')
        
        print(f"""
    🎯 Production Calculator Debug Info:
    ═══════════════════════════════════
    📊 Current Rates:
       • Sheets: {self.current_rates['sheets_per_hour']}/h
       • PCS: {self.current_rates['pcs_per_hour']}/h  
       • Shots: {self.current_rates['shots_per_hour']}/h
    
    ⚙️ Configuration:
       • PCS per Shot: {config['pcs_per_shot']}
       • Shots per Sheet: {config['shots_per_sheet']}
       • PCS per Sheet: {config['pcs_per_sheet']}
    
    📈 Production Data:
       • Last Sheet Count: {self.last_sheet_count}
       • Total Sheets: {self.current_rates['total_sheets']}
       • Last Data Received: {elapsed:.1f}s ago
       • Timer Active: {'✅ Yes' if self.calc_timer.isActive() else '❌ No'}
    """)
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.calc_timer.isActive():
                self.calc_timer.stop()
            self.logger.info("ProductionCalculator cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during ProductionCalculator cleanup: {e}")