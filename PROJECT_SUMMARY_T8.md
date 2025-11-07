# Digital Safe Locker - LILYGO T8 V1.7 Complete Package

## 🎯 Project Overview - T8 Version

**ESP32-WROVER based digital safe locker with advanced features:**
- ✅ 4x3 matrix keypad for password entry
- ✅ Bluetooth Low Energy (BLE) control via Android
- ✅ 6V relay controlling door lock
- ✅ Battery powered (4x AA, 2-3 months runtime)
- ✅ Hardware reset button in battery compartment
- ✅ **8MB PSRAM** for advanced features
- ✅ **TF Card slot** for unlimited logging
- ✅ **3D Antenna** for 30-50m BLE range
- ✅ **Onboard LED** for status indication

---

## 📦 Complete File Package - LILYGO T8 V1.7

### 🆕 T8-Specific Files

**Hardware Guides:**
1. **[LILYGO_T8_WIRING_GUIDE.md](computer:///mnt/user-data/outputs/LILYGO_T8_WIRING_GUIDE.md)** - Complete T8 wiring instructions
2. **[circuit_diagram_T8.html](computer:///mnt/user-data/outputs/circuit_diagram_T8.html)** - Interactive T8 circuit diagram
3. **[LILYGO_T8_COMPARISON.md](computer:///mnt/user-data/outputs/LILYGO_T8_COMPARISON.md)** - T8 vs Pico comparison

**Software/Code:**
4. **[digital_safe_locker_T8.py](computer:///mnt/user-data/outputs/digital_safe_locker_T8.py)** - Main program for T8
5. **[digital_safe_locker_T8_battery_optimized.py](computer:///mnt/user-data/outputs/digital_safe_locker_T8_battery_optimized.py)** - Battery optimized version

### 📚 Universal Files (Work for Both Boards)

**BLE Libraries:**
6. **[ble_simple_peripheral.py](computer:///mnt/user-data/outputs/ble_simple_peripheral.py)** - BLE support
7. **[ble_advertising.py](computer:///mnt/user-data/outputs/ble_advertising.py)** - BLE advertising

**Documentation:**
8. **[BATTERY_POWER_GUIDE.md](computer:///mnt/user-data/outputs/BATTERY_POWER_GUIDE.md)** - Power analysis
9. **[ANDROID_BLE_APPS_GUIDE.md](computer:///mnt/user-data/outputs/ANDROID_BLE_APPS_GUIDE.md)** - Android app options
10. **[MIT_APP_INVENTOR_TUTORIAL.md](computer:///mnt/user-data/outputs/MIT_APP_INVENTOR_TUTORIAL.md)** - DIY app tutorial
11. **[RESET_BUTTON_GUIDE.md](computer:///mnt/user-data/outputs/RESET_BUTTON_GUIDE.md)** - Reset button installation

---

## 🔌 LILYGO T8 V1.7 Wiring Summary

### 4x3 Keypad (Updated Pins!)
```
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ A │  ← Row 1 → GPIO 22 ⭐
├───┼───┼───┼───┤
│ 4 │ 5 │ 6 │ B │  ← Row 2 → GPIO 21 ⭐
├───┼───┼───┼───┤
│ 7 │ 8 │ 9 │ C │  ← Row 3 → GPIO 15 ⭐
└───┴───┴───┴───┘
  ↓   ↓   ↓   ↓
 C1  C2  C3  C4
GPIO GPIO GPIO GPIO
 13⭐ 12⭐ 14⭐ 27⭐
```

### Complete Pin Table
| Component | Function | T8 GPIO | Notes |
|-----------|----------|---------|-------|
| Keypad | Row 1 | GPIO 22 | Changed from 13 |
| Keypad | Row 2 | GPIO 21 | Changed from 12 |
| Keypad | Row 3 | GPIO 15 | Changed from 14 |
| Keypad | Col 1 | GPIO 13 | Changed from 27 |
| Keypad | Col 2 | GPIO 12 | Safe to use |
| Keypad | Col 3 | GPIO 14 | Safe to use |
| Keypad | Col 4 | GPIO 27 | Changed from 33 |
| Relay | Control | GPIO 32 | ✓ Same as Pico |
| LED | Status | GPIO 2 | Built-in LED |
| Reset | Button | EN + GND | ✓ Same as Pico |

---

## 🌟 Why LILYGO T8 V1.7?

### Superior Specifications
```
ESP32 Pico DevKit          LILYGO T8 V1.7
────────────────────────────────────────────────
520KB RAM              →   520KB + 8MB PSRAM ⭐
4MB Flash              →   16MB Flash ⭐
PCB Antenna            →   3D Ceramic Antenna ⭐
10-30m BLE Range       →   30-50m BLE Range ⭐
No SD Card             →   TF Card Slot ⭐
No LED                 →   Onboard LED ⭐
$8-12                  →   $15-20 (+$7-8)
```

### Key Advantages
1. **Better BLE:** 3D antenna provides 2-3x better range and stability
2. **More Memory:** 8MB PSRAM for access logs, multiple users, advanced features
3. **Data Logging:** TF card slot for unlimited access history
4. **Status Feedback:** Onboard LED (GPIO 2) for visual indication
5. **Future-Proof:** Room to grow with more features
6. **Industrial Grade:** WROVER module, more reliable

**Cost:** Only $7-8 more than Pico  
**Value:** Significantly better hardware for small premium

---

## 🔋 Battery Life (Same as Pico!)

| Configuration | Battery Life | Use Case |
|--------------|--------------|----------|
| **BLE + Deep Sleep** | **2-3 months** ⭐ | Recommended |
| BLE Always On | 2-3 weeks | Testing |
| WiFi Always On | <1 day | ❌ Not viable |

**T8 actually has slightly better deep sleep:** 0.01mA vs 0.15mA

---

## 📱 Android App Options (Same!)

All Android app options work identically with T8:

### Ready to Use:
1. **nRF Connect** - Professional BLE terminal (recommended)
2. **Serial Bluetooth Terminal** - Simple command sending

### DIY Custom App:
3. **MIT App Inventor** - Build your own (no coding!)

**Only difference:** Device name changes from "ESP32-SafeLock" to "T8-SafeLock"

---

## 🚀 Quick Start Guide (T8 Specific)

### Step 1: Firmware (CRITICAL!)
```bash
# Download SPIRAM firmware (NOT regular ESP32)
https://micropython.org/download/esp32/
File: esp32spiram-*.bin

# Flash it
esptool.py --chip esp32 --port /dev/ttyUSB0 \
  write_flash -z 0x1000 esp32spiram-*.bin
```

**⚠️ MUST use SPIRAM firmware for WROVER!**

### Step 2: Upload Code
```bash
# Upload 3 files
ampy --port /dev/ttyUSB0 put ble_advertising.py
ampy --port /dev/ttyUSB0 put ble_simple_peripheral.py
ampy --port /dev/ttyUSB0 put digital_safe_locker_T8.py main.py
```

### Step 3: Wire Components
1. **Keypad (7 wires):** Follow T8 pinout (different from Pico!)
2. **Relay (3 wires):** Same as Pico (GPIO 32)
3. **Reset (2 wires):** Same as Pico (EN + GND)
4. **Power:** 4x AA to VIN + GND or USB

### Step 4: Test
1. Power on → LED blinks 3x
2. Press keypad → See response
3. Connect BLE → "T8-SafeLock"
4. Enter password → Lock operates
5. Done! ✅

**Total Time:** 30-60 minutes

---

## 🎯 Pin Restrictions (IMPORTANT!)

### ⛔ NEVER Use:
- **GPIO 6-11:** Internal flash (will brick board!)
- **GPIO 16-17:** PSRAM (if using 8MB)
- **GPIO 0:** Boot button
- **GPIO 1, 3:** Serial UART

### ⚠️ Avoid if Using SD Card:
- GPIO 4, 5, 18, 19, 23

### ✅ Safe to Use (Used in Project):
- GPIO 12, 13, 14, 15, 21, 22, 27, 32, 33

---

## 💡 Advanced Features (With T8)

### Access Logging
```python
# Use PSRAM for large logs
access_log = []
def log_access(user, action):
    access_log.append({
        'time': time.time(),
        'user': user,
        'action': action
    })
```

### SD Card Logging
```python
# Log to TF card
from machine import SDCard
sd = SDCard(slot=2)
os.mount(sd, '/sd')

with open('/sd/access.log', 'a') as f:
    f.write(f"{time.time()}: Unlocked\n")
```

### Multiple Users
```python
# Store in PSRAM
users = {
    'user1': '1234',
    'user2': '5678',
    'user3': '9012'
}
```

### Status LED
```python
# Already in code!
led = Pin(2, Pin.OUT)
led.value(1)  # Lock opened
led.value(0)  # Lock closed
```

---

## 🛠️ Hardware Components (Updated)

| Component | Spec | Qty | Cost |
|-----------|------|-----|------|
| **LILYGO T8 V1.7** | ESP32-WROVER, 8MB PSRAM | 1 | $15-20 |
| Relay Module | 6V, 1-channel | 1 | $3-5 |
| Matrix Keypad | 4x3 (3 rows, 4 cols) | 1 | $3-6 |
| Door Lock | 12V Solenoid/EM | 1 | $8-15 |
| Battery Holder | 4x AA | 1 | $2-3 |
| AA Batteries | Alkaline or NiMH | 4 | $4-8 |
| Reset Button | Tactile momentary | 1 | $0.50-1 |
| Jumper Wires | Male-to-Female | ~20 | $2-5 |
| **TOTAL** | | | **$38-63** |

**Compared to Pico:** +$7-8 for significantly better hardware

---

## 📊 Specifications

| Feature | Specification |
|---------|--------------|
| **Board** | LILYGO T8 V1.7 ESP32-WROVER |
| **MCU** | Dual-core 240MHz |
| **RAM** | 520KB SRAM + 8MB PSRAM |
| **Flash** | 16MB |
| **Connectivity** | WiFi + BLE 4.2 |
| **Antenna** | 3D Ceramic |
| **BLE Range** | 30-50 meters |
| **Power** | 6V (4x AA) or 5V USB |
| **Current Draw** | 100-120mA (BLE), 0.01mA (sleep) |
| **Battery Life** | 2-3 months (BLE + sleep) |
| **Keypad** | 4x3 matrix (12 keys) |
| **Lock Type** | 12V solenoid or EM lock |
| **Storage** | TF/MicroSD card slot |
| **LED** | Onboard (GPIO 2) |

---

## 🔄 Migration from Pico to T8

### If You Built with Pico:

**Changes Needed:**
1. ✅ **Rewire keypad** (pins changed!)
2. ✅ **Flash SPIRAM firmware** (not regular)
3. ✅ **Upload T8 code** (new file)
4. ✅ **Update app** (device name to "T8-SafeLock")

**Stays Same:**
- ✅ Relay wiring (GPIO 32)
- ✅ Reset button (EN + GND)
- ✅ Power options
- ✅ Lock mechanism
- ✅ BLE libraries
- ✅ Android apps

**Time:** 30 minutes to swap

---

## 🎓 Learning Outcomes

After this project with T8, you'll understand:
- ✅ ESP32-WROVER vs regular ESP32
- ✅ PSRAM usage and benefits
- ✅ Advanced BLE with better hardware
- ✅ Pin restrictions and multiplexing
- ✅ Power optimization techniques
- ✅ Data logging (RAM vs SD card)
- ✅ Industrial-grade embedded design

---

## 🐛 T8-Specific Troubleshooting

### Upload Fails
- **Hold BOOT button** during upload
- Use SPIRAM firmware (critical!)
- Check USB cable (data, not charge-only)

### Memory Errors
- Using regular ESP32 firmware? → Use SPIRAM!
- PSRAM not working? → Check firmware

### Pins Not Working
- Avoid GPIO 6-11 (flash)
- Don't use GPIO 16-17 (PSRAM)
- Check pinout carefully

### BLE Issues
- Turn off WiFi (they conflict)
- 3D antenna should give better range
- Check "T8-SafeLock" name

---

## ✅ Complete Checklist

**Hardware:**
- [ ] LILYGO T8 V1.7 purchased
- [ ] SPIRAM firmware flashed ⚠️
- [ ] All 7 keypad wires correct
- [ ] Relay wired (GPIO 32)
- [ ] Reset button installed
- [ ] Power connected
- [ ] LED blinking on boot

**Software:**
- [ ] T8 code uploaded (not Pico code!)
- [ ] Password changed from "1234"
- [ ] BLE connects as "T8-SafeLock"
- [ ] All commands work
- [ ] LED shows status

**Testing:**
- [ ] 10+ unlock cycles successful
- [ ] BLE range acceptable (30-50m)
- [ ] Battery life ~2-3 months
- [ ] Reset button works
- [ ] Emergency access maintained

---

## 📚 Documentation Quick Links

**Start Here:**
1. Read: [LILYGO_T8_COMPARISON.md](computer:///mnt/user-data/outputs/LILYGO_T8_COMPARISON.md)
2. Follow: [LILYGO_T8_WIRING_GUIDE.md](computer:///mnt/user-data/outputs/LILYGO_T8_WIRING_GUIDE.md)
3. View: [circuit_diagram_T8.html](computer:///mnt/user-data/outputs/circuit_diagram_T8.html)

**Then:**
4. Install: [ANDROID_BLE_APPS_GUIDE.md](computer:///mnt/user-data/outputs/ANDROID_BLE_APPS_GUIDE.md)
5. Optimize: [BATTERY_POWER_GUIDE.md](computer:///mnt/user-data/outputs/BATTERY_POWER_GUIDE.md)

---

## 🎉 Why T8 is Worth It

**For just $7-8 more than Pico, you get:**
- 2-3x better BLE reliability
- 4x more memory for features
- SD card for unlimited logging
- Better range (50m vs 30m)
- Industrial-grade stability
- Room for future expansion
- Built-in status LED

**Bottom line:** Unless budget is critical, T8 is the better choice!

---

## 🚀 Next Steps

1. **Order LILYGO T8 V1.7** ($15-20 online)
2. **Download SPIRAM firmware** (micropython.org)
3. **Read T8 wiring guide** completely
4. **Flash and upload code** (T8 versions!)
5. **Wire according to T8 pinout** (different!)
6. **Test thoroughly** before final install
7. **Enjoy your advanced smart lock!** 🔒

---

**Project Version:** LILYGO T8 V1.7 Edition  
**Total Files:** 11 comprehensive guides  
**Estimated Build Time:** 4-8 hours  
**Skill Level:** Intermediate+  
**Total Cost:** $38-63  

**LILYGO T8 V1.7:** Better hardware, better reliability, better future! ⭐

*All documentation, code, and guides included in this package.*
