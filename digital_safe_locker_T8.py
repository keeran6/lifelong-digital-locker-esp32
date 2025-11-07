"""
Digital Safe Locker - LILYGO T8 V1.7 ESP32-WROVER
Features:
- 3x4 or 4x3 Keypad for manual password entry
- Bluetooth control from Android app
- 6V Relay for door lock control
- 8MB PSRAM, TF Card support, 3D Antenna

Board: LILYGO T8 V1.7 ESP32-WROVER 8MB PSRAM
"""

from machine import Pin
import time
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# ===== CONFIGURATION =====
CORRECT_PASSWORD = "1234"  # Change this to your desired password
LOCK_OPEN_TIME = 5  # Seconds to keep lock open
MAX_ATTEMPTS = 3  # Maximum wrong password attempts

# ===== LILYGO T8 V1.7 PIN DEFINITIONS =====
# Relay control pin
RELAY_PIN = 32

# 4x3 Keypad pins (3 rows, 4 columns)
# Using safe GPIO pins that don't conflict with SD card or PSRAM
ROW_PINS = [22, 21, 15]      # Row 1, 2, 3
COL_PINS = [13, 12, 14, 27]  # Col 1, 2, 3, 4

# Keypad matrix layout (3 rows x 4 columns)
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C']
]

# ===== IMPORTANT: LILYGO T8 V1.7 PIN RESTRICTIONS =====
# DO NOT USE these pins (reserved for board functions):
# GPIO 0  - Boot/Flash button
# GPIO 2  - Onboard LED
# GPIO 4  - SD Card CS (if using SD card)
# GPIO 5  - SD Card
# GPIO 6-11 - Internal Flash (NEVER USE)
# GPIO 16-17 - PSRAM (if using PSRAM)
# GPIO 18 - SD Card SCK
# GPIO 19 - SD Card MISO
# GPIO 23 - SD Card MOSI

# SAFE TO USE (used in this project):
# GPIO 12, 13, 14, 15, 21, 22, 27, 32, 33

# ===== RESET BUTTON =====
# Hardware reset button wiring:
# - Connect one side of tactile button to EN pin
# - Connect other side to GND
# - Press button to reset ESP32
# - Accessible from battery compartment

# ===== HARDWARE SETUP =====
# Initialize relay (active HIGH)
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)  # Start with lock closed

# Initialize keypad rows as outputs (HIGH by default)
rows = [Pin(pin, Pin.OUT) for pin in ROW_PINS]
for row in rows:
    row.value(1)

# Initialize keypad columns as inputs with pull-up
cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in COL_PINS]

# Onboard LED (optional - for status indication)
led = Pin(2, Pin.OUT)

# ===== GLOBAL VARIABLES =====
entered_password = ""
failed_attempts = 0
lock_state = False  # False = locked, True = unlocked

# ===== DOOR LOCK FUNCTIONS =====
def open_lock():
    """Open the door lock"""
    global lock_state
    print("🔓 Lock OPENED")
    relay.value(1)  # Activate relay
    led.value(1)    # Turn on LED
    lock_state = True

def close_lock():
    """Close the door lock"""
    global lock_state
    print("🔒 Lock CLOSED")
    relay.value(0)  # Deactivate relay
    led.value(0)    # Turn off LED
    lock_state = False

def toggle_lock():
    """Toggle lock state"""
    if lock_state:
        close_lock()
    else:
        open_lock()

# ===== KEYPAD FUNCTIONS =====
def read_keypad():
    """
    Scan the keypad matrix and return pressed key
    Returns None if no key is pressed
    """
    for row_num, row_pin in enumerate(rows):
        # Set current row LOW
        row_pin.value(0)
        
        # Check each column
        for col_num, col_pin in enumerate(cols):
            if col_pin.value() == 0:  # Key pressed (column pulled LOW)
                # Debounce
                time.sleep_ms(20)
                if col_pin.value() == 0:
                    # Wait for key release
                    while col_pin.value() == 0:
                        time.sleep_ms(10)
                    
                    # Set row back to HIGH
                    row_pin.value(1)
                    
                    return KEYS[row_num][col_num]
        
        # Set row back to HIGH
        row_pin.value(1)
    
    return None

def process_keypad_input(key):
    """Process keypad button press"""
    global entered_password, failed_attempts
    
    print(f"Key pressed: {key}")
    
    if key == '#' or key == 'C':  # Enter/Submit
        if entered_password == CORRECT_PASSWORD:
            print("✅ Correct password!")
            open_lock()
            time.sleep(LOCK_OPEN_TIME)
            close_lock()
            failed_attempts = 0
        else:
            failed_attempts += 1
            print(f"❌ Wrong password! Attempt {failed_attempts}/{MAX_ATTEMPTS}")
            
            if failed_attempts >= MAX_ATTEMPTS:
                print("🚨 TOO MANY FAILED ATTEMPTS! Locking for 30 seconds...")
                # Blink LED during lockout
                for _ in range(30):
                    led.value(1)
                    time.sleep(0.5)
                    led.value(0)
                    time.sleep(0.5)
                failed_attempts = 0
        
        entered_password = ""  # Clear entered password
        
    elif key == '*' or key == 'A':  # Clear
        entered_password = ""
        print("🔄 Password cleared")
        
    elif key == 'B':  # Quick unlock (for testing/emergency)
        print("⚡ Emergency unlock!")
        open_lock()
        time.sleep(LOCK_OPEN_TIME)
        close_lock()
        
    else:  # Number key
        if len(entered_password) < 8:  # Limit password length
            entered_password += key
            print(f"Password: {'*' * len(entered_password)}")

# ===== BLUETOOTH FUNCTIONS =====
def on_rx(data):
    """Handle received Bluetooth data"""
    global failed_attempts
    
    command = data.decode().strip().upper()
    print(f"BT Command received: {command}")
    
    if command.startswith("PASS:"):
        # Password received from app
        password = command[5:]
        if password == CORRECT_PASSWORD:
            print("✅ Correct BT password!")
            open_lock()
            time.sleep(LOCK_OPEN_TIME)
            close_lock()
            ble.send("OK:UNLOCKED\n")
            failed_attempts = 0
        else:
            failed_attempts += 1
            print(f"❌ Wrong BT password! Attempt {failed_attempts}/{MAX_ATTEMPTS}")
            ble.send(f"ERROR:WRONG_PASSWORD:{failed_attempts}/{MAX_ATTEMPTS}\n")
    
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
        # Send board information
        info = "BOARD:LILYGO_T8_V1.7_ESP32-WROVER_8MB_PSRAM\n"
        ble.send(info)
    
    else:
        ble.send("ERROR:UNKNOWN_COMMAND\n")

# ===== BLUETOOTH SETUP =====
print("\n" + "="*50)
print("  LILYGO T8 V1.7 - Digital Safe Locker")
print("="*50)
print("Board: ESP32-WROVER with 8MB PSRAM")
print("Initializing Bluetooth...")

ble = BLESimplePeripheral("T8-SafeLock")
ble.on_write(on_rx)
print("✅ Bluetooth ready! Device name: T8-SafeLock")

# ===== MAIN LOOP =====
def main():
    """Main program loop"""
    print("\n" + "="*50)
    print("   DIGITAL SAFE LOCKER - READY")
    print("="*50)
    print(f"Set Password: {CORRECT_PASSWORD}")
    print("Keypad: Enter password, press # or C to submit")
    print("Keypad: Press * or A to clear")
    print("Keypad: Press B for emergency unlock")
    print("Bluetooth: Send 'PASS:xxxx' or 'OPEN'/'CLOSE'")
    print("="*50 + "\n")
    
    # Startup LED flash
    for _ in range(3):
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.1)
    
    while True:
        # Check for keypad input
        key = read_keypad()
        if key:
            process_keypad_input(key)
        
        # Small delay to prevent excessive CPU usage
        time.sleep_ms(50)

# ===== START PROGRAM =====
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Program stopped by user")
        close_lock()
        led.value(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        close_lock()
        led.value(0)
