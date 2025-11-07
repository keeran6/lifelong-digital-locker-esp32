"""
Digital Safe Locker - LILYGO T8 V1.7 - BATTERY OPTIMIZED
ESP32-WROVER with deep sleep for extended battery life

Features:
- Deep sleep after inactivity
- Wake on keypad press
- BLE only (no WiFi) for power saving
- Optimized for 2-3 months on 4x AA batteries
"""

from machine import Pin, deepsleep, reset
import time
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import esp32

# ===== CONFIGURATION =====
CORRECT_PASSWORD = "1234"
LOCK_OPEN_TIME = 5
MAX_ATTEMPTS = 3

# Power saving settings
IDLE_TIMEOUT = 30  # Seconds before deep sleep
DEEP_SLEEP_DURATION = 1000 * 60 * 5  # 5 minutes in milliseconds

# ===== LILYGO T8 V1.7 PIN DEFINITIONS =====
RELAY_PIN = 32

# Keypad pins (3 rows, 4 columns)
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
last_activity = time.time()

# ===== POWER MANAGEMENT =====
def check_idle_timeout():
    """Check if system should enter deep sleep"""
    global last_activity
    if time.time() - last_activity > IDLE_TIMEOUT:
        print("💤 Entering deep sleep to save battery...")
        close_lock()
        led.value(0)
        time.sleep(1)
        
        # Configure wake on keypad press (any column pin)
        # Wake when any column goes LOW (key pressed)
        esp32.wake_on_ext0(pin=Pin(13), level=esp32.WAKEUP_ANY_HIGH)
        
        deepsleep(DEEP_SLEEP_DURATION)

def reset_activity_timer():
    """Reset the inactivity timer"""
    global last_activity
    last_activity = time.time()

def check_wakeup_reason():
    """Check why ESP32 woke up"""
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("🔄 Woke from deep sleep")
        # Quick LED flash to indicate wake
        led.value(1)
        time.sleep(0.2)
        led.value(0)

# ===== DOOR LOCK FUNCTIONS =====
def open_lock():
    global lock_state
    print("🔓 Lock OPENED")
    relay.value(1)
    led.value(1)
    lock_state = True
    reset_activity_timer()

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
                    reset_activity_timer()
                    return KEYS[row_num][col_num]
        row_pin.value(1)
    return None

def process_keypad_input(key):
    global entered_password, failed_attempts
    
    print(f"Key pressed: {key}")
    
    if key == '#' or key == 'C':
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
                time.sleep(30)
                failed_attempts = 0
        entered_password = ""
        
    elif key == '*' or key == 'A':
        entered_password = ""
        print("🔄 Password cleared")
        
    elif key == 'B':
        print("⚡ Emergency unlock!")
        open_lock()
        time.sleep(LOCK_OPEN_TIME)
        close_lock()
        
    else:
        if len(entered_password) < 8:
            entered_password += key
            print(f"Password: {'*' * len(entered_password)}")

# ===== BLUETOOTH FUNCTIONS =====
def on_rx(data):
    global failed_attempts
    reset_activity_timer()
    
    command = data.decode().strip().upper()
    print(f"BT Command: {command}")
    
    if command.startswith("PASS:"):
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
        uptime = time.time()
        ble.send(f"STATUS:{state},UPTIME:{uptime}s\n")
    
    elif command == "SLEEP":
        ble.send("OK:ENTERING_SLEEP\n")
        time.sleep(1)
        check_idle_timeout()
    
    else:
        ble.send("ERROR:UNKNOWN_COMMAND\n")

# ===== BLUETOOTH SETUP =====
print("\n" + "="*50)
print("  LILYGO T8 V1.7 - BATTERY OPTIMIZED")
print("="*50)
print("Initializing Bluetooth (BLE only)...")

ble = BLESimplePeripheral("T8-SafeLock")
ble.on_write(on_rx)
print("✅ Bluetooth ready!")

# Check wakeup reason
check_wakeup_reason()

# ===== MAIN LOOP =====
def main():
    print("\n" + "="*50)
    print("  BATTERY OPTIMIZED SAFE LOCKER")
    print("="*50)
    print("🔋 Power saving mode enabled")
    print(f"💤 Sleep after {IDLE_TIMEOUT}s idle")
    print("="*50 + "\n")
    
    reset_activity_timer()
    
    # Startup LED pattern
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
        
        # Check for idle timeout
        check_idle_timeout()
        
        # Small delay
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
