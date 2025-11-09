# Password Management Guide - Enhanced Version

## 🎯 Overview

The **enhanced version** adds full password management:

✅ **Change password via keypad**  
✅ **Change password via BLE app**  
✅ **Persistent storage** (survives reboot)  
✅ **Admin password** for factory reset  
✅ **Interchangeable authentication** (keypad ↔ BLE)

---

## 📦 Files

**For ESP32 Pico:**
- **[digital_safe_locker_enhanced.py](computer:///mnt/user-data/outputs/digital_safe_locker_enhanced.py)** - Enhanced version

**For LILYGO T8:**
- **[digital_safe_locker_T8_enhanced.py](computer:///mnt/user-data/outputs/digital_safe_locker_T8_enhanced.py)** - T8 enhanced version

---

## 🔑 How It Works

### 1. Password Storage

**File-based storage:**
```python
# Stored in: password.json
{
  "password": "1234"
}
```

**Features:**
- Survives reboot/power cycle
- Automatically saved on change
- Falls back to default if corrupted

### 2. Two Passwords

**User Password:**
- Default: `"1234"`
- Used to: Unlock safe
- Changed by: User (keypad or BLE)

**Admin Password:**
- Default: `"9999"`
- Used to: Factory reset
- Changed in: Code only (for security)

---

## 🎮 Keypad Controls

### Normal Mode (Unlock)

| Key | Action |
|-----|--------|
| **0-9** | Enter password digits |
| **# or C** | Submit & unlock |
| **\*** | Clear entry |
| **A** | Enter password change mode |
| **B** then **#** | Admin reset (enter admin password first) |

### Password Change Mode

**Step 1: Enter old password**
```
1. Press [A] to enter change mode
2. Enter current password: [1][2][3][4]
3. Press [#] to confirm
```

**Step 2: Enter new password**
```
1. Enter new password: [5][6][7][8]
2. Press [#] to confirm
```

**Step 3: Confirm new password**
```
1. Re-enter new password: [5][6][7][8]
2. Press [#] to save
3. LED blinks 3x = SUCCESS! 🎉
```

**Cancel at any time:**
```
Press [*] or [A] to cancel and return to normal mode
```

---

## 📱 BLE Commands

### Unlock with Password
```
Command: PASS:1234
Response: OK:UNLOCKED
```

### Change Password
```
Command: CHANGE:oldpass:newpass
Example: CHANGE:1234:5678

Responses:
- OK:PASSWORD_CHANGED
- ERROR:WRONG_OLD_PASSWORD
- ERROR:PASSWORD_TOO_SHORT
- ERROR:INVALID_FORMAT
```

### Factory Reset (Admin)
```
Command: RESET:9999
Response: OK:PASSWORD_RESET

Password is reset to: 1234
```

### Other Commands (Same as Before)
```
OPEN          - Open lock
CLOSE         - Close lock
TOGGLE        - Toggle lock
STATUS        - Get current state
INFO          - Board information (T8 only)
```

---

## 🔄 Complete Example Workflows

### Example 1: Change Password via Keypad

**Scenario:** Change password from `1234` to `5678`

```
1. Press [A]
   → "Password change mode activated"
   → "Enter OLD password:"

2. Enter [1] [2] [3] [4]
   → "Password: ****"

3. Press [#]
   → "✅ Old password correct. Enter NEW password:"
   → LED blinks 2x

4. Enter [5] [6] [7] [8]
   → "Password: ****"

5. Press [#]
   → "✅ New password set. CONFIRM new password:"
   → LED blinks 2x

6. Enter [5] [6] [7] [8] again
   → "Password: ****"

7. Press [#]
   → "🎉 Password changed successfully!"
   → LED blinks 3x
   → Password saved to storage

8. Test: Enter [5] [6] [7] [8] [#]
   → Lock opens! ✅
```

### Example 2: Change Password via BLE

**Using nRF Connect or Serial BT Terminal:**

```
1. Connect to ESP32-SafeLock or T8-SafeLock

2. Send command:
   CHANGE:1234:5678

3. Receive response:
   OK:PASSWORD_CHANGED

4. Test with new password:
   PASS:5678

5. Response:
   OK:UNLOCKED
```

### Example 3: Admin Factory Reset

**Via Keypad:**
```
1. Enter admin password: [9] [9] [9] [9]
2. Press [B] (admin reset)
3. Press [#] to confirm
4. LED blinks rapidly
5. Password reset to: 1234
```

**Via BLE:**
```
1. Send: RESET:9999
2. Response: OK:PASSWORD_RESET
3. Password is now: 1234
```

---

## 🔒 Security Features

### 1. Old Password Required
Can't change password without knowing current password

### 2. Password Confirmation
Must enter new password twice to prevent typos

### 3. Failed Attempt Lockout
- 3 wrong attempts → 30 second lockout
- Applies to both keypad and BLE
- Counter resets on correct password

### 4. Admin Protection
Factory reset requires separate admin password

### 5. Persistent Storage
Password survives:
- Power loss
- Reboot
- Code updates (unless you delete password.json)

---

## 📊 Password Rules

**Minimum Length:** 4 digits  
**Maximum Length:** 8 digits  
**Allowed Characters:** 0-9 (numbers only)  
**Storage:** Persistent (password.json file)

**Recommendations:**
- Use 6+ digits for better security
- Don't use obvious patterns (1234, 0000)
- Change admin password in code
- Keep a backup of your password!

---

## 🐛 Troubleshooting

### Password Change Not Working

**Issue:** Can't change password
- ✓ Make sure you enter OLD password correctly first
- ✓ New password must be 4+ digits
- ✓ Both new password entries must match

### Password Not Saving

**Issue:** Password resets after reboot
- ✓ Check password.json file exists
- ✓ Flash memory may be full (delete unused files)
- ✓ Check for file system errors

**Manual fix:**
```python
# Connect via serial/Thonny
import json
with open('password.json', 'w') as f:
    json.dump({'password': '1234'}, f)
```

### Forgot Password

**Solution 1: Admin reset via keypad**
```
Enter [9][9][9][9] then press [B] then [#]
Password resets to: 1234
```

**Solution 2: Admin reset via BLE**
```
Send: RESET:9999
Password resets to: 1234
```

**Solution 3: Delete password file**
```python
# Connect via serial/Thonny
import os
os.remove('password.json')
# Then reboot - will use default: 1234
```

**Solution 4: Re-upload code**
```
Upload code again via Thonny or ampy
Default password: 1234
```

### Forgot Admin Password

**Issue:** Can't reset to default

**Solution:** Edit code and re-upload
```python
# In the code file, change:
ADMIN_PASSWORD = "9999"  # Change to something you remember
```

---

## 🎨 LED Feedback (T8 Only)

LILYGO T8 version has visual feedback:

**LED Patterns:**
- **1 short flash** - Key pressed
- **2 blinks** - Step successful (old password correct, new password set)
- **3 blinks (slow)** - Password changed successfully!
- **5 fast blinks** - Error (wrong password, mismatch, etc.)
- **Rapid blinking** - Admin reset in progress
- **Continuous blink (30s)** - Failed attempt lockout

---

## 🔄 Migration from Basic Version

**If you're currently using basic version:**

### Step 1: Backup Current Setup
Note your current password if you changed it

### Step 2: Upload Enhanced Version
```bash
# For Pico
ampy --port /dev/ttyUSB0 put digital_safe_locker_enhanced.py main.py

# For T8
ampy --port /dev/ttyUSB0 put digital_safe_locker_T8_enhanced.py main.py
```

### Step 3: First Boot
- Default password is: 1234
- Change it via keypad [A] or BLE CHANGE command

### Step 4: Test Everything
- Test keypad unlock
- Test BLE unlock
- Test password change
- Test admin reset

---

## 💡 Advanced Tips

### 1. Change Admin Password
```python
# Edit in code before uploading:
ADMIN_PASSWORD = "123456"  # Use 6+ digits
```

### 2. Change Default Password
```python
# Edit in code:
DEFAULT_PASSWORD = "0000"  # Your preferred default
```

### 3. Increase Password Length Limit
```python
# In process_keypad_input function, change:
if len(entered_password) < 8:  # Change 8 to higher number
```

### 4. Disable Admin Reset (High Security)
```python
# Comment out admin reset code in process_keypad_input:
# elif key == 'B':  # Admin reset
#     ... (comment out entire block)
```

### 5. Log Password Changes
```python
# Add to save_password function:
with open('password_log.txt', 'a') as f:
    f.write(f"{time.time()}: Password changed\n")
```

---

## 📱 MIT App Inventor Integration

To add password change to your custom app:

**Add Components:**
1. TextBox: `OldPasswordInput`
2. TextBox: `NewPasswordInput`
3. Button: `ChangePasswordButton`

**Add Blocks:**
```
WHEN ChangePasswordButton.Click:
  SET command TO JOIN("CHANGE:", OldPasswordInput.Text, ":", NewPasswordInput.Text)
  CALL BLE.WriteStrings(service_uuid, char_uuid, command)

WHEN BLE.StringsReceived:
  IF stringValues CONTAINS "OK:PASSWORD_CHANGED":
    SHOW "Password changed successfully!"
  ELSE IF stringValues CONTAINS "ERROR":
    SHOW "Error: Check old password"
```

---

## ✅ Summary

**Enhanced Version Features:**

| Feature | Keypad | BLE App | Both |
|---------|--------|---------|------|
| **Unlock** | ✅ | ✅ | ✅ |
| **Change Password** | ✅ | ✅ | ✅ |
| **Factory Reset** | ✅ Admin | ✅ Admin | ✅ |
| **Persistent Storage** | ✅ | ✅ | ✅ |
| **Interchangeable** | - | - | ✅ |

**Authentication:**
- Set password via keypad → Use on keypad ✅
- Set password via keypad → Use on BLE ✅
- Set password via BLE → Use on keypad ✅
- Set password via BLE → Use on BLE ✅

**Everything works interchangeably!** 🎉

---

## 🎯 Quick Command Reference

### Keypad
```
Unlock:    [password] [#]
Change:    [A] → [old] [#] → [new] [#] → [new] [#]
Clear:     [*]
Reset:     [admin] [B] [#]
```

### BLE
```
Unlock:    PASS:1234
Change:    CHANGE:old:new
Reset:     RESET:admin
Status:    STATUS
```

---

**You now have full password management! 🎉**
