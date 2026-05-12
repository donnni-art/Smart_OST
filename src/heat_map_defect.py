"""
heat_map_defect.py
==================
วิเคราะห์และแสดงแผนที่ defect (Heat Map) แบบ real-time

หน้าที่หลัก:
  - รับข้อมูล defect จาก PLC (DM1923 bitmap) และแปลงเป็น per-PCS record
  - สร้าง Heat Map (matplotlib) แสดงตำแหน่ง defect บน grid แม่พิมพ์
  - สร้าง Stacked Bar Chart แสดงสัดส่วน defect ตามประเภท
  - บันทึก raw data ลงไฟล์ JSON สำหรับวิเคราะห์ย้อนหลัง
  - throttle การ redraw ด้วย QTimer (200ms) เพื่อไม่ให้ UI กระตุก

การใช้งาน:
  - สร้างโดย MainWindow ใน __init__:
      self.heat_map_defect = HeatMapDefectPCS(self.plc_window, self)
  - รับ product info ผ่าน signal:
      self.product_info_updated.connect(self.heat_map_defect.set_product_info)
  - รีเซ็ต: self.heat_map_defect.clear_heatmap()

ความสัมพันธ์กับโมดูลอื่น:
  - PLCWindow     : subscribe data_updated signal รับ DM1923 + shot count
  - config_manager: อ่าน path สำหรับบันทึก raw data
  - MainWindow    : embed canvas ใน QFrame ของ ui
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Slot, QTimer, Qt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import re
from matplotlib.figure import Figure
from PySide6.QtWidgets import QSizePolicy
from matplotlib import patches as mpatches
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import os
import json
from datetime import datetime
from src.config_manager import config_manager
class HeatMapDefectPCS:
    def __init__(self, plc_window, parent_window=None):
        self.plc_window = plc_window
        self.parent = parent_window
        self.plc_window = plc_window
        # โหลด configuration
        self.paths_config = config_manager.get_paths_config()
        self.defect_data_path = config_manager.get_full_path(self.paths_config.get('defect_data', 'defect_raw_data'))
        if not os.path.exists(self.defect_data_path):
            os.makedirs(self.defect_data_path, exist_ok=True)

        self.last_dm1923 = None
        self.last_shot_cnt = None
        self.current_dm1923 = None
        self.quadmesh = None
        self.result_all_by_pcs = {}
        self.result_defect_only = {}
        self.defect_data_for_heatmap = {}
        self.current_product_name = None
        self.current_lot_number = None
        # ตัวแปรสำหรับระบบบันทึกข้อมูล
        self.current_product_info = {
            'product_name': 'Unknown',
            'lot_number': 'Unknown', 
            'tooling_code': 'Unknown',
            'operator_name': 'Unknown',
            'operator_id': 'Unknown'
        }
        self.current_data_folder = None
        self.raw_data_records = []
        self.raw_data_file = None
        self.metadata_file = None
        self.session_start_time = None

        self._update_timer = QTimer()
        self._update_timer.setSingleShot(True)
        self._update_timer.setInterval(200)
        self._update_pending = False
        self._update_timer.timeout.connect(self._perform_throttled_update)
        self.is_first_data = True
        self.first_dm1923_checked = False

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        if hasattr(self.parent.ui, 'heat_map'):
            if self.parent.ui.heat_map.layout():
                QWidget().setLayout(self.parent.ui.heat_map.layout())

            layout = QVBoxLayout()
            self.parent.ui.heat_map.setLayout(layout)
            layout.addWidget(self.canvas)
            self.canvas.draw()

        if self.plc_window:
            self.plc_window.data_updated.connect(self.handle_plc_data)

        self.plot_stacked_bar_defects()

    @Slot(dict)
    def set_product_info(self, product_data):
        """Slot สำหรับรับข้อมูลผลิตภัณฑ์จาก MainWindow"""
        try:
            product_name = product_data.get('product_name', 'Unknown')
            lot_number = product_data.get('lot_number', 'Unknown')
            
            print(f"📥 HeatMapDefectPCS received product: {product_name}, lot: {lot_number}")
            
            # ✅ ตรวจสอบว่าเป็นผลิตภัณฑ์ใหม่หรือไม่
            if (product_name != self.current_product_name or 
                lot_number != self.current_lot_number):
                
                print("🔄 New product/lot detected - resetting heatmap data")
                
                # รีเซ็ตข้อมูล
                self.result_all_by_pcs = {}
                self.result_defect_only = {}
                self.defect_data_for_heatmap = {}
                self.last_dm1923 = None
                self.last_shot_cnt = None
                self.first_dm1923_checked = False
                
                # อัพเดตข้อมูลปัจจุบัน
                self.current_product_name = product_name
                self.current_lot_number = lot_number
                
                # ล้างและแสดง heatmap ใหม่
                self.clear_heatmap()
                self.plot_stacked_bar_defects()
                
            else:
                print("ℹ️ Same product/lot - no reset needed")
                
        except Exception as e:
            print(f"❌ Error in set_product_info: {e}")
            
    @Slot(dict)
    def set_product_info(self, product_data):
        """Slot สำหรับรับข้อมูลผลิตภัณฑ์จาก MainWindow"""
        try:
            product_name = product_data.get('product_name', 'Unknown')
            lot_number = product_data.get('lot_number', 'Unknown')
            tooling_code = product_data.get('tooling_code', 'Unknown')
            operator_name = product_data.get('operator_name', 'Unknown')
            operator_id = product_data.get('operator_id', 'Unknown')
            
            new_product_info = {
                'product_name': product_name,
                'lot_number': lot_number,
                'tooling_code': tooling_code,
                'operator_name': operator_name,
                'operator_id': operator_id
            }
            
            print(f"📥 HeatMapDefectPCS ได้รับข้อมูลผลิตภัณฑ์:")
            print(f"   Product: {product_name}")
            print(f"   Lot: {lot_number}")
            print(f"   Tooling: {tooling_code}")
            
            # ตรวจสอบว่าข้อมูลเปลี่ยนแปลงหรือไม่
            if self.has_product_changed(new_product_info):
                print("🔄 ตรวจพบการเปลี่ยนแปลง Product/Lot")
                
                # บันทึกข้อมูลเก่าก่อนเปลี่ยน (ถ้ามี)
                if self.raw_data_records:
                    self.finalize_current_batch()
                
                # อัพเดตข้อมูลใหม่
                self.current_product_info = new_product_info
                self.is_product_info_ready = True
                self.setup_product_based_logging()
                
                # รีเซ็ตข้อมูลใน memory
                self.raw_data_records = []
                self.result_all_by_pcs = {}
                self.result_defect_only = {}
                self.defect_data_for_heatmap = {}
                
                # รีเซ็ต UI
                self.clear_heatmap()
                self.plot_stacked_bar_defects()
            else:
                print("ℹ️ ข้อมูลผลิตภัณฑ์เหมือนเดิม ไม่มีการเปลี่ยนแปลง")
                
        except Exception as e:
            print(f"❌ ข้อผิดพลาดใน set_product_info: {e}")

    def has_product_changed(self, new_info):
        """ตรวจสอบว่าข้อมูลผลิตภัณฑ์เปลี่ยนแปลงหรือไม่"""
        if self.current_product_info['product_name'] == 'Unknown':
            return True
            
        return (self.current_product_info['product_name'] != new_info['product_name'] or 
                self.current_product_info['lot_number'] != new_info['lot_number'])

    def setup_product_based_logging(self):
        """ตั้งค่าระบบบันทึกข้อมูลตาม Product และ Lot"""
        try:
            # สร้างชื่อโฟลเดอร์และไฟล์ตาม product และ lot
            product_name_clean = self.sanitize_filename(self.current_product_info['product_name'])
            lot_number_clean = self.sanitize_filename(self.current_product_info['lot_number'])
            
            # โครงสร้างโฟลเดอร์: defect_raw_data/{product_name}/{lot_number}/
            self.current_data_folder = os.path.join(
                self.defect_data_path,
                product_name_clean,
                lot_number_clean
            )
            
            if not os.path.exists(self.current_data_folder):
                os.makedirs(self.current_data_folder)
                print(f"✅ สร้างโฟลเดอร์ใหม่: {self.current_data_folder}")

            # ชื่อไฟล์
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.raw_data_file = os.path.join(
                self.current_data_folder, 
                f"defect_data_{current_time}.csv"
            )
            
            # ไฟล์ metadata
            self.metadata_file = os.path.join(
                self.current_data_folder, 
                "metadata.json"
            )
            
            # เริ่ม session ใหม่
            self.session_start_time = datetime.now()
            self.raw_data_records = []
            
            # บันทึก metadata
            self.save_metadata()
            
            print(f"🎯 เริ่มบันทึกข้อมูลสำหรับ:")
            print(f"   Product: {self.current_product_info['product_name']}")
            print(f"   Lot: {self.current_product_info['lot_number']}")
            print(f"   โฟลเดอร์: {self.current_data_folder}")
            
        except Exception as e:
            print(f"❌ ข้อผิดพลาดใน setup_product_based_logging: {e}")

    def sanitize_filename(self, name):
        """ทำความสะอาดชื่อไฟล์"""
        cleaned = re.sub(r'[<>:"/\\|?*]', '_', str(name))
        return cleaned.strip()[:50]

    def save_metadata(self):
        """บันทึก metadata ของ product และ lot"""
        try:
            metadata = {
                'product_info': self.current_product_info,
                'session_start': self.session_start_time.isoformat(),
                'data_file': self.raw_data_file,
                'total_records': len(self.raw_data_records),
                'last_update': datetime.now().isoformat(),
                'software_version': '1.0'
            }
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึก metadata ได้: {e}")

    @Slot(dict)
    def handle_plc_data(self, data):
        shot = data.get("shot_number", "")
        shot_cnt = data.get("dm1923", "")  # ใช้ dm1923 เป็น shot_cnt
        
        if not self.first_dm1923_checked:
            if shot_cnt >= 0 :  # มีค่า dm1923 จริง
                self.last_shot_cnt = shot_cnt
                self.first_dm1923_checked = True
                return
            else:
                return

        # ข้ามข้อมูลซ้ำ
        if shot_cnt == self.last_shot_cnt:
            self.last_shot_cnt = shot_cnt
            return

        # อัปเดตค่าและเริ่มทำงานจริง
        self.last_shot_cnt = shot_cnt
        defects_dict = self.parse_defect_results(data.get("defect_results", ""))
        
        # บันทึกข้อมูลดิบ
        self.add_raw_data_record(shot_cnt, defects_dict)
        
        self.process_for_heatmap(defects_dict)
        self.summary_result(shot_cnt)
        
        # ตั้งค่าการอัพเดตกราฟ
        self._update_pending = True
        if not self._update_timer.isActive():
            self._update_timer.start()

    def add_raw_data_record(self, shot_cnt, parsed_defects):
        """เพิ่มบันทึกข้อมูลดิบพร้อมข้อมูล product"""
        # ตรวจสอบอีกครั้งว่าข้อมูลผลิตภัณฑ์พร้อม
        if not self.is_product_info_ready or self.current_product_info is None:
            print("⚠️  ระบบบันทึกข้อมูลยังไม่พร้อม ข้ามการบันทึก")
            return
            
        timestamp = datetime.now()
        
        for shot_key, pcs_list in parsed_defects.items():
            shot_name = shot_key.replace(":", "").strip()
            
            for pcs_info in pcs_list:
                pcs_name_full = pcs_info['pcs'].split(':')[0].strip()
                result_string = pcs_info['result']
                defect_details = self.extract_defect_counts(result_string)
                
                # ✅ แก้ไข: แยกเฉพาะหมายเลข PCS และเปลี่ยนเป็นรูปแบบ PCS1, PCS2, ...
                pcs_match = re.search(r'P(\d+)', pcs_name_full)  # หาตัวเลขหลัง P
                if pcs_match:
                    pcs_number = pcs_match.group(1)  # ได้ตัวเลข 1, 2, 3, ...
                    pcs_name = f"PCS{pcs_number}"    # เปลี่ยนเป็น PCS1, PCS2, ...
                else:
                    pcs_name = pcs_name_full  # fallback ถ้าไม่ match
                
                # แยก defect types
                defect_types_list = [dt for dt in defect_details.keys() 
                                   if dt not in ['total', 'PASS']]
                defect_types_str = ', '.join(defect_types_list) if defect_types_list else '-'
                
                # สร้าง record ข้อมูลดิบ
                raw_record = {
                    'Timestamp': timestamp.time().strftime('%H:%M:%S'),
                    'Product_Name': self.current_product_info['product_name'],
                    'Lot_Number': self.current_product_info['lot_number'],
                    'Tooling_Code': self.current_product_info['tooling_code'],
                    'Operator_Name': self.current_product_info['operator_name'],
                    'Operator_ID': self.current_product_info['operator_id'],
                    'Date': timestamp.date().isoformat(),
                    'Shot_CNT(Sheet)': shot_cnt,
                    'Shot': shot_name,
                    'PCS': pcs_name,  # ✅ ใช้ pcs_name ที่เป็น PCS1, PCS2, ...
                    'Defect_Result_String': result_string,
                    'Total_Defects': defect_details.get('total', 0),
                    'Defect_Types': defect_types_str,
                    'OPEN': defect_details.get('OPEN', 0),
                    'SHORT': defect_details.get('SHORT', 0),
                    'BLKM': defect_details.get('BLKM', 0),
                    'MAT': defect_details.get('MAT', 0),
                    'SHOT': defect_details.get('SHOT', 0),
                    'Result': 'PASS' if defect_details.get('total', 0) == 0 else 'FAIL',
                    'Time': timestamp.time().strftime('%H:%M:%S')
                }
                
                # เพิ่ม record ลงใน memory
                self.raw_data_records.append(raw_record)
                
                # บันทึกลงไฟล์ทันที
                self.append_to_raw_data_file(raw_record)
        
        print(f"✅ บันทึกข้อมูลสำหรับ {self.current_product_info['product_name']} - Lot {self.current_product_info['lot_number']}")

    def append_to_raw_data_file(self, record):
        """เพิ่ม record ใหม่ลงไฟล์ CSV"""
        try:
            df_record = pd.DataFrame([record])
            
            if not os.path.exists(self.raw_data_file):
                # สร้างไฟล์ใหม่
                df_record.to_csv(self.raw_data_file, index=False, encoding='utf-8-sig')
                print(f"📁 สร้างไฟล์ใหม่: {os.path.basename(self.raw_data_file)}")
            else:
                # เพิ่มลงไฟล์ที่มีอยู่
                df_record.to_csv(self.raw_data_file, mode='a', header=False, 
                               index=False, encoding='utf-8-sig')
                
        except Exception as e:
            print(f"❌ ไม่สามารถบันทึกข้อมูลดิบลงไฟล์ได้: {e}")

    def finalize_current_batch(self):
        """บันทึกและปิด batch ปัจจุบันก่อนเปลี่ยน product/lot"""
        if self.raw_data_records:
            print(f"💾 บันทึกข้อมูลสุดท้ายสำหรับ {self.current_product_info['product_name']} - {self.current_product_info['lot_number']}")
            print(f"   จำนวน records: {len(self.raw_data_records)}")

    @Slot()
    def _perform_throttled_update(self):
        """เมธอดนี้จะถูกเรียกเมื่อ Timer หมดเวลา"""
        if self._update_pending:
            self.update_heatmap()
            self._update_pending = False

    def parse_defect_results(self, defect_text):
        """แปลงผลลัพธ์จากสตริงเป็น Dictionary"""
        defects = {}
        current_shot = None
        
        for line in defect_text.split('\n'):
            if line.strip().startswith("SHOT "):
                match = re.search(r"SHOT (\d+):", line.strip())
                if match:
                    current_shot = f"SHOT {match.group(1)}"
                    if current_shot not in defects:
                        defects[current_shot] = []
                else:
                    current_shot = None
            elif "→" in line and current_shot:
                pcs_info = {
                    "pcs": line.split("→")[0].strip(),
                    "result": line.split("→")[1].strip()
                }
                if current_shot:
                    defects[current_shot].append(pcs_info)
                
        return defects

    def extract_defect_counts(self, result_string):
        """
        แยกประเภทและจำนวน Defect จากสตริงผลลัพธ์
        """
        defect_counts = {}
        
        # ตรวจสอบกรณี PASS/OK
        if "PASS" in result_string or "OK" in result_string:
            return {'total': 0}
        
        # แยกจำนวน total defects
        total_defects = 0
        total_match = re.search(r'(\d+)\s*defect[s]?', result_string)
        if total_match:
            total_defects = int(total_match.group(1))
        
        # แยก defect types ด้วย regex ที่ทนทานกว่า
        defect_types = re.findall(r'([A-Z]+)(?:\s*,\s*)?', result_string.split('(')[0])
        
        # นับ defect types
        for d_type in defect_types:
            if d_type != "PASS" and d_type != "OK":
                defect_counts[d_type] = defect_counts.get(d_type, 0) + 1
        
        # ถ้าไม่เจอใน regex ให้ใช้ผลรวมจาก dict แทน
        if total_defects == 0:
            total_defects = sum(defect_counts.values())
        
        defect_counts['total'] = total_defects
        return defect_counts

    def process_for_heatmap(self, parsed_defects):
        """
        ประมวลผลข้อมูลจาก parsed_defects เพื่อเตรียมสำหรับ Heat Map
        """
        for shot_key, pcs_list in parsed_defects.items():
            shot_name = shot_key.replace(":", "") 
            if shot_name not in self.defect_data_for_heatmap:
                self.defect_data_for_heatmap[shot_name] = {}
            
            for pcs_info in pcs_list:
                pcs_name_full = pcs_info['pcs'].split(':')[0].strip() 
                defect_details = self.extract_defect_counts(pcs_info['result'])
                self.defect_data_for_heatmap[shot_name][pcs_name_full] = defect_details
        
        print("Processed for Heatmap:", self.defect_data_for_heatmap)

    def summary_result(self, shot_cnt):
        if shot_cnt == self.last_dm1923:
            return
        
        self.last_dm1923 = shot_cnt
        
        # Reset data when shot_cnt is 0
        if shot_cnt == 0:
            print(f"\n📌 [RESET] shot count: {shot_cnt} - Resetting data...")
            self.result_all_by_pcs = {}
            self.result_defect_only = {}
            self.defect_data_for_heatmap = {}
            
            # ล้างและแสดง heatmap เป็นสีเทา
            self.clear_heatmap()
            self.plot_stacked_bar_defects()
            return
        
        print(f"\n📌 [SHOT_CNT Changed]: {shot_cnt}")
        print("🔄 สร้างสรุปผลรวม...")

        # Process data only when shot_cnt is not 0
        for shot, pcs_dict in self.defect_data_for_heatmap.items():
            for pcs, defect_info in pcs_dict.items():
                total_defects_in_scan = defect_info.get('total', 0)

                # --- เก็บผลรวมรวมทั้ง PASS และ DEFECT (นับเป็นครั้งที่ตรวจสอบ) ---
                if pcs not in self.result_all_by_pcs:
                    self.result_all_by_pcs[pcs] = {"PASS": 0, "FAIL": 0} 

                if total_defects_in_scan == 0:
                    self.result_all_by_pcs[pcs]["PASS"] += 1
                else:
                    self.result_all_by_pcs[pcs]["FAIL"] += 1 

                # --- เก็บเฉพาะ Defect เท่านั้น (สำหรับ Stacked Bar Chart) ---
                if total_defects_in_scan > 0:
                    if pcs not in self.result_defect_only:
                        self.result_defect_only[pcs] = {}
                    for defect_type, count in defect_info.items():
                        if defect_type in ("total", "PASS"):
                            continue
                        self.result_defect_only[pcs][defect_type] = self.result_defect_only[pcs].get(defect_type, 0) + count

        self.plot_stacked_bar_defects()

        print("\n✅ [รวมทุกผล] result_all_by_pcs:")
        for pcs, results in self.result_all_by_pcs.items():
            print(f"{pcs}: {results}")

        print("\n✅ [เฉพาะ defect] result_defect_only:")
        for pcs, results in self.result_defect_only.items():
            print(f"{pcs}: {results}")

    def clear_heatmap(self):
        """ล้าง heatmap และแสดงพื้นหลังสีเทา"""
        self.ax.clear()
        
        # ตั้งค่าพื้นหลังเป็นสีเทา
        self.ax.set_facecolor('#f0f0f0')
        
        # แสดงข้อความ "No Data" หรือ "Waiting for Data"
        self.ax.text(0.5, 0.5, "No Data\nWaiting for Data", 
                    ha='center', va='center', 
                    color='gray', fontsize=12, fontweight='bold',
                    transform=self.ax.transAxes)
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        self.ax.set_title('RATIO (PASS/PCS) - RESET', fontsize=12, fontweight="bold")
        
        # ลบ colorbar ถ้ามี
        if hasattr(self, 'cbar') and self.cbar:
            try:
                self.cbar.remove()
                self.cbar = None
            except:
                pass
        
        self.canvas.draw()

    def plot_stacked_bar_defects(self):
        # ใช้ result_defect_only แสดงเฉพาะ Defect
        result_by_pcs = self.result_defect_only

        # กรองเฉพาะ PCS ที่มี Defect จริงๆ
        pcs_names = [pcs for pcs, defects in result_by_pcs.items() if defects]

        # ถ้าไม่มี PCS ที่มี Defect เลย
        if not pcs_names:
            # ตรวจสอบว่ามี figure อยู่แล้วหรือไม่
            if not hasattr(self, 'stacked_bar_fig'):
                # สร้าง figure เปล่า (ไม่มีข้อมูล)
                self.stacked_bar_fig = Figure(figsize=(8, 4))
                self.stacked_bar_ax = self.stacked_bar_fig.add_subplot(111)
                self.stacked_bar_canvas = FigureCanvas(self.stacked_bar_fig)
                self.stacked_bar_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
                # เพิ่ม Canvas เข้า Layout
                self._clear_stacked_bar_layout()
                layout = self.parent.ui.scrollAreaWidgetContents_2.layout()
                layout.addWidget(self.stacked_bar_canvas)
            else:
                # ไม่ต้องล้าง layout ใหม่ ถ้ามีอยู่แล้ว
                self.stacked_bar_ax.clear()

            # วาดกราฟ placeholder
            self.stacked_bar_ax.set_title("Total Defects per PCS (Waiting for Data)", fontsize=8, fontweight='bold')
            self.stacked_bar_ax.set_ylabel("Defect Count")
            self.stacked_bar_ax.set_xlim(0, 1)
            self.stacked_bar_ax.set_ylim(0, 1)
            
            # วาดกราฟโดยไม่ต้องสร้างใหม่ทั้งหมด
            self.stacked_bar_canvas.draw_idle()
            return

        # กำหนดลำดับ defect type (ใช้ของเดิมหากมีอยู่)
        desired_order = ['OPEN', 'BLKM', 'MAT', 'SHOT']
        all_defect_types = sorted({key for val in result_by_pcs.values() for key in val.keys() if key != 'total'})
        ordered_defects = [d for d in desired_order if d in all_defect_types] + \
                         [d for d in all_defect_types if d not in desired_order]

        # เตรียมข้อมูลสำหรับกราฟ
        data = {defect_type: [] for defect_type in ordered_defects}
        for pcs in pcs_names:
            for defect_type in ordered_defects:
                data[defect_type].append(result_by_pcs[pcs].get(defect_type, 0))

        # จัดกลุ่ม PCS และเรียงลำดับให้ถูกต้อง
        grouped_pcs = []
        pcs_names = sorted(
            [pcs for pcs, defects in result_by_pcs.items() if defects],
            key=lambda x: (int(re.search(r'S(\d+)', x).group(1)), 
                          int(re.search(r'P(\d+)', x).group(1)))
        )

        # แยกกลุ่ม Shot และเรียงลำดับ
        current_group = None
        groups = []
        for pcs in pcs_names:
            match = re.match(r'(S\d+)P\d+', pcs)
            group = match.group(1) if match else ''
            if group != current_group:
                current_group = group
                groups.append(current_group)
            grouped_pcs.append((pcs, current_group))

        # กำหนดตำแหน่งแกน X พร้อมเว้นช่องว่างระหว่างกลุ่ม
        x_positions = []
        pos = 0
        prev_group = None
        gap = 0.6
        for pcs, group in grouped_pcs:
            if prev_group is not None and group != prev_group:
                pos += gap
            x_positions.append(pos)
            pos += 1
            prev_group = group
        x = np.array(x_positions)

        # สร้างหรืออัปเดตกราฟ
        if not hasattr(self, 'stacked_bar_fig'):
            self.stacked_bar_fig = Figure(figsize=(max(8, len(x_positions)*0.4), 4))
            self.stacked_bar_ax = self.stacked_bar_fig.add_subplot(111)
            self.stacked_bar_canvas = FigureCanvas(self.stacked_bar_fig)
            self.stacked_bar_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # เพิ่ม Canvas เข้า Layout
            self._clear_stacked_bar_layout()
            layout = self.parent.ui.scrollAreaWidgetContents_2.layout()
            layout.addWidget(self.stacked_bar_canvas)
        else:
            # ล้างเฉพาะกราฟเก่าใน Axes
            self.stacked_bar_ax.clear()

        # วาดกราฟใหม่ด้วยข้อมูลอัปเดต
        bottom = np.zeros(len(pcs_names))
        custom_colors = {
                "OPEN": "#F57309",
                "SHORT": "#E60F19",
                "BLKM": "#D9F008",
                "SHOT": "#2105C0",
                "MAT": "#DF089F"
            }

        default_colors = plt.cm.tab20.colors
        color_map = {
            defect_type: custom_colors.get(defect_type, default_colors[i % len(default_colors)])
            for i, defect_type in enumerate(ordered_defects)
        }

        # วาด stacked bar
        bar_width = 0.3 if len(x) < 5 else 0.8
        for defect_type in ordered_defects:
            values = data[defect_type]
            bars = self.stacked_bar_ax.bar(x, values, bottom=bottom, color=color_map[defect_type], 
                                         label=defect_type, width=bar_width, alpha=0.70)
            for bar, val in zip(bars, values):
                if val > 0:
                    self.stacked_bar_ax.text(
                        bar.get_x() + bar.get_width()/2, 
                        bar.get_y() + bar.get_height()/2,
                        str(val), ha='center', va='center', fontsize=6, color='black'
                    )
            bottom += values

        # ปรับแต่งแกนและ Legend
        total_per_pcs = np.sum([data[dt] for dt in ordered_defects], axis=0)
        max_total = max(total_per_pcs) if len(total_per_pcs) > 0 else 0
        self.stacked_bar_ax.set_ylim(0, max_total * 1.1 if max_total > 0 else 1)
        self.stacked_bar_ax.set_xlim(x.min() - 0.5, x.max() + 0.5)
        self.stacked_bar_ax.set_yticks(np.arange(0, max_total + 1, 10))
        self.stacked_bar_ax.tick_params(axis='y', labelsize=6)

        # แสดงผลรวม defect บนยอดแท่ง
        for i, total in enumerate(total_per_pcs):
            if total > 0:
                self.stacked_bar_ax.text(
                    x[i], total + max_total*0.02, str(int(total)),
                    ha='center', va='bottom', fontsize=5, fontweight='bold',
                    color='black', bbox=dict(facecolor='white', edgecolor='none', alpha=0.75, pad=1)
                )

        self.stacked_bar_ax.set_xticks(x)
        formatted_labels = [label.replace('P', ' P') for label in pcs_names]
        self.stacked_bar_ax.set_xticklabels(formatted_labels, rotation=45, ha='right', fontsize=6)

        # แกนบน: ชื่อกลุ่ม (Shot)
        group_positions = {}
        for pcs, group in grouped_pcs:
            idx = pcs_names.index(pcs)
            xpos = x[idx]
            group_positions.setdefault(group, []).append(xpos)
        group_midpoints = {g: np.mean(pos_list) for g, pos_list in group_positions.items()}
        
        # ลบ ax_top ถ้ามีอยู่แล้ว
        if hasattr(self, 'ax_top'):
            self.ax_top.remove()
        
        self.ax_top = self.stacked_bar_ax.twiny()
        self.ax_top.set_xlim(self.stacked_bar_ax.get_xlim())
        self.ax_top.set_xticks(list(group_midpoints.values()))
        self.ax_top.set_xticklabels(list(group_midpoints.keys()), fontsize=5)
        self.ax_top.tick_params(axis='x', length=0)

        self.stacked_bar_ax.set_title('Total Defects per PCS', fontsize=8, fontweight='bold')
        self.stacked_bar_ax.set_ylabel("Defect Count")

        # สร้าง Legend
        dummy_patch = mpatches.Patch(color='white', label='Defect Type:')
        handles, labels = self.stacked_bar_ax.get_legend_handles_labels()
        handles = [dummy_patch] + handles
        labels = ['Defect Type:'] + labels
        legend = self.stacked_bar_ax.legend(
            handles, labels,
            loc='upper right',
            fontsize=6,
            frameon=True,
            facecolor='white',
            edgecolor='black',
            framealpha=0.5,
            ncol=1
        )
        legend.set_zorder(0)

        # วาดกราฟด้วย draw_idle เพื่อลดการกระพริบ
        self.stacked_bar_canvas.draw_idle()

    def _clear_stacked_bar_layout(self):
        """ล้าง Layout ของกราฟ Stacked Bar โดยไม่ทำลาย Figure"""
        layout = self.parent.ui.scrollAreaWidgetContents_2.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None and widget != getattr(self, 'stacked_bar_canvas', None):
                widget.setParent(None)

    def show_heatmap_error(self, error_msg):
        """แสดงข้อความผิดพลาดบน heatmap"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, f"Error:\n{error_msg}", 
                    ha='center', va='center', 
                    color='red', fontsize=6)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def _prepare_heatmap_data(self):
        df_data = []
        for pcs_name, counts in self.result_all_by_pcs.items():
            match = re.match(r'(S\d+)(P\d+)', pcs_name)
            if match:
                row = {
                    'shot': match.group(1),
                    'pcs': match.group(2),
                    'PASS': counts.get('PASS', 0),
                    'FAIL': counts.get('FAIL', 0)
                }
                
                # แก้ไขการคำนวณ Total: Total = PASS + FAIL
                row['Total'] = row['PASS'] + row['FAIL']
                
                # คำนวณ Pass_Ratio จาก PASS และ Total ที่ถูกต้อง
                if row['Total'] > 0:
                    row['Pass_Ratio'] = (row['PASS'] / row['Total'] * 100)
                else:
                    row['Pass_Ratio'] = 0

                df_data.append(row)

        if not df_data:
            return None

        df = pd.DataFrame(df_data)
        return df

    def update_heatmap(self):
        try:
            df = self._prepare_heatmap_data()
            if df is None or df.empty:
                print("[WARNING] No valid data for heatmap")
                return

            pivot_df = df.pivot(index='shot', columns='pcs', values='Pass_Ratio')
            
            # แก้ไข: เรียงลำดับ Shot ใหม่
            shot_nums = pivot_df.index.str.extract(r'S(\d+)')[0].astype(int)
            sorted_indices = shot_nums.argsort()
            pivot_df = pivot_df.iloc[sorted_indices]
            
            # แก้ไข: เรียงลำดับ PCS ใหม่
            pcs_nums = pivot_df.columns.str.extract(r'P(\d+)')[0].astype(int)
            sorted_cols = pcs_nums.argsort()
            pivot_df = pivot_df.iloc[:, sorted_cols]
            
            self._initialize_heatmap(pivot_df)
            self._update_annotations(pivot_df)
            
            # แก้ไข: พลิกแกน Y เพื่อให้ S1 อยู่ด้านบน
            self.ax.invert_yaxis()
            
            self.canvas.draw_idle()

        except Exception as e:
            print(f"[ERROR] Failed to update heatmap: {str(e)}")
            import traceback
            traceback.print_exc()

    def _initialize_heatmap(self, pivot_df):
        self.figure.clf()
        self.ax = self.figure.add_subplot(111)

        if hasattr(self, 'cbar') and self.cbar:
            try:
                self.cbar.remove()
            except Exception as e:
                print(f"[WARNING] Failed to remove colorbar: {e}")
            self.cbar = None

        if pivot_df.shape[0] < 2:
            dummy_row = pd.DataFrame(
                [[np.nan] * pivot_df.shape[1]],
                index=["dummy_row"],
                columns=pivot_df.columns
            )
            pivot_df = pd.concat([pivot_df, dummy_row])

        self.quadmesh = self.ax.pcolormesh(
            pivot_df.columns,
            pivot_df.index,
            pivot_df.values,
            cmap=self._create_cmap(),
            shading='auto',
            vmin=0,
            vmax=100
        )
        self.cbar = self.figure.colorbar(self.quadmesh, ax=self.ax, location='right')
        self.cbar.ax.tick_params(labelsize=8)
        # แกน X: PCS (P1, P2, ...)
        self.ax.set_xticks(np.arange(len(pivot_df.columns)))
        self.ax.set_xticklabels(pivot_df.columns, fontsize=8, rotation=45, ha='right')
        # แกน Y: SHOT (S1, S2, ...)
        self.ax.set_yticks(np.arange(len(pivot_df.index)))
        self.ax.set_yticklabels(pivot_df.index, fontsize=8)
        self.ax.set_title("RATIO (PASS/PCS) ", fontsize=8, fontweight="bold")

        # เพิ่มเส้นกริดรอบแต่ละเซลล์
        self.ax.set_xticks(np.arange(-0.5, len(pivot_df.columns), 1), minor=True)
        self.ax.set_yticks(np.arange(-0.5, len(pivot_df.index), 1), minor=True)
        self.ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        self.ax.tick_params(which='minor', bottom=False, left=False)

    def _update_annotations(self, pivot_df):
        for txt in self.ax.texts:
            txt.remove()

        # ใช้ตำแหน่งกลางของเซลล์ในการวางข้อความ
        for i, y in enumerate(pivot_df.index):
            for j, x in enumerate(pivot_df.columns):
                val = pivot_df.loc[y, x]
                if not pd.isna(val):
                    self.ax.text(
                        j,
                        i,
                        f"{val:.1f}",
                        ha='center',
                        va='center',
                        fontsize=8
                    )
    def stop(self):
        """Stop timers/threads and release resources safely."""
        try:
            # หยุด QTimer ถ้ามี
            if hasattr(self, 'update_timer') and self.update_timer:
                try:
                    self.update_timer.stop()
                except Exception:
                    pass

            # หยุดหรือ join worker thread ถ้ามี
            if hasattr(self, 'worker_thread') and self.worker_thread:
                try:
                    if hasattr(self.worker_thread, 'stop'):
                        self.worker_thread.stop()
                    if hasattr(self.worker_thread, 'join'):
                        self.worker_thread.join(timeout=1)
                except Exception:
                    pass

            # ยกเลิกการเชื่อมต่อสัญญาณที่อาจผูกกับ MainWindow
            try:
                # ตัวอย่าง: self.some_signal.disconnect()
                pass
            except Exception:
                pass

        except Exception as e:
            print(f"⚠️ HeatMapDefectPCS.stop() error: {e}")
            
    def _create_cmap(self):
        colors = [
            (0.0, "#a50026"),
            (0.2, "#d73027"),
            (0.4, "#f46d43"),
            (0.5, "#fdae61"),
            (0.6, "#fee08b"),
            (0.7, "#ffffbf"),
            (0.75, "#d9ef8b"),
            (0.8, "#a6d96a"),
            (0.85, "#66bd63"),
            (0.9, "#1a9850"),
            (1.0, "#006837")
        ]
        return LinearSegmentedColormap.from_list("custom_heatmap", colors)