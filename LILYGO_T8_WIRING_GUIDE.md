# LILYGO T8 V1.7 ESP32-WROVER - Complete Wiring Guide

## 🎯 Board Overview

**LILYGO T8 V1.7 ESP32-WROVER Specifications:**
- **MCU:** ESP32-WROVER (dual-core, 240MHz)
- **RAM:** 520KB SRAM + 8MB PSRAM
- **Flash:** 16MB
- **Features:** WiFi, Bluetooth 4.2 BLE
- **TF Card:** MicroSD card slot
- **Antenna:** 3D antenna for better signal
- **Size:** Compact form factor
- **USB:** Micro-USB for programming and power
- **Voltage:** 3.3V logic, 5V input via USB

### Key Advantages Over ESP32 Pico:
✅ **More Memory:** 8MB PSRAM for complex applications  
✅ **Better Antenna:** 3D antenna for improved range  
✅ **SD Card Support:** Log access history, store data  
✅ **More Stable:** WROVER module more reliable  
✅ **Better BLE Range:** ~30-50 meters vs 10-30 meters  

---

## 🔌 Complete Pin Assignments

### Safe GPIO Pins for This Project

```
FUNCTION              GPIO PIN     NOTES
──────────────────────────────────────────────────────
Keypad Row 1          GPIO 22      Safe to use
Keypad Row 2          GPIO 21      Safe to use
Keypad Row 3          GPIO 15      Safe to use
Keypad Col 1          GPIO 13      Safe to use
Keypad Col 2          GPIO 12      Safe to use (no boot issue)
Keypad Col 3          GPIO 14      Safe to use
Keypad Col 4          GPIO 27      Safe to use
Relay Control         GPIO 32      Safe to use
Onboard LED           GPIO 2       Built-in (optional use)
```

### Reserved/Don't Use Pins

```
PIN       FUNCTION              WHY NOT TO USE
─────────────────────────────────────────────────────
GPIO 0    Boot/Flash button     Used for programming
GPIO 1    UART0 TX              Serial communication
GPIO 3    UART0 RX              Serial communication
GPIO 4    SD Card CS            If using TF card
GPIO 5    SD Card               Part of SD interface
GPIO 6-11 Internal Flash        NEVER USE - will brick board
GPIO 16   PSRAM                 Used by PSRAM
GPIO 17   PSRAM                 Used by PSRAM
GPIO 18   SD Card SCK           If using TF card
GPIO 19   SD Card MISO          If using TF card
GPIO 23   SD Card MOSI          If using TF card
```

---

## 🔧 Detailed Wiring Diagram

### 4x3 Keypad → LILYGO T8

```
Keypad Layout (3 rows × 4 columns):
┌───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ A │  ← Row 1 → GPIO 22
├───┼───┼───┼───┤
│ 4 │ 5 │ 6 │ B │  ← Row 2 → GPIO 21
├───┼───┼───┼───┤
│ 7 │ 8 │ 9 │ C │  ← Row 3 → GPIO 15
└───┴───┴───┴───┘
  ↓   ↓   ↓   ↓
Col1 Col2 Col3 Col4
GPIO GPIO GPIO GPIO
 13  12  14  27
```

**Connection Table:**
| Keypad Pin | Function | T8 GPIO |
|------------|----------|---------|
| Pin 1      | Row 1    | GPIO 22 |
| Pin 2      | Row 2    | GPIO 21 |
| Pin 3      | Row 3    | GPIO 15 |
| Pin 4      | Col 1    | GPIO 13 |
| Pin 5      | Col 2    | GPIO 12 |
| Pin 6      | Col 3    | GPIO 14 |
| Pin 7      | Col 4    | GPIO 27 |

### 6V Relay → LILYGO T8

| Relay Pin | T8 Pin | Wire Color | Notes |
|-----------|--------|------------|-------|
| VCC       | 5V     | Red        | From USB or VIN |
| GND       | GND    | Black      | Common ground |
| IN        | GPIO 32| Yellow     | Control signal |

### Reset Button → LILYGO T8

| Button Pin | T8 Pin | Notes |
|------------|--------|-------|
| Pin 1      | EN     | Enable/Reset pin |
| Pin 2      | GND    | Ground |

**Location:** Inside battery compartment or case

### Relay → Door Lock

| Relay Terminal | Connection | Notes |
|----------------|------------|-------|
| COM            | Lock PSU + | Common terminal |
| NO             | Lock +     | Normally Open |
| Lock (-)       | Lock PSU - | Complete circuit |

---

## ⚡ Power Supply Options

### Option 1: 4x AA Batteries (Portable)
```
Battery Pack (6V) → T8 VIN pin
Battery GND       → T8 GND pin

Expected Life: 2-3 months with BLE + deep sleep
```

### Option 2: USB Power (Permanent Installation)
```
USB 5V Adapter → Micro-USB port on T8

Pros: Unlimited power, no battery changes
Best for: Fixed installations
```

### Option 3: 18650 Battery + Holder
```
18650 Battery (3.7V) → 5V Boost Converter → T8 5V pin

Capacity: 3000mAh
Expected Life: 4-6 months
Rechargeable: Yes
```

### Option 4: LiPo Battery (Advanced)
```
3.7V LiPo → Charge controller → T8 3.3V pin

Best for: Compact installations
Requires: Battery management
```

---

## 📐 Physical Layout

### Component Placement Suggestion

```
┌─────────────────────────────────────┐
│                                     │
│  [4x3 Keypad]                       │
│                                     │
│  ┌──────────────┐                  │
│  │  LILYGO T8   │     [Relay]     │
│  │   V1.7       │                  │
│  │  (ESP32)     │                  │
│  └──────────────┘                  │
│                                     │
│  [4x AA Batteries]    [Reset Btn]  │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔌 Pinout Diagram (Visual)

```
LILYGO T8 V1.7 Pinout (Top View):

                    ┌─────────────┐
         EN ────────┤1          40├──────── GPIO 0
      GPIO 36 ──────┤2          39├──────── GPIO 4
      GPIO 39 ──────┤3          38├──────── GPIO 2 (LED)
      GPIO 34 ──────┤4          37├──────── GPIO 15 ← Row 3
      GPIO 35 ──────┤5          36├──────── GPIO 13 ← Col 1
      GPIO 32 ──────┤6          35├──────── GPIO 12 ← Col 2
      GPIO 33 ──────┤7          34├──────── GPIO 14 ← Col 3
      GPIO 25 ──────┤8          33├──────── GPIO 27 ← Col 4
      GPIO 26 ──────┤9          32├──────── GPIO 26
         DAC2 ──────┤10         31├──────── GPIO 25
         DAC1 ──────┤11         30├──────── GPIO 33
         3.3V ──────┤12         29├──────── GPIO 32 ← Relay
          GND ──────┤13         28├──────── GPIO 35
         GPIO 5 ────┤14         27├──────── GPIO 34
         GPIO 18 ───┤15         26├──────── VN
         GPIO 19 ───┤16         25├──────── VP
         GPIO 21 ───┤17  LILYGO 24├──────── GPIO 22 ← Row 1
          RXD ──────┤18    T8   23├──────── GPIO 21 ← Row 2
          TXD ──────┤19   V1.7  22├──────── GPIO 1
         GPIO 22 ───┤20         21├──────── GPIO 3
                    └─────────────┘
                     [USB Port]
```

---

## 🛠️ Assembly Steps

### Step 1: Prepare Board (5 min)
1. Unbox LILYGO T8 V1.7
2. Inspect for damage
3. Identify GPIO pins using pinout
4. Test USB connection (should see LED)

### Step 2: Wire Keypad (10 min)
1. Strip 7 wires (~15cm each)
2. Solder/connect to keypad:
   - Row 1 (red) → GPIO 22
   - Row 2 (orange) → GPIO 21
   - Row 3 (yellow) → GPIO 15
   - Col 1 (green) → GPIO 13
   - Col 2 (blue) → GPIO 12
   - Col 3 (purple) → GPIO 14
   - Col 4 (white) → GPIO 27
3. Use heat shrink or tape
4. Test continuity with multimeter

### Step 3: Wire Relay (5 min)
1. Connect VCC (red) → T8 5V
2. Connect GND (black) → T8 GND
3. Connect IN (yellow) → T8 GPIO 32
4. Secure connections

### Step 4: Install Reset Button (5 min)
1. Position in battery compartment
2. Wire Pin 1 → T8 EN
3. Wire Pin 2 → T8 GND
4. Test (press = board resets)
5. Secure with hot glue

### Step 5: Power Connection (5 min)
1. For batteries:
   - Connect + to VIN
   - Connect - to GND
2. For USB:
   - Just plug in Micro-USB

### Step 6: Test Before Final (10 min)
1. Power on T8
2. Check LED lights up
3. Press keypad buttons (log to serial)
4. Test relay clicking
5. Connect via BLE
6. Verify all functions

---

## 💻 Software Setup

### Flash MicroPython

1. **Download Firmware:**
   - Go to: https://micropython.org/download/esp32/
   - Get: `esp32spiram-*.bin` (SPIRAM version for WROVER)
   - **Important:** Use SPIRAM version, not regular!

2. **Install esptool:**
   ```bash
   pip install esptool
   ```

3. **Erase Flash:**
   ```bash
   esptool.py --port /dev/ttyUSB0 erase_flash
   ```

4. **Flash Firmware:**
   ```bash
   esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32spiram-*.bin
   ```

### Upload Code

**Required Files:**
1. `digital_safe_locker_T8.py` → rename to `main.py`
2. `ble_simple_peripheral.py`
3. `ble_advertising.py`

**Upload Method 1: Using ampy**
```bash
pip install adafruit-ampy
ampy --port /dev/ttyUSB0 put ble_advertising.py
ampy --port /dev/ttyUSB0 put ble_simple_peripheral.py
ampy --port /dev/ttyUSB0 put digital_safe_locker_T8.py main.py
```

**Upload Method 2: Using Thonny**
1. Install Thonny IDE
2. Select MicroPython (ESP32) interpreter
3. Open and save files to device

---

## 📱 BLE Device Name

**Device broadcasts as:** `T8-SafeLock`

Changed from "ESP32-SafeLock" to identify the LILYGO board.

---

## 🔋 Battery Life (LILYGO T8 V1.7)

### Power Consumption

| Mode | Current | Notes |
|------|---------|-------|
| **WiFi Active** | 160-240mA | Not recommended for battery |
| **BLE Active** | 100-120mA | Good for battery use |
| **Light Sleep** | 0.8mA | CPU on, radios off |
| **Deep Sleep** | 0.01mA | Very low power |

### Expected Battery Life (4x AA, 2500mAh)

| Configuration | Daily Usage | Battery Life |
|--------------|-------------|--------------|
| **BLE + Deep Sleep** | ~35mAh | **2-3 months** ⭐ |
| BLE Always On | ~120mAh | 3 weeks |
| WiFi Always On | ~4800mAh | <1 day ❌ |

**Recommendation:** Use battery_optimized version for 2-3 month life!

---

## 🎯 Special LILYGO T8 Features

### 1. SD Card Logging (Optional)
```python
from machine import SDCard, SPI

# Mount SD card
sd = SDCard(slot=2)
os.mount(sd, '/sd')

# Log access events
with open('/sd/access_log.txt', 'a') as f:
    f.write(f"{time.time()}: Door unlocked\n")
```

### 2. PSRAM Usage (Advanced)
```python
import gc
import esp32

# Check PSRAM
print(f"PSRAM free: {gc.mem_free()} bytes")
print(f"PSRAM size: {esp32.PSRAM_SIZE()} bytes")

# Large data structures use PSRAM automatically
large_list = [0] * 100000  # Uses PSRAM
```

### 3. Better BLE Range
- 3D antenna provides 20-30% better range
- Typical: 30-50 meters line of sight
- Through walls: 10-20 meters

### 4. Onboard LED (GPIO 2)
- Use for status indication
- Already in code for lock status
- Blue LED on most T8 boards

---

## 🐛 Troubleshooting LILYGO T8

### Upload Fails
- **Hold BOOT button** while connecting USB
- Try lower baud: `esptool.py --baud 115200`
- Check USB cable (data cable, not charge-only)

### Wrong Firmware
- **Must use SPIRAM version** for WROVER
- Regular ESP32 firmware won't work properly
- Download from: https://micropython.org/download/esp32/

### Pins Not Working
- **Avoid GPIO 6-11** (internal flash)
- **Don't use GPIO 16-17** if using PSRAM
- Check pinout diagram carefully

### BLE Won't Start
- Make sure WiFi is off (they conflict)
- Try power cycle
- Check serial output for errors

### SD Card Issues
- Format as FAT32
- Some pins conflict with keypad
- Optional feature, not required

---

## ✅ Testing Checklist

**Before Powering:**
- [ ] All wires connected correctly
- [ ] No shorts between pins
- [ ] Battery polarity correct
- [ ] Reset button installed

**After Powering:**
- [ ] Onboard LED lights up
- [ ] Serial output shows boot
- [ ] Keypad responds
- [ ] Relay clicks on command
- [ ] BLE "T8-SafeLock" visible
- [ ] Lock activates properly

**Full System:**
- [ ] Password entry works
- [ ] Wrong password lockout works
- [ ] BLE commands work
- [ ] Auto-lock after timeout
- [ ] Reset button functions
- [ ] Battery life acceptable

---

## 📊 Component Compatibility

| Component | Compatible | Notes |
|-----------|-----------|-------|
| 3.3V Relay | ✅ Yes | Direct GPIO control |
| 5V Relay | ✅ Yes | Powered from 5V pin |
| 12V Relay | ⚠️ Needs transistor | GPIO can't drive directly |
| 3x4 Keypad | ✅ Yes | Any matrix keypad |
| 4x3 Keypad | ✅ Yes | Current configuration |
| 4x4 Keypad | ✅ Yes | Need one more GPIO |

---

## 🎓 Pin Summary

```
COMPONENT        PIN      FUNCTION
─────────────────────────────────────
Keypad Row 1  →  GPIO 22  Row scan
Keypad Row 2  →  GPIO 21  Row scan
Keypad Row 3  →  GPIO 15  Row scan
Keypad Col 1  →  GPIO 13  Column read
Keypad Col 2  →  GPIO 12  Column read
Keypad Col 3  →  GPIO 14  Column read
Keypad Col 4  →  GPIO 27  Column read
Relay Control →  GPIO 32  Lock control
LED Status    →  GPIO 2   Built-in LED
Reset Button  →  EN       Hardware reset
Power (+)     →  VIN/5V   6V or 5V input
Power (-)     →  GND      Common ground
```

---

## 🚀 Quick Start Summary

1. **Flash** ESP32 SPIRAM firmware
2. **Upload** 3 Python files
3. **Wire** keypad (7 wires)
4. **Wire** relay (3 wires)
5. **Wire** reset button (2 wires)
6. **Connect** batteries or USB
7. **Test** via serial monitor
8. **Connect** via BLE
9. **Done!** System operational

**Total Time:** 30-60 minutes  
**Difficulty:** ⭐⭐⭐☆☆ (Intermediate)

---

## 📚 Additional Resources

**LILYGO GitHub:**
- https://github.com/LilyGO/TTGO-T8-ESP32

**MicroPython Docs:**
- https://docs.micropython.org/en/latest/esp32/quickref.html

**ESP32-WROVER Datasheet:**
- https://www.espressif.com/sites/default/files/documentation/esp32-wrover_datasheet_en.pdf

---

**Board:** LILYGO T8 V1.7 ESP32-WROVER  
**RAM:** 520KB + 8MB PSRAM  
**Flash:** 16MB  
**Features:** WiFi, BLE, SD Card, 3D Antenna  
**Perfect for:** Advanced embedded projects with battery power
