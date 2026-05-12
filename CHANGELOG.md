# CHANGELOG — Smart OST

---

## [2026-05-12] — PLC Data Reading Bug Fixes

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `src/PLCdata.py` | แก้ไข 4 bugs: default data, defect dict, TCP sync, config usage |
| `pi_plc_reader.py` | แก้ไข: เพิ่ม product_name และ dm1251 ใน JSON broadcast |

---

### สิ่งที่แก้ไข

**1. `PLCdata.py` — `_default_data()` keys ไม่ครบ (Critical)**
- Before: คืนแค่ 11 keys (dm registers + lot_number) ทำให้ subscriber ที่รับ signal เมื่อ serial ไม่เชื่อมต่อ เจอ KeyError หรือ NoneType error
- After: เพิ่ม `shot_number`, `pcs_number`, `shot_per_pcs`, `defect_results: {}` ให้ตรงกับ `get_updated_values()`

**2. `PLCdata.py` — `defect_results` type mismatch ใน serial mode (Critical)**
- Before: `get_updated_values()` ใส่ผล `analyze_defect_addresses()` ซึ่งคืน **string** (formatted text) ใน key `defect_results` แต่ TCP mode คืน **dict** `{S1P1: ["PASS"|defect]}` → code ที่เรียก `.values()` crash ใน serial mode
- After: เพิ่มเมธอด `_defect_results_dict()` ที่ใช้ logic เดียวกับ `pi_plc_reader._analyze_defects()` คืนค่าเป็น dict, ให้ `get_updated_values()` เรียกใช้ทั้ง 2 mode

**3. `PLCdata.py` — `handle_data_update()` TCP mode: shot counting ไม่ทำงาน (Critical)**
- Before: ฟังก์ชัน re-emit ข้อมูลผ่าน signal เฉยๆ ไม่อัพเดต cached attributes → `get_product_and_shot_count()` คืน 0/`""` ตลอด → `shot_counting.update()` เห็น `product_now=""` และ `total_sheet=0` ทุก cycle → shot count ไม่เคยเพิ่มขึ้นในโหมด TCP
- After: sync `product_name`, `value_dm1923`, `value_dm1251`, `shot_number`, `pcs_number`, `value_dm5050/5051`, `current_lot_number`, `defect_shot_per_pcs` จาก data dict ก่อน emit

**4. `PLCdata.py` — `try_connect_to_port()` hardcode serial params (Medium)**
- Before: baudrate=9600, parity=EVEN, bytesize=8, stopbits=1, timeout=0.3 แบบตายตัว ทำให้ config.json ที่ตั้ง baudrate อื่นไม่มีผล
- After: ใช้ `self.plc_config.get(...)` พร้อม fallback เหมือนกับ `_init_serial()`

**5. `pi_plc_reader.py` — JSON broadcast ขาด `product_name` และ `dm1251` (Medium)**
- Before: PC side ไม่รู้ว่า Pi กำลังผลิตอะไร (ไม่มี product_name) และไม่มี dm1251 สำหรับคำนวณ shot multiplier
- After: เพิ่ม `"product_name": self.product_name` และ `"dm1251": self.value_dm1251` ใน `_build_data_dict()`

---

## [2026-05-08-3] — PM System Bug Fixes

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `src/pm_window.py` | แก้ไข 3 bugs: duplicate methods, corrupt except, missing init |
| `src/pm_manager.py` | แก้ไข: Qt.WA_DeleteOnClose deprecated API |

---

### สิ่งที่แก้ไข

**1. `pm_window.py` — Duplicate method definitions (Critical)**
- Before: เมธอด `set_excel_data`, `parse_and_set_row_3b_data`, `_highlight_table_by_next_pm`, `_clear_table_highlight` ถูก define ซ้ำ 2 รอบ (ไฟล์มี 928 บรรทัด)
- Before: `_clear_table_highlight` (ชุดแรก บรรทัด ~694) มี except block ที่ corrupt — มีโค้ดจาก `_display_login_info` หลุดเข้ามา ใช้ตัวแปร `leader`, `login_data`, `staff_date` ที่ไม่ได้ define ใน scope → ถ้า table clear ล้มเหลวจะเกิด `NameError` ซ้อน
- After: ลบ duplicate ออก, ไฟล์เหลือ 711 บรรทัด, เมธอดแต่ละชื่อมีเพียงหนึ่งนิยาม

**2. `pm_window.py` — `_current_login_info` not initialized (Medium)**
- Before: `_current_login_info` ถูกสร้างเฉพาะใน `_display_login_info()` (เมื่อ login_data ไม่ใช่ None) แต่ `_save_login_info_to_excel` อ่าน `self._current_login_info` โดยตรง → `AttributeError` ถ้าผู้ใช้กด Save ก่อน login สำเร็จ
- After: เพิ่ม `self._current_login_info = {}` ใน `__init__` บรรทัดแรกก่อน `setupUi`

**3. `pm_manager.py` — `Qt.WA_DeleteOnClose` deprecated (Medium)**
- Before: `c.pm_window.setAttribute(Qt.WA_DeleteOnClose)` — ใช้ enum แบบเก่า
- After: `c.pm_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)` — PySide6 ที่ถูกต้อง

---

## [2026-05-08-2] — Production Dashboard (LAN / Offline)

### ไฟล์ที่สร้างใหม่ / แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `src/machine_monitor.py` | สร้างใหม่ — Multi-Pi TCP manager + mock mode |
| `src/ui_dashboard_window.py` | สร้างใหม่ — Dashboard UI with machine card grid |
| `dashboard.py` | สร้างใหม่ — entry point, รองรับ `--mock` flag |
| `config.json` | แก้ไข — เพิ่ม `machines` array (4 เครื่องตัวอย่าง) |

---

### สิ่งที่สร้าง

**1. `src/machine_monitor.py` — Multi-machine TCP Monitor**
- `MachineTCPWorker`: QObject ทำงานใน QThread เชื่อมต่อ Pi เครื่องเดียวผ่าน TCP
  - Auto-reconnect เมื่อ connection หลุด
  - Emit `data_ready(machine_id, data)` และ `status_changed(machine_id, status)`
- `MachineMonitor`: Orchestrate Workers ทุกเครื่อง
  - Real mode: สร้าง MachineTCPWorker 1 ตัวต่อ Pi
  - Mock mode: ใช้ `QTimer(1000ms)` generate ข้อมูลสุ่ม (ไม่ต้องมี Pi จริง)
  - Signals: `machine_updated(id, data)`, `machine_status(id, status)`

**2. `src/ui_dashboard_window.py` — Dashboard Window**
- `MachineCard(QFrame)`: card แต่ละใบแสดงสถานะเครื่องเดียว
  - Header: ชื่อเครื่อง + status badge (สีเขียว/ส้ม/แดง)
  - Body: LOT, PRODUCT, SHOT TYPE, PCS/SHOT, TOTAL SHOTS, DEFECT COUNT, PASS RATE
  - Pass rate แสดงสี: ≥99% เขียว, ≥95% เหลือง, <95% แดง
  - Footer: เวลาอัพเดตล่าสุด
- `DashboardWindow(QMainWindow)`: หน้าต่างหลัก
  - Header bar: ชื่อระบบ + สรุป Online/Offline + นาฬิกา real-time
  - Grid layout (max 4 column) + scroll area สำหรับเครื่องจำนวนมาก
  - Dark industrial theme (bg #0d1117, accent #58a6ff)
  - Resize-friendly: ปรับ column อัตโนมัติตามจำนวนเครื่อง

**3. `dashboard.py` — Standalone Entry Point**
- Before: ไม่มี → ต้องเปิดผ่าน main.py ซึ่งเป็น per-machine app
- After: `python dashboard.py` เปิด dashboard บน Supervisor PC
- `--mock` flag: บังคับ mock_mode เพื่อทดสอบโดยไม่ต้องมี Pi จริง

**4. `config.json` — เพิ่ม machines array**
- Before: ไม่มี `machines` key
- After: มี 4 เครื่องตัวอย่าง M01-M04 (IP 192.168.1.10-13, port 9999)
  - แต่ละเครื่องมี `mock_lot` / `mock_product` สำหรับ mock mode

---

### วิธีใช้งาน

```bash
# โหมดทดสอบ (ไม่ต้องมี Pi บน LAN)
python dashboard.py --mock

# โหมดจริง (ต้องมี Pi ที่ IP ที่กำหนดใน config.json)
# แก้ config.json: "mock_mode": false, แก้ IP ของ Pi แต่ละเครื่อง
python dashboard.py
```

---

## [2026-05-08] — Mock Database System & Bug Fixes

### ไฟล์ที่แก้ไข / สร้างใหม่
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `config.json` | สร้างใหม่ — config ครบทุก section พร้อม `mock_mode: true` |
| `src/mock_database.py` | สร้างใหม่ — SQLite in-memory mock สำหรับ MySQL + Oracle |
| `test_mock_db.py` | สร้างใหม่ — script ทดสอบ 9 หมวด 28 test cases |
| `src/database_manager.py` | แก้ไข — เพิ่ม mock mode support |
| `src/lot_checker.py` | แก้ไข — fix 3 bugs + mock mode |
| `src/config_manager.py` | แก้ไข — เพิ่ม default DB sections + ลบ PySide6 import ที่ไม่จำเป็น |
| `src/login_scan.py` | แก้ไข — fix KeyError ใน `handle_mode_change` |

---

### สิ่งที่แก้ไข

**1. สร้างระบบ Mock Database (`src/mock_database.py`)**
- `MockMySQLConnection` + `MockCursor` : wrap SQLite in-memory ให้ interface เหมือน mysql.connector
- `MockOracleConnection` + `MockOracleCursor` : จำลอง Oracle สำหรับ lot check
- แบ่ง 2 in-memory DB: `_REMOTE_CONN` (แทน 10.17.86.154) และ `_LOCAL_CONN` (แทน localhost)
- ข้อมูลตัวอย่าง: Lot TEST001/TEST002, Operator EMP001/EMP002/EMP003, Fixture FIX-001~004

**2. `config.json` — สร้างใหม่ครบถ้วน**
- Before: ไม่มีไฟล์ → ทุก module ใช้ค่า hardcode
- After: มี `read_database`, `write_database`, `read_database_staff`, `check_lot_database` ครบ
- `"mock_mode": true` → เปลี่ยนเป็น `false` เมื่อต่อ production DB จริง

**3. `src/database_manager.py` — mock mode**
- Before: `get_read/write/staff_connection()` ต่อ MySQL จริงเสมอ
- After: ตรวจ `mock_mode` ก่อน → คืน mock connection แทน

**4. `src/lot_checker.py` — fix 3 bugs**
- Bug 1 (Critical): `oracledb.init_oracle_client(lib_dir=r"C:\instantclient_19_29")` hardcode Windows path ใน `__init__` → crash ทันทีบน macOS/Linux
  → แก้: อ่าน path จาก config + ข้ามถ้าไม่มี path
- Bug 2 (Critical): `except Error as e:` บรรทัด 372 → `Error` ไม่ได้ import → `NameError` ตอน query ผิดพลาด
  → แก้: เปลี่ยนเป็น `except oracledb.Error as e:`
- Bug 3 (Medium): เข้าถึง `cursor.description` ก่อนตรวจว่า `rows` ว่างเปล่า → `TypeError` เมื่อ lot ไม่พบ
  → แก้: ย้าย `if not rows:` ขึ้นมาก่อน `columns = [...]`
- เพิ่ม mock mode: ใช้ `MockOracleConnection` เมื่อ `mock_mode = true`

**5. `src/config_manager.py`**
- Before: `load_default_config()` มีแค่ `"database"` key เดียว → `database_manager` ไม่เจอ `read_database` / `write_database` / `read_database_staff`
- After: เพิ่ม 4 sections ใหม่ใน default config
- ลบ `from PySide6.QtWidgets import QApplication` ที่ import แต่ไม่ได้ใช้ (ทำให้ import config_manager ต้องการ Qt)

**6. `src/login_scan.py` — fix KeyError**
- Before: `config_manager.current_config['read_database']['database'] = ...` → `KeyError` ถ้า key ไม่มี
- After: ตรวจก่อน + สร้าง dict ถ้าจำเป็น

---

## [2026-05-08] — UI Redesign & Stability Improvements

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `Qss/scss/defaultStyle.scss` | เขียนใหม่ — design system ครบถ้วน |
| `json-styles/style.json` | แก้ไข — แก้สี LightBlue, เพิ่ม Dark-Blue theme |
| `src/Functions.py` | แก้ไข — เพิ่ม `_clear_inline_styles()` |
| `src/graph_updater.py` | แก้ไข — ลบ polling timer ซ้ำซ้อน |

---

### สิ่งที่แก้ไข

**1. Design System (`Qss/scss/defaultStyle.scss`)**
- กำหนด font: Product Sans → Segoe UI → Sans Serif
- Card style สำหรับ frame_3/4/5/6/7: พื้นหลัง theme-adaptive, border-radius 10px, border
- KPI cards (widget_9/10/11): label สีขาว background transparent
- Shot Count card: accent border-left สีฟ้า
- MANUAL PM button: theme-adaptive, hover เปลี่ยนเป็น accent
- FINISH LOT button: เขียว, hover/pressed state
- Scrollbar สวยงาม 8px
- Dialog redesign: rounded, padding, button states
- Header: height constraint, divider line
- Left menu: hover กับ active indicator

**2. Theme (`json-styles/style.json`)**
- LightBlue: Text เปลี่ยนจาก `#010000` → `#1A1A2E` (navy สำหรับ readability)
- LightBlue: Icons เปลี่ยนจาก `#000000` → `#6B7280` (gray ดูดี)
- Dark-Yellow: Icons เปลี่ยนเป็น `#adb5bd`
- เพิ่ม theme ใหม่: **Dark-Blue** (background `#0f1923`, accent `#26bae3`)
- แก้ typo: "Ligh-tBlue" → "LightBlue"

**3. Inline style cleanup (`src/Functions.py`)**
- `_clear_inline_styles()`: ลบ `background-color: rgb(255,255,255)` และ `color: rgb(0,0,0)` จาก .ui
- KPI cards: ตั้ง palette ใหม่ orange (#e67e22) / blue (#2980b9) / teal (#1abc9c)
- ผลลัพธ์: Dark theme ใช้งานได้ถูกต้องแล้ว (ไม่มีกล่องขาวค้าง)

**4. Stability (`src/graph_updater.py`)**
- ลบ QTimer ที่ poll ทุก 1 วินาที
- เหลือเพียง `plc_window.data_updated.connect(handle_plc_data_update)`
- ป้องกัน double-update ที่ทำให้กราฟกระตุก

---

### ความแตกต่างจากเดิม (Before → After)
| ประเด็น | ก่อนแก้ | หลังแก้ |
|--------|---------|---------|
| Dark theme | card ขาวทุก card | card theme-adaptive |
| KPI cards | orange/blue/light-blue (low contrast) | orange/blue/teal พร้อม white text |
| กราฟ update | timer 1s + signal (double) | signal only |
| Fonts | Sans Serif เดียว | Product Sans → Segoe UI → Sans Serif |
| Themes | 2 (Light, Dark-Yellow) | 3 (+Dark-Blue) |
| Shot Count label | สีดำ | สี accent ใหญ่ 14pt |

---

## [2026-05-08] — Code Reorganization (Module Separation)

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `src/excel_manager.py` | สร้างใหม่ — Excel I/O ทั้งหมดจาก shot_counting.py |
| `src/pm_manager.py` | สร้างใหม่ — PM workflow จาก shot_counting.py |
| `src/system_manager.py` | สร้างใหม่ — process/thread lifecycle จาก main.py |
| `src/shot_counting.py` | เขียนใหม่ — เหลือเฉพาะ core counting + delegate methods |
| `main.py` | แก้ไข — ใช้ SystemManager, ลบ method เก่า, ลบ import ที่ไม่ใช้ |

---

### สิ่งที่แก้ไข

**1. `src/excel_manager.py` (ใหม่ ~280 บรรทัด)**
- สกัด Excel I/O ทั้งหมดออกจาก shot_counting.py (auto_save, manual_save, load for PM, slot prediction)
- Pattern: `ExcelManager(shot_counter)` — อ่าน state ผ่าน `self.counter`
- Named constants แทน magic numbers: `_DATA_START_ROW=7`, `_ROW_STEP=3`, `_SLOT_SIZE=9`

**2. `src/pm_manager.py` (ใหม่ ~220 บรรทัด)**
- สกัด PM workflow ออกจาก shot_counting.py (check_pm_condition, predictive PM, login dialog, PM window)
- Pattern: `PMManager(shot_counter)` — อ่าน/เขียน flags ผ่าน `self.counter`

**3. `src/system_manager.py` (ใหม่ ~170 บรรทัด)**
- สกัด process/thread management ออกจาก main.py
- Methods: `kill_zombie_processes()`, `stop_all_threads_and_timers()`, `safe_restart()`, `force_quit()`, `clean_temp_files()`
- `safe_restart()` ใช้ `os.execv` (Unix) หรือ `subprocess.Popen` (Windows)

**4. `src/shot_counting.py` (เขียนใหม่ 1055 → ~320 บรรทัด)**
- เหลือเฉพาะ core counting logic + state management
- สร้าง sub-managers ใน `__init__`: `self.excel_mgr = ExcelManager(self)`, `self.pm_mgr = PMManager(self)`
- Thin delegate methods เพื่อ backward compatibility: `manual_pm_trigger()`, `manual_save()`, `load_excel_data_for_pm()`

**5. `main.py` (refactored)**
- สร้าง `self.sys_mgr = SystemManager(self)` ใน `__init__` แทน inline code
- ลบ 9 method เก่า: `_kill_zombie_processes`, `_stop_all_threads_and_timers`, `restart_application`, `_safe_restart_process`, `_force_quit`, `_clean_temp_files`, `_reset_heat_map_data`, `_reset_plc_data`, `_reset_shot_counter_data`
- ลบ import ที่ไม่ใช้: numpy, matplotlib, pandas, seaborn, psutil, QDialog, QFrame, QObject, QTimer, QMargins, QChart group, QColor, QPainter, GraphManager, MyWindow
- เปลี่ยน `print()` ทั้งหมดเป็น `log.*`

---

### เหตุผล
shot_counting.py (1055 บรรทัด) และ main.py ยากต่อการ maintain เพราะรวม concern หลายอย่างไว้ด้วยกัน
การแยก module ทำให้แต่ละไฟล์มีหน้าที่เดียว ง่ายต่อการทดสอบและแก้ไข

---

### ความแตกต่างจากเดิม (Before → After)
| ประเด็น | ก่อนแก้ | หลังแก้ |
|--------|---------|---------|
| shot_counting.py | 1055 บรรทัด (counting + Excel + PM) | ~320 บรรทัด (counting only) |
| Excel logic | ฝังใน ShotCounter | ExcelManager แยกไฟล์ |
| PM workflow | ฝังใน ShotCounter | PMManager แยกไฟล์ |
| Process lifecycle | method ใน MainWindow | SystemManager แยกไฟล์ |
| main.py imports | numpy, matplotlib, pandas, seaborn, psutil ฯลฯ | เฉพาะที่ใช้จริง |
| main.py LOC | ~870 บรรทัด | ~330 บรรทัด |

---

## [2026-05-07] — Code Quality & Reliability Improvements

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `main.py` | แก้ไข — ลบโค้ดซ้ำ cleanup, เพิ่ม TCP indicator, wire TCP signal |
| `src/PLCdata.py` | แก้ไข — เพิ่ม `connection_status` signal ใน TCPWorker, เพิ่ม logger |
| `src/database_manager.py` | แก้ไข — เพิ่ม retry logic, เปลี่ยนเป็น logger |
| `src/shot_counting.py` | แก้ไข — เพิ่ม .bak atomic write |
| `src/app_logger.py` | สร้างใหม่ — centralized rotating file logger |
| `tests/test_shot_count_save.py` | สร้างใหม่ — 11 unit tests |
| `tests/test_database_manager_retry.py` | สร้างใหม่ — 5 unit tests |
| `tests/test_tcp_worker_signals.py` | สร้างใหม่ — 4 unit tests |
| `src/shot_counting1.py` | ลบ — ไม่มีการใช้งาน (dead code) |

---

### สิ่งที่แก้ไข

**1. ลบโค้ดซ้ำ cleanup (`main.py`)**
- สกัด `_cleanup_heatmap()` method เดียวแทนที่จะซ้ำ 3 ครั้งใน `_cleanup_before_restart()`, `_cleanup_before_exit()`, `handle_forced_logout_completion()`

**2. Centralized Logger (`src/app_logger.py`)**
- `get_logger(name)` ส่งคืน child logger ภายใต้ namespace `SmartOST`
- Log ไปยัง console (INFO+) และ rotating file (DEBUG+, max 5 MB × 5 backup) ใน logs folder
- `database_manager.py` และ `PLCdata.py` เปลี่ยนจาก `print()` เป็น `log.*`

**3. TCP Connection Status UI (`src/PLCdata.py`, `main.py`)**
- `TCPWorker` emit signal `connection_status` = `"connected"` / `"disconnected"` / `"reconnecting"`
- `PLCWindow` forward เป็น signal `tcp_status_changed`
- `MainWindow._setup_tcp_status_indicator()` เพิ่ม QLabel แสดงสีใน header (เฉพาะ TCP mode)

**4. DB Retry Logic (`src/database_manager.py`)**
- เพิ่ม `_connect_with_retry()`: 3 attempts, exponential backoff (1s → 2s → 4s)
- ทั้ง 3 connection (read/write/staff) ใช้ method นี้แทนการ connect ครั้งเดียว

**5. Shot Count Atomic Write (`src/shot_counting.py`)**
- เขียน `.bak` ก่อน แล้วใช้ `shutil.move()` replace ไฟล์จริง
- ป้องกันไฟล์ corrupt ถ้าแอปปิดกลางทาง

**6. Unit Tests (`tests/`)**
- `test_shot_count_save.py` — persistence roundtrip, backup-no-leftover, edge cases
- `test_database_manager_retry.py` — retry succeed/fail scenarios
- `test_tcp_worker_signals.py` — status string logic
- รัน: `python3 -m unittest discover -s tests -v` → 19/19 passed

---

### เหตุผล
เพิ่มความน่าเชื่อถือและ maintainability ของระบบ:
- ลด bug surface จากโค้ดซ้ำ
- ป้องกันข้อมูล shot count หายเมื่อไฟดับ
- แสดง TCP status ให้ผู้ใช้รู้ทันทีเมื่อ Pi หลุด
- DB ไม่ล้มเหลวจาก network hiccup ชั่วคราว

---

### ความแตกต่างจากเดิม (Before → After)
| ประเด็น | ก่อนแก้ | หลังแก้ |
|--------|---------|---------|
| cleanup heatmap | ซ้ำ 3 ที่ใน main.py | method เดียว `_cleanup_heatmap()` |
| Logging | `print()` ปนกับ `logging` | `SmartOST` logger ทุกที่ |
| TCP disconnected | ไม่มีแจ้งใน UI | QLabel สีแดง/เขียว/เหลืองใน header |
| DB connection fail | fail ทันที | retry 3 ครั้ง + exponential backoff |
| Shot count save | เขียนไฟล์ตรงๆ | เขียน .bak ก่อน → atomic move |
| Tests | ไม่มี | 19 unit tests, 0 failures |
| Dead code | `shot_counting1.py` (1706 บรรทัด) | ลบแล้ว |

---

## [2026-05-07] — Pi-to-PC TCP Integration (Dual-Mode Serial/TCP)

### ไฟล์ที่แก้ไข
| ไฟล์ | ประเภทการเปลี่ยน |
|------|-----------------|
| `src/config_manager.py` | แก้ไข — เพิ่ม config keys ใหม่ |
| `src/PLCdata.py` | แก้ไข — เพิ่ม class + แก้ logic init |
| `pi_plc_reader.py` | สร้างใหม่ — script สำหรับ Raspberry Pi |

---

### สิ่งที่แก้ไข

**`src/config_manager.py`**
- เพิ่ม `"connection_mode": "serial"` ใน `plc` section (ค่า default)
- เพิ่ม `"tcp"` section ใหม่: `pi_ip`, `pi_port`, `reconnect_interval`
- เพิ่ม method `get_tcp_config()`

**`src/PLCdata.py`**
- เพิ่ม class `TCPWorker(QObject)` — รับ JSON จาก Pi ผ่าน TCP พร้อม auto-reconnect
- แก้ `PLCWindow.__init__()` — เลือก Worker ตาม `connection_mode` จาก config

**`pi_plc_reader.py`** (ใหม่)
- class `PLCReader` — อ่าน PLC ผ่าน Serial (logic เดียวกับ PLCdata.py เดิม)
- class `TCPServer` — รับ connection จาก PC และ broadcast JSON
- `--mock` flag — ส่ง dummy data สำหรับทดสอบโดยไม่ต้องต่อ PLC จริง

---

### เหตุผล
ต้องการย้าย Serial reader ออกจาก PC ไปยัง Raspberry Pi ที่อยู่ใกล้ PLC มากกว่า
เชื่อมต่อผ่านสาย Ethernet โดยตรง (Point-to-Point) โดยไม่ต้องใช้ Internet หรือ Router

---

### ความแตกต่างจากเดิม (Before → After)
| ประเด็น | ก่อนแก้ | หลังแก้ |
|--------|---------|---------|
| อ่าน PLC บนอุปกรณ์ใด | PC โดยตรง | Raspberry Pi |
| การส่งข้อมูลมา PC | Serial port | TCP Socket ผ่าน Ethernet |
| config.json | ไม่มี `connection_mode` / `tcp` section | มี `connection_mode: serial/tcp` และ `tcp` section |
| PLCdata.py | มีแค่ `PLCWorker` | มีทั้ง `PLCWorker` และ `TCPWorker` |
| กลับโหมดเดิม | — | เปลี่ยน `connection_mode: "serial"` ใน config.json |
| ไฟล์ downstream | ไม่เปลี่ยน | ไม่เปลี่ยน (ใช้ signal เดิม) |

---
