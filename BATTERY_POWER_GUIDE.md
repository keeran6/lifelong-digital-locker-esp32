# Battery Power Guide - 4x AA Batteries

## 🔋 Battery Specifications

**4x AA Alkaline Batteries:**
- Voltage: 6V nominal (1.5V × 4)
- Capacity: 2000-3000mAh (typically 2500mAh)
- Discharge curve: 6V → 4.8V (usable range)
- Self-discharge: ~5-10% per year
- Operating temp: -18°C to 55°C

**4x AA NiMH Rechargeable:**
- Voltage: 4.8V nominal (1.2V × 4)
- Capacity: 1900-2500mAh
- Self-discharge: 15-20% per month (standard), 5% per year (low self-discharge)
- Rechargeable: 500-1000 cycles
- Better for environment and long-term cost

---

## ⚡ Power Consumption Breakdown

### ESP32 Pico Power Draw

| Mode | Current Draw | Notes |
|------|--------------|-------|
| WiFi Active | 160-260mA | Very power hungry! |
| BLE Active | 100-130mA | Much better than WiFi |
| Modem Sleep | 15-30mA | WiFi/BLE off, CPU on |
| Light Sleep | 0.8mA | Can wake quickly |
| Deep Sleep | 0.01-0.15mA | Takes ~1s to wake |
| Powered Off | 0mA | Need to press reset |

### 6V Solenoid Lock

| State | Current Draw | Duration |
|-------|--------------|----------|
| Locked (idle) | 0mA | 99.9% of time |
| Unlocking | 200-500mA | 3-5 seconds |
| Holding (if needed) | 50-150mA | Continuous |

**Note:** Most solenoids are momentary - they only need power to actuate, not to hold position.

---

## 📊 Battery Life Calculations

### Scenario 1: BLE Only (RECOMMENDED) ⭐

**Daily Usage Pattern:**
- 10 unlocks per day
- Each unlock: 3 seconds solenoid + 10 seconds ESP32 active
- Rest of time: Deep sleep

**Calculation:**
```
Lock usage:     10 × 3s × 300mA = 25 mAh/day
ESP32 active:   10 × 10s × 120mA = 3.3 mAh/day  
ESP32 sleep:    ~24h × 0.1mA = 2.4 mAh/day
Voltage reg loss: 20% overhead = 6.1 mAh/day
─────────────────────────────────────────
TOTAL:          ~37 mAh/day
```

**Battery Life:**
```
2500 mAh ÷ 37 mAh/day = 67 days ≈ 2-2.5 months
```

### Scenario 2: WiFi Standby

**Daily Usage Pattern:**
- Same unlock pattern
- WiFi checks connection every 5 minutes

**Calculation:**
```
Lock usage:     25 mAh/day
WiFi checks:    288 × 5s × 200mA = 80 mAh/day
ESP32 active:   10 × 10s × 120mA = 3.3 mAh/day
ESP32 sleep:    ~24h × 0.1mA = 2.4 mAh/day
Voltage reg loss: 20% overhead = 22.1 mAh/day
─────────────────────────────────────────
TOTAL:          ~133 mAh/day
```

**Battery Life:**
```
2500 mAh ÷ 133 mAh/day = 18 days ≈ 2-3 weeks
```

### Scenario 3: WiFi Always On ❌

**Calculation:**
```
Lock usage:     25 mAh/day
WiFi 24/7:      24h × 180mA = 4320 mAh/day
ESP32 active:   3.3 mAh/day
Voltage reg loss: 20% overhead = 869 mAh/day
─────────────────────────────────────────
TOTAL:          ~5217 mAh/day
```

**Battery Life:**
```
2500 mAh ÷ 5217 mAh/day = 0.5 days = 12 HOURS!
```

---

## 📈 Real-World Battery Life Estimates

| Configuration | Theoretical | Realistic | Notes |
|--------------|-------------|-----------|-------|
| **BLE + Deep Sleep** | 67 days | 2-3 months | Best option! ⭐ |
| **BLE Always On** | 18 days | 2-3 weeks | Okay for testing |
| **WiFi Periodic** | 18 days | 2-3 weeks | Same as BLE always on |
| **WiFi Always On** | 12 hours | <1 day | Not viable ❌ |

**Realistic = Theoretical × 70%** (accounts for battery self-discharge, temperature effects, etc.)

---

## 🚀 Battery Life Optimization Tips

### 1. Use BLE Instead of WiFi
```python
# Save 50-150mA!
# BLE: ~120mA active
# WiFi: ~200mA active
```

### 2. Implement Deep Sleep
```python
from machine import deepsleep

# After 30 seconds idle, sleep for 5 minutes
deepsleep(5 * 60 * 1000)  # milliseconds

# Power: 0.1mA vs 120mA = 1200x savings!
```

### 3. Optimize Solenoid Usage
```python
# Short pulse = less power
def quick_unlock():
    relay.on()
    time.sleep(1)  # Just 1 second instead of 5
    relay.off()

# Saves 80% of solenoid power!
```

### 4. Use Interrupt Wake-Up
```python
from machine import Pin

# Wake ESP32 only when keypad pressed
# Instead of constantly scanning
ext0_wake = Pin(13, mode=Pin.IN, pull=Pin.PULL_UP)
# Configure as wake source in deep sleep
```

### 5. Lower CPU Frequency
```python
import machine

# Reduce from 240MHz to 80MHz
machine.freq(80000000)
# Saves ~30% power when active
```

---

## 🔌 Alternative Power Solutions

### Option 1: USB Power (Recommended for Permanent Installation)
```
Cost: $5 for 5V/2A adapter
Pros: Unlimited power, reliable
Cons: Needs nearby outlet
```

### Option 2: Rechargeable Battery Pack
```
Cost: $15-30 for 18650 battery + holder
Capacity: 3000-6000mAh at 3.7V
Life: 4-6 months per charge
Pros: Higher capacity, rechargeable
```

### Option 3: Solar + Battery
```
Cost: $20-40 for solar panel + charge controller
Capacity: Unlimited with sun
Life: Indefinite
Pros: Self-sustaining
Best for: Outdoor installations
```

### Option 4: Power Bank
```
Cost: $10-20 for 10,000mAh power bank
Life: 6-12 months per charge
Pros: USB output, easy to recharge
```

---

## 🔧 Hardware Power Optimization

### Use a Better Voltage Regulator
```
Standard ESP32 regulator: 70-80% efficient
Buck converter (LM2596): 85-95% efficient

Power saved: 15-25%
Cost: $2-5
```

### Choose Low-Power Relay
```
Standard relay: 70-100mA coil current
Solid-state relay: 5-20mA
MOSFET circuit: <1mA

Power saved: Up to 95%
Cost: $3-8
```

### Use Efficient Solenoid
```
Standard solenoid: 300-500mA
Low-power solenoid: 100-200mA
Latch solenoid: 500mA for 50ms only

Power saved: 50-90%
Cost: $5-15
```

---

## 📊 Power Consumption Monitoring

### Measure Real Usage
```python
# Add this to your code
import time

start_time = time.time()
unlock_count = 0

def track_usage():
    global unlock_count
    unlock_count += 1
    
    runtime = (time.time() - start_time) / 3600  # hours
    avg_unlocks = unlock_count / runtime if runtime > 0 else 0
    
    print(f"Runtime: {runtime:.1f}h")
    print(f"Unlocks: {unlock_count}")
    print(f"Rate: {avg_unlocks:.1f}/hour")
```

### Calculate Remaining Battery Life
```python
# Theoretical remaining capacity
BATTERY_CAPACITY = 2500  # mAh
DAILY_USAGE = 37  # mAh/day

def estimate_battery_life():
    days_remaining = BATTERY_CAPACITY / DAILY_USAGE
    print(f"Estimated battery life: {days_remaining:.0f} days")
    print(f"Replace by: {days_remaining:.1f} weeks")
```

---

## ⚠️ Battery Safety

### Do NOT:
- ❌ Mix old and new batteries
- ❌ Mix different brands/types
- ❌ Use damaged batteries
- ❌ Short circuit battery terminals
- ❌ Charge non-rechargeable batteries
- ❌ Exceed 6.5V input to ESP32

### DO:
- ✅ Replace all 4 batteries at once
- ✅ Use same brand/capacity
- ✅ Check polarity before connecting
- ✅ Add fuse (1A) for safety
- ✅ Monitor for overheating
- ✅ Remove batteries if not using for >3 months

---

## 🎯 Recommended Setup for Best Battery Life

```python
# Configuration for 2-3 month battery life:

1. Use BLE ONLY (no WiFi)
2. Enable deep sleep after 30s idle
3. Use interrupt wake on keypad
4. Lower CPU freq to 80MHz
5. Short solenoid pulse (1-2s)
6. Use low self-discharge NiMH batteries

Expected battery life: 2-3 months (60-90 days)
```

### Weekly Routine:
- Check battery voltage (should be >5V)
- Test unlock function
- Verify BLE connection

### Monthly Routine:
- Measure actual unlocks vs estimate
- Clean keypad contacts
- Check all connections

### Battery Replacement:
- Replace when voltage <4.8V
- Or after 60-90 days
- Or when lock becomes unreliable

---

## 📱 Low Battery Warning Implementation

```python
from machine import ADC, Pin

# Connect voltage divider to GPIO34
battery_adc = ADC(Pin(34))
battery_adc.atten(ADC.ATTN_11DB)  # 0-3.6V range

def check_battery():
    # Read voltage (needs calibration)
    voltage = battery_adc.read() * 3.6 / 4095 * 2  # voltage divider
    
    if voltage < 5.0:
        print("⚠️ LOW BATTERY!")
        # Flash LED or send BLE notification
        return True
    return False

# Check every hour
while True:
    check_battery()
    time.sleep(3600)
```

---

## 💰 Cost Comparison (1 Year)

| Power Source | Initial Cost | Running Cost | Total |
|-------------|--------------|--------------|-------|
| Alkaline AA | $8 (4-pack) | $48 (6 changes) | $56 |
| NiMH AA + Charger | $25 | $2 (electricity) | $27 |
| USB Adapter | $5 | $3 (electricity) | $8 |
| Solar Setup | $35 | $0 | $35 |

**Winner: USB Adapter** for permanent installations  
**Runner-up: NiMH Rechargeable** for portability

---

## 🎓 Summary

**Can 4x AA power both ESP32 and solenoid?**
✅ **YES!**

**How long?**
- **Best case (BLE + Deep Sleep):** 2-3 months
- **Typical (BLE always on):** 2-3 weeks  
- **Worst case (WiFi always on):** <1 day

**Recommendations:**
1. Use BLE instead of WiFi (50-100mA savings)
2. Implement deep sleep when idle (saves 99% power)
3. Consider USB power for permanent installation
4. Use NiMH rechargeable for best value
5. Monitor battery voltage weekly

**Bottom line:** 4x AA batteries work great for **BLE mode with 2-3 month life**. WiFi always-on is not viable with AA batteries.
