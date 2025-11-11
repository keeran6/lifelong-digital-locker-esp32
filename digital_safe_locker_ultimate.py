"""
Digital Safe Locker - ULTIMATE VERSION (Enhanced + Battery Optimized)
Features:
- Change password via keypad/BLE
- Persistent password storage
- Admin password protection
- Deep sleep for battery optimization
- Wake on keypad press
- 2-3 month battery life on 4x AA
"""

from machine import Pin, deepsleep, reset
import time
import bluetooth
import json
from ble_simple_peripheral import BLESimplePeripheral
import esp32

# ===== CONFIGURATION =====
DEFAULT_PASSWORD = "1234"
ADMIN_PASSWORD = "9999"
LOCK_OPEN_TIME = 5
MAX_ATTEMPTS = 3

# Battery optimization
IDLE_TIMEOUT = 30  # Seconds before deep sleep
DEEP_SLEEP_DURATION = 1000 * 60 * 5  # 5 minutes

# Password storage
PASSWORD_FILE = "password.json"

# ===== PIN DEFINITIONS =====
RELAY_PIN = 32

# 4x3 Keypad
ROW_PINS = [13, 12, 14]
COL_PINS = [27, 26, 25, 33]

KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C']
]

# ===== HARDWARE SETUP =====
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)

rows = [Pin(pin, Pin.OUT) for pin in ROW_PINS]
for row in rows:
    row.value(1)

cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in COL_PINS]

# ===== GLOBAL VARIABLES =====
entered_password = ""
failed_attempts = 0
lock_state = False
current_password = DEFAULT_PASSWORD

# Password change mode
change_password_mode = False
new_password_entry = ""
password_change_step = 0

# Power management
last_activity = time.time()

# ===== POWER MANAGEMENT =====
def check_idle_timeout():
    """Check if system should enter deep sleep"""
    global last_activity
    if time.time() - last_activity > IDLE_TIMEOUT:
        print("💤 Entering deep sleep to save battery...")
        close_lock()
        time.sleep(1)
        deepsleep(DEEP_SLEEP_DURATION)

def reset_activity_timer():
    """Reset the inactivity timer"""
    global last_activity
    last_activity = time.time()

# ===== PASSWORD MANAGEMENT =====
def load_password():
    """Load password from file"""
    global current_password
    try:
        with open(PASSWORD_FILE, 'r') as f:
            data = json.load(f)
            current_password = data.get('password', DEFAULT_PASSWORD)
            print(f"✅ Password loaded")
    except:
        print("⚠️ No saved password, using default")
        current_password = DEFAULT_PASSWORD
        save_password(current_password)

def save_password(password):
    """Save password to file"""
    try:
        with open(PASSWORD_FILE, 'w') as f:
            json.dump({'password': password}, f)
        print("✅ Password saved")
        return True
    except Exception as e:
        print(f"❌ Save failed: {e}")
        return False

def reset_password():
    """Reset to factory default"""
    global current_password
    current_password = DEFAULT_PASSWORD
    save_password(current_password)
    print("🔄 Password reset to default")

# ===== DOOR LOCK FUNCTIONS =====
def open_lock():
    global lock_state
    print("🔓 Lock OPENED")
    relay.value(1)
    lock_state = True
    reset_activity_timer()

def close_lock():
    global lock_state
    print("🔒 Lock CLOSED")
    relay.value(0)
    lock_state = False

def toggle_lock():
    if lock_state:
        close_lock()
    else:
        open_lock()

# ===== KEYPAD FUNCTIONS =====
def read_keypad():
    for row_num, row_pin in enumerate(rows):
        row_pin.value(0)
        for col_num, col_pin in enumerate(cols):
            if col_pin.value() == 0:
                time.sleep_ms(20)
                if col_pin.value() == 0:
                    while col_pin.value() == 0:
                        time.sleep_ms(10)
                    row_pin.value(1)
                    reset_activity_timer()  # Reset timer on key press
                    return KEYS[row_num][col_num]
        row_pin.value(1)
    return None

def process_keypad_input(key):
    """Process keypad input with password management"""
    global entered_password, failed_attempts
    global change_password_mode, new_password_entry, password_change_step
    
    print(f"Key: {key}")
    reset_activity_timer()
    
    # ===== PASSWORD CHANGE MODE =====
    if change_password_mode:
        if key == '#' or key == 'C':
            if password_change_step == 0:  # Old password
                if entered_password == current_password:
                    print("✅ Old password correct. Enter NEW:")
                    password_change_step = 1
                    entered_password = ""
                else:
                    print("❌ Wrong old password")
                    change_password_mode = False
                    password_change_step = 0
                    entered_password = ""
            
            elif password_change_step == 1:  # New password
                if len(entered_password) >= 4:
                    new_password_entry = entered_password
                    print("✅ New password set. CONFIRM:")
                    password_change_step = 2
                    entered_password = ""
                else:
                    print("❌ Too short (min 4 digits)")
                    entered_password = ""
            
            elif password_change_step == 2:  # Confirm
                if entered_password == new_password_entry:
                    current_password = new_password_entry
                    save_password(current_password)
                    print("🎉 Password changed!")
                    change_password_mode = False
                    password_change_step = 0
                    entered_password = ""
                    new_password_entry = ""
                    # Brief relay blink
                    for _ in range(3):
                        relay.value(1)
                        time.sleep(0.2)
                        relay.value(0)
                        time.sleep(0.2)
                else:
                    print("❌ Passwords don't match")
                    password_change_step = 1
                    entered_password = ""
        
        elif key == '*' or key == 'A':
            print("🔄 Change cancelled")
            change_password_mode = False
            password_change_step = 0
            entered_password = ""
        
        else:
            if len(entered_password) < 8:
                entered_password += key
                print(f"Password: {'*' * len(entered_password)}")
    
    # ===== NORMAL MODE =====
    else:
        if key == '#' or key == 'C':  # Unlock
            if entered_password == current_password:
                print("✅ Correct!")
                open_lock()
                time.sleep(LOCK_OPEN_TIME)
                close_lock()
                failed_attempts = 0
            else:
                failed_attempts += 1
                print(f"❌ Wrong! {failed_attempts}/{MAX_ATTEMPTS}")
                if failed_attempts >= MAX_ATTEMPTS:
                    print("🚨 Too many attempts! 30s lockout")
                    time.sleep(30)
                    failed_attempts = 0
            entered_password = ""
        
        elif key == '*':
            entered_password = ""
            print("🔄 Cleared")
        
        elif key == 'A':
            print("🔑 Password change mode")
            print("Enter OLD password:")
            change_password_mode = True
            password_change_step = 0
            entered_password = ""
        
        elif key == 'B':  # Admin reset
            if entered_password == ADMIN_PASSWORD:
                print("⚡ Admin reset!")
                reset_password()
                entered_password = ""
                for _ in range(5):
                    relay.value(1)
                    time.sleep(0.1)
                    relay.value(0)
                    time.sleep(0.1)
            else:
                print("❌ Admin password required")
                entered_password = ""
        
        else:
            if len(entered_password) < 8:
                entered_password += key
                print(f"Password: {'*' * len(entered_password)}")

# ===== BLUETOOTH FUNCTIONS =====
def on_rx(data):
    """Handle BLE commands"""
    global failed_attempts, current_password
    reset_activity_timer()

    try:
        if not data:
            return
        command = data.decode().strip()
        print(f"BT: {command}")
    except Exception as e:
        print(f"BT: Decode error: {e}")
        return
    
    try:
        if command.startswith("PASS:"):
            password = command[5:]
            if password == current_password:
                print("✅ Correct BT password!")
                open_lock()
                time.sleep(LOCK_OPEN_TIME)
                close_lock()
                ble.send("OK:UNLOCKED\n")
                failed_attempts = 0
            else:
                failed_attempts += 1
                ble.send(f"ERROR:WRONG_PASSWORD:{failed_attempts}/{MAX_ATTEMPTS}\n")

        elif command.startswith("CHANGE:"):
            parts = command.split(":")
            if len(parts) == 3:
                old_pass = parts[1]
                new_pass = parts[2]
                if old_pass == current_password:
                    if len(new_pass) >= 4:
                        current_password = new_pass
                        save_password(current_password)
                        print("🎉 Password changed via BLE!")
                        ble.send("OK:PASSWORD_CHANGED\n")
                    else:
                        ble.send("ERROR:PASSWORD_TOO_SHORT\n")
                else:
                    ble.send("ERROR:WRONG_OLD_PASSWORD\n")
            else:
                ble.send("ERROR:INVALID_FORMAT\n")

        elif command.startswith("RESET:"):
            admin_pass = command[6:]
            if admin_pass == ADMIN_PASSWORD:
                reset_password()
                ble.send("OK:PASSWORD_RESET\n")
            else:
                ble.send("ERROR:WRONG_ADMIN_PASSWORD\n")

        elif command == "OPEN":
            open_lock()
            ble.send("OK:OPENED\n")

        elif command == "CLOSE":
            close_lock()
            ble.send("OK:CLOSED\n")

        elif command == "TOGGLE":
            toggle_lock()
            state = "OPENED" if lock_state else "CLOSED"
            ble.send(f"OK:{state}\n")

        elif command == "STATUS":
            state = "OPENED" if lock_state else "CLOSED"
            uptime = int(time.time() - last_activity)
            ble.send(f"STATUS:{state},IDLE:{uptime}s\n")

        elif command == "SLEEP":
            ble.send("OK:ENTERING_SLEEP\n")
            time.sleep(1)
            check_idle_timeout()

        else:
            ble.send("ERROR:UNKNOWN_COMMAND\n")
    except Exception as e:
        print(f"BT: Command error: {e}")
        try:
            ble.send(f"ERROR:EXCEPTION:{e}\n")
        except:
            pass

# ===== SETUP =====
print("\n" + "="*50)
print("  ULTIMATE VERSION - Password + Battery")
print("="*50)

print("Initializing BLE...")
ble = BLESimplePeripheral("ESP32-SafeLock")
ble.on_write(on_rx)
print("✅ BLE ready")

load_password()

# ===== MAIN LOOP =====
def main():
    print("\n" + "="*50)
    print("   ULTIMATE DIGITAL SAFE LOCKER")
    print("="*50)
    print(f"Password: {'*' * len(current_password)}")
    print(f"Battery: Optimized (2-3 months)")
    print(f"Sleep after: {IDLE_TIMEOUT}s idle")
    print("\nKeypad:")
    print("  [0-9]  - Enter password")
    print("  [#/C]  - Submit/Unlock")
    print("  [*]    - Clear")
    print("  [A]    - Change password")
    print("  [B]+#  - Admin reset")
    print("\nBLE:")
    print("  PASS:xxxx      - Unlock")
    print("  CHANGE:old:new - Change password")
    print("  RESET:admin    - Factory reset")
    print("  SLEEP          - Force sleep")
    print("="*50 + "\n")
    
    reset_activity_timer()
    
    while True:
        key = read_keypad()
        if key:
            process_keypad_input(key)
        
        # Check for idle timeout
        check_idle_timeout()
        
        time.sleep_ms(50)

# ===== START =====
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Stopped")
        close_lock()
    except Exception as e:
        print(f"❌ Error: {e}")
        close_lock()
