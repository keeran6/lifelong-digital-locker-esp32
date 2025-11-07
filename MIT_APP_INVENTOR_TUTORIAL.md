# MIT App Inventor - Safe Lock App Tutorial

## 🎯 Create Your Own Safe Lock Control App (No Coding!)

**Time Required:** 1-2 hours  
**Skill Level:** Beginner (no programming needed)  
**Cost:** Free  

---

## 📋 What You'll Build

A custom Android app with:
- ✅ BLE device scanner
- ✅ One-tap connection to your safe
- ✅ Password entry field
- ✅ Lock/Unlock buttons
- ✅ Status display
- ✅ Custom branding (your name/logo)

---

## 🚀 Step-by-Step Tutorial

### Part 1: Setup (5 minutes)

1. **Create Account**
   - Go to: http://ai2.appinventor.mit.edu/
   - Click "Create Apps!"
   - Sign in with Google account
   - Accept terms

2. **Start New Project**
   - Click "Start new project"
   - Name it: `SafeLockControl`
   - Click OK

---

### Part 2: Design the Interface (15 minutes)

#### Screen Layout

You'll be in the "Designer" view. On the left is the "Palette" with components.

**Add Components (Drag from Palette to Viewer):**

1. **Connectivity** section:
   - Drag `BluetoothLE` → Rename to `BLE`
   - (This is invisible - appears below viewer)

2. **Layout** section:
   - Drag `VerticalArrangement` → Set width to "Fill parent"
   - Inside this arrangement, add all other components:

3. **User Interface** section:
   - Drag `Label` → Rename to `TitleLabel`
     - Text: "🔒 Safe Lock Control"
     - FontSize: 24
     - FontBold: ✓
     - TextAlignment: center
   
   - Drag `Label` → Rename to `StatusLabel`
     - Text: "Status: Disconnected"
     - FontSize: 16
     - TextColor: Red
   
   - Drag `Button` → Rename to `ScanButton`
     - Text: "📡 Scan for Safe"
     - Width: Fill parent
     - BackgroundColor: Blue
     - TextColor: White
   
   - Drag `ListPicker` → Rename to `DevicePicker`
     - Text: "Select Device"
     - Width: Fill parent
     - Visible: unchecked initially
   
   - Drag `TextBox` → Rename to `PasswordInput`
     - Hint: "Enter password"
     - Width: Fill parent
     - PasswordTextBox: ✓ (hides password)
   
   - Drag `HorizontalArrangement` → Width: Fill parent
     - Inside this, add 2 buttons:
   
   - Drag `Button` → Rename to `UnlockButton`
     - Text: "🔓 Unlock"
     - Width: 50%
     - BackgroundColor: Green
     - TextColor: White
   
   - Drag `Button` → Rename to `LockButton`
     - Text: "🔒 Lock"
     - Width: 50%
     - BackgroundColor: Red
     - TextColor: White
   
   - Drag `HorizontalArrangement` → Width: Fill parent
     - Inside this, add 2 more buttons:
   
   - Drag `Button` → Rename to `ToggleButton`
     - Text: "🔄 Toggle"
     - Width: 50%
   
   - Drag `Button` → Rename to `StatusButton`
     - Text: "📊 Status"
     - Width: 50%
   
   - Drag `Label` → Rename to `ResponseLabel`
     - Text: ""
     - FontSize: 14
     - Width: Fill parent

4. **Add Notifier** (for alerts):
   - From Palette → User Interface
   - Drag `Notifier` → Rename to `Alert`

---

### Part 3: Program the Blocks (30-45 minutes)

Click "Blocks" button (top right) to switch to programming view.

#### Block 1: Scan for Devices

```
WHEN ScanButton.Click DO:
  CALL BLE.StartScanning
  SET StatusLabel.Text TO "Scanning..."
  SET StatusLabel.TextColor TO Orange
```

**How to create:**
1. Blocks panel (left) → ScanButton → `when ScanButton.Click`
2. Blocks panel → BLE → `call BLE.StartScanning`
3. Blocks panel → StatusLabel → `set StatusLabel.Text to`
4. Blocks panel → Text → `" "` (text block) → type "Scanning..."
5. Repeat for TextColor

#### Block 2: Device Found

```
WHEN BLE.DeviceScanResult DO:
  IF name CONTAINS "ESP32-SafeLock" THEN:
    ADD name TO DevicePicker.Elements
    SET DevicePicker.Visible TO true
```

**How to create:**
1. BLE → `when BLE.DeviceScanResult`
2. Control → `if then` block
3. Text → `contains` block
4. BLE → `get name` (from DeviceScanResult parameters)
5. Text block → type "ESP32-SafeLock"
6. Lists → `add items to list`
7. DevicePicker → `DevicePicker.Elements`
8. Set → `set DevicePicker.Visible to`
9. Logic → `true`

#### Block 3: Connect to Device

```
WHEN DevicePicker.AfterPicking DO:
  SET StatusLabel.Text TO "Connecting..."
  CALL BLE.Connect deviceAddress
```

**How to create:**
1. DevicePicker → `when DevicePicker.AfterPicking`
2. StatusLabel → `set StatusLabel.Text`
3. BLE → `call BLE.Connect`
4. BLE → `get deviceAddress`

#### Block 4: Connected Successfully

```
WHEN BLE.Connected DO:
  SET StatusLabel.Text TO "Connected ✓"
  SET StatusLabel.TextColor TO Green
  CALL Alert.ShowAlert message: "Connected to Safe!"
```

#### Block 5: Unlock Button

```
WHEN UnlockButton.Click DO:
  SET command TO JOIN "PASS:" PasswordInput.Text
  CALL BLE.WriteStringsWithResponse:
    serviceUuid: "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    characteristicUuid: "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    values: LIST command
  SET ResponseLabel.Text TO "Sending unlock command..."
```

**Note:** You'll need to type these UUIDs carefully!

**Service UUID:** `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`  
**RX UUID (Write):** `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`  
**TX UUID (Read):** `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`

#### Block 6: Lock Button

```
WHEN LockButton.Click DO:
  CALL BLE.WriteStringsWithResponse:
    serviceUuid: "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    characteristicUuid: "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    values: LIST "CLOSE"
  SET ResponseLabel.Text TO "Sending lock command..."
```

#### Block 7: Toggle Button

```
WHEN ToggleButton.Click DO:
  CALL BLE.WriteStringsWithResponse:
    serviceUuid: "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    characteristicUuid: "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    values: LIST "TOGGLE"
```

#### Block 8: Status Button

```
WHEN StatusButton.Click DO:
  CALL BLE.WriteStringsWithResponse:
    serviceUuid: "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
    characteristicUuid: "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
    values: LIST "STATUS"
```

#### Block 9: Receive Response

```
WHEN BLE.StringsReceived DO:
  SET ResponseLabel.Text TO stringValues
  IF stringValues CONTAINS "OK:UNLOCKED" THEN:
    CALL Alert.ShowAlert message: "Unlocked! ✓"
  IF stringValues CONTAINS "OK:LOCKED" THEN:
    CALL Alert.ShowAlert message: "Locked! ✓"
  IF stringValues CONTAINS "ERROR" THEN:
    CALL Alert.ShowAlert message: "Error: Wrong password"
```

#### Block 10: Handle Disconnection

```
WHEN BLE.Disconnected DO:
  SET StatusLabel.Text TO "Disconnected"
  SET StatusLabel.TextColor TO Red
  CALL Alert.ShowAlert message: "Lost connection to safe"
```

---

### Part 4: Build the App (10 minutes)

1. **Test in Emulator (Optional)**
   - Click "Connect" → "AI Companion"
   - Install "MIT AI2 Companion" on phone
   - Scan QR code
   - Test the app

2. **Build APK**
   - Click "Build" → "Android App (.apk)"
   - Wait 2-5 minutes
   - Download APK to computer
   - Transfer to phone
   - Install (enable "Unknown Sources" in Android settings)

3. **Build AAB (for Play Store)**
   - Click "Build" → "Android App (.aab)"
   - Use this if you want to publish on Google Play

---

## 🎨 Customization Ideas

### Change Colors
- Unlock button: Green (#4CAF50)
- Lock button: Red (#F44336)
- Toggle button: Blue (#2196F3)
- Status button: Orange (#FF9800)

### Add Icon
1. Properties → Screen1 → Icon
2. Upload image (PNG, 512×512px recommended)

### Add Background
1. Properties → Screen1 → BackgroundImage
2. Upload image

### Add Sounds
1. Palette → Media → Sound
2. Upload .mp3 files
3. Play on unlock/lock

---

## 🐛 Troubleshooting

### App Crashes on Startup
- Check all UUIDs are correct
- Remove spaces from UUIDs
- Ensure BLE component is added

### Can't Find Device
- Make sure ESP32 is powered on
- Check device name is "ESP32-SafeLock"
- Try restarting scan
- Enable Location on Android (required for BLE)

### Won't Connect
- Check BLE permissions in Android settings
- Try uninstalling and reinstalling app
- Make sure only one device is trying to connect

### Commands Not Working
- Verify UUIDs are exactly correct
- Check ESP32 is receiving commands (check serial monitor)
- Try sending simpler commands first ("OPEN")

---

## 📱 App Permissions

Your app will need these Android permissions:
- ✅ Bluetooth
- ✅ Bluetooth Admin
- ✅ Location (required for BLE scanning on Android)

These are automatically added by App Inventor.

---

## 🔒 Security Tips

1. **Password Storage**
   - Don't hardcode password in app
   - Always require user to enter password
   - Consider adding "Remember Password" checkbox

2. **BLE Security**
   - BLE range is limited (~10-30 meters)
   - Consider adding app PIN code
   - Add encryption for sensitive commands

3. **User Authentication**
   - Add login screen with PIN
   - Store PIN in TinyDB (encrypted)
   - Lock app after inactivity

---

## 🚀 Advanced Features (Optional)

### 1. Add Multiple Safes

Store multiple device addresses in TinyDB:
```
WHEN DevicePicker.AfterPicking:
  CALL TinyDB.StoreValue:
    tag: "SafeAddress"
    value: deviceAddress
```

### 2. Activity Log

Track unlock/lock events:
```
WHEN UnlockButton.Click:
  SET timestamp TO Clock.Now
  CALL TinyDB.AppendValueToList:
    tag: "ActivityLog"
    value: JOIN timestamp " - Unlocked"
```

### 3. Add Notifications

Send Android notification on unlock:
```
WHEN BLE.StringsReceived:
  IF stringValues CONTAINS "OK:UNLOCKED":
    CALL Notifier.ShowAlert:
      notice: "Safe unlocked!"
```

### 4. Add Timer/Scheduler

Auto-lock after timeout:
```
WHEN Clock.Timer:
  IF unlocked for 30 seconds THEN:
    CALL BLE.WriteStrings: "CLOSE"
```

---

## 📦 Export/Share Your App

### Share APK with Family
1. Build APK
2. Upload to Google Drive
3. Share link
4. They install APK

### Publish on Play Store
1. Build AAB
2. Create Play Console account ($25 one-time)
3. Upload AAB
4. Fill out store listing
5. Submit for review

### Make it Open Source
1. Export .aia file (Project → Export to computer)
2. Upload to GitHub
3. Others can import and modify

---

## 🎓 Complete Block Summary

Here's what your blocks should look like:

```
1. Scan Button → Start BLE scanning
2. Device Found → Add to list if ESP32-SafeLock
3. Device Picker → Connect to selected device
4. BLE Connected → Update status, show alert
5. Unlock Button → Send PASS:password
6. Lock Button → Send CLOSE
7. Toggle Button → Send TOGGLE
8. Status Button → Send STATUS
9. BLE Response → Display result, show alert
10. BLE Disconnected → Update status
```

---

## 📚 Resources

**MIT App Inventor:**
- Website: http://ai2.appinventor.mit.edu/
- Tutorials: https://appinventor.mit.edu/explore/ai2/tutorials
- Forum: https://community.appinventor.mit.edu/

**BLE Extension:**
- Docs: http://iot.appinventor.mit.edu/assets/resources/edu.mit.appinventor.ble.pdf

**Example Projects:**
- BLE Scanner: http://iot.appinventor.mit.edu/examples

---

## ✅ Testing Checklist

Before building final APK:

- [ ] Scan finds ESP32-SafeLock
- [ ] Connection succeeds
- [ ] Password field hides characters
- [ ] Unlock command works
- [ ] Lock command works
- [ ] Toggle command works
- [ ] Status command returns state
- [ ] Disconnection handled gracefully
- [ ] UI looks good on your phone
- [ ] All buttons work as expected

---

## 🎉 You're Done!

You now have a custom Android app to control your safe!

**Next Steps:**
- Customize colors and icons
- Add more features
- Share with family
- Publish on Play Store (optional)

**Estimated Total Time:** 1-2 hours

**Difficulty:** ⭐⭐☆☆☆ (Easy - No coding required!)

---

## 💡 Quick Tips

- Save your work frequently (File → Checkpoint)
- Test on real device, not just emulator
- Start simple, add features gradually
- Ask for help on App Inventor forum
- Export .aia file as backup

Happy coding! 🚀
