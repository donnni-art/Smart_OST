"""
mock_database.py
================
จำลอง MySQL และ Oracle connections ด้วย SQLite in-memory
ใช้เมื่อ mock_mode = true ใน config.json

ข้อมูลตัวอย่างที่มี:
  Lot Numbers : TEST001 (CAW-076W-1A / FOST) , TEST002 (SUS-Z018M / FOST2)
  Operators   : EMP001 (F4/1) , EMP002 (F4/2) , EMP003 (ไม่มีสิทธิ์ F3/1)
  Fixtures    : FIX-001 (CAW-076W) , FIX-002 (SUS-Z018M) , FIX-003 (CAW-076W/SYC-480W)
  Staff       : S001 , S002 , EMP001
"""

import sqlite3
import threading
from datetime import datetime

# ─── shared in-memory databases ──────────────────────────────────────────────
# remote แทน 10.17.86.154  (tooling_fix + design)
# local  แทน localhost      (tooling_fix write)
_REMOTE_CONN = sqlite3.connect(':memory:', check_same_thread=False)
_LOCAL_CONN  = sqlite3.connect(':memory:', check_same_thread=False)
_LOCK        = threading.Lock()


# ─── init remote (10.17.86.154) ──────────────────────────────────────────────

def _init_remote(conn: sqlite3.Connection):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_fpc (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            fpc_type    TEXT,
            fpc_code    TEXT,
            fpc_pd_name TEXT,
            use_for     TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_database (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            Types        TEXT,
            Tooling_Code TEXT,
            Product_Name TEXT,
            use_for      TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_staff (
            Code TEXT PRIMARY KEY,
            Name TEXT
        )
    """)

    cur.executemany("INSERT OR IGNORE INTO tbl_fpc VALUES (?,?,?,?,?)", [
        (1, 'FIXTURE', 'FIX-001', 'CAW-076W',              'FOST'),
        (2, 'FIXTURE', 'FIX-002', 'SUS-Z018M',             'FOST2'),
        (3, 'FIXTURE', 'FIX-003', 'CAW-076W / SYC-480W',   'FOST'),
        (4, 'FIXTURE', 'FIX-004', 'SUS-Z018M',             'FOST3'),
    ])

    cur.executemany("INSERT OR IGNORE INTO tbl_database VALUES (?,?,?,?,?)", [
        (1, 'FIXTURE', 'FIX-FA-001', 'CAW-076W',   'FOST'),
        (2, 'FIXTURE', 'FIX-FA-002', 'SUS-Z018M',  'FOST2'),
    ])

    cur.executemany("INSERT OR IGNORE INTO tbl_staff VALUES (?,?)", [
        ('S001',   'สมชาย ใจดี'),
        ('S002',   'สมหญิง รักดี'),
        ('EMP001', 'ทดสอบ ระบบ'),
    ])

    conn.commit()
    cur.close()


# ─── init local (localhost) ───────────────────────────────────────────────────

def _init_local(conn: sqlite3.Connection):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_result_test (
            lot_number           TEXT PRIMARY KEY,
            product_name         TEXT,
            operator_id          TEXT,
            operator_name        TEXT,
            process              TEXT,
            job_title            TEXT,
            code_training        TEXT,
            train_topic          TEXT,
            date_time            TEXT,
            tooling_code         TEXT,
            ost_type             TEXT,
            total_sheet          INTEGER DEFAULT 0,
            good_sheet           INTEGER DEFAULT 0,
            reject_sheet         INTEGER DEFAULT 0,
            total_pcs            INTEGER DEFAULT 0,
            good_pcs             INTEGER DEFAULT 0,
            reject_pcs           INTEGER DEFAULT 0,
            reject_ratio         REAL    DEFAULT 0.0,
            short                INTEGER DEFAULT 0,
            open                 INTEGER DEFAULT 0,
            blkm                 INTEGER DEFAULT 0,
            mat                  INTEGER DEFAULT 0,
            shot                 INTEGER DEFAULT 0,
            confirm_closs_lot_by TEXT,
            confirm_total_ng     INTEGER DEFAULT 0,
            confirm_open         INTEGER DEFAULT 0,
            confirm_short        INTEGER DEFAULT 0,
            confirm_blkm         INTEGER DEFAULT 0,
            confirm_mat          INTEGER DEFAULT 0,
            confirm_shot         INTEGER DEFAULT 0,
            note                 TEXT,
            closs_time           TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tbl_training (
            id_code       TEXT PRIMARY KEY,
            name          TEXT,
            process       TEXT,
            job_title     TEXT,
            code_training TEXT,
            train_item    TEXT
        )
    """)

    cur.executemany(
        "INSERT OR IGNORE INTO tbl_result_test (lot_number, product_name) VALUES (?,?)", [
        ('TEST001', 'CAW-076W-1A'),
        ('TEST002', 'SUS-Z018M-W1B'),
    ])

    cur.executemany("INSERT OR IGNORE INTO tbl_training VALUES (?,?,?,?,?,?)", [
        ('EMP001', 'ทดสอบ ระบบ',  'FOST',  'Operator', 'F4/1', 'OST Training'),
        ('EMP002', 'สมชาย ใจดี',  'FOST2', 'Operator', 'F4/2', 'OST Training'),
        ('EMP003', 'ไม่มีสิทธิ์', 'OTHER', 'Operator', 'F3/1', 'General'),
    ])

    conn.commit()
    cur.close()


_init_remote(_REMOTE_CONN)
_init_local(_LOCAL_CONN)


# ─── Mock Cursor ─────────────────────────────────────────────────────────────

class MockCursor:
    """wrap SQLite cursor ให้ interface เหมือน mysql.connector cursor"""

    def __init__(self, sqlite_cursor: sqlite3.Cursor, dictionary: bool = False):
        self._cur = sqlite_cursor
        self._dictionary = dictionary
        self.description = None
        self.lastrowid = None

    def execute(self, query: str, params=None):
        q = query.replace('%s', '?')
        q = q.replace('NOW()', "datetime('now')")
        with _LOCK:
            self._cur.execute(q, params or ())
        self.description = self._cur.description
        self.lastrowid = self._cur.lastrowid

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        if self._dictionary and self._cur.description:
            return dict(zip([d[0] for d in self._cur.description], row))
        return row

    def fetchall(self):
        rows = self._cur.fetchall()
        if self._dictionary and self._cur.description:
            cols = [d[0] for d in self._cur.description]
            return [dict(zip(cols, r)) for r in rows]
        return rows

    def close(self):
        self._cur.close()


# ─── Mock MySQL Connection ────────────────────────────────────────────────────

class MockMySQLConnection:
    """จำลอง mysql.connector.MySQLConnection ด้วย SQLite in-memory"""

    def __init__(self, sqlite_conn: sqlite3.Connection, label: str):
        self._conn = sqlite_conn
        self._label = label
        self._connected = True

    def is_connected(self) -> bool:
        return self._connected

    def cursor(self, dictionary: bool = False) -> MockCursor:
        return MockCursor(self._conn.cursor(), dictionary=dictionary)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._connected = False

    def __repr__(self):
        return f"<MockMySQL label={self._label}>"


# ─── Mock Oracle ──────────────────────────────────────────────────────────────

_NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

MOCK_LOT_DATA: dict = {
    'TEST001': [
        {
            'PROC_DISP':            'FOST',
            'TTT_TOOLS_TYPE_NAME':  'FIXTURE',
            'TTL_SCAN_TYPE':        'IN',
            'TTL_PRD_ITEM_CODE':    'CAW076W1A',
            'TTL_LOT_MOS':          'TEST001',
            'TTL_PROCESS':          'P001',
            'TTL_MC_NO':            'MC-01',
            'TTL_TOOLS_TYPE':       'FIX',
            'TTL_TOOLS_CODE':       'FIX-001',
            'TTL_TOOLS_REV':        '1',
            'TTL_SCAN_STATION':     '10.17.86.10',
            'TTL_SCAN_BY':          'SYSTEM',
            'TTL_SCAN_DATE':        _NOW,
            'TTL_CHANGE_TIME':      _NOW,
        },
        {
            'PROC_DISP':            'FOST',
            'TTT_TOOLS_TYPE_NAME':  'OPERATOR',
            'TTL_SCAN_TYPE':        'IN',
            'TTL_PRD_ITEM_CODE':    'CAW076W1A',
            'TTL_LOT_MOS':          'TEST001',
            'TTL_PROCESS':          'P001',
            'TTL_MC_NO':            'MC-01',
            'TTL_TOOLS_TYPE':       'OPR',
            'TTL_TOOLS_CODE':       'EMP001',
            'TTL_TOOLS_REV':        '1',
            'TTL_SCAN_STATION':     '10.17.86.10',
            'TTL_SCAN_BY':          'SYSTEM',
            'TTL_SCAN_DATE':        _NOW,
            'TTL_CHANGE_TIME':      _NOW,
        },
    ],
    'TEST002': [
        {
            'PROC_DISP':            'FOST2',
            'TTT_TOOLS_TYPE_NAME':  'FIXTURE',
            'TTL_SCAN_TYPE':        'IN',
            'TTL_PRD_ITEM_CODE':    'SUSZ018MW1B',
            'TTL_LOT_MOS':          'TEST002',
            'TTL_PROCESS':          'P002',
            'TTL_MC_NO':            'MC-02',
            'TTL_TOOLS_TYPE':       'FIX',
            'TTL_TOOLS_CODE':       'FIX-002',
            'TTL_TOOLS_REV':        '1',
            'TTL_SCAN_STATION':     '10.17.86.11',
            'TTL_SCAN_BY':          'SYSTEM',
            'TTL_SCAN_DATE':        _NOW,
            'TTL_CHANGE_TIME':      _NOW,
        },
        {
            'PROC_DISP':            'FOST2',
            'TTT_TOOLS_TYPE_NAME':  'OPERATOR',
            'TTL_SCAN_TYPE':        'IN',
            'TTL_PRD_ITEM_CODE':    'SUSZ018MW1B',
            'TTL_LOT_MOS':          'TEST002',
            'TTL_PROCESS':          'P002',
            'TTL_MC_NO':            'MC-02',
            'TTL_TOOLS_TYPE':       'OPR',
            'TTL_TOOLS_CODE':       'EMP002',
            'TTL_TOOLS_REV':        '1',
            'TTL_SCAN_STATION':     '10.17.86.11',
            'TTL_SCAN_BY':          'SYSTEM',
            'TTL_SCAN_DATE':        _NOW,
            'TTL_CHANGE_TIME':      _NOW,
        },
    ],
}


class MockOracleCursor:
    def __init__(self):
        self._rows: list = []
        self.description = None

    def execute(self, query: str, **kwargs):
        lot_number = kwargs.get('lot_number', '')
        data = MOCK_LOT_DATA.get(lot_number, [])
        self._rows = data
        if data:
            self.description = [
                (k, None, None, None, None, None, None) for k in data[0]
            ]

    def fetchall(self):
        return [tuple(row.values()) for row in self._rows]

    def close(self):
        pass


class MockOracleConnection:
    def cursor(self) -> MockOracleCursor:
        return MockOracleCursor()

    def close(self):
        pass


# ─── public helpers ───────────────────────────────────────────────────────────

def get_mock_read_connection() -> MockMySQLConnection:
    c = MockMySQLConnection(_REMOTE_CONN, 'READ')
    c._connected = True
    return c


def get_mock_write_connection() -> MockMySQLConnection:
    c = MockMySQLConnection(_LOCAL_CONN, 'WRITE')
    c._connected = True
    return c


def get_mock_staff_connection() -> MockMySQLConnection:
    c = MockMySQLConnection(_REMOTE_CONN, 'STAFF')
    c._connected = True
    return c


def get_mock_oracle_connection() -> MockOracleConnection:
    return MockOracleConnection()


def print_mock_summary():
    """แสดงข้อมูล mock ทั้งหมด (ใช้ debug)"""
    print("\n" + "=" * 55)
    print("  MOCK DATABASE — ข้อมูลตัวอย่างสำหรับทดสอบ")
    print("=" * 55)

    local_cur = _LOCAL_CONN.cursor()
    local_cur.execute("SELECT lot_number, product_name FROM tbl_result_test")
    print("\n[LOCAL] tbl_result_test:")
    for r in local_cur.fetchall():
        print(f"  Lot={r[0]}  Product={r[1]}")

    local_cur.execute("SELECT id_code, name, code_training FROM tbl_training")
    print("\n[LOCAL] tbl_training:")
    for r in local_cur.fetchall():
        print(f"  ID={r[0]}  Name={r[1]}  Training={r[2]}")
    local_cur.close()

    remote_cur = _REMOTE_CONN.cursor()
    remote_cur.execute("SELECT fpc_code, fpc_pd_name, use_for FROM tbl_fpc")
    print("\n[REMOTE] tbl_fpc:")
    for r in remote_cur.fetchall():
        print(f"  Code={r[0]}  Product={r[1]}  FOST={r[2]}")

    remote_cur.execute("SELECT Code, Name FROM tbl_staff")
    print("\n[REMOTE] tbl_staff:")
    for r in remote_cur.fetchall():
        print(f"  Code={r[0]}  Name={r[1]}")
    remote_cur.close()

    print("\n[ORACLE] Lot Numbers พร้อมใช้:", list(MOCK_LOT_DATA.keys()))
    print("=" * 55 + "\n")
