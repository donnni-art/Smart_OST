"""
test_mock_db.py
===============
ทดสอบการเชื่อมต่อ database ทั้งหมดในโหมด mock
รัน: python test_mock_db.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

# mock PySide6 ไว้ก่อนเพื่อให้ import modules อื่นผ่าน
# (เครื่องนี้ไม่ได้ install PySide6)
import unittest.mock as _mock
import types

_pyside6 = types.ModuleType('PySide6')
for _sub in ['QtWidgets', 'QtCore', 'QtGui']:
    _m = types.ModuleType(f'PySide6.{_sub}')
    setattr(_pyside6, _sub, _m)
    sys.modules[f'PySide6.{_sub}'] = _m
    for _cls in ['QApplication', 'QDialog', 'QLabel', 'QComboBox', 'QPushButton',
                 'QLineEdit', 'QVBoxLayout', 'QFileDialog', 'QRadioButton',
                 'QDialogButtonBox', 'QMessageBox', 'QHBoxLayout', 'QButtonGroup',
                 'QWidget', 'QMainWindow', 'QFrame', 'QScrollArea']:
        setattr(_m, _cls, type(_cls, (), {}))
    for _cls2 in ['Qt', 'QEvent', 'Signal', 'QTimer', 'QThread', 'QObject',
                  'QKeyEvent', 'QIcon', 'QColor', 'QFont', 'QPixmap', 'QPalette']:
        setattr(_m, _cls2, type(_cls2, (), {}))
sys.modules['PySide6'] = _pyside6

# mock mysql.connector และ oracledb สำหรับเครื่องที่ไม่ได้ install
import types as _types

_mysql_pkg = _types.ModuleType('mysql')
_mysql_conn = _types.ModuleType('mysql.connector')
_mysql_conn.Error = Exception
_mysql_conn.MySQLConnection = object
_mysql_conn.connect = lambda **kw: None
_mysql_pkg.connector = _mysql_conn
sys.modules['mysql'] = _mysql_pkg
sys.modules['mysql.connector'] = _mysql_conn

_oracle = _types.ModuleType('oracledb')
_oracle.Error = Exception
_oracle.connect = lambda **kw: None
_oracle.init_oracle_client = lambda **kw: None
_oracle.makedsn = lambda *a, **kw: ''
sys.modules['oracledb'] = _oracle

from src.config_manager import config_manager
from src.database_manager import database_manager
from src.mock_database import print_mock_summary

PASS = "✅"
FAIL = "❌"

def header(title):
    print(f"\n{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}")


def test(label, expr, expected=True):
    result = bool(expr) == bool(expected)
    icon = PASS if result else FAIL
    print(f"  {icon}  {label}")
    if not result:
        print(f"       got: {repr(expr)}")
    return result


# ─── แสดงข้อมูล mock ──────────────────────────────────────────────────────────
print_mock_summary()

# ─── ตรวจ config ─────────────────────────────────────────────────────────────
header("1. Config")
test("mock_mode = True",  config_manager.current_config.get('mock_mode'))
test("read_database key มี",  'read_database'       in config_manager.current_config)
test("write_database key มี", 'write_database'      in config_manager.current_config)
test("read_database_staff key มี", 'read_database_staff' in config_manager.current_config)
test("check_lot_database key มี",  'check_lot_database'  in config_manager.current_config)

# ─── ตรวจ database connections ───────────────────────────────────────────────
header("2. Database Connections (mock)")
read_conn  = database_manager.get_read_connection()
write_conn = database_manager.get_write_connection()
staff_conn = database_manager.get_staff_connection()

test("READ connection ได้", read_conn  is not None)
test("WRITE connection ได้", write_conn is not None)
test("STAFF connection ได้", staff_conn is not None)
test("READ is_connected()", read_conn  and read_conn.is_connected())
test("WRITE is_connected()", write_conn and write_conn.is_connected())
test("STAFF is_connected()", staff_conn and staff_conn.is_connected())

# ─── ตรวจ WRITE DB queries ───────────────────────────────────────────────────
header("3. WRITE DB — tbl_result_test")
cur = write_conn.cursor(dictionary=True)

cur.execute("SELECT product_name FROM tbl_result_test WHERE lot_number = %s", ('TEST001',))
row = cur.fetchone()
test("Lot TEST001 มีอยู่",     row is not None)
test("Product = CAW-076W-1A",  row and row.get('product_name') == 'CAW-076W-1A')

cur.execute("SELECT product_name FROM tbl_result_test WHERE lot_number = %s", ('NOTEXIST',))
test("Lot ไม่มี → None",       cur.fetchone() is None)
cur.close()

header("4. WRITE DB — tbl_training")
cur = write_conn.cursor(dictionary=True)

cur.execute("SELECT * FROM tbl_training WHERE id_code = %s", ('EMP001',))
row = cur.fetchone()
test("EMP001 มีอยู่",          row is not None)
test("Training code = F4/1",   row and row.get('code_training') == 'F4/1')

cur.execute("SELECT * FROM tbl_training WHERE id_code = %s", ('EMP003',))
row = cur.fetchone()
test("EMP003 มีอยู่ (ไม่มีสิทธิ์)", row is not None)
test("Training code = F3/1",   row and row.get('code_training') == 'F3/1')
cur.close()

# ─── ตรวจ READ DB queries ────────────────────────────────────────────────────
header("5. READ DB — tbl_fpc")
cur = read_conn.cursor(dictionary=True)

cur.execute("SELECT * FROM tbl_fpc WHERE fpc_type = 'FIXTURE' AND fpc_code = %s", ('FIX-001',))
row = cur.fetchone()
test("FIX-001 มีอยู่",         row is not None)
test("fpc_pd_name = CAW-076W", row and row.get('fpc_pd_name') == 'CAW-076W')
test("use_for = FOST",         row and row.get('use_for') == 'FOST')

cur.execute("SELECT * FROM tbl_fpc WHERE fpc_type = 'FIXTURE' AND fpc_code = %s", ('NOTEXIST',))
test("Fixture ไม่มี → None",   cur.fetchone() is None)
cur.close()

# ─── ตรวจ STAFF DB queries ───────────────────────────────────────────────────
header("6. STAFF DB — tbl_staff")
cur = staff_conn.cursor(dictionary=True)

cur.execute("SELECT Code, Name FROM tbl_staff WHERE Code = %s", ('EMP001',))
row = cur.fetchone()
test("Staff EMP001 มีอยู่",    row is not None)
test("Name ถูกต้อง",           row and row.get('Name') == 'ทดสอบ ระบบ')
cur.close()

# ─── ตรวจ INSERT / UPDATE ────────────────────────────────────────────────────
header("7. WRITE DB — INSERT & UPDATE")
cur = write_conn.cursor(dictionary=True)

cur.execute(
    "INSERT OR IGNORE INTO tbl_result_test (lot_number, product_name) VALUES (%s, %s)",
    ('LOT-NEW-001', 'SUS-Z018M-W1B')
)
write_conn.commit()
cur.execute("SELECT product_name FROM tbl_result_test WHERE lot_number = %s", ('LOT-NEW-001',))
row = cur.fetchone()
test("INSERT lot ใหม่สำเร็จ",  row is not None)

cur.execute(
    "UPDATE tbl_result_test SET total_pcs = %s WHERE lot_number = %s",
    (100, 'LOT-NEW-001')
)
write_conn.commit()
cur.execute("SELECT total_pcs FROM tbl_result_test WHERE lot_number = %s", ('LOT-NEW-001',))
row = cur.fetchone()
test("UPDATE total_pcs = 100", row and row.get('total_pcs') == 100)
cur.close()

# ─── ตรวจ Oracle mock ────────────────────────────────────────────────────────
header("8. Oracle Mock — LotChecker")
from src.lot_checker import lot_checker

result = lot_checker.check_lot('TEST001')
test("TEST001 status = VALID",      result.get('status') == 'VALID')
test("TEST001 มี data",              result.get('data') is not None)
test("Tooling = FIX-001",           result.get('data', {}).get('tooling_code') == 'FIX-001')
test("Operator = EMP001",           result.get('data', {}).get('operator_id') == 'EMP001')

result2 = lot_checker.check_lot('TEST002')
test("TEST002 status = VALID",      result2.get('status') == 'VALID')
test("PROC_DISP = FOST2",           result2.get('data', {}).get('ost_type') == 'FOST2')

result3 = lot_checker.check_lot('NOTEXIST')
test("Lot ไม่มี → NOT_FOUND",       result3.get('status') == 'NOT_FOUND')

# ─── ตรวจ DataUploader integration ───────────────────────────────────────────
header("9. DataUploader Integration")
from src.data_upload import DataUploader
uploader = DataUploader()

name, err = uploader.get_product_name_by_lot('TEST001')
test("get_product_name TEST001",    name == 'CAW-076W-1A')
test("get_product_name no error",   err is None)

ok, user_data = uploader.check_user_permission('EMP001')
test("EMP001 permission = True",    ok is True)
test("operator_name ไม่ว่าง",       user_data and bool(user_data.get('operator_name')))

ok2, _ = uploader.check_user_permission('EMP003')
test("EMP003 permission = False",   ok2 is False)

ok3, fix_data = uploader.check_fixture_validity('FIX-001', mode='mass')
test("FIX-001 mass valid",          ok3 is True)
test("fpc_code = FIX-001",          fix_data and fix_data.get('fpc_code') == 'FIX-001')

ok4, _ = uploader.check_fixture_validity('NOTEXIST', mode='mass')
test("Fixture ไม่มี → False",       ok4 is False)

# ─── สรุป ─────────────────────────────────────────────────────────────────────
print(f"\n{'='*55}")
print("  ทดสอบเสร็จสิ้น — ถ้าเห็น ❌ ให้ตรวจสอบ mock data")
print(f"{'='*55}\n")
