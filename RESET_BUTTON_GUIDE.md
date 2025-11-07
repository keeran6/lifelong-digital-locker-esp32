# Reset Button Installation Guide

## 🔘 Hardware Reset Button Wiring

### Simple Method (Recommended)

**Components Needed:**
- 1× Tactile push button (momentary switch)
- 2× Wires (~10cm each)
- Optional: Hot glue or mounting bracket

**Wiring:**
```
ESP32 Pin       Wire        Button        Wire        ESP32 Pin
───────────────────────────────────────────────────────────────
   EN pin   ──────────┤  Switch  ├──────────   GND
                      └──────────┘

When button pressed: EN connects to GND → ESP32 resets
When button released: ESP32 runs normally
```

### Detailed Connection

```
                     ESP32 PICO
                  ┌──────────────┐
Battery           │              │
Compartment       │      EN ─────┼─────┐
    │             │              │     │
    │             │     GND ─────┼───┐ │
    │             └──────────────┘   │ │
    │                                │ │
    └─── [Reset Button] ─────────────┘ │
         (Tactile Switch)               │
              │                         │
              └─────────────────────────┘
```

### Physical Layout

```
Battery Compartment (Top View):
┌─────────────────────────────┐
│  [AA] [AA]                  │
│                    ┌───┐    │
│  [AA] [AA]         │ R │◄───┼── Reset Button
│                    └───┘    │
│  ┌──────────┐               │
│  │  ESP32   │               │
│  └──────────┘               │
└─────────────────────────────┘

Button placement options:
1. Side of battery holder (drill small hole)
2. Inside compartment lid
3. On PCB/breadboard inside compartment
```

---

## 📋 Step-by-Step Installation

### Method 1: Inside Battery Compartment

1. **Position the button**
   - Find accessible spot in battery compartment
   - Should be easy to reach but not accidentally pressed
   - Consider drilling small hole in compartment side

2. **Wire connections**
   ```
   Button Pin 1 ──→ ESP32 EN pin
   Button Pin 2 ──→ ESP32 GND pin
   ```

3. **Secure the button**
   - Use hot glue to fix button in place
   - Or use small mounting bracket
   - Ensure wires won't get pinched by batteries

4. **Test**
   - Power on ESP32
   - Press button
   - ESP32 should reset (program restarts)

### Method 2: External Button Through Case

1. **Drill hole in case**
   - Use 6mm drill bit for standard tactile button
   - Smooth edges with sandpaper
   - Location: Side or back of safe, near battery

2. **Mount button**
   - Insert button through hole
   - Secure with nut if button has threads
   - Or use hot glue from inside

3. **Wire internally**
   - Run wires from button to ESP32
   - Keep wires neat and secured
   - Use cable ties or adhesive clips

---

## 🔧 Button Types & Options

### Option 1: Tactile Push Button (Recommended)
```
Cost: $0.50-1.00
Size: 6×6mm or 12×12mm
Type: Momentary (normally open)
Pros: Small, cheap, reliable
Cons: Needs mounting hole
```

### Option 2: Panel Mount Button
```
Cost: $2-5
Size: 16mm diameter
Type: Momentary
Pros: Professional look, easy mounting
Cons: Slightly more expensive
```

### Option 3: Micro Switch
```
Cost: $0.50
Size: Very small
Type: Momentary
Pros: Tiny, no drill needed
Cons: Harder to press
```

---

## 🔌 Wiring Diagram

### Visual Wiring

```
                    ESP32 PICO DEVKIT
           ┌────────────────────────────────┐
           │                                │
           │  EN (Enable) ●                 │
Battery    │             │                  │
Holder     │             │                  │
  │        │            [R]  Reset          │
  │        │             │   Button         │
  │        │             ●                  │
  │        │            GND                 │
  │        └────────────────────────────────┘
  │                     │
  └─────────────────────┴─── Battery GND
```

### Circuit Schematic

```
     VIN ────┬──── (+) Batteries
             │
          ESP32
             │
     GND ────┴──── (-) Batteries
             │
             └──── [Button] ──── EN
             
When button pressed: EN pulls to GND
Result: ESP32 resets
```

---

## ⚡ Why This Works

### ESP32 EN (Enable) Pin

The EN pin controls whether the ESP32 is running:
- **EN = HIGH (3.3V)**: ESP32 runs normally ✅
- **EN = LOW (GND)**: ESP32 is held in reset ❌

**Internal Pull-up:**
- ESP32 has internal 45kΩ pull-up on EN
- Normally pulls EN HIGH
- Button connects EN to GND
- Overrides pull-up → Resets ESP32

**No External Resistor Needed:**
- Internal pull-up is sufficient
- Just wire button between EN and GND
- Simple 2-wire connection

---

## 🛠️ Installation Tips

### For Battery Compartment Access:

1. **Button Placement**
   - Near front of compartment (easy access)
   - Away from batteries (avoid shorting)
   - Not under batteries (can't press)

2. **Wire Management**
   - Use thin wires (22-26 AWG)
   - Different colors for EN and GND
   - Keep wires short (~10-15cm)
   - Secure with tape or zip ties

3. **Mounting Options**
   - Hot glue (removable with isopropyl alcohol)
   - Double-sided tape
   - Small bracket with screws
   - Drill hole through compartment wall

### Troubleshooting:

**Button doesn't reset:**
- ✓ Check EN pin connection
- ✓ Verify GND connection
- ✓ Test button with multimeter (continuity mode)
- ✓ Ensure button is momentary, not latching

**ESP32 won't boot:**
- ✓ Button may be stuck pressed
- ✓ Check for short between EN and GND
- ✓ Disconnect button and test

**Random resets:**
- ✓ Button wires may be loose
- ✓ Wires touching metal causing shorts
- ✓ Button getting accidentally pressed

---

## 🎯 Alternative: Software Reset Button

If you don't want hardware reset, add a software reset via keypad:

```python
# Add to process_keypad_input function:

def process_keypad_input(key):
    # ... existing code ...
    
    elif key == 'D':  # Software reset on 'D' key
        print("🔄 Resetting system...")
        close_lock()  # Ensure lock is closed
        time.sleep(1)
        import machine
        machine.reset()  # Software reset
```

**Keypad Combination Reset:**
```python
# Press '*' then 'A' then 'B' to reset
reset_sequence = ""

def check_reset_combo(key):
    global reset_sequence
    reset_sequence += key
    
    if reset_sequence.endswith("*AB"):
        print("🔄 Reset combo detected!")
        machine.reset()
    
    # Keep only last 3 keys
    if len(reset_sequence) > 3:
        reset_sequence = reset_sequence[-3:]
```

---

## 📊 Comparison: Hardware vs Software Reset

| Feature | Hardware Reset | Software Reset |
|---------|---------------|----------------|
| **Complexity** | Very simple | Requires code |
| **Reliability** | 100% works | 99% works |
| **When frozen** | ✅ Always works | ❌ May not work |
| **Components** | Button + wires | No hardware |
| **Cost** | ~$1 | $0 |
| **Installation** | 5 minutes | 2 minutes (code) |
| **Accessibility** | Physical access | Via keypad/BLE |
| **Best for** | Debugging, emergencies | Convenience |

**Recommendation:** Add **both** hardware and software reset options!

---

## 🔒 Security Note

**Reset Button Security:**
- Reset clears entered password (but doesn't bypass lock)
- Lock remains in its current state after reset
- Does NOT automatically unlock safe
- Password still required after reset

**For High Security:**
- Hide reset button inside battery compartment
- Require opening safe to access reset
- Or add small recessed button (needs paperclip to press)

---

## 📋 Shopping List

| Item | Quantity | Cost | Source |
|------|----------|------|--------|
| Tactile button 6×6mm | 1 | $0.50 | Amazon/eBay |
| 22 AWG wire (red) | 15cm | $0.10 | Any electronics |
| 22 AWG wire (black) | 15cm | $0.10 | Any electronics |
| Heat shrink tubing | 2cm | $0.05 | Optional |
| Hot glue | Small dab | $0.05 | Dollar store |

**Total: ~$1**

---

## ✅ Testing Procedure

1. **Visual Check**
   - [ ] Button securely mounted
   - [ ] Wires properly connected
   - [ ] No loose connections
   - [ ] Button accessible from outside

2. **Electrical Test**
   - [ ] Power off ESP32
   - [ ] Use multimeter in continuity mode
   - [ ] Press button: should beep (closed circuit)
   - [ ] Release button: no beep (open circuit)

3. **Functional Test**
   - [ ] Power on ESP32
   - [ ] Wait for boot (see LED activity)
   - [ ] Press reset button
   - [ ] ESP32 should restart
   - [ ] Program runs from beginning

4. **Integration Test**
   - [ ] Enter password on keypad
   - [ ] Press reset button mid-entry
   - [ ] Password should be cleared
   - [ ] System should restart normally

---

## 🎓 Quick Reference

**Fastest Installation (5 minutes):**

1. Get tactile button
2. Solder two wires to button pins
3. Connect Wire 1 → ESP32 EN pin
4. Connect Wire 2 → ESP32 GND pin
5. Hot glue button inside battery compartment
6. Test: Press button = ESP32 resets
7. Done! ✅

**EN Pin Location:**
- Usually labeled "EN" on ESP32
- Near the USB port
- Check your ESP32 Pico pinout diagram
- Sometimes also labeled "RESET"

**Remember:**
- No resistor needed
- Simple 2-wire connection
- Momentary button (springs back)
- Press to reset, release to run
