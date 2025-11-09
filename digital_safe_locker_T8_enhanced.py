"""
Digital Safe Locker - LILYGO T8 V1.7 ENHANCED VERSION
Features:
- Change password via keypad
- Change password via BLE
- Persistent password storage  
- Admin password protection
- Password reset mechanism
- LED status indication
"""

from machine import Pin
import time
import bluetooth
import json
from ble_simple_peripheral import BLESimplePeripheral

# ===== CONFIGURATION =====
DEFAULT_PASSWORD = "1234"  # Factory default
ADMIN_PASSWORD = "9999"    # Admin password (change this!)
LOCK_OPEN_TIME = 5
MAX_ATTEMPTS = 3

# Password storage file
PASSWORD_FILE = "password.json"

# ===== LILYGO T8 PIN DEFINITIONS =====
RELAY_PIN = 32

# 4x3 Keypad pins (3 rows, 4 columns)
ROW_PINS = [22, 21, 15]
COL_PINS = [13, 12, 14, 27]

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

led = Pin(2, Pin.OUT)

# ===== GLOBAL VARIABLES =====
entered_password = ""
failed_attempts = 0
lock_state = False
current_password = DEFAULT_PASSWORD

# Password change mode
change_password_mode = False
new_password_entry = ""
confirm_password_entry = ""
password_change_step = 0  # 0=old, 1=new, 2=confirm

# ===== PASSWORD MANAGEMENT =====
def load_password():
    """Load password from file"""
    global current_password
    try:
        with open(PASSWORD_FILE, 'r') as f:
            data = json.load(f)
            current_password = data.get('password', DEFAULT_PASSWORD)
            print(f"✅ Password loaded from storage")
            # Flash LED to confirm
            led.value(1)
            time.sleep(0.5)
            led.value(0)
    except:
        print("⚠️ No saved password, using default")
        current_password = DEFAULT_PASSWORD
        save_password(current_password)

def save_password(password):
    """Save password to file"""
    try:
        with open(PASSWORD_FILE, 'w') as f:
            json.dump({'password': password}, f)
        print("✅ Password saved to storage")
        return True
    except Exception as e:
        print(f"❌ Failed to save password: {e}")
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
    led.value(1)
    lock_state = True

def close_lock():
    global lock_state
    print("🔒 Lock CLOSED")
    relay.value(0)
    led.value(0)
    lock_state = False

def toggle_lock():
    if lock_state:
        close_lock()
    else:
        open_lock()

# ===== LED FEEDBACK =====
def led_blink(times, delay_ms=200):
    """Blink LED for feedback"""
    for _ in range(times):
        led.value(1)
        time.sleep_ms(delay_ms)
        led.value(0)
        time.sleep_ms(delay_ms)

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
                    # Brief LED flash on key press
                    led.value(1)
                    time.sleep_ms(50)
                    led.value(0)
                    return KEYS[row_num][col_num]
        row_pin.value(1)
    return None

def process_keypad_input(key):
    """Process keypad button press"""
    global entered_password, failed_attempts
    global change_password_mode, new_password_entry, confirm_password_entry, password_change_step
    
    print(f"Key pressed: {key}")
    
    # ===== PASSWORD CHANGE MODE =====
    if change_password_mode:
        if key == '#' or key == 'C':  # Submit
            if password_change_step == 0:  # Old password entered
                if entered_password == current_password:
                    print("✅ Old password correct. Enter NEW password:")
                    led_blink(2)  # Success indication
                    password_change_step = 1
                    entered_password = ""
                else:
                    print("❌ Wrong old password!")
                    led_blink(5, 100)  # Error indication
                    change_password_mode = False
                    password_change_step = 0
                    entered_password = ""
            
            elif password_change_step == 1:  # New password entered
                if len(entered_password) >= 4:
                    new_password_entry = entered_password
                    print("✅ New password set. CONFIRM new password:")
                    led_blink(2)
                    password_change_step = 2
                    entered_password = ""
                else:
                    print("❌ Password too short (min 4 digits)")
                    led_blink(5, 100)
                    entered_password = ""
            
            elif password_change_step == 2:  # Confirm password
                if entered_password == new_password_entry:
                    current_password = new_password_entry
                    save_password(current_password)
                    print("🎉 Password changed successfully!")
                    led_blink(3, 300)  # Success pattern
                    change_password_mode = False
                    password_change_step = 0
                    entered_password = ""
                    new_password_entry = ""
                    confirm_password_entry = ""
                else:
                    print("❌ Passwords don't match! Try again.")
                    led_blink(5, 100)
                    password_change_step = 1
                    entered_password = ""
                    new_password_entry = ""
        
        elif key == '*' or key == 'A':  # Cancel
            print("🔄 Password change cancelled")
            led_blink(1, 500)
            change_password_mode = False
            password_change_step = 0
            entered_password = ""
            new_password_entry = ""
        
        else:  # Number key
            if len(entered_password) < 8:
                entered_password += key
                print(f"Password: {'*' * len(entered_password)}")
    
    # ===== NORMAL UNLOCK MODE =====
    else:
        if key == '#' or key == 'C':  # Submit/Unlock
            if entered_password == current_password:
                print("✅ Correct password!")
                open_lock()
                time.sleep(LOCK_OPEN_TIME)
                close_lock()
                failed_attempts = 0
            else:
                failed_attempts += 1
                print(f"❌ Wrong password! Attempt {failed_attempts}/{MAX_ATTEMPTS}")
                led_blink(failed_attempts, 150)
                
                if failed_attempts >= MAX_ATTEMPTS:
                    print("🚨 TOO MANY FAILED ATTEMPTS! Locking for 30 seconds...")
                    for _ in range(30):
                        led.value(1)
                        time.sleep(0.5)
                        led.value(0)
                        time.sleep(0.5)
                    failed_attempts = 0
            
            entered_password = ""
        
        elif key == '*':  # Clear
            entered_password = ""
            print("🔄 Password cleared")
        
        elif key == 'A':  # Enter password change mode
            print("🔑 Password change mode activated")
            print("Enter OLD password:")
            led_blink(2, 500)
            change_password_mode = True
            password_change_step = 0
            entered_password = ""
        
        elif key == 'B':  # Admin reset (requires admin password)
            if entered_password == ADMIN_PASSWORD:
                print("⚡ Admin reset activated!")
                reset_password()
                entered_password = ""
                led_blink(5, 100)
            else:
                print("❌ Admin password required for reset")
                entered_password = ""
        
        else:  # Number key
            if len(entered_password) < 8:
                entered_password += key
                print(f"Password: {'*' * len(entered_password)}")

# ===== BLUETOOTH FUNCTIONS =====
def on_rx(data):
    """Handle received Bluetooth data"""
    global failed_attempts, current_password
    
    command = data.decode().strip()
    print(f"BT Command: {command}")
    
    # Parse command
    if command.startswith("PASS:"):
        # Unlock with password
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
        # Change password: CHANGE:oldpass:newpass
        parts = command.split(":")
        if len(parts) == 3:
            old_pass = parts[1]
            new_pass = parts[2]
            
            if old_pass == current_password:
                if len(new_pass) >= 4:
                    current_password = new_pass
                    save_password(current_password)
                    print("🎉 Password changed via BLE!")
                    led_blink(3, 300)
                    ble.send("OK:PASSWORD_CHANGED\n")
                else:
                    ble.send("ERROR:PASSWORD_TOO_SHORT\n")
            else:
                ble.send("ERROR:WRONG_OLD_PASSWORD\n")
        else:
            ble.send("ERROR:INVALID_FORMAT\n")
    
    elif command.startswith("RESET:"):
        # Reset password: RESET:adminpass
        admin_pass = command[6:]
        if admin_pass == ADMIN_PASSWORD:
            reset_password()
            led_blink(5, 100)
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
        ble.send(f"STATUS:{state}\n")
    
    elif command == "INFO":
        info = f"BOARD:LILYGO_T8_V1.7,PASS_LEN:{len(current_password)}\n"
        ble.send(info)
    
    else:
        ble.send("ERROR:UNKNOWN_COMMAND\n")

# ===== BLUETOOTH SETUP =====
print("\n" + "="*50)
print("  LILYGO T8 V1.7 - ENHANCED SAFE LOCKER")
print("="*50)
print("Initializing Bluetooth...")
ble = BLESimplePeripheral("T8-SafeLock")
ble.on_write(on_rx)
print("✅ Bluetooth ready!")

# Load saved password
load_password()

# ===== MAIN LOOP =====
def main():
    print("\n" + "="*50)
    print("   ENHANCED DIGITAL SAFE LOCKER")
    print("="*50)
    print(f"Current Password: {'*' * len(current_password)}")
    print(f"Admin Password: {'*' * len(ADMIN_PASSWORD)}")
    print("\nKeypad Commands:")
    print("  [0-9] - Enter password")
    print("  [#/C] - Submit password / Unlock")
    print("  [*]   - Clear entry")
    print("  [A]   - Change password mode")
    print("  [B]+# - Admin reset (enter admin pass first)")
    print("\nBLE Commands:")
    print("  PASS:xxxx      - Unlock")
    print("  CHANGE:old:new - Change password")
    print("  RESET:admin    - Reset to default")
    print("  STATUS         - Get lock status")
    print("  INFO           - Board information")
    print("="*50 + "\n")
    
    # Startup LED pattern
    led_blink(3, 100)
    
    while True:
        key = read_keypad()
        if key:
            process_keypad_input(key)
        
        time.sleep_ms(50)

# ===== START PROGRAM =====
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Program stopped")
        close_lock()
        led.value(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        close_lock()
        led.value(0)
