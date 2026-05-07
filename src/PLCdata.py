import sys
import serial
import time
import os
import json
from src.config_manager import config_manager
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QInputDialog, QMessageBox
import serial.tools.list_ports


# ---------- PLCWorker สำหรับรันใน Thread ----------
class PLCWorker(QObject):
    finished = Signal()
    data_ready = Signal(dict)

    def __init__(self, plc_window):
        super().__init__()
        self.plc_window = plc_window
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            try:
                self.plc_window.update_data_from_thread(self.data_ready)
                time.sleep(0.5)
            except Exception:
                print("Error in PLCWorker loop")
        self.finished.emit()

# ---------- Main PLC Window ----------
class PLCWindow(QMainWindow):
    data_updated = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        
         # โหลด configuration
        self.plc_config = config_manager.get_plc_config()
        
        # ใช้ค่าจาก config
        self.last_reconnect_attempt = 0
        self.reconnect_interval = self.plc_config.get('reconnect_interval', 5)
        self.auto_reconnect_enabled = self.plc_config.get('auto_reconnect', True)

        self.shot_cnt_total = 0
        self.shot_cnt_total_config = 0
        self.new_cnt = 0
        self.previous_product_name = None
        self.product_name = ""
        self.lot_number = ""
        self.last_data = None
        self.current_lot_number = None

        self.serial_connected = False
        self.serial_port = None
        self._init_plc_values()
        self.force_emit_counter = 0

        self._init_serial()

        # === ใช้ QThread แทน QTimer ===
        self.worker_thread = QThread()
        self.worker = PLCWorker(self)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.data_ready.connect(self.handle_data_update)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.start()

        print("PLCWindow initialized")

    def _init_plc_values(self):
        print("Initializing PLC values")
        self.value_dm1923 = 0
        self.value_dm1924 = 0
        self.value_dm1925 = 0
        self.value_dm1917 = 0
        self.value_dm1919 = 0
        self.value_dm1911 = 0
        self.value_dm1912 = 0
        self.value_dm1915 = 0
        self.value_dm1914 = 0
        self.value_dm1913 = 0
        self.value_dm1921 = 0
        self.value_dm1901 = 0
        self.value_dm1902 = 0
        self.value_dm1905 = 0
        self.value_dm1904 = 0
        self.value_dm1900 = 0
        self.shot_number = 0
        self.pcs_number = 0

    def _init_serial(self):
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            # อ่านพอร์ตจาก config
            configured_port = self.plc_config.get('port', '')

            # ถ้าไม่ได้กำหนดพอร์ตหรือพอร์ตนั้นไม่มีในระบบ ให้พยายาม reconnect อัตโนมัติ
            try:
                available_ports = [p.device for p in serial.tools.list_ports.comports()]
            except Exception:
                available_ports = []

            if not configured_port or configured_port not in available_ports:
                # Log useful info for troubleshooting
                print(f"Configured port '{configured_port}' not found in available ports: {available_ports}")
                # เรียก auto reconnect (จะลองทุกพอร์ตที่มี)
                if self.plc_config.get('auto_reconnect', True):
                    self.auto_reconnect_serial()
                    return
                else:
                    # ถ้าไม่ต้องการ auto reconnect ให้มาร์กว่าไม่ได้เชื่อมต่อ
                    self.serial_connected = False
                    return

            # ถ้าพอร์ตถูกต้อง ให้เปิดการเชื่อมต่อแบบปกติ
            self.serial_port = serial.Serial(
                port=configured_port,
                baudrate=self.plc_config.get('baudrate', 9600),
                bytesize=self.plc_config.get('bytesize', serial.EIGHTBITS),
                parity=self.get_parity(self.plc_config.get('parity', 'E')),
                stopbits=self.get_stopbits(self.plc_config.get('stopbits', 1)),
                timeout=self.plc_config.get('timeout', 0.3)
            )
            
            if self.serial_port.is_open:
                print(f"Serial port {self.plc_config.get('port')} opened successfully")
                self.serial_connected = True
                self.shot_pcs_number()
                self.send_mws_command()
            else:
                print(f"Failed to open {self.plc_config.get('port')}")
                self.serial_connected = False
        except Exception as e:
            # Log the init error and mark as disconnected
            print(f"Serial init error: {e}")
            self.serial_connected = False

            # Try an automatic reconnect attempt (non-blocking). This helps when the configured
            # COM port is not present at startup (e.g., device connected later or port changed).
            try:
                if getattr(self, 'auto_reconnect_enabled', False):
                    print("Attempting auto-reconnect after serial init failure")
                    # We don't raise here; auto_reconnect_serial handles its own errors
                    self.auto_reconnect_serial()
            except Exception:
                # Ensure any error here doesn't crash initialization--it has already been logged above
                print("Auto-reconnect attempt failed during _init_serial")

    def get_parity(self, parity_char):
        """Convert parity character to serial parity constant"""
        parity_map = {
            'N': serial.PARITY_NONE,
            'E': serial.PARITY_EVEN,
            'O': serial.PARITY_ODD,
            'M': serial.PARITY_MARK,
            'S': serial.PARITY_SPACE
        }
        return parity_map.get(parity_char, serial.PARITY_EVEN)

    def get_stopbits(self, stopbits):
        """Convert stopbits to serial stopbits constant"""
        stopbits_map = {
            1: serial.STOPBITS_ONE,
            1.5: serial.STOPBITS_ONE_POINT_FIVE,
            2: serial.STOPBITS_TWO
        }
        return stopbits_map.get(stopbits, serial.STOPBITS_ONE)

    def shot_pcs_number(self):
        if not self.serial_connected or not self.serial_port or not self.serial_port.is_open:
            print("Serial not connected")
            return

        try:
            # เริ่ม handshake
            self.serial_port.write(b"CR\r")
            cr = self.serial_port.readline().decode().strip()
            #print(f"[START Respond]: {cr}")

            # ตั้งค่า MWS
            cmd = "MWS DM5050.U DM5051.U\r"
            self.serial_port.write(cmd.encode())
            mws = self.serial_port.readline().decode().strip()
            #print(f"[MWS Response]: {mws}")

            # รอให้ PLC เตรียมข้อมูล
            time.sleep(0.3)

            # ดึงค่าจริง (ลอง 3 ครั้งถ้ายังไม่ได้ตัวเลข)
            response = ""
            for i in range(3):
                self.serial_port.write(b"MWR\r")
                resp = self.serial_port.readline().decode().strip()
                if resp and all(x.isdigit() for x in resp.split()[:2]):
                    response = resp
                    break
                time.sleep(0.2)

            if not response:
                print("❌ Failed to read DM5050/DM5051")
                return

            print(f"[MWR Response]: {response}")
            values = response.split()

            self.value_dm5050 = int(values[0])
            self.value_dm5051 = int(values[1])
            self.shot_number = self.value_dm5051
            self.pcs_number = self.value_dm5050

            print(f"SHOT NUMBER: {self.shot_number}")
            print(f"PCS NUMBER: {self.pcs_number}")

            # จบการสื่อสาร
            self.serial_port.write(b"CQ\r")
            cq = self.serial_port.readline().decode().strip()
            print(f"[END Respond]: {cq}")

        except Exception as e:
            print(f"Error in shot_pcs_number: {e}")

    ##############################################################################################
    def send_mws_command(self):
        """Send MWS command to the serial device with improved stability and error handling."""
        # Constants configuration
        TOTAL_SHOTS = 16
        ADDRESSES_PER_SHOT = 32
        START_DM_ADDRESS = 3300
        
        # Fixed command parts (could be moved to class constants if reused)
        BASE_COMMANDS = (
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

        # Validate serial connection first
        if not self._validate_serial_connection():
            return

        try:
            # Initialize communication
            self._send_initial_command()

            # Generate device addresses
            device_shots_dict = self._generate_device_addresses(
                TOTAL_SHOTS, 
                ADDRESSES_PER_SHOT, 
                START_DM_ADDRESS
            )

            # Process the requested shots
            result_shot_command = self._process_requested_shots(
                device_shots_dict,
                self.shot_number,
                self.pcs_number,
                TOTAL_SHOTS
            )

            if result_shot_command is None:
                return  # Error already logged

            # Construct and send full command
            full_cmd = f"{BASE_COMMANDS}{result_shot_command}\r"
            self._send_full_command(full_cmd)

        except Exception as e:
            print(f"Unexpected error in MWS command processing: {e}")
            raise  # Re-raise if you want calling code to handle it

    def _validate_serial_connection(self):
        """Validate the serial connection is available and open."""
        if not (self.serial_connected and self.serial_port and self.serial_port.is_open):
            print("Serial port not available or not open")
            return False
        return True

    def _send_initial_command(self):
        """Send the initial CR command and read response."""
        try:
            self.serial_port.write(b"CR\r")
            cr_response = self.serial_port.readline().decode().strip()
            print(f"[START Respond]: {cr_response}")
            time.sleep(1)  # Consider making this delay configurable
        except Exception as e:
            print(f"Failed to send initial CR command: {e}")
            raise

    def _generate_device_addresses(self, total_shots, addresses_per_shot, start_dm_address):
        """Generate device addresses dictionary."""
        device_shots_dict = {}
        for shot in range(1, total_shots + 1):
            start_index = start_dm_address + (shot - 1) * addresses_per_shot
            device_shots_dict[f"device_shot_{shot}"] = self.generate_device_shot(
                start_index, 
                addresses_per_shot
            )
        return device_shots_dict

    def _process_requested_shots(self, device_shots_dict, shot_number, pcs_number, max_shots):
        """Process the requested shots and return the command string."""
        if shot_number > max_shots:
            error_msg = f"Error: shot_number {shot_number} exceeds maximum {max_shots}"
            print(f"❌ {error_msg}")
            return None

        result_list = []
        for shot in range(1, shot_number + 1):
            device_list = device_shots_dict[f"device_shot_{shot}"]
            selected_devices = device_list[:pcs_number]
            result_list.extend(selected_devices)

        result_shot_command = " ".join(result_list)
        print("✅ Result Shot Command =", result_shot_command)
        
        return result_shot_command

    def _send_full_command(self, full_cmd):
        """Send the full command to the serial device."""
        try:
            self.serial_port.write(full_cmd.encode())
            print("MWS command sent successfully")
            #print("✅ Full Command =", full_cmd)
            
            response_command = self.serial_port.readline().decode().strip()
            print(f"[MWS Respond]: {response_command}")
        except Exception as e:
            print(f"Failed to send full MWS command: {e}")
            raise

    def generate_device_shot(self, start_index, count):
        """Generate device addresses for a shot.
        
        Args:
            start_index: Starting DM address index
            count: Number of addresses to generate
            
        Returns:
            List of device address strings (e.g., ["DM3300.U", "DM3301.U", ...])
        """
        return [f"DM{start_index + i}.U" for i in range(count)]

    ###############################################################################################
    # Read data and update
    ###############################################################################################
    
    def update_data_from_thread(self, emit_signal):
        try:
            # ตรวจสอบการเชื่อมต่อและพยายาม reconnect อัตโนมัติ
            if not self.serial_connected and self.auto_reconnect_enabled:
                current_time = time.time()
                if current_time - self.last_reconnect_attempt >= self.reconnect_interval:
                    self.last_reconnect_attempt = current_time
                    self.auto_reconnect_serial()
            
            if not self.serial_connected:
                if self.last_data:
                    emit_signal.emit(self.last_data)
                return

            value_str = self.read_plc_device()
            if not value_str or value_str.startswith("E"):
                default_data = self._default_data()
                emit_signal.emit(default_data)
                self.last_data = default_data
                return

            values = value_str.split()
            filtered = [v for v in values if not v.startswith("E") and v.isdigit()]

            if len(filtered) < 14:
                emit_signal.emit(self._default_data())
                return

            self._parse_plc_values(filtered)
            new_data = self.get_updated_values()
            defect_results = self.analyze_defect_addresses(self.defect_shot_per_pcs)
            #print(defect_results)

            self.force_emit_counter += 1
            if new_data != self.last_data or self.force_emit_counter >= 10:
                emit_signal.emit(new_data)
                self.last_data = new_data
                self.force_emit_counter = 0
        except Exception as e:
            print(f"update_data_from_thread error: {e}")

    def auto_reconnect_serial(self):
        """พยายามเชื่อมต่ออัตโนมัติโดยไม่ต้องถามผู้ใช้"""
        try:
            # หา COM Port ที่มีอยู่
            available_ports = [port.device for port in serial.tools.list_ports.comports()]
            
            if not available_ports:
                print("No COM ports available for auto-reconnect")
                return
            
            # ลองเชื่อมต่อกับทุกพอร์ตที่หาได้
            for port_name in available_ports:
                if self.try_connect_to_port(port_name):
                    print(f"✅ Auto-reconnected to {port_name}")
                    return
            
            print("Auto-reconnect failed for all available ports")
            
        except Exception as e:
            print(f"Auto-reconnect error: {e}")

    def try_connect_to_port(self, port_name):
        """พยายามเชื่อมต่อกับพอร์ตที่กำหนด"""
        try:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()
            
            self.serial_port = serial.Serial(
                port=port_name,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.3
            )
            
            if self.serial_port.is_open:
                # ทดสอบการเชื่อมต่อด้วยการส่งคำสั่งง่ายๆ
                self.serial_port.write(b"CR\r")
                response = self.serial_port.readline().decode().strip()
                
                if response:  # ถ้ามี response แสดงว่าเชื่อมต่อได้
                    self.serial_connected = True
                    self.serial_port.write(b"CQ\r")  # ปิดการสื่อสารทดสอบ
                    self.serial_port.readline()
                    
                    # ตั้งค่าการเชื่อมต่อใหม่
                    self.shot_pcs_number()
                    self.send_mws_command()
                    return True
            
            return False
            
        except Exception:
            return False

    def read_plc_device(self):
        if not self.serial_connected or not self.serial_port or not self.serial_port.is_open:
            # ไม่เรียก popup อัตโนมัติที่นี่ เพื่อหลีกเลี่ยงการรบกวนผู้ใช้
            # การ reconnect จะจัดการใน update_data_from_thread แทน
            return ""

        try:
            for attempt in range(3):
                self.serial_port.write(b"MWR\r")
                response = self.serial_port.readline().decode(errors='ignore').strip()
                if response:
                    return response
            
            # ถ้าอ่านข้อมูลไม่ได้ 3 ครั้ง ให้ทำเครื่องหมายว่าการเชื่อมต่อหลุด
            print("PLC response empty after retries, marking as disconnected")
            self.serial_connected = False
            return ""
            
        except Exception:
            print("Error reading PLC, marking as disconnected")
            self.serial_connected = False
            return ""

    def reconnect_serial(self, show_popup=True):
        """พยายามเชื่อมต่อ COM ใหม่ โดยสามารถเลือกได้ว่าจะแสดง popup หรือไม่"""
        try:
            selected_port = None
            
            if show_popup:
                # แสดง popup ให้ผู้ใช้เลือก (เหมือนเดิม)
                selected_port = self.select_com_port_popup()
                if not selected_port:
                    print("User cancelled COM port selection")
                    return
            else:
                # โหมดอัตโนมัติ - เลือกพอร์ตแรกที่หาได้
                available_ports = [port.device for port in serial.tools.list_ports.comports()]
                if available_ports:
                    selected_port = available_ports[0]
                    print(f"Auto-selecting first available port: {selected_port}")
                else:
                    print("No COM ports available for auto-reconnect")
                    return
            
            # เชื่อมต่อกับพอร์ตที่เลือก (code เดิม)
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()

            self.serial_port = serial.Serial(
                port=selected_port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.3
            )

            if self.serial_port.is_open:
                print(f"✅ Connected to {selected_port} successfully")
                if show_popup:
                    QMessageBox.information(self, "Connection Successful", f"Connected to {selected_port} successfully")
                self.serial_connected = True
                self.shot_pcs_number()
                self.send_mws_command()
            else:
                self.serial_connected = False
                
        except Exception as e:
            print(f"❌ Reconnect failed: {e}")
            if show_popup:
                QMessageBox.critical(self, "Connection Error", f"Unable to connect to the port\n{e}")
            self.serial_connected = False

    def check_connection_on_startup(self):
        """ตรวจสอบว่าการเชื่อมต่อ PLC พร้อมก่อนเริ่มใช้งาน"""
        # ถ้ายังไม่เชื่อมต่อ → เปิด popup ให้เลือก COM
        if not self.serial_connected or not self.serial_port or not self.serial_port.is_open:
            print("PLC not connected, opening COM port selection popup...")
            self.reconnect_serial()

        # หลังจาก popup แล้ว ยังเชื่อมต่อไม่ได้ → แจ้งเตือนและ return False
        if not self.serial_connected or not self.serial_port or not self.serial_port.is_open:
            QMessageBox.critical(self, "Connection Error", "Unable to connect to PLC\nPlease check COM Port settings")
            return False

        print("✅ PLC Connected Successfully")
        return True

    
    def select_com_port_popup(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]

        if not ports:
            QMessageBox.warning(self, "No COM Ports Found", "No connectable COM ports detected")
            return None

        port, ok = QInputDialog.getItem(
            self,
            "Select COM Port",
            "Please select the COM port to connect:",
            ports,
            0,
            False
        )

        if ok and port:
            return port
        return None

    def analyze_defect_addresses(self, defect_shot_per_pcs):
        if not hasattr(self, 'shot_number') or not hasattr(self, 'pcs_number'):
            return "❌ Shot or PCS number not set."
        try:
            output_lines = []
            self.shot_pcs_dict = {}
            self.defect_count_per_sp = {}

            DEFECTS = {
                "OPEN":  0x05,
                "SHORT": 0x03,
                "BLKM":  0x21,
                "SHOT":  0x09,
                "MAT":   0x11
            }

            for shot_index in range(self.shot_number):
                start = shot_index * self.pcs_number
                end = start + self.pcs_number
                shot_data = defect_shot_per_pcs[start:end]

                line_items = []
                shot_defect_counter = {key: 0 for key in DEFECTS}

                for pcs_index, value in enumerate(shot_data):
                    var_name = f"S{shot_index + 1}P{pcs_index + 1}"

                    try:
                        int_value = int(value)
                    except ValueError:
                        return f"❌ Invalid data at {var_name}: {value}"

                    low_byte = int_value & 0xFF
                    defects_found = []

                    # นับ defect แต่ละประเภท
                    defect_counts = {defect_name: 0 for defect_name in DEFECTS}
                    
                    for defect_name, defect_pattern in DEFECTS.items():
                        match_bits = low_byte & defect_pattern
                        if bin(match_bits).count("1") >= 2:
                            defects_found.append(defect_name)
                            shot_defect_counter[defect_name] += 1
                            defect_counts[defect_name] = 1  # ตั้งค่าเป็น 1 เมื่อพบ defect

                    defect_text = ", ".join(defects_found) if defects_found else "PASS"
                    defect_count = len(defects_found)

                    self.shot_pcs_dict[var_name] = [value, defect_text]
                    self.defect_count_per_sp[var_name] = defect_counts  # เก็บจำนวน defect ทุกประเภท

                    if defect_text == "PASS":
                        line_items.append(f"\n{var_name}: {value} → PASS")
                    else:
                        line_items.append(
                            f"\n{var_name}: {value} → {defect_text} ({defect_count} defect{'s' if defect_count > 1 else ''})"
                        )

                defect_summary = ", ".join([f"{k}: {v}" for k, v in shot_defect_counter.items() if v > 0]) or "No Defects"
                output_lines.append(f"SHOT {shot_index + 1}:")
                output_lines.extend(line_items)
                output_lines.append(f"➡️ Defect Summary for SHOT {shot_index + 1}: {defect_summary}\n")

            return "\n".join(output_lines)

        except Exception as e:
            return f"❌ Error generating data: {e}"
    ###########################################################################################
    # Set default 
    ###########################################################################################

    def _default_data(self):
        return {
            "dm1917": 0, "dm1919": 0, "dm1924": 0, "dm1925": 0, "dm1923": 0,
            "dm1911": 0, "dm1912": 0, "dm1915": 0, "dm1914": 0, "dm1913": 0,
            "lot_number": self.current_lot_number
        }

    ###########################################################################################
    # parse_plc_value
    ###########################################################################################   
    def _parse_plc_values(self, values):
        try:
            int_values = [int(val) if val.isdigit() else 0 for val in values[:14]]
            (
                self.value_dm1923, self.value_dm1924, self.value_dm1925,
                self.value_dm1921, self.value_dm1911, self.value_dm1912,
                self.value_dm1915, self.value_dm1914, self.value_dm1901,
                self.value_dm1902, self.value_dm1905, self.value_dm1904,
                self.value_dm1900, self.value_dm1913
            ) = int_values

            self.product_name = self._parse_product_name(values[14:28])
            self.value_dm1251 = int(values[29]) if len(values) > 29 else 0
            self.value_dm1919 = int(values[46]) if len(values) > 46 else 0
            self.value_dm1917 = int(values[47]) if len(values) > 47 else 0

            if len(values) > 48:
                self.defect_shot_per_pcs = [int(val) if val.isdigit() else 0 for val in values[48:]]
            else:
                self.defect_shot_per_pcs = []

            return self.defect_shot_per_pcs

        except Exception:
            print("Failed to parse PLC values")

    ### Product name 
    def _parse_product_name(self, raw_values):
        product_name = ""
        for val in raw_values:
            try:
                word = int(val)
                high = (word >> 8) & 0xFF
                low = word & 0xFF
                product_name += chr(high) + chr(low)
            except:
                continue
        return product_name.strip('\x00')

    def get_updated_values(self):
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
            "lot_number": self.current_lot_number,
            "shot_number": getattr(self, "shot_number", 0),   # ✅ fallback
            "pcs_number": getattr(self, "pcs_number", 0),     # ✅ fallback
            "shot_per_pcs": getattr(self, "defect_shot_per_pcs", []),  # ✅ fallback
            "defect_results": self.analyze_defect_addresses(
                getattr(self, "defect_shot_per_pcs", [])
            )
        }

    def get_updated_production_calculator(self):
        shot_number = getattr(self, "shot_number", 0)   # ✅ fallback
        dm1923 =getattr(self, 'value_dm1923', 0)
        pcs_number = getattr(self, "pcs_number", 0)
        return {
            "pcs_number": pcs_number,
            "dm1923": dm1923,
            "shot_number": shot_number,
        }

    def handle_data_update(self, data):
        self.data_updated.emit(data)

    def set_current_lot_number(self, lot_number):
        """ตั้งค่า lot number ปัจจุบัน"""
        self.current_lot_number = lot_number
        print(f"Set current lot number: {lot_number}")

    def get_current_lot_number(self):
        return self.current_lot_number

    def get_product_and_shot_count(self):
        """
        คืนค่า product_name และ value_dm1251 (shot count) จากข้อมูลที่อ่านล่าสุด
        Returns:
            dict: {'product_name': str, 'value_dm1251': int}
        """
        # ถ้าไม่มีค่า value_dm1251 ให้คืนเป็น 0
        shot_count = getattr(self, 'value_dm1251', 0)
        total_sheet = getattr(self, 'value_dm1923', 0)
        pcs_number = getattr(self, 'value_dm5050', 0)
        #pcs_per_sheet = total_sheet * total_sheet
        product = self.product_name if self.product_name else ""
        return {
            "product_name": product,
            "shot_count": shot_count,
            "total_sheet": total_sheet,
            "pcs_number":pcs_number,
        }