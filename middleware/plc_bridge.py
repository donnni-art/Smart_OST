"""
PLC Bridge Middleware
Connects PLC serial communication to WebSocket server
"""

import asyncio
import websockets
import json
import serial
import time
import sys
import os
from datetime import datetime

# Configuration
WS_URL = "ws://localhost:8080"
SERIAL_PORT = ""  # Will be loaded from config
SERIAL_BAUDRATE = 9600
SERIAL_BYTESIZE = 8
SERIAL_PARITY = 'E'
SERIAL_STOPBITS = 1
SERIAL_TIMEOUT = 1

RECONNECT_INTERVAL = 5
HEARTBEAT_INTERVAL = 30

class PLCBridge:
    def __init__(self):
        self.ws = None
        self.serial_conn = None
        self.running = False
        self.last_data = {}
        self.load_config()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            plc_config = config.get('plc', {})
            global SERIAL_PORT, SERIAL_BAUDRATE, SERIAL_BYTESIZE, SERIAL_PARITY, SERIAL_STOPBITS, SERIAL_TIMEOUT
            
            SERIAL_PORT = plc_config.get('port', '')
            SERIAL_BAUDRATE = plc_config.get('baudrate', 9600)
            SERIAL_BYTESIZE = plc_config.get('bytesize', 8)
            SERIAL_PARITY = plc_config.get('parity', 'E')
            SERIAL_STOPBITS = plc_config.get('stopbits', 1.0)
            SERIAL_TIMEOUT = plc_config.get('timeout', 1)
            
            print(f"✅ Configuration loaded: Port={SERIAL_PORT}, Baudrate={SERIAL_BAUDRATE}")
            
        except Exception as e:
            print(f"⚠️ Error loading config: {e}")
            print("Using default configuration")
    
    def connect_serial(self):
        """Connect to PLC via serial port"""
        try:
            if not SERIAL_PORT:
                print("⚠️ Serial port not configured")
                return False
                
            self.serial_conn = serial.Serial(
                port=SERIAL_PORT,
                baudrate=SERIAL_BAUDRATE,
                bytesize=SERIAL_BYTESIZE,
                parity=SERIAL_PARITY,
                stopbits=SERIAL_STOPBITS,
                timeout=SERIAL_TIMEOUT
            )
            print(f"✅ Connected to PLC on {SERIAL_PORT}")
            return True
            
        except Exception as e:
            print(f"❌ Serial connection error: {e}")
            return False
    
    async def connect_websocket(self):
        """Connect to WebSocket server"""
        try:
            self.ws = await websockets.connect(WS_URL)
            print(f"✅ Connected to WebSocket server at {WS_URL}")
            
            # Subscribe to PLC channel
            await self.ws.send(json.dumps({
                'type': 'subscribe',
                'channel': 'plc'
            }))
            
            return True
            
        except Exception as e:
            print(f"❌ WebSocket connection error: {e}")
            return False
    
    def read_plc_data(self):
        """Read data from PLC"""
        try:
            if not self.serial_conn or not self.serial_conn.is_open:
                return None
            
            # Send read command to PLC
            # This is based on the existing PLCdata.py implementation
            commands = {
                'product_name': 'RD DM1900 10\r',
                'total_sheet': 'RD DM1920 1\r',
                'shot_per_sheet': 'RD DM1921 1\r',
                'pcs_number': 'RD DM1922 1\r',
                'dm1923': 'RD DM1923 1\r'
            }
            
            data = {}
            
            for key, command in commands.items():
                self.serial_conn.write(command.encode('ascii'))
                time.sleep(0.1)
                
                response = self.serial_conn.readline().decode('ascii', errors='ignore').strip()
                
                if key == 'product_name':
                    # Parse product name from response
                    if response:
                        # Extract product name from response
                        parts = response.split()
                        if len(parts) > 1:
                            # Convert hex values to ASCII
                            hex_values = parts[1:]
                            product_name = ''
                            for hex_val in hex_values:
                                try:
                                    # Convert hex to int, then to char
                                    val = int(hex_val, 16)
                                    if val > 0:
                                        product_name += chr(val)
                                except:
                                    pass
                            data[key] = product_name.strip()
                        else:
                            data[key] = ''
                    else:
                        data[key] = ''
                else:
                    # Parse numeric value
                    if response:
                        parts = response.split()
                        if len(parts) > 1:
                            try:
                                data[key] = int(parts[1], 16)
                            except:
                                data[key] = 0
                        else:
                            data[key] = 0
                    else:
                        data[key] = 0
            
            return data
            
        except Exception as e:
            print(f"❌ Error reading PLC data: {e}")
            return None
    
    async def send_to_websocket(self, data):
        """Send PLC data to WebSocket server"""
        try:
            if self.ws and self.ws.open:
                message = {
                    'type': 'plc_update',
                    'data': data,
                    'timestamp': datetime.now().isoformat()
                }
                await self.ws.send(json.dumps(message))
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error sending to WebSocket: {e}")
            return False
    
    async def heartbeat(self):
        """Send periodic heartbeat to keep connection alive"""
        while self.running:
            try:
                if self.ws and self.ws.open:
                    await self.ws.send(json.dumps({'type': 'ping'}))
                await asyncio.sleep(HEARTBEAT_INTERVAL)
            except Exception as e:
                print(f"⚠️ Heartbeat error: {e}")
                break
    
    async def main_loop(self):
        """Main processing loop"""
        self.running = True
        
        # Connect to serial
        if not self.connect_serial():
            print("⚠️ Running without serial connection (demo mode)")
        
        while self.running:
            try:
                # Connect to WebSocket if not connected
                if not self.ws or not self.ws.open:
                    await self.connect_websocket()
                    if self.ws and self.ws.open:
                        # Start heartbeat task
                        asyncio.create_task(self.heartbeat())
                
                # Read PLC data
                plc_data = self.read_plc_data()
                
                if plc_data:
                    # Check if data changed
                    if plc_data != self.last_data:
                        print(f"📊 PLC Data: {plc_data}")
                        
                        # Send to WebSocket
                        if await self.send_to_websocket(plc_data):
                            self.last_data = plc_data.copy()
                        else:
                            print("⚠️ Failed to send data to WebSocket")
                
                # Wait before next read
                await asyncio.sleep(1)
                
            except websockets.exceptions.ConnectionClosed:
                print("⚠️ WebSocket connection closed, reconnecting...")
                self.ws = None
                await asyncio.sleep(RECONNECT_INTERVAL)
                
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                await asyncio.sleep(RECONNECT_INTERVAL)
    
    def stop(self):
        """Stop the bridge"""
        self.running = False
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        print("🛑 PLC Bridge stopped")

async def main():
    """Main entry point"""
    print("=" * 50)
    print("PLC Bridge Middleware")
    print("=" * 50)
    
    bridge = PLCBridge()
    
    try:
        await bridge.main_loop()
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    finally:
        bridge.stop()

if __name__ == "__main__":
    asyncio.run(main())
