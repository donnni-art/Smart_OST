import json
import os
import sys
import oracledb

# Set up Oracle client
oracledb.init_oracle_client(lib_dir=r"C:\instantclient_19_29")

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('check_lot_database', {})
    except Exception as e:
        print(f"Error loading config.json: {e}")
        return {}

def connect_db(db_config):
    try:
        host = db_config.get('host', 'localhost')
        port = db_config.get('port', 1521)
        user = db_config.get('user', 'system')
        password = db_config.get('password', '')
        service_name = db_config.get('service_name') or db_config.get('database') or 'ORCL'
        
        dsn = f"{host}:{port}/{service_name}"
        print(f"Connecting to {dsn}...")
        return oracledb.connect(user=user, password=password, dsn=dsn)
    except Exception as e:
        print(f"Connection failed: {e}")
        # Try SID
        try:
            name = db_config.get('service_name')
            dsn_sid = oracledb.makedsn(host, port, sid=name)
            print(f"Retrying with SID: {dsn_sid}")
            return oracledb.connect(user=user, password=password, dsn=dsn_sid)
        except Exception as e2:
             print(f"SID Connection failed: {e2}")
             return None

def analyze_lot(lot_number):
    db_config = load_config()
    if not db_config:
        return

    conn = connect_db(db_config)
    if not conn:
        return

    cursor = conn.cursor()

    # Query without filters (LEFT JOINs, No Station Filter)
    print(f"\n--- Analyzing LOT: {lot_number} ---")
    
    query = """
        SELECT
               ft.TTL_LOT_MOS,
               ft.TTL_SCAN_STATION,
               ft.TTL_TOOLS_TYPE,
               fttt.TTT_TOOLS_TYPE_NAME,
               ft.TTL_PROCESS,
               fp.PROC_DISP,
               ft.TTL_SCAN_DATE
        FROM FPC.FPCT_TRACE_TOOLS_LOT ft
        LEFT JOIN FPC.FPC_PROCESS fp 
               ON ft.TTL_PROCESS = fp.PROC_ID
        LEFT JOIN FPC.FPCT_TRACE_TOOLS_TYPE fttt 
               ON ft.TTL_TOOLS_TYPE = fttt.TTT_TOOLS_TYPE
        WHERE ft.TTL_LOT_MOS = :lot_number
    """
    
    try:
        cursor.execute(query, lot_number=lot_number)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print(f"❌ Lot {lot_number} NOT FOUND in FPCT_TRACE_TOOLS_LOT")
        else:
            print(f"✅ Found {len(rows)} records in FPCT_TRACE_TOOLS_LOT:")
            print("-" * 80)
            
            has_valid_fixture = False
            has_valid_operator = False
            
            for row in rows:
                data = dict(zip(columns, row))
                station = data.get('TTL_SCAN_STATION', 'None')
                tools_type = data.get('TTT_TOOLS_TYPE_NAME', 'Unknown')
                proc = data.get('PROC_DISP', 'Unknown')
                
                print(f"Row Data:")
                print(f"  - Station: {station}")
                print(f"  - Type: {tools_type} (ID: {data.get('TTL_TOOLS_TYPE')})")
                print(f"  - Process: {proc} (ID: {data.get('TTL_PROCESS')})")
                
                # Check Station
                is_station_valid = False
                if station and '10.17.86' in station:
                    print("    ✅ Station OK")
                    is_station_valid = True
                else:
                    print("    ❌ Station INVALID (Must contain '10.17.86')")
                
                # Check Joins
                if tools_type == 'Unknown':
                    print("    ❌ Missing Tool Type (Join Fail)")
                if proc == 'Unknown':
                    print("    ❌ Missing Process (Join Fail)")
                    
                if tools_type == 'FIXTURE':
                    if is_station_valid:
                        has_valid_fixture = True
                        print("    ✅ VALID FIXTURE FOUND")
                    else:
                        print("    ⚠️ Found FIXTURE but at INVALID Station (App will hide this)")
                        
                if tools_type == 'OPERATOR':
                    if is_station_valid:
                        has_valid_operator = True
                        print("    ✅ VALID OPERATOR FOUND")
                    else:
                         print("    ⚠️ Found OPERATOR but at INVALID Station (App will hide this)")
                         
                print("-" * 40)

            print("\n--- Summary ---")
            if not has_valid_fixture:
                print("❌ FAILED: No FIXTURE found at valid station (10.17.86%)")
            if not has_valid_operator:
                print("❌ FAILED: No OPERATOR found at valid station (10.17.86%)")
            
            if has_valid_fixture and has_valid_operator:
                 print("✅ PASS: Found both Fixture and Operator at Valid Station")
            else:
                 print("❌ FAIL: App will reject this Lot because Fixture/Operator were scanned at wrong IP.")

    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        lot = sys.argv[1]
    else:
        lot = input("Enter Lot Number: ").strip()
    
    if lot:
        analyze_lot(lot)
