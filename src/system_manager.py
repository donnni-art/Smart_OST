"""
system_manager.py
=================
จัดการ lifecycle ระดับ OS ของแอปพลิเคชัน

หน้าที่หลัก:
  - ฆ่า Python process ที่ค้างอยู่ (zombie) ก่อนเริ่มแอป
  - หยุด worker thread และ Qt timer ทั้งหมดก่อนปิด
  - Restart กระบวนการอย่างปลอดภัย (ใช้ os.execv บน Unix, subprocess บน Windows)
  - Force-quit โดยไม่รอ event loop
  - ลบไฟล์ชั่วคราวใน temp folders ที่กำหนด

การใช้งาน:
  - สร้างโดย MainWindow ใน __init__:
      self.sys_mgr = SystemManager(self)
  - เรียกใช้:
      self.sys_mgr.kill_zombie_processes()
      self.sys_mgr.stop_all_threads_and_timers()
      self.sys_mgr.safe_restart()
      self.sys_mgr.force_quit()

ความสัมพันธ์กับโมดูลอื่น:
  - ไม่ import จาก src/ เพื่อหลีกเลี่ยง circular import
  - อ่าน component references จาก main_window ที่ส่งเข้ามา
"""

import os
import sys
import time
import psutil

from src.app_logger import get_logger
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication

log = get_logger("system")

# โฟลเดอร์ที่ต้องการล้างไฟล์ชั่วคราว (.tmp / temp_*)
_TEMP_FOLDERS = [
    "shot_counts",
    "defect_raw_data/temp",
    "PM/temp",
]


class SystemManager:
    """
    จัดการ lifecycle ระดับ OS / process ของแอปพลิเคชัน

    Attributes:
        win: MainWindow — อ้างอิง components (plc_window, shot_counter, ฯลฯ)
    """

    def __init__(self, main_window):
        """
        Args:
            main_window: MainWindow instance
        """
        self.win = main_window

    # =========================================================================
    # PROCESS MANAGEMENT
    # =========================================================================

    def kill_zombie_processes(self) -> None:
        """
        ฆ่า Python process ที่รันสคริปต์เดียวกันและค้างอยู่

        ตรวจสอบทุก Python process → ถ้ารัน script เดียวกับ process ปัจจุบัน
        แต่ PID ต่างกัน → ส่ง SIGTERM เพื่อยุติ

        ใช้ก่อนเริ่มแอปเพื่อป้องกัน instance ซ้ำ
        """
        current_pid = os.getpid()
        current_script = os.path.basename(sys.argv[0])
        log.info("Checking zombie processes (current PID=%d, script=%s)",
                 current_pid, current_script)

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                name = proc.info["name"] or ""
                cmdline = proc.info["cmdline"] or []
                if (
                    "python" in name.lower()
                    and len(cmdline) > 1
                    and current_script in cmdline[1]
                    and proc.info["pid"] != current_pid
                ):
                    log.warning("Killing zombie process PID=%d", proc.info["pid"])
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    # =========================================================================
    # THREAD & TIMER SHUTDOWN
    # =========================================================================

    def stop_all_threads_and_timers(self) -> None:
        """
        หยุด worker thread และ Qt timer ทั้งหมดอย่างสะอาด

        ลำดับ:
          1. PLC worker thread
          2. ShotCounter _update_timer
          3. HeatMapDefectPCS _update_timer
          4. MainWindow _update_timer (ถ้ามี)
        """
        log.info("Stopping all threads and timers")
        win = self.win

        # 1. PLC worker thread
        try:
            plc = getattr(win, "plc_window", None)
            if plc and hasattr(plc, "stop_threads"):
                plc.stop_threads()
        except Exception as e:
            log.warning("Error stopping PLC thread: %s", e)

        # 2. ShotCounter timer
        try:
            sc = getattr(win, "shot_counter", None)
            if sc and hasattr(sc, "_update_timer"):
                timer = sc._update_timer
                if timer and timer.isActive():
                    timer.stop()
        except Exception as e:
            log.warning("Error stopping shot counter timer: %s", e)

        # 3. HeatMap timer
        try:
            hm = getattr(win, "heat_map_defect", None)
            if hm and hasattr(hm, "_update_timer"):
                timer = hm._update_timer
                if timer and timer.isActive():
                    timer.stop()
        except Exception as e:
            log.warning("Error stopping heat map timer: %s", e)

        # 4. MainWindow timer
        try:
            timer = getattr(win, "_update_timer", None)
            if timer and timer.isActive():
                timer.stop()
        except Exception as e:
            log.warning("Error stopping main window timer: %s", e)

        log.info("All threads and timers stopped")

    # =========================================================================
    # RESTART
    # =========================================================================

    def safe_restart(self) -> None:
        """
        รีสตาร์ทแอปพลิเคชันอย่างปลอดภัย

        บันทึก shot count → หยุด threads → ปิดหน้าต่าง → เปิด process ใหม่

        บน Unix: ใช้ os.execv (แทนที่ process ปัจจุบัน)
        บน Windows: ใช้ subprocess.Popen แล้ว os._exit(0)
        """
        log.info("Restarting application")
        win = self.win

        # บันทึก shot count ก่อน restart
        try:
            sc = getattr(win, "shot_counter", None)
            if sc:
                sc._save_shot_count()
        except Exception as e:
            log.warning("Error saving shot count before restart: %s", e)

        self.stop_all_threads_and_timers()
        win.close()
        self._exec_new_process()

    def _exec_new_process(self) -> None:
        """ปิด process ปัจจุบันและเริ่ม process ใหม่"""
        python = sys.executable
        script = sys.argv[0]
        args = [python, script] + sys.argv[1:]
        log.info("Launching new process: %s", " ".join(args))

        if os.name == "nt":
            import subprocess
            subprocess.Popen(args)
            os._exit(0)
        else:
            os.execv(python, args)

    # =========================================================================
    # FORCE QUIT
    # =========================================================================

    def force_quit(self, exit_code: int = 0) -> None:
        """
        บังคับปิดแอปทันที — ใช้เมื่อ cleanup ปกติล้มเหลว

        Args:
            exit_code: รหัสออก (0 = ปกติ, 1 = error)
        """
        log.info("Force quitting application (exit_code=%d)", exit_code)
        try:
            QApplication.quit()
        except Exception:
            pass
        os._exit(exit_code)

    # =========================================================================
    # TEMP FILE CLEANUP
    # =========================================================================

    def clean_temp_files(self) -> None:
        """
        ลบไฟล์ชั่วคราว (.tmp หรือชื่อขึ้นต้นด้วย temp_) ใน temp folders ที่กำหนด

        โฟลเดอร์ที่สแกน: shot_counts/, defect_raw_data/temp/, PM/temp/
        ไม่ลบโฟลเดอร์เอง — ลบเฉพาะไฟล์ที่ตรงเงื่อนไข
        """
        log.info("Cleaning temporary files")
        for folder in _TEMP_FOLDERS:
            if not os.path.exists(folder):
                continue
            for filename in os.listdir(folder):
                if filename.endswith(".tmp") or filename.startswith("temp_"):
                    file_path = os.path.join(folder, filename)
                    try:
                        os.remove(file_path)
                        log.debug("Deleted temp file: %s", file_path)
                    except Exception as e:
                        log.warning("Cannot delete %s: %s", file_path, e)
        log.info("Temp file cleanup complete")
