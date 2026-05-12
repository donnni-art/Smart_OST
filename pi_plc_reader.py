"""
pi_plc_reader.py — รันบน Raspberry Pi
อ่านข้อมูล PLC ผ่าน Serial แล้วส่ง JSON ไปยัง PC ผ่าน TCP Socket

การใช้งาน:
    python3 pi_plc_reader.py               # โหมดปกติ
    python3 pi_plc_reader.py --mock        # โหมดทดสอบ (ส่ง dummy data ไม่ต้องต่อ PLC)

Network:
    Pi IP  : 192.168.1.10  (ตั้ง Static IP บน eth0)
    PC IP  : 192.168.1.20
    Port   : 9999
"""

import sys
import time
import json
import socket
import threading
import argparse

try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except ImportError:
    SERIAL_AVAILABLE = False
    print("⚠️  pyserial not installed — only --mock mode available")


# ─────────────────────────────────────────────
# Config (แก้ตามเครื่อง Pi จริง)
# ─────────────────────────────────────────────
PLC_PORT        = "/dev/ttyUSB0"   # หรือ /dev/ttyS0, /dev/ttyAMA0
PLC_BAUDRATE    = 9600
PLC_BYTESIZE    = serial.EIGHTBITS if SERIAL_AVAILABLE else 8
PLC_PARITY      = serial.PARITY_EVEN if SERIAL_AVAILABLE else "E"
PLC_STOPBITS    = serial.STOPBITS_ONE if SERIAL_AVAILABLE else 1
PLC_TIMEOUT     = 0.3

TCP_HOST        = "0.0.0.0"   # รับจากทุก interface
TCP_PORT        = 9999
READ_INTERVAL   = 0.5         # วินาที


# ─────────────────────────────────────────────
# PLC Reader
# ─────────────────────────────────────────────
class PLCReader:
    def __init__(self):
        self.serial_port = None
        self.connected = False

        # ค่า DM ทั้งหมด
        self.value_dm1923 = 0
        self.value_dm1924 = 0
        self.value_dm1925 = 0
        self.value_dm1921 = 0
        self.value_dm1917 = 0
        self.value_dm1919 = 0
        self.value_dm1911 = 0
        self.value_dm1912 = 0
        self.value_dm1915 = 0
        self.value_dm1914 = 0
        self.value_dm1913 = 0
        self.value_dm1901 = 0
        self.value_dm1902 = 0
        self.value_dm1905 = 0
        self.value_dm1904 = 0
        self.value_dm1900 = 0
        self.value_dm1251 = 0
        self.value_dm5050 = 0
        self.value_dm5051 = 0
        self.shot_number = 0
        self.pcs_number = 0
        self.defect_shot_per_pcs = []
        self.product_name = ""
        self.lot_number = ""
        self.shot_pcs_dict = {}
        self.defect_count_per_sp = {}

    def connect(self):
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()

            self.serial_port = serial.Serial(
                port=PLC_PORT,
                baudrate=PLC_BAUDRATE,
                bytesize=PLC_BYTESIZE,
                parity=PLC_PARITY,
                stopbits=PLC_STOPBITS,
                timeout=PLC_TIMEOUT
            )
            if self.serial_port.is_open:
                print(f"✅ Serial connected: {PLC_PORT}")
                self.connected = True
                self._init_plc()
                return True
        except Exception as e:
            print(f"❌ Serial connect error: {e}")
            self.connected = False
        return False

    def _init_plc(self):
        self._read_shot_pcs_number()
        self._send_mws_command()

    def _read_shot_pcs_number(self):
        try:
            self.serial_port.write(b"CR\r")
            self.serial_port.readline()

            cmd = "MWS DM5050.U DM5051.U\r"
            self.serial_port.write(cmd.encode())
            self.serial_port.readline()

            time.sleep(0.3)
            response = ""
            for _ in range(3):
                self.serial_port.write(b"MWR\r")
                resp = self.serial_port.readline().decode().strip()
                if resp and all(x.isdigit() for x in resp.split()[:2]):
                    response = resp
                    break
                time.sleep(0.2)

            if response:
                vals = response.split()
                self.value_dm5050 = int(vals[0])
                self.value_dm5051 = int(vals[1])
                self.pcs_number = self.value_dm5050
                self.shot_number = self.value_dm5051
                print(f"PCS={self.pcs_number}  SHOT={self.shot_number}")

            self.serial_port.write(b"CQ\r")
            self.serial_port.readline()
        except Exception as e:
            print(f"_read_shot_pcs_number error: {e}")

    def _send_mws_command(self):
        TOTAL_SHOTS = 16
        ADDRESSES_PER_SHOT = 32
        START_DM = 3300

        BASE_CMD = (
            "MWS DM1923.U DM1924.U DM1925.U DM1921.U DM1911.U DM1912.U "
            "DM1915.U DM1914.U DM1901.U DM1902.U DM1905.U DM1904.U DM1900.U DM1913.U "
            "DM5000.U DM5001.U DM5002.U DM5003.U DM5004.U "
            "DM5005.U DM5006.U DM5007.U DM5008.U DM5009.U "
            "DM5010.U DM5011.U DM5012.U DM5013.U DM5014.U "
            "DM1251.U "
            "DM1230.U DM1231.U DM1232.U DM1233.U DM1234.U "
            "DM1235.U DM1236.U DM1237.U DM1238.U DM1239.U "
            "DM1240.U DM1241.U DM1242.U DM1243.U DM1244.U DM1245.U "
            "DM1919.U DM1917.U "
        )

        if not (self.connected and self.serial_port and self.serial_port.is_open):
            return

        try:
            self.serial_port.write(b"CR\r")
            self.serial_port.readline()
            time.sleep(1)

            device_shots_dict = {}
            for shot in range(1, TOTAL_SHOTS + 1):
                start = START_DM + (shot - 1) * ADDRESSES_PER_SHOT
                device_shots_dict[f"device_shot_{shot}"] = [
                    f"DM{start + i}.U" for i in range(ADDRESSES_PER_SHOT)
                ]

            result_list = []
            for shot in range(1, self.shot_number + 1):
                result_list.extend(device_shots_dict[f"device_shot_{shot}"][:self.pcs_number])

            full_cmd = f"{BASE_CMD}{' '.join(result_list)}\r"
            self.serial_port.write(full_cmd.encode())
            self.serial_port.readline()
            print("✅ MWS command sent")
        except Exception as e:
            print(f"_send_mws_command error: {e}")

    def read(self):
        if not (self.connected and self.serial_port and self.serial_port.is_open):
            return None

        try:
            for _ in range(3):
                self.serial_port.write(b"MWR\r")
                response = self.serial_port.readline().decode(errors='ignore').strip()
                if response:
                    return response
            self.connected = False
            return None
        except Exception:
            self.connected = False
            return None

    def parse(self, value_str):
        values = value_str.split()
        filtered = [v for v in values if not v.startswith("E") and v.isdigit()]
        if len(filtered) < 14:
            return None

        try:
            int_vals = [int(v) for v in filtered[:14]]
            (
                self.value_dm1923, self.value_dm1924, self.value_dm1925,
                self.value_dm1921, self.value_dm1911, self.value_dm1912,
                self.value_dm1915, self.value_dm1914, self.value_dm1901,
                self.value_dm1902, self.value_dm1905, self.value_dm1904,
                self.value_dm1900, self.value_dm1913
            ) = int_vals

            self.product_name = self._parse_product_name(filtered[14:28])
            self.value_dm1251 = int(filtered[29]) if len(filtered) > 29 else 0
            self.value_dm1919 = int(filtered[46]) if len(filtered) > 46 else 0
            self.value_dm1917 = int(filtered[47]) if len(filtered) > 47 else 0
            self.defect_shot_per_pcs = [int(v) for v in filtered[48:]] if len(filtered) > 48 else []

            return self._build_data_dict()
        except Exception as e:
            print(f"parse error: {e}")
            return None

    def _parse_product_name(self, raw):
        name = ""
        for val in raw:
            try:
                word = int(val)
                name += chr((word >> 8) & 0xFF) + chr(word & 0xFF)
            except Exception:
                continue
        return name.strip('\x00')

    def _analyze_defects(self):
        DEFECTS = {"OPEN": 0x05, "SHORT": 0x03, "BLKM": 0x21, "SHOT": 0x09, "MAT": 0x11}
        result = {}
        for shot_i in range(self.shot_number):
            start = shot_i * self.pcs_number
            shot_data = self.defect_shot_per_pcs[start:start + self.pcs_number]
            for pcs_i, value in enumerate(shot_data):
                key = f"S{shot_i+1}P{pcs_i+1}"
                low = int(value) & 0xFF
                found = [name for name, pat in DEFECTS.items() if bin(low & pat).count("1") >= 2]
                result[key] = found if found else ["PASS"]
        return result

    def _build_data_dict(self):
        return {
            "dm1917": self.value_dm1917,
            "dm1919": self.value_dm1919,
            "dm1923": self.value_dm1923,
            "dm1924": self.value_dm1924,
            "dm1925": self.value_dm1925,
            "dm1911": self.value_dm1911,
            "dm1912": self.value_dm1912,
            "dm1915": self.value_dm1915,
            "dm1914": self.value_dm1914,
            "dm1913": self.value_dm1913,
            "dm1251":     self.value_dm1251,
            "lot_number":   self.lot_number,
            "product_name": self.product_name,
            "shot_number":  self.shot_number,
            "pcs_number":   self.pcs_number,
            "shot_per_pcs": self.defect_shot_per_pcs,
            "defect_results": self._analyze_defects(),
        }

    def default_data(self):
        return {
            "dm1917": 0, "dm1919": 0, "dm1923": 0, "dm1924": 0, "dm1925": 0,
            "dm1911": 0, "dm1912": 0, "dm1915": 0, "dm1914": 0, "dm1913": 0,
            "lot_number": self.lot_number,
            "shot_number": self.shot_number,
            "pcs_number": self.pcs_number,
            "shot_per_pcs": [],
            "defect_results": {},
        }


# ─────────────────────────────────────────────
# TCP Server — broadcast ข้อมูลให้ทุก client
# ─────────────────────────────────────────────
class TCPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients: list[socket.socket] = []
        self.lock = threading.Lock()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"🚀 TCP Server listening on {self.host}:{self.port}")

        t = threading.Thread(target=self._accept_loop, args=(server,), daemon=True)
        t.start()

    def _accept_loop(self, server):
        while True:
            try:
                conn, addr = server.accept()
                print(f"🔗 PC connected from {addr}")
                with self.lock:
                    self.clients.append(conn)
            except Exception as e:
                print(f"Accept error: {e}")

    def broadcast(self, data: dict):
        line = json.dumps(data, ensure_ascii=False) + "\n"
        encoded = line.encode("utf-8")
        with self.lock:
            dead = []
            for c in self.clients:
                try:
                    c.sendall(encoded)
                except Exception:
                    dead.append(c)
            for c in dead:
                self.clients.remove(c)
                print("⚠️  Client disconnected")


# ─────────────────────────────────────────────
# Mock data generator (ใช้ทดสอบโดยไม่ต้อง PLC)
# ─────────────────────────────────────────────
def mock_data_generator():
    import math
    t = 0
    while True:
        t += 1
        data = {
            "dm1917": 100 + t,
            "dm1919": 95 + t,
            "dm1923": t % 50,
            "dm1924": (t + 1) % 50,
            "dm1925": (t + 2) % 50,
            "dm1911": 1, "dm1912": 0, "dm1915": 0, "dm1914": 0, "dm1913": 0,
            "lot_number": "LOT-TEST-001",
            "shot_number": 4,
            "pcs_number": 2,
            "shot_per_pcs": [0] * 8,
            "defect_results": {},
        }
        yield data
        time.sleep(READ_INTERVAL)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Pi PLC Reader — TCP Server")
    parser.add_argument("--mock", action="store_true", help="ส่ง dummy data แทน PLC จริง")
    args = parser.parse_args()

    server = TCPServer(TCP_HOST, TCP_PORT)
    server.start()

    if args.mock:
        print("🧪 Mock mode — sending dummy data")
        for data in mock_data_generator():
            server.broadcast(data)
        return

    if not SERIAL_AVAILABLE:
        print("❌ pyserial not installed. Run: pip install pyserial")
        sys.exit(1)

    reader = PLCReader()
    last_data = reader.default_data()
    reconnect_interval = 5
    last_reconnect = 0

    print("📡 Starting PLC read loop...")
    while True:
        try:
            if not reader.connected:
                now = time.time()
                if now - last_reconnect >= reconnect_interval:
                    last_reconnect = now
                    reader.connect()
                if not reader.connected:
                    server.broadcast(last_data)
                    time.sleep(READ_INTERVAL)
                    continue

            raw = reader.read()
            if raw:
                data = reader.parse(raw)
                if data:
                    last_data = data
                    server.broadcast(data)
                else:
                    server.broadcast(last_data)
            else:
                server.broadcast(last_data)

            time.sleep(READ_INTERVAL)

        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(READ_INTERVAL)


if __name__ == "__main__":
    main()
