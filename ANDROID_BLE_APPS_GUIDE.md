# Open Source Android BLE Apps for Safe Control

## 📱 Ready-to-Use Open Source BLE Apps

### Option 1: nRF Connect (Recommended ⭐)

**Best for: Testing and advanced control**

- **Developer:** Nordic Semiconductor
- **License:** Open Source (BSD)
- **Source Code:** https://github.com/NordicSemiconductor/Android-nRF-Connect
- **Download:** Google Play Store (free)

**Features:**
- ✅ Full BLE scanner and GATT browser
- ✅ Send/receive data to UART service
- ✅ Save custom commands
- ✅ No ads, completely free
- ✅ Professional interface
- ✅ Works with ESP32 BLE UART

**How to Use:**
1. Install nRF Connect from Play Store
2. Scan for "ESP32-SafeLock"
3. Connect to device
4. Find "Nordic UART Service"
5. Enable notifications on TX characteristic
6. Write to RX characteristic:
   - `PASS:1234`
   - `OPEN`
   - `CLOSE`
   - etc.

**Pros:**
- Most reliable and feature-rich
- Actively maintained
- Great for debugging

**Cons:**
- Not specifically designed for door locks
- Requires understanding GATT services
- More complex than needed for basic use

---

### Option 2: Serial Bluetooth Terminal

**Best for: Simple command sending**

- **Developer:** Kai Morich
- **License:** Open Source (MIT)
- **Source Code:** https://github.com/kai-morich/SimpleBluetoothTerminal
- **Download:** Google Play Store (free)

**Features:**
- ✅ Simple terminal interface
- ✅ Send text commands easily
- ✅ Command history
- ✅ Macros for common commands
- ✅ Works with BLE UART

**How to Use:**
1. Install from Play Store
2. Select "ESP32-SafeLock"
3. Type commands:
   - `PASS:1234`
   - `OPEN`
   - `CLOSE`
4. Press send

**Pros:**
- Very simple to use
- Perfect for text commands
- Lightweight

**Cons:**
- Basic UI (not pretty)
- Limited customization

---

### Option 3: BLE Terminal (HM-10)

**Best for: Quick testing**

- **Download:** Play Store (search "BLE Terminal")
- **Type:** Various open source options available
- **License:** Most are MIT/Apache

**Features:**
- Simple send/receive
- Basic but functional
- Multiple apps available with similar names

---

## 🛠️ DIY Options: Build Your Own

### Option A: MIT App Inventor (No Coding!)

**Best for: Custom branded app, no programming experience**

- **Website:** http://ai2.appinventor.mit.edu/
- **Cost:** Free
- **Coding:** Visual blocks (like Scratch)
- **Time:** 1-2 hours
- **License:** Your app is yours (any license)

**I'll create a template for you below!**

---

### Option B: Flutter BLE App

**Best for: Professional looking app**

- **Language:** Dart/Flutter
- **Time:** 4-6 hours
- **Skill:** Basic programming
- **Cost:** Free

**Template structure:**
```dart
dependencies:
  flutter_blue_plus: ^1.14.0  // BLE library
  
Features to implement:
- Scan for ESP32-SafeLock
- Connect button
- Password input field
- Lock/Unlock buttons
- Status display
```

---

### Option C: React Native BLE

**Best for: Cross-platform (Android + iOS)**

- **Language:** JavaScript/React
- **Time:** 4-6 hours
- **Skill:** Web development experience
- **Cost:** Free

**Template structure:**
```javascript
dependencies:
  react-native-ble-plx  // BLE library
  
Features to implement:
- Device scanner
- Connection manager
- Command sender
- Response display
```

---

## 🎯 MIT App Inventor Template (Step-by-Step)

### Complete App Design

I'll guide you through creating a custom app!

**Components Needed:**
1. BluetoothLE1 (BLE extension)
2. ListPicker (select device)
3. TextBox (password entry)
4. Buttons (Lock/Unlock)
5. Label (status display)

**Screen Layout:**
```
┌─────────────────────────────┐
│     Safe Lock Control       │
├─────────────────────────────┤
│                             │
│  [Select Device] ▼          │
│                             │
│  Password: [__________]     │
│                             │
│  [🔓 Unlock]  [🔒 Lock]     │
│                             │
│  [Toggle]    [Status]       │
│                             │
│  Status: Disconnected       │
│                             │
└─────────────────────────────┘
```

### MIT App Inventor Blocks (Pseudo-code)

```
WHEN ListPicker.Click:
  CALL BluetoothLE.StartScanning
  WAIT for devices
  SHOW list of devices with "ESP32" in name

WHEN Device Selected:
  CALL BluetoothLE.Connect(device)
  SET StatusLabel = "Connected"

WHEN UnlockButton.Click:
  GET password from TextBox
  SEND "PASS:" + password to BLE
  WAIT for response
  IF response contains "OK":
    SHOW "Unlocked!"
  ELSE:
    SHOW "Wrong password"

WHEN LockButton.Click:
  SEND "CLOSE" to BLE
  SHOW "Locked"

WHEN ToggleButton.Click:
  SEND "TOGGLE" to BLE

WHEN StatusButton.Click:
  SEND "STATUS" to BLE
  WAIT for response
  SHOW response in StatusLabel
```

### Detailed MIT App Inventor Guide

**Step 1: Create New Project**
1. Go to http://ai2.appinventor.mit.edu/
2. Sign in with Google
3. Create New Project: "SafeLockControl"

**Step 2: Add Components**

Drag these from Palette:
- Connectivity → BluetoothLE → Rename to "BLE"
- User Interface → ListPicker → Rename to "SelectDevice"
- User Interface → TextBox → Rename to "PasswordInput"
- User Interface → Button → Rename to "UnlockBtn" (change text to "🔓 Unlock")
- User Interface → Button → Rename to "LockBtn" (change text to "🔒 Lock")
- User Interface → Label → Rename to "StatusLabel"

**Step 3: Configure BLE Service**

You need to tell the app which BLE service to use:
- Service UUID: `6E400001-B5A3-F393-E0A9-E50E24DCCA9E`
- TX Characteristic: `6E400003-B5A3-F393-E0A9-E50E24DCCA9E`
- RX Characteristic: `6E400002-B5A3-F393-E0A9-E50E24DCCA9E`

**Step 4: Programming Blocks**

Switch to "Blocks" view and create these:

```
WHEN SelectDevice.Click:
  CALL BLE.StartScanning
  
WHEN BLE.DeviceFound:
  IF device_name contains "ESP32-SafeLock":
    ADD to SelectDevice list

WHEN SelectDevice.AfterSelection:
  CALL BLE.Connect(selected_device)

WHEN UnlockBtn.Click:
  SET command = "PASS:" + PasswordInput.Text
  CALL BLE.WriteStrings(service_uuid, rx_uuid, command)

WHEN LockBtn.Click:
  CALL BLE.WriteStrings(service_uuid, rx_uuid, "CLOSE")

WHEN BLE.StringsReceived:
  SET StatusLabel.Text = received_string
```

**Step 5: Build APK**
1. Build → Android App (.apk)
2. Download to phone
3. Install (enable "Install from unknown sources")
4. Done!

---

## 🚀 Quick Start Recommendations

### For Immediate Use (Today):
**Use nRF Connect** ✅
- Download from Play Store
- Works immediately
- No setup needed
- Professional features

### For Simple Control (This Weekend):
**Use Serial Bluetooth Terminal** ✅
- Easy to use
- Type commands directly
- No learning curve

### For Custom App (Next Week):
**Try MIT App Inventor** ✅
- No coding required
- Visual programming
- Custom branding
- 1-2 hours to build

### For Professional App (Next Month):
**Build Flutter App** ✅
- Beautiful UI
- Full control
- Professional result
- Shareable with others

---

## 📋 Comparison Table

| App | Open Source | Free | Easy | Custom | Professional |
|-----|-------------|------|------|--------|--------------|
| **nRF Connect** | ✅ | ✅ | ⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **Serial BT Terminal** | ✅ | ✅ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| **MIT App Inventor** | ✅ | ✅ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Flutter App** | ✅ | ✅ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **React Native** | ✅ | ✅ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 💾 Flutter Template (Basic Structure)

I'll create a basic Flutter app structure for you:

```dart
// pubspec.yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_blue_plus: ^1.14.0

// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

void main() => runApp(SafeLockApp());

class SafeLockApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Safe Lock Control',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: SafeLockHome(),
    );
  }
}

class SafeLockHome extends StatefulWidget {
  @override
  _SafeLockHomeState createState() => _SafeLockHomeState();
}

class _SafeLockHomeState extends State<SafeLockHome> {
  BluetoothDevice? device;
  BluetoothCharacteristic? txChar;
  String status = "Disconnected";
  TextEditingController passwordController = TextEditingController();

  void scanForDevices() async {
    FlutterBluePlus.startScan(timeout: Duration(seconds: 4));
    
    FlutterBluePlus.scanResults.listen((results) {
      for (ScanResult r in results) {
        if (r.device.name == "ESP32-SafeLock") {
          device = r.device;
          FlutterBluePlus.stopScan();
          connectToDevice();
        }
      }
    });
  }

  void connectToDevice() async {
    await device!.connect();
    setState(() => status = "Connected");
    
    // Discover services
    List<BluetoothService> services = await device!.discoverServices();
    for (var service in services) {
      for (var char in service.characteristics) {
        if (char.uuid.toString() == "6e400002-b5a3-f393-e0a9-e50e24dcca9e") {
          txChar = char;
        }
      }
    }
  }

  void sendCommand(String command) async {
    if (txChar != null) {
      await txChar!.write(command.codeUnits);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Safe Lock Control')),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            Text('Status: $status', style: TextStyle(fontSize: 18)),
            SizedBox(height: 20),
            
            ElevatedButton(
              onPressed: scanForDevices,
              child: Text('Connect to Safe'),
            ),
            
            SizedBox(height: 20),
            
            TextField(
              controller: passwordController,
              decoration: InputDecoration(labelText: 'Password'),
              obscureText: true,
            ),
            
            SizedBox(height: 20),
            
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () => sendCommand('PASS:${passwordController.text}'),
                  child: Text('🔓 Unlock'),
                ),
                ElevatedButton(
                  onPressed: () => sendCommand('CLOSE'),
                  child: Text('🔒 Lock'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 🎓 Summary & Recommendations

### Immediate Solution (Use Today):
1. **Download nRF Connect** (Play Store)
2. Connect to "ESP32-SafeLock"
3. Navigate to UART service
4. Send commands via RX characteristic

### Best For Beginners:
1. **Serial Bluetooth Terminal** (simplest)
2. Type commands directly
3. No configuration needed

### Best For Custom App:
1. **MIT App Inventor** (no coding)
2. Visual programming
3. Custom branding
4. Shareable APK

### Best For Developers:
1. **Flutter** (professional UI)
2. Full source control
3. Cross-platform
4. Play Store ready

---

## 📚 Additional Resources

**nRF Connect:**
- GitHub: https://github.com/NordicSemiconductor/Android-nRF-Connect
- Docs: https://developer.nordicsemi.com/

**Serial Bluetooth Terminal:**
- GitHub: https://github.com/kai-morich/SimpleBluetoothTerminal

**MIT App Inventor:**
- Website: http://ai2.appinventor.mit.edu/
- Tutorials: https://appinventor.mit.edu/explore/ai2/tutorials

**Flutter BLE:**
- Package: https://pub.dev/packages/flutter_blue_plus
- Tutorial: https://flutter.dev/docs/get-started/install

---

## ✅ Quick Decision Guide

**Choose based on your needs:**

| Your Need | Recommended Solution |
|-----------|---------------------|
| Test immediately | nRF Connect ⭐ |
| Simple daily use | Serial BT Terminal |
| Custom app, no coding | MIT App Inventor |
| Professional app | Flutter |
| Cross-platform | React Native |
| Share with family | MIT App Inventor APK |
| Publish on store | Flutter/React Native |

**My Top Pick: Start with nRF Connect, then build MIT App Inventor app later!**
