from src.PLCdata import PLCWindow
import logging
from src.app_logger import get_logger

log = get_logger("update_mgr")

class update_sever:
    def __init__(self, plc_window, parent=None):
        self.parent = parent
        self.plc_window = plc_window
        self.plc_window.data_updated.connect(self.get_data_from_PLC)

    def get_data_from_PLC(self, data):
        #print("=== get_data_from_PLC called ===")
        #print("Received data from PLC:", data)

        # เตรียมค่าที่จำเป็น
        required_values = {
            'dm1917': data.get('dm1917', 0),
            'dm1919': data.get('dm1919', 0),
            'dm1924': data.get('dm1924', 0),
            'dm1925': data.get('dm1925', 0),
            'dm1923': data.get('dm1923', 0)
        }

        # คำนวณค่าใหม่จากค่าที่ได้รับ
        new_values = {
            "good_pcs": max(0, required_values['dm1919']),
            "ng_pcs": max(0, required_values['dm1917'] - required_values['dm1919']),
            "good_sheet": max(0, required_values['dm1924']),
            "ng_sheet": max(0, required_values['dm1925']),
            "total_sheet": max(0, required_values['dm1923'])
        }

        # เก็บค่า defects
        defects = {
            "SHORT": data.get('dm1911', 0),
            "OPEN": data.get('dm1912', 0),
            "BLKM": data.get('dm1915', 0),
            "MAT": data.get('dm1914', 0),
            "SHOT": data.get('dm1913', 0)
        }

        # ดึง lot_number จาก plc_window
        lot_number = None
        if hasattr(self.plc_window, "get_current_lot_number"):
            lot_number = self.plc_window.get_current_lot_number()

        # เตรียมข้อมูลสำหรับ upload
        upload_data = {
            'lot_number': lot_number,
            'good_pcs': new_values['good_pcs'],
            'ng_pcs': new_values['ng_pcs'],
            'total_sheet': new_values['total_sheet'],
            'good_sheet': new_values['good_sheet'],
            'reject_sheet': new_values['ng_sheet'],
            'defects': defects,
            'total_pcs': new_values['good_pcs'] + new_values['ng_pcs']  # เพิ่มฟิลด์นี้
        }

        #print("Prepared upload data:", upload_data)

        # เรียก upload ผ่าน parent.data_uploader.update_counts_only()
        if hasattr(self.parent, 'data_uploader'):
            try:
                result = self.parent.data_uploader.update_counts_only(upload_data)
                #print("Upload result:", result)
                if result.get('status') == 'success':
                    log.info("Uploaded to server")
                else:
                    log.error("Upload failed: %s", result.get('message'))
            except Exception as e:
                log.error("Exception during upload: %s", e)
        else:
            log.error("No data_uploader available in parent")