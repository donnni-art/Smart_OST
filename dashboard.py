"""
dashboard.py
============
จุดเริ่มต้นของ SMART OST Production Dashboard

รันบน Supervisor/Monitoring PC บน LAN เดียวกับ Raspberry Pi
ไม่ต้องเชื่อมต่อ PLC โดยตรง — รับข้อมูล real-time จากทุก Pi ผ่าน TCP

การใช้งาน:
    python dashboard.py              # โหมดปกติ (ต้องมี Pi จริงบน LAN)
    python dashboard.py --mock       # โหมดทดสอบ (ข้อมูลจำลอง ไม่ต้องมี Pi)

ก่อนใช้งานจริง:
    แก้ config.json → เพิ่ม "machines" array พร้อม IP ของ Pi แต่ละเครื่อง
    แก้ "mock_mode": false เพื่อเชื่อมต่อจริง
"""

import sys
import argparse

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from src.config_manager import config_manager
from src.app_logger import get_logger

log = get_logger("dashboard_main")


def main():
    parser = argparse.ArgumentParser(description="SMART OST Production Dashboard")
    parser.add_argument(
        "--mock", action="store_true",
        help="ใช้ข้อมูลจำลอง (ไม่ต้องเชื่อมต่อ Pi จริง)"
    )
    args = parser.parse_args()

    # override mock_mode ถ้าส่ง --mock มา
    if args.mock:
        config_manager.current_config['mock_mode'] = True
        log.info("--mock flag: forced mock_mode = True")

    app = QApplication(sys.argv)
    app.setApplicationName("SMART OST Dashboard")
    app.setOrganizationName("Smart OST")
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # import ช้า (หลัง QApplication) เพื่อให้ Qt widgets ทำงานได้
    from src.ui_dashboard_window import DashboardWindow
    win = DashboardWindow()
    win.show()

    log.info("Dashboard launched")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
