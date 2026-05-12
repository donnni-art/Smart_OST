"""
shot_counting.py
================
จัดการการนับ Shot Count และ Lot lifecycle ของเครื่องปั๊ม

หน้าที่หลัก:
  - รับข้อมูลจาก PLCWindow ผ่าน Signal data_updated
  - นับ shot count สะสม โดยเปรียบเทียบ total_sheet กับรอบก่อน
  - ตรวจจับการเปลี่ยน Product / การ reset total_sheet
  - บันทึก shot count ลงไฟล์ .txt พร้อม .bak safety copy
  - Delegate งาน Excel → ExcelManager
  - Delegate งาน PM workflow → PMManager

การใช้งาน (ถูก instantiate โดย MainWindow):
  shot_counter = ShotCounter(
      plc_window,
      parent_window=main_window,
      lot_size_value=product_info['lot_size_value'],
      product_data=product_data,
  )

โครงสร้าง internal:
  ShotCounter
    ├── excel_mgr : ExcelManager   ← Excel I/O ทั้งหมด
    └── pm_mgr   : PMManager       ← PM workflow ทั้งหมด
"""

import os
import sys
import shutil

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from src.app_logger import get_logger
from src.config_manager import config_manager
from src.excel_manager import ExcelManager
from src.pm_manager import PMManager

log = get_logger("shot")


class ShotCounter(QObject):
    """
    นับ shot count จากข้อมูล PLC และจัดการ lot lifecycle

    Signals:
        path_changed(str): ส่งเมื่อเปลี่ยน directory บันทึกข้อมูล

    Attributes:
        shot_count (int): shot count สะสมทั้งหมดของ tool นี้
        start_lot_shot (int): shot count ณ จุดเริ่มต้น lot ปัจจุบัน
        product_name (str): ชื่อ product ที่กำลังผลิต
        product_data (dict): ข้อมูล product (product_name, lot_number, tooling_code, ฯลฯ)
        excel_mgr (ExcelManager): จัดการไฟล์ Excel
        pm_mgr (PMManager): จัดการ PM workflow
    """

    path_changed = Signal(str)

    def __init__(self, plc_window, parent_window=None,
                 lot_size_value=1, product_data=None):
        """
        Args:
            plc_window: PLCWindow — แหล่งข้อมูล shot count จาก PLC
            parent_window: MainWindow — ใช้แสดง UI dialogs
            lot_size_value: จำนวน PCS ต่อ lot (สำหรับ predictive PM)
            product_data: dict ข้อมูลสินค้าจาก login
        """
        super().__init__()
        self.plc_window = plc_window
        self.parent = parent_window
        self.main_window = parent_window
        self.lot_size_value = lot_size_value
        self.product_data = product_data or {}

        self._initialize_variables()
        self._load_configuration()
        self._setup_directories()

        # ─── สร้าง sub-managers ─────────────────────────────────────────
        self.excel_mgr = ExcelManager(self)
        self.pm_mgr = PMManager(self)

        self._setup_connections()
        self._load_initial_data()

    # =========================================================================
    # INITIALIZATION
    # =========================================================================

    def _initialize_variables(self) -> None:
        """กำหนดค่าเริ่มต้นของทุก attribute"""
        # ─── state flags ────────────────────────────────────────────────
        self._should_stop_for_pm = False
        self.pm_triggered = False
        self.pm_window_visible = False
        self.pm_window = None
        self._just_reset = False
        self._next_pm_pair = None

        # ─── shot counting state ─────────────────────────────────────────
        self.max_shot_limit = 30_000
        self.shot_count = 0
        self.old_shot_count = 0
        self.start_lot_shot = 0
        self.last_total_sheet = None

        # ─── product state ───────────────────────────────────────────────
        self.product_name = None
        self.file_path = None

    def _load_configuration(self) -> None:
        """โหลด path config จาก config_manager"""
        self.paths_config = config_manager.get_paths_config()

    def _setup_directories(self) -> None:
        """สร้างโฟลเดอร์ที่จำเป็นถ้ายังไม่มี"""
        get = config_manager.get_full_path
        paths = self.paths_config

        self.base_dir = get(paths.get("shot_counts", "shot_counts"))
        self.pm_folder = get(paths.get("pm_folder", "PM"))
        self.pm_complete_dir = get(paths.get("pm_complete", "PM/PM compleat"))
        self.pm_in_progress_dir = get(paths.get("pm_in_progress", "PM/PM in Progress"))
        self.templates_dir = get(paths.get("templates", "templat"))

        for d in (self.pm_folder, self.pm_complete_dir, self.pm_in_progress_dir, self.templates_dir):
            os.makedirs(d, exist_ok=True)

    def _setup_connections(self) -> None:
        """เชื่อม Qt signals กับ handlers"""
        # ปุ่ม Manual PM
        parent_ui = getattr(self.parent, "ui", None)
        if parent_ui and hasattr(parent_ui, "pushButton_2"):
            try:
                parent_ui.pushButton_2.clicked.connect(self.manual_pm_trigger)
            except Exception as e:
                log.warning("Cannot connect PM button: %s", e)

        # ปุ่ม Finish Lot
        if parent_ui and hasattr(parent_ui, "finish_lot"):
            try:
                parent_ui.finish_lot.clicked.connect(self.parent.show_logout_window)
            except Exception as e:
                log.warning("Cannot connect finish_lot button: %s", e)

        self.path_changed.connect(self._on_path_changed)
        self.plc_window.data_updated.connect(self.handle_plc_update)

    def _load_initial_data(self) -> None:
        """โหลดข้อมูลเริ่มต้น: ตรวจ product change + โหลด shot count"""
        self._check_product_change()
        self._load_product_and_data()
        self._load_last_selected_directory()

    # =========================================================================
    # PATH & DIRECTORY MANAGEMENT
    # =========================================================================

    def _on_path_changed(self, new_path: str) -> None:
        """อัพเดต file_path ใน PM Window เมื่อ directory เปลี่ยน"""
        if self.pm_window:
            self.pm_window.file_path = new_path

    def _load_last_selected_directory(self) -> None:
        """โหลด directory ที่เลือกล่าสุดจาก config"""
        last_dir = (config_manager.current_config
                    .get("user_preferences", {})
                    .get("last_selected_directory", ""))
        if last_dir and os.path.exists(last_dir):
            self.custom_base_dir = last_dir
            log.debug("Loaded last directory: %s", last_dir)
        else:
            self.custom_base_dir = self.base_dir

    def select_save_directory(self) -> str:
        """
        เปิด dialog ให้ผู้ใช้เลือก directory สำหรับบันทึก shot count

        Returns:
            str: path ที่เลือก หรือ "" ถ้ายกเลิก
        """
        last_dir = (config_manager.current_config
                    .get("user_preferences", {})
                    .get("last_selected_directory", "") or self.base_dir)

        directory = QFileDialog.getExistingDirectory(
            self.parent, "Select Directory for Shot Count Data", last_dir
        )
        if not directory:
            return ""

        if "user_preferences" not in config_manager.current_config:
            config_manager.current_config["user_preferences"] = {}
        config_manager.current_config["user_preferences"]["last_selected_directory"] = directory
        config_manager.save_config()

        self.custom_base_dir = directory
        self._reload_data_from_new_directory(directory)
        self.path_changed.emit(self.file_path)
        return directory

    def _reload_data_from_new_directory(self, new_dir: str) -> None:
        """โหลดข้อมูล shot count ใหม่หลังเปลี่ยน directory"""
        try:
            old_count = self.shot_count
            self.custom_base_dir = new_dir
            self._load_product_and_data()
            if old_count != self.shot_count:
                log.info("Shot count changed after directory switch: %d → %d",
                         old_count, self.shot_count)
            parent_ui = getattr(self.parent, "ui", None)
            if parent_ui and hasattr(parent_ui, "shot_cnt"):
                parent_ui.shot_cnt.setText(str(self.shot_count))
            QMessageBox.information(
                self.parent, "Data Loaded",
                f"Data loaded from:\n{new_dir}\n\nCurrent Shot Count: {self.shot_count}"
            )
        except Exception as e:
            log.exception("Error reloading from directory: %s", e)
            QMessageBox.warning(self.parent, "Error", f"Cannot load data: {e}")

    # =========================================================================
    # PRODUCT & FILE PERSISTENCE
    # =========================================================================

    def _check_product_change(self) -> None:
        """ตรวจสอบว่า product เปลี่ยนหรือไม่ → reset ถ้าเปลี่ยน"""
        try:
            data = self.plc_window.get_product_and_shot_count()
            new_name = data.get("product_name", "")
            if new_name != self.product_name:
                log.info("Product changed: %s → %s", self.product_name, new_name)
                self._reset_for_new_product(new_name)
        except Exception as e:
            log.exception("Error checking product change: %s", e)

    def _reset_for_new_product(self, new_name: str) -> None:
        """
        Reset state เมื่อ product เปลี่ยน

        Args:
            new_name: ชื่อ product ใหม่
        """
        if not new_name or not new_name.strip():
            return
        self.product_name = new_name
        self.start_lot_shot = self.shot_count
        self.last_total_sheet = None
        self.file_path = os.path.join(self.base_dir, f"shotcount_{new_name}.txt")
        log.info("Reset for new product: %s (shot_count stays at %d)", new_name, self.shot_count)

    def _load_product_and_data(self) -> None:
        """
        โหลด product name และ shot count จากไฟล์ .txt

        ถ้าไม่มีไฟล์ → ใช้ 0 เป็นค่าเริ่มต้น
        โหลดเสร็จ → เรียก _save_shot_count() เพื่อยืนยัน
        """
        data = self.plc_window.get_product_and_shot_count()
        self.product_name = data.get("product_name", "").strip()

        if not self.product_name:
            log.warning("No product name from PLC")
            return

        base_dir = getattr(self, "custom_base_dir", self.base_dir)
        self.file_path = os.path.join(base_dir, f"shotcount_{self.product_name}.txt")

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    lines = f.read().strip().split("\n")
                self.shot_count = int(lines[0]) if lines[0].strip() else 0
                self.last_total_sheet = (
                    int(lines[1]) if len(lines) > 1 and lines[1].strip() else
                    data.get("total_sheet", 0)
                )
                log.info("Loaded shot_count=%d, last_total_sheet=%s from file",
                         self.shot_count, self.last_total_sheet)
            except Exception as e:
                log.error("Error loading shot count file: %s", e)
                self.shot_count = 0
        else:
            log.info("No shot count file found — starting at 0")

        self.start_lot_shot = self.shot_count
        self._save_shot_count()
        self.pm_mgr.check_pm_condition()

    def _save_shot_count(self) -> None:
        """
        บันทึก shot count ลงไฟล์ .txt แบบ atomic (เขียน .bak ก่อน)

        รูปแบบไฟล์:
          บรรทัด 1: shot_count
          บรรทัด 2: last_total_sheet (optional)
        """
        if not self.product_name or not self.product_name.strip():
            return
        try:
            bak = self.file_path + ".bak"
            with open(bak, "w", encoding="utf-8") as f:
                f.write(f"{self.shot_count}\n")
                if self.last_total_sheet is not None:
                    f.write(f"{self.last_total_sheet}\n")
            shutil.move(bak, self.file_path)
            log.debug("Saved shot_count=%d to %s", self.shot_count, self.file_path)
        except Exception as e:
            log.error("Error saving shot count: %s", e)

    # =========================================================================
    # PLC DATA HANDLING
    # =========================================================================

    def handle_plc_update(self, data: dict) -> None:
        """Slot รับ Signal data_updated จาก PLCWindow → เรียก update()"""
        self.update()

    def update(self) -> None:
        """
        อัพเดต shot count จากข้อมูล PLC ล่าสุด

        ขั้นตอน:
          1. ตรวจ Predictive PM
          2. Skip ถ้า PM กำลังดำเนินการ หรือ _just_reset = True
          3. ตรวจ product change
          4. ตรวจ reset (total_sheet ลดลง)
          5. นับ shot count เมื่อ total_sheet เพิ่มขึ้น
        """
        data = self.plc_window.get_product_and_shot_count()
        product_now = data.get("product_name", "")
        total_sheet = data.get("total_sheet", 0)
        shot_per_sheet = data.get("shot_count", 0)
        pcs_per_shot = data.get("pcs_number", 1)

        # ─── 1. Predictive PM check ──────────────────────────────────────
        self.pm_mgr.check_predictive_pm(self.shot_count, pcs_per_shot)

        # ─── 2. Skip ถ้า PM กำลังทำงาน ──────────────────────────────────
        if self._should_stop_for_pm:
            return

        # ─── 3. Skip รอบแรกหลัง reset ────────────────────────────────────
        if self._just_reset:
            self.last_total_sheet = total_sheet
            self._just_reset = False
            return

        new_file = os.path.join(self.base_dir, f"shotcount_{product_now}.txt")

        # ─── 4. Product change ────────────────────────────────────────────
        if product_now != self.product_name:
            self._handle_product_change(product_now, new_file)
            return

        # ─── 5. Reset detection (total_sheet ลด) ─────────────────────────
        if self.last_total_sheet is not None and total_sheet < self.last_total_sheet:
            log.info("Reset detected: %d → %d", self.last_total_sheet, total_sheet)
            self.last_total_sheet = total_sheet
            return

        # ─── 6. Count shots ───────────────────────────────────────────────
        if (self.last_total_sheet is not None
                and total_sheet > self.last_total_sheet):
            old_count = self.shot_count
            delta_sheets = total_sheet - self.last_total_sheet
            delta_shots = delta_sheets * shot_per_sheet
            self.shot_count += delta_shots
            self.last_total_sheet = total_sheet
            self._save_shot_count()
            log.debug("Shot count: +%d sheets × %d = +%d → total %d",
                      delta_sheets, shot_per_sheet, delta_shots, self.shot_count)

            parent_ui = getattr(self.parent, "ui", None)
            if parent_ui and hasattr(parent_ui, "shot_cnt"):
                parent_ui.shot_cnt.setText(str(self.shot_count))

            self.excel_mgr.auto_save_check(old_count)
            self.pm_mgr.check_pm_condition()

        elif self.last_total_sheet is None:
            self.last_total_sheet = total_sheet

    def _handle_product_change(self, new_name: str, new_file: str) -> None:
        """
        โหลดข้อมูลสำหรับ product ใหม่เมื่อ PLC เปลี่ยนชิ้นงาน

        Args:
            new_name: ชื่อ product ใหม่
            new_file: path ไฟล์ .txt สำหรับ product ใหม่
        """
        self.pm_triggered = False
        self.pm_window_visible = False
        self.product_name = new_name
        self.file_path = new_file

        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    lines = f.read().splitlines()
                self.shot_count = int(lines[0]) if lines else 0
                self.last_total_sheet = int(lines[1]) if len(lines) > 1 else None
                log.info("Loaded shot_count=%d for new product %s", self.shot_count, new_name)
            except (ValueError, IndexError):
                self.shot_count = 0
                self.last_total_sheet = None
        else:
            self.shot_count = 0
            self.last_total_sheet = None
            log.info("No file for product %s — starting at 0", new_name)

        self.start_lot_shot = self.shot_count
        self._save_shot_count()

    # =========================================================================
    # DELEGATE METHODS
    # (thin wrappers เพื่อให้ external callers เรียกผ่าน shot_counter ได้ต่อ)
    # =========================================================================

    def manual_pm_trigger(self) -> None:
        """Delegate ไปยัง PMManager.manual_pm_trigger()"""
        self.pm_mgr.manual_pm_trigger()

    def manual_save(self) -> None:
        """Delegate ไปยัง ExcelManager.manual_save()"""
        self.excel_mgr.manual_save()

    def load_excel_data_for_pm(self, file_path: str):
        """Delegate ไปยัง ExcelManager.load_excel_data_for_pm()"""
        return self.excel_mgr.load_excel_data_for_pm(file_path)

    # =========================================================================
    # UI MANAGEMENT
    # =========================================================================

    def show_logout_window(self) -> None:
        """
        เปิด LogoutWindow จาก ShotCounter

        ใช้เมื่อ finish_lot button ถูกกดและ main_window ไม่สามารถเรียกได้โดยตรง
        """
        try:
            from src.logout_window import LogoutWindow
            self.logout_window = LogoutWindow(
                parent=self.parent,
                shot_counter=self,
                theme_settings=getattr(self.parent, "theme_settings", {}),
            )
            self.logout_window.show()
        except Exception as e:
            log.exception("Error showing logout window: %s", e)
            self.excel_mgr.manual_save()
