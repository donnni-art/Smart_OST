"""
excel_manager.py
================
จัดการไฟล์ Excel ทั้งหมดที่เกี่ยวกับการบันทึก Shot Count และ PM

หน้าที่หลัก:
  - สร้างและอัพเดตไฟล์ Excel จาก template
  - อ่านข้อมูล Lot/Shot จาก Excel เพื่อแสดงใน PM Window
  - คำนวณ PM Slot ถัดไปด้วย Linear Regression
  - ไฮไลท์เซลล์ PM ที่คาดการณ์ (เหลือง = ก่อน, แดง = ถัดไป)
  - Auto-save ทุก 30 shot ที่เพิ่มขึ้น

การใช้งาน:
  - สร้างขึ้นโดย ShotCounter ใน __init__:
      self.excel_mgr = ExcelManager(self)
  - เรียกใช้ผ่าน ShotCounter:
      self.excel_mgr.manual_save()
      self.excel_mgr.auto_save_check(old_count)
"""

import os
import math
import shutil
import numpy as np
from copy import copy
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill

from src.app_logger import get_logger
from sklearn.linear_model import LinearRegression

log = get_logger("excel")

# ─── Excel layout constants ──────────────────────────────────────────────────
_DATA_START_ROW = 7       # แถวแรกของข้อมูล lot
_DATA_END_ROW = 100       # แถวสุดท้ายที่สแกน
_DATA_COLS = range(2, 11) # คอลัมน์ B–J
_ROW_STEP = 3             # แถว data วางทุก 3 แถว (7, 10, 13 …)
_SLOT_SIZE = 9            # จำนวน slot ต่อแถว (คอลัมน์ B–J)
_PM_SHOT_LIMIT = 30_000   # จำนวน shot ที่ต้องทำ PM
_AUTO_SAVE_THRESHOLD = 30 # auto-save ทุก N shot


class ExcelManager:
    """
    จัดการไฟล์ Excel สำหรับบันทึก Shot Count และ PM

    Attributes:
        counter: ShotCounter instance (อ่าน/เขียน state ผ่าน reference)
    """

    def __init__(self, shot_counter):
        """
        Args:
            shot_counter: ShotCounter — owner ที่ ExcelManager อ่าน state จาก
        """
        self.counter = shot_counter

    # =========================================================================
    # PUBLIC API
    # =========================================================================

    def auto_save_check(self, old_shot_count: int) -> None:
        """
        ตรวจสอบและ auto-save เมื่อ shot เพิ่มขึ้นถึง threshold

        Args:
            old_shot_count: ค่า shot count ก่อนการอัพเดตล่าสุด
        """
        diff = self.counter.shot_count - self.counter.old_shot_count
        log.debug("Auto-save check: old=%d, new=%d, diff=%d",
                  self.counter.old_shot_count, self.counter.shot_count, diff)

        if diff >= _AUTO_SAVE_THRESHOLD:
            log.info("Auto-save triggered (+%d shots)", diff)
            self.manual_save()
            self.counter.old_shot_count = self.counter.shot_count
            self._show_status(f"Auto Save: {self.counter.shot_count} shots", 3000)
        else:
            log.debug("Auto-save not triggered: %d/%d shots", diff, _AUTO_SAVE_THRESHOLD)

    def manual_save(self) -> None:
        """
        บันทึก Shot Count ของ Lot ปัจจุบันลงไฟล์ Excel

        ขั้นตอน:
          1. ถ้าไม่มีไฟล์ Excel → copy จาก template และบันทึก header (B3)
          2. ค้นหา lot_number ในเซลล์ที่มีอยู่แล้ว → อัพเดต shot count
          3. ถ้าไม่พบ → แทนที่เลขลำดับว่างด้วย lot ใหม่
          4. ถ้าไม่มีที่ว่าง → เพิ่มแถวใหม่ท้ายตาราง
          5. คำนวณและไฮไลท์ PM slot ถัดไป
        """
        try:
            counter = self.counter
            txt_filename = os.path.basename(counter.file_path)
            excel_filename = os.path.splitext(txt_filename)[0] + ".xlsx"
            dest_path = os.path.join(counter.pm_in_progress_dir, excel_filename)
            lot_number = counter.product_data.get("lot_number", "N/A")
            shot_now = counter.shot_count

            os.makedirs(counter.pm_in_progress_dir, exist_ok=True)

            # ─── สร้างไฟล์ใหม่จาก template ถ้ายังไม่มี ──────────────────
            if not os.path.exists(dest_path):
                self._create_from_template(dest_path)
                self._save_header_b3(dest_path)

            wb = load_workbook(dest_path)
            ws = wb.active
            font_style = Font(name="Angsana New", size=12, bold=True)

            current_lot_shots = shot_now - counter.start_lot_shot
            log.debug("Lot shots this run: %d - %d = %d",
                      shot_now, counter.start_lot_shot, current_lot_shots)

            if current_lot_shots == 0:
                log.info("No new shots — skip save")
                self._show_status("No new shots in this lot, no need to save", 5000)
                return

            columns_to_resize = set()
            found = self._update_existing_lot(
                ws, lot_number, current_lot_shots, shot_now, font_style, columns_to_resize
            )
            if not found:
                found = self._fill_empty_slot(
                    ws, lot_number, current_lot_shots, shot_now, font_style, columns_to_resize
                )
            if not found:
                self._append_new_row(
                    ws, lot_number, current_lot_shots, shot_now, font_style, columns_to_resize
                )

            # ─── อัพเดต PM prediction ────────────────────────────────────
            predicted_slot = self._predict_next_pm_slot(ws)
            self._update_header_b3(ws, predicted_slot)
            if predicted_slot not in (None, "N/A", "Error"):
                self._highlight_predicted_slots(ws, predicted_slot)

            for col_letter in columns_to_resize:
                ws.column_dimensions[col_letter].width = 8

            wb.save(dest_path)
            log.info("Saved Excel to %s", dest_path)

        except Exception as e:
            log.exception("Error in manual_save: %s", e)

    def load_excel_data_for_pm(self, file_path: str):
        """
        อ่านข้อมูล Lot/Shot จากไฟล์ Excel เพื่อแสดงใน PM Window

        Args:
            file_path: path ของไฟล์ Excel

        Returns:
            tuple: (data_list, row_3b_value)
              data_list: list of (lot_id, shot_count) tuples
              row_3b_value: string ใน cell B3 หรือ None
        """
        data_list = []
        row_3b_value = None

        if not os.path.exists(file_path):
            log.warning("Excel file not found: %s", file_path)
            return data_list, row_3b_value

        try:
            wb = load_workbook(file_path)
            ws = wb.active

            cell_b3 = ws.cell(row=3, column=2)
            if cell_b3.value:
                row_3b_value = cell_b3.value
                log.debug("Read B3: %s", row_3b_value)

            for row in range(7, 22):
                for col in range(2, 11):
                    cell = ws.cell(row=row, column=col)
                    if isinstance(cell.value, str) and "shot" in cell.value:
                        try:
                            parts = cell.value.split("\n")
                            lot_id = parts[0] if parts else "N/A"
                            shot_count = int(parts[1].split("shot ")[1]) if len(parts) > 1 else 0
                            data_list.append((lot_id, shot_count))
                        except (ValueError, IndexError):
                            log.warning("Cannot parse cell %s: %s", cell.coordinate, cell.value)

            return data_list, row_3b_value

        except Exception as e:
            log.exception("Error loading Excel: %s", e)
            return [], None

    # =========================================================================
    # PRIVATE — ไฟล์และ template
    # =========================================================================

    def _create_from_template(self, dest_path: str) -> None:
        """Copy template .xlsx ไปยัง dest_path"""
        template_dir = self.counter.templates_dir
        templates = [f for f in os.listdir(template_dir) if f.lower().endswith(".xlsx")]
        if not templates:
            log.error("No .xlsx template found in %s", template_dir)
            raise FileNotFoundError(f"No template in {template_dir}")
        template_path = os.path.join(template_dir, templates[0])
        shutil.copy(template_path, dest_path)
        log.info("Created Excel from template: %s → %s", template_path, dest_path)

    def _save_header_b3(self, excel_path: str) -> None:
        """บันทึก header ข้อมูลสินค้า + lot ลงเซลล์ B3 (ใหม่)"""
        try:
            wb = load_workbook(excel_path)
            ws = wb.active
            ws["B3"] = self._build_header_text(next_pm="N/A")
            wb.save(excel_path)
            log.debug("Saved initial B3 header: %s", excel_path)
        except Exception as e:
            log.error("Cannot save B3 header: %s", e)

    def _build_header_text(self, next_pm: str) -> str:
        """สร้าง string header ที่แสดงในเซลล์ B3"""
        c = self.counter
        product_name = c.product_data.get("product_name", "N/A")
        tooling_code = c.product_data.get("tooling_code", "N/A")
        if tooling_code.startswith("OSTE"):
            tooling_type = "E-FPC"
        elif tooling_code.startswith("OSTM"):
            tooling_type = "SMT"
        else:
            tooling_type = "N/A"
        return (
            f"Product name:  {product_name}      "
            f"Tooling code:  {tooling_code}      "
            f"Tooling for:   {tooling_type}       "
            f"Next p.m.: {next_pm}"
        )

    # =========================================================================
    # PRIVATE — เขียนข้อมูลลงเซลล์
    # =========================================================================

    def _update_existing_lot(self, ws, lot_number, lot_shots, shot_now,
                              font_style, cols_to_resize) -> bool:
        """อัพเดต lot ที่มีอยู่แล้วในตาราง → คืน True ถ้าพบ"""
        for row in range(_DATA_START_ROW, _DATA_END_ROW + 1, _ROW_STEP):
            for col in _DATA_COLS:
                cell = self._resolve_merged(ws, row, col)
                label = str(cell.value).strip() if cell.value else ""
                if lot_number in label:
                    old_shots = self._extract_shot_count(label)
                    new_total = old_shots + lot_shots
                    cell.value = f"{lot_number}\nshot {new_total}"
                    cell.alignment = Alignment(wrapText=True)
                    cell.font = font_style
                    cols_to_resize.add(ws.cell(row=1, column=col).column_letter)
                    self.counter.start_lot_shot = shot_now
                    log.info("Updated lot %s at %s: +%d → %d",
                             lot_number, cell.coordinate, lot_shots, new_total)
                    return True
        return False

    def _fill_empty_slot(self, ws, lot_number, lot_shots, shot_now,
                          font_style, cols_to_resize) -> bool:
        """แทนที่ slot ว่าง (ค่าเป็น int) ด้วย lot ใหม่ → คืน True ถ้าพบ"""
        for row in range(_DATA_START_ROW, _DATA_END_ROW + 1, _ROW_STEP):
            for col in _DATA_COLS:
                cell = self._resolve_merged(ws, row, col)
                if isinstance(cell.value, int):
                    cell.value = f"{lot_number}\nshot {lot_shots}"
                    cell.alignment = Alignment(wrapText=True)
                    cell.font = font_style
                    cols_to_resize.add(ws.cell(row=1, column=col).column_letter)
                    self.counter.start_lot_shot = shot_now
                    log.info("Filled slot %s with new lot %s", cell.coordinate, lot_number)
                    return True
        return False

    def _append_new_row(self, ws, lot_number, lot_shots, shot_now,
                         font_style, cols_to_resize) -> None:
        """เพิ่มแถวใหม่ท้ายตารางเมื่อไม่มี slot ว่าง"""
        new_row = _DATA_END_ROW + 1
        cell = ws.cell(row=new_row, column=2)
        cell.value = f"{lot_number}\nshot {lot_shots}"
        cell.alignment = Alignment(wrapText=True)
        cell.font = font_style
        cols_to_resize.add("B")
        self.counter.start_lot_shot = shot_now
        log.info("Appended new row %d for lot %s", new_row, lot_number)

    # =========================================================================
    # PRIVATE — PM Prediction
    # =========================================================================

    def _predict_next_pm_slot(self, ws) -> object:
        """
        คำนวณ slot PM ถัดไปด้วย Linear Regression

        อ่าน shot count สะสมในแต่ละ slot แล้ว fit เส้นตรง
        เพื่อหาว่า slot ที่เท่าไรจะถึง 30,000 shot

        Returns:
            int slot number, "N/A" ถ้าข้อมูลน้อยเกินไป, "Error" ถ้า exception
        """
        try:
            shot_data = []
            slot_indices = []
            slot_index = 0

            for row in range(_DATA_START_ROW, _DATA_END_ROW + 1, _ROW_STEP):
                for col in _DATA_COLS:
                    slot_index += 1
                    cell = self._resolve_merged(ws, row, col)
                    if cell.value and isinstance(cell.value, str) and "shot" in cell.value:
                        try:
                            shot_val = int(cell.value.split("shot")[-1].strip())
                            shot_data.append(shot_val)
                            slot_indices.append(slot_index)
                        except (ValueError, IndexError):
                            continue

            if len(shot_data) < 2:
                return "N/A"

            cumulative = []
            total = 0
            for s in shot_data:
                total += s
                cumulative.append(total)

            X = np.array(slot_indices).reshape(-1, 1)
            y = np.array(cumulative)
            model = LinearRegression()
            model.fit(X, y)

            slope = model.coef_[0]
            if abs(slope) < 1e-6:
                return "N/A"

            predicted = math.ceil((_PM_SHOT_LIMIT - model.intercept_) / slope)
            max_slots = sum(
                1 for r in range(_DATA_START_ROW, _DATA_END_ROW + 1, _ROW_STEP)
                for _ in _DATA_COLS
            )
            predicted = max(1, min(predicted, max_slots))
            prev = max(predicted - 1, 1)
            self.counter._next_pm_pair = f"{prev}-{predicted}"
            log.info("PM prediction: slot %d (pair %s)", predicted, self.counter._next_pm_pair)
            return predicted

        except Exception as e:
            log.exception("Prediction error: %s", e)
            return "Error"

    def _update_header_b3(self, ws, predicted_slot) -> None:
        """อัพเดตเซลล์ B3 ด้วยข้อมูล PM ล่าสุด"""
        try:
            next_pm_text = getattr(self.counter, "_next_pm_pair", "N/A")
            cell = ws["B3"]
            old_fill = copy(cell.fill)
            cell.value = self._build_header_text(next_pm=next_pm_text)
            cell.fill = old_fill
            log.debug("Updated B3 with next PM: %s", next_pm_text)
        except Exception as e:
            log.error("Error updating B3: %s", e)

    def _highlight_predicted_slots(self, ws, predicted_slot) -> None:
        """ไฮไลท์เซลล์ PM (เหลือง = ก่อน, แดง = ที่คาดการณ์)"""
        try:
            pred = int(predicted_slot)
        except Exception:
            log.warning("predicted_slot is not an int: %s", predicted_slot)
            return

        try:
            yellow = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
            red = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

            self._reset_table_colors(ws)

            prev = max(pred - 1, 1)
            for slot_num, fill in ((prev, yellow), (pred, red)):
                row = _DATA_START_ROW + ((slot_num - 1) // _SLOT_SIZE) * _ROW_STEP
                col = 2 + ((slot_num - 1) % _SLOT_SIZE)
                cell = self._resolve_merged(ws, row, col)
                cell.fill = fill
                log.debug("Highlighted slot %d at %s", slot_num, cell.coordinate)

            self.counter._next_pm_pair = f"{prev}-{pred}"
        except Exception as e:
            log.exception("Error highlighting slots: %s", e)

    def _reset_table_colors(self, ws) -> None:
        """ล้างสีทุกเซลล์ในตารางก่อนไฮไลท์ใหม่"""
        no_fill = PatternFill(fill_type=None)
        for row in range(_DATA_START_ROW, _DATA_END_ROW, _ROW_STEP):
            for col in _DATA_COLS:
                cell = self._resolve_merged(ws, row, col)
                cell.fill = no_fill

    # =========================================================================
    # PRIVATE — helpers
    # =========================================================================

    @staticmethod
    def _resolve_merged(ws, row: int, col: int):
        """คืน master cell ของ merged range หรือ cell ปกติ"""
        cell = ws.cell(row=row, column=col)
        for merged_range in ws.merged_cells.ranges:
            if cell.coordinate in merged_range:
                return ws.cell(merged_range.min_row, merged_range.min_col)
        return cell

    @staticmethod
    def _extract_shot_count(label: str) -> int:
        """แยก shot count จาก string เช่น 'LOT001\\nshot 1500' → 1500"""
        try:
            return int(label.split("shot ")[-1])
        except (ValueError, IndexError):
            return 0

    def _show_status(self, message: str, ms: int = 3000) -> None:
        """แสดง status bar message ถ้ามี"""
        try:
            parent = self.counter.parent
            if parent and hasattr(parent, "ui") and hasattr(parent.ui, "statusbar"):
                parent.ui.statusbar.showMessage(message, ms)
        except Exception:
            pass
