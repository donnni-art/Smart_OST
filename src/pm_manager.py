"""
pm_manager.py
=============
จัดการ workflow ทั้งหมดของ Preventive Maintenance (PM)

หน้าที่หลัก:
  - ตรวจสอบเงื่อนไข PM (shot count >= 30,000 หรือ predictive)
  - แสดง Login Dialog สำหรับยืนยันตัวตนก่อนเข้า PM
  - เปิด PM Window (Pmwindow) พร้อมข้อมูล Excel
  - จัดการ lifecycle ของ PM Window (เปิด/ปิด/ยกเลิก)
  - รับ Manual PM trigger จากปุ่มบนหน้าจอ

การใช้งาน:
  - สร้างโดย ShotCounter ใน __init__:
      self.pm_mgr = PMManager(self)
  - เรียกผ่าน ShotCounter:
      self.pm_mgr.check_pm_condition()
      self.pm_mgr.check_predictive_pm(shot_count, pcs_per_shot)
      self.pm_mgr.manual_pm_trigger()

ความสัมพันธ์กับโมดูลอื่น:
  - อ่าน/เขียน state ผ่าน self.counter (ShotCounter reference)
  - เรียก self.counter.excel_mgr.load_excel_data_for_pm()
  - ใช้ LoginPM, Pmwindow จาก src/
"""

import os
from src.app_logger import get_logger

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox
from PySide6.QtCore import Qt

log = get_logger("pm")

_PM_SHOT_LIMIT = 30_000  # จำนวน shot ที่ trigger PM อัตโนมัติ


class PMManager:
    """
    จัดการ Preventive Maintenance workflow

    Attributes:
        counter: ShotCounter — อ่าน/เขียน shot count, flags, product data
    """

    def __init__(self, shot_counter):
        """
        Args:
            shot_counter: ShotCounter instance ที่ PMManager ทำงานร่วมด้วย
        """
        self.counter = shot_counter

    # =========================================================================
    # PM CONDITION CHECKS
    # =========================================================================

    def check_pm_condition(self) -> None:
        """
        ตรวจสอบว่าถึงเวลาทำ PM หรือยัง (shot count >= 30,000)

        เรียกทุกครั้งที่ shot count เพิ่มขึ้น
        ถ้าเงื่อนไขครบ → เรียก handle_pm_needed() อัตโนมัติ
        """
        try:
            c = self.counter
            if (c.shot_count >= _PM_SHOT_LIMIT
                    and not c.pm_triggered
                    and not c.pm_window_visible):
                log.info("PM condition met: shot_count=%d >= %d", c.shot_count, _PM_SHOT_LIMIT)
                self.handle_pm_needed()
            else:
                log.debug("PM check: shot_count=%d, pm_triggered=%s", c.shot_count, c.pm_triggered)
        except Exception as e:
            log.exception("Error checking PM condition: %s", e)

    def check_predictive_pm(self, current_shot_count: int, pcs_per_shot: int) -> None:
        """
        คำนวณล่วงหน้าว่า lot ปัจจุบันจะเกิน shot limit หรือไม่

        ใช้สูตร: predicted = current + lot_size / pcs_per_shot
        ถ้า predicted > 30,000 → หยุดนับและ trigger PM

        Args:
            current_shot_count: shot count ปัจจุบัน
            pcs_per_shot: จำนวน PCS ต่อ 1 shot
        """
        try:
            c = self.counter
            lot_size = getattr(c, "lot_size_value", None)

            if not lot_size or lot_size <= 0 or pcs_per_shot <= 0:
                log.debug("Predictive PM: incomplete data (lot=%s, pcs=%d)",
                          lot_size, pcs_per_shot)
                return

            increment = lot_size / pcs_per_shot
            predicted = current_shot_count + increment

            log.debug("Predictive PM: current=%d + increment=%.2f = %.2f (limit=%d)",
                      current_shot_count, increment, predicted, _PM_SHOT_LIMIT)

            if predicted > _PM_SHOT_LIMIT:
                log.info("Predictive PM triggered: predicted=%.0f > %d", predicted, _PM_SHOT_LIMIT)
                c._should_stop_for_pm = True
                self._mark_shot_cnt_label_warning()
                if not c.pm_triggered and not c.pm_window_visible:
                    self.handle_pm_needed()
            else:
                c._should_stop_for_pm = False
                remaining = _PM_SHOT_LIMIT - predicted
                log.debug("Predictive PM: %.0f shots remaining", remaining)
                self._clear_shot_cnt_label_warning()

        except Exception as e:
            log.exception("Error in predictive PM check: %s", e)

    # =========================================================================
    # PM TRIGGER
    # =========================================================================

    def manual_pm_trigger(self) -> None:
        """
        PM ที่เรียกโดยผู้ใช้กดปุ่ม Manual PM

        แสดง confirmation dialog ก่อน ถ้ายืนยัน → handle_pm_needed(is_manual=True)
        """
        try:
            c = self.counter
            if c.pm_triggered or c.pm_window_visible:
                QMessageBox.information(
                    c.parent, "PM in Progress",
                    "Preventive Maintenance is already in progress.\nPlease wait."
                )
                return

            if not c.product_name or not c.product_name.strip():
                QMessageBox.warning(
                    c.parent, "Incomplete Data",
                    "Product information not found.\nPlease wait for machine data."
                )
                return

            reply = QMessageBox.question(
                c.parent,
                "Confirm Preventive Maintenance",
                (f"Do you want to perform Manual Preventive Maintenance?\n\n"
                 f"Product: {c.product_name}\n"
                 f"Current Shot Count: {c.shot_count}\n\n"
                 f"After PM completion:\n"
                 f"• Reset Shot Count to 0\n"
                 f"• Save PM data to system\n"
                 f"• Generate PM Report file"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                log.info("User confirmed Manual PM")
                self.handle_pm_needed(is_manual=True)
            else:
                log.info("User canceled Manual PM")

        except Exception as e:
            log.exception("Error in manual PM trigger: %s", e)
            QMessageBox.critical(c.parent, "Error", f"Error starting Manual PM:\n{e}")

    def handle_pm_needed(self, is_manual: bool = False) -> None:
        """
        เริ่มกระบวนการ PM (ทั้ง Auto และ Manual)

        ขั้นตอน:
          1. ตรวจสอบว่า PM ไม่ได้กำลังดำเนินการอยู่
          2. โหลดข้อมูล Excel สำหรับ PM Window
          3. เปิด Login Dialog (LoginPM) เพื่อยืนยันตัวตน
          4. ถ้า login สำเร็จ → เปิด PM Window

        Args:
            is_manual: True = ผู้ใช้กด Manual PM, False = Auto PM
        """
        c = self.counter
        if c.pm_triggered or c.pm_window_visible:
            log.warning("PM already in progress — skipping")
            return

        pm_type = "Manual" if is_manual else "Auto"
        log.info("Starting PM process (%s): shot_count=%d", pm_type, c.shot_count)
        c.pm_triggered = True

        excel_filename = f"shotcount_{c.product_name}.xlsx"
        excel_file = os.path.join(c.pm_in_progress_dir, excel_filename)
        lot_shot_data, row_3b_value = c.excel_mgr.load_excel_data_for_pm(excel_file)

        try:
            from src.login_pm import LoginPM
            login_dialog = LoginPM(parent=c.main_window, main_window=c.main_window)
            result = login_dialog.exec()

            if result == QDialog.Accepted and login_dialog.login_successful:
                login_data = login_dialog.get_login_data()
                log.info("PM login success (%s)", pm_type)
                self.show_pm_window(lot_shot_data, row_3b_value, login_data, is_manual)
            else:
                log.info("PM login canceled (%s)", pm_type)
                c.pm_triggered = False
                c.pm_window_visible = False
                c._should_stop_for_pm = False

        except Exception as e:
            log.exception("Error in PM login (%s): %s", pm_type, e)
            c.pm_triggered = False
            c.pm_window_visible = False

    # =========================================================================
    # PM WINDOW
    # =========================================================================

    def show_pm_window(self, lot_shot_data=None, row_3b_value=None,
                       login_data=None, is_manual: bool = False) -> None:
        """
        สร้างและแสดง PM Window (Pmwindow)

        Args:
            lot_shot_data: list of (lot_id, shot_count) จาก Excel
            row_3b_value: string ใน cell B3 ของ Excel
            login_data: dict ข้อมูล technician จาก LoginPM
            is_manual: ชนิดของ PM
        """
        c = self.counter
        pm_type = "Manual" if is_manual else "Auto"

        try:
            if c.pm_window_visible:
                log.warning("PM window already visible")
                return

            if c.parent is None:
                c.parent = QApplication.activeWindow()

            from src.pm_window import Pmwindow
            c.pm_window = Pmwindow(
                parent=c.parent,
                login_data=login_data,
                file_path=c.file_path,
                shot_counter=c,
            )
            c.pm_window_visible = True
            c.pm_window.is_logged_in = True

            title = f"Preventive Maintenance ({'Manual' if is_manual else 'Auto'}) — {c.product_name}"
            c.pm_window.setWindowTitle(title)

            if lot_shot_data is not None:
                c.pm_window.set_excel_data(lot_shot_data)
            if row_3b_value is not None:
                c.pm_window.parse_and_set_row_3b_data(row_3b_value)

            c.pm_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            c.pm_window.destroyed.connect(self.on_pm_window_closed)
            c.pm_window.show()
            log.info("PM window (%s) shown", pm_type)

        except Exception as e:
            log.exception("Error showing PM window (%s): %s", pm_type, e)

    def on_pm_window_closed(self) -> None:
        """เรียกเมื่อ PM Window ถูกปิด — reset state flags"""
        c = self.counter
        c.pm_window_visible = False
        c.pm_triggered = False
        c.pm_window = None
        log.info("PM window closed — flags reset")

    # =========================================================================
    # PRIVATE — UI helpers
    # =========================================================================

    def _mark_shot_cnt_label_warning(self) -> None:
        """เปลี่ยนสี shot_cnt label เป็นสีแดงเตือน"""
        try:
            ui = getattr(self.counter.parent, "ui", None)
            if ui and hasattr(ui, "shot_cnt"):
                ui.shot_cnt.setStyleSheet(
                    "background-color: #ffcccc; color: #cc0000; font-weight: bold;"
                )
        except Exception:
            pass

    def _clear_shot_cnt_label_warning(self) -> None:
        """คืนสี shot_cnt label กลับปกติ"""
        try:
            ui = getattr(self.counter.parent, "ui", None)
            if ui and hasattr(ui, "shot_cnt"):
                ui.shot_cnt.setStyleSheet("")
        except Exception:
            pass
