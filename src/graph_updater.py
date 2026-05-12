from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt, QObject, QTimer
from src.graph_manager import GraphManager
import logging

log = logging.getLogger("SmartOST.graph")

class GraphUpdater(QObject):
    def __init__(self, plc_window, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.graph_manager = GraphManager()
        self.plc_window = plc_window
        self.current_chart = None
        self.last_values = {"good_pcs": -1, "ng_pcs": -1, "good_sheet": -1, "ng_sheet": -1}
        self.last_data = None

        # อัพเดตกราฟเมื่อ PLC ส่ง data_updated เท่านั้น — ไม่ใช้ polling timer
        # เพื่อป้องกัน double-update และ UI กระตุก
        self.plc_window.data_updated.connect(self.handle_plc_data_update)

    def handle_plc_data_update(self, data):
        """รับการอัปเดตข้อมูลจาก PLC และอัปเดตกราฟ"""
        try:
            if data == self.last_data:
                return

            logging.info("\n--- Received PLC Data Update ---")
            logging.info("PLC Raw Data: %s", data)
            
            # ตรวจสอบค่าที่จำเป็น
            required_values = {
                'dm1917': data.get('dm1917', 0),
                'dm1919': data.get('dm1919', 0),
                'dm1924': data.get('dm1924', 0),
                'dm1925': data.get('dm1925', 0)
            }
            
            new_values = {
                "good_pcs":   max(0, required_values['dm1919']),
                "ng_pcs":     max(0, required_values['dm1917'] - required_values['dm1919']),
                "good_sheet": max(0, required_values['dm1924']),
                "ng_sheet":   max(0, required_values['dm1925'])
            }
            
            logging.info("Calculated Values: %s", new_values)
            
            # ตรวจสอบการเปลี่ยนแปลง
            if new_values == self.last_values:
                logging.info("Data unchanged, skipping update")
                return
                
            self.last_values = new_values
            self.last_data = data
            
            # อัปเดต UI ใน thread หลัก
            QTimer.singleShot(0, lambda: self._update_ui(new_values, data))
            
        except Exception as e:
            logging.exception("Error in handle_plc_data_update")

    def _update_ui(self, new_values, data):
        try:
            if self.parent is None or not hasattr(self.parent, 'ui'):
                logging.error("Parent or parent.ui is not available")
                return

            if self.current_chart is None:
                self._initialize_chart(new_values)
            else:
                try:
                    self.graph_manager.update_chart_data(
                        self.current_chart,
                        new_values["good_pcs"],
                        new_values["ng_pcs"],
                        new_values["good_sheet"],
                        new_values["ng_sheet"]
                    )
                except Exception as e:
                    logging.error("Failed to update chart, reinitializing...")
                    self.current_chart = None
                    self._initialize_chart(new_values)
            
            self._update_progress_bars(data)
        except Exception as e:
            logging.exception("Error in _update_ui")

    def _calculate_values(self, data):
        try:
            return {
                "good_pcs": max(0, data.get('dm1919', 0)),
                "ng_pcs": max(0, data.get('dm1917', 1) - data.get('dm1919', 0)),
                "good_sheet": max(0, data.get('dm1924', 0)),
                "ng_sheet": max(0, data.get('dm1925', 0))
            }
        except Exception as e:
            logging.exception("Error in _calculate_values")
            return {"good_pcs": 0, "ng_pcs": 0, "good_sheet": 0, "ng_sheet": 0}

    def _initialize_chart(self, new_values):
        """สร้างกราฟครั้งแรก"""
        try:
            if self.parent is None or not hasattr(self.parent, 'ui'):
                logging.error("Cannot initialize chart - parent or parent.ui is None")
                return

            layout = self.parent.ui.widget_chart_area.layout()
            if layout is None:
                logging.error("Chart area layout is None")
                return
            
            # ล้าง widget เก่าทั้งหมด
            while layout.count():
                item = layout.takeAt(0)
                if item and item.widget():
                    item.widget().deleteLater()
            
            self.current_chart = self.graph_manager.create_double_donut_chart(
                new_values["good_pcs"],
                new_values["ng_pcs"],
                new_values["good_sheet"],
                new_values["ng_sheet"]
            )
            
            if self.current_chart:
                layout.addWidget(self.current_chart)
            else:
                logging.error("Failed to create chart")
        except Exception as e:
            logging.exception("Error in _initialize_chart")

    def _update_progress_bars(self, data):
        try:
            if self.parent is None or not hasattr(self.parent, 'ui'):
                logging.error("Cannot update progress bars - parent or parent.ui is None")
                return

            defects = {
                "SHORT": data.get('dm1911', 0),
                "OPEN": data.get('dm1912', 0),
                "BLKM": data.get('dm1915', 0),
                "MAT": data.get('dm1914', 0),
                "SHOT": data.get('dm1913', 0)
            }
            
            self.graph_manager.display_plc_values(
                list(defects.keys()),
                list(defects.values()),
                self.parent.ui.scrollAreaWidgetContents
            )
        except Exception as e:
            logging.exception("Error in _update_progress_bars")

    def cleanup(self):
        """ล้างทรัพยากรทั้งหมด"""
        try:
            if self.current_chart:
                self.current_chart.deleteLater()
                self.current_chart = None
                
            if hasattr(self, 'graph_manager'):
                self.graph_manager.cleanup()
                
            if hasattr(self, 'timer') and self.timer.isActive():
                self.timer.stop()
                
            if hasattr(self, 'plc_window'):
                self.plc_window.close()
        except Exception as e:
            logging.exception("Error in cleanup")