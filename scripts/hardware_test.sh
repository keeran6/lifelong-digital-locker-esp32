#!/bin/bash
# ESP32 Hardware Testing Script
# This script uploads and tests code on a physical ESP32 device

set -e

PORT="${1:-/dev/ttyUSB0}"
TIMEOUT=30
TEST_RESULTS_DIR="test-results"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=========================================="
echo "ESP32 Hardware Testing"
echo "=========================================="
echo "Port: $PORT"
echo "Timestamp: $TIMESTAMP"
echo ""

# Create test results directory
mkdir -p "$TEST_RESULTS_DIR"

# Function to check if port exists
check_port() {
    if [ ! -e "$PORT" ]; then
        echo "❌ Error: ESP32 not found on $PORT"
        echo "Available ports:"
        ls -la /dev/tty* 2>/dev/null | grep -E "(USB|ACM)" || echo "No USB devices found"
        exit 1
    fi
    echo "✅ ESP32 device found on $PORT"
}

# Function to test serial connection
test_connection() {
    echo ""
    echo "Testing serial connection..."

    if command -v mpremote &> /dev/null; then
        timeout $TIMEOUT mpremote connect $PORT exec "print('Connection OK')" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ Serial connection successful"
            return 0
        fi
    fi

    echo "❌ Serial connection failed"
    return 1
}

# Function to get ESP32 info
get_device_info() {
    echo ""
    echo "Getting device information..."

    if command -v esptool.py &> /dev/null; then
        esptool.py --port $PORT chip_id 2>&1 | tee "$TEST_RESULTS_DIR/device_info_$TIMESTAMP.txt"
    fi
}

# Function to upload test file
upload_files() {
    echo ""
    echo "Uploading files to ESP32..."

    local files=(
        "ble_advertising.py"
        "ble_simple_peripheral.py"
        "digital_safe_locker_T8_battery_optimized.py"
    )

    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            echo "  Uploading $file..."
            if command -v mpremote &> /dev/null; then
                timeout $TIMEOUT mpremote connect $PORT fs cp "$file" : || {
                    echo "❌ Failed to upload $file"
                    return 1
                }
            else
                echo "⚠️  mpremote not found, skipping upload"
                return 1
            fi
        fi
    done

    echo "✅ All files uploaded successfully"
    return 0
}

# Function to run basic syntax check
run_syntax_check() {
    echo ""
    echo "Running syntax check..."

    cat > /tmp/esp32_syntax_test.py << 'EOF'
import sys
import os

files_to_check = [
    'ble_advertising.py',
    'ble_simple_peripheral.py',
    'digital_safe_locker_T8_battery_optimized.py'
]

errors = []
for filename in files_to_check:
    try:
        if filename in os.listdir():
            with open(filename, 'r') as f:
                code = f.read()
                compile(code, filename, 'exec')
                print(f'✅ {filename}: OK')
    except SyntaxError as e:
        errors.append(f'{filename}: {e}')
        print(f'❌ {filename}: {e}')
    except Exception as e:
        print(f'⚠️  {filename}: {e}')

if errors:
    print('SYNTAX_CHECK:FAIL')
    sys.exit(1)
else:
    print('SYNTAX_CHECK:PASS')
    sys.exit(0)
EOF

    if command -v mpremote &> /dev/null; then
        timeout $TIMEOUT mpremote connect $PORT fs cp /tmp/esp32_syntax_test.py : || return 1
        timeout $TIMEOUT mpremote connect $PORT exec "exec(open('esp32_syntax_test.py').read())" 2>&1 | tee "$TEST_RESULTS_DIR/syntax_check_$TIMESTAMP.txt"

        if grep -q "SYNTAX_CHECK:PASS" "$TEST_RESULTS_DIR/syntax_check_$TIMESTAMP.txt"; then
            echo "✅ Syntax check passed"
            return 0
        else
            echo "❌ Syntax check failed"
            return 1
        fi
    fi

    return 1
}

# Function to run BLE module tests
run_ble_tests() {
    echo ""
    echo "Running BLE module tests..."

    cat > /tmp/esp32_ble_test.py << 'EOF'
import sys

print("Testing BLE modules...")
errors = []

try:
    print("  Importing ble_advertising...")
    import ble_advertising
    print("  ✅ ble_advertising imported")
except Exception as e:
    errors.append(f"ble_advertising: {e}")
    print(f"  ❌ ble_advertising: {e}")

try:
    print("  Importing ble_simple_peripheral...")
    import ble_simple_peripheral
    print("  ✅ ble_simple_peripheral imported")
except Exception as e:
    errors.append(f"ble_simple_peripheral: {e}")
    print(f"  ❌ ble_simple_peripheral: {e}")

try:
    print("  Testing advertising_payload function...")
    payload = ble_advertising.advertising_payload(name="TEST")
    if len(payload) > 0 and len(payload) <= 31:
        print(f"  ✅ Payload generated: {len(payload)} bytes")
    else:
        errors.append(f"Invalid payload length: {len(payload)}")
        print(f"  ❌ Invalid payload length: {len(payload)}")
except Exception as e:
    errors.append(f"advertising_payload: {e}")
    print(f"  ❌ advertising_payload: {e}")

if errors:
    print("BLE_TEST:FAIL")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("BLE_TEST:PASS")
    sys.exit(0)
EOF

    if command -v mpremote &> /dev/null; then
        timeout $TIMEOUT mpremote connect $PORT fs cp /tmp/esp32_ble_test.py : || return 1
        timeout $TIMEOUT mpremote connect $PORT exec "exec(open('esp32_ble_test.py').read())" 2>&1 | tee "$TEST_RESULTS_DIR/ble_test_$TIMESTAMP.txt"

        if grep -q "BLE_TEST:PASS" "$TEST_RESULTS_DIR/ble_test_$TIMESTAMP.txt"; then
            echo "✅ BLE tests passed"
            return 0
        else
            echo "❌ BLE tests failed"
            return 1
        fi
    fi

    return 1
}

# Function to generate test report
generate_report() {
    local exit_code=$1

    echo ""
    echo "=========================================="
    echo "Test Results Summary"
    echo "=========================================="

    cat > "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt" << EOF
ESP32 Hardware Test Results
Timestamp: $TIMESTAMP
Port: $PORT

Test Results:
EOF

    if [ $exit_code -eq 0 ]; then
        echo "Overall Status: ✅ PASS" | tee -a "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt"
    else
        echo "Overall Status: ❌ FAIL" | tee -a "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt"
    fi

    echo "" | tee -a "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt"
    echo "Test artifacts saved to: $TEST_RESULTS_DIR/" | tee -a "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt"

    ls -lh "$TEST_RESULTS_DIR/" | tee -a "$TEST_RESULTS_DIR/summary_$TIMESTAMP.txt"
}

# Main execution
main() {
    local exit_code=0

    check_port || exit_code=1

    if [ $exit_code -eq 0 ]; then
        test_connection || exit_code=1
    fi

    if [ $exit_code -eq 0 ]; then
        get_device_info
    fi

    if [ $exit_code -eq 0 ]; then
        upload_files || exit_code=1
    fi

    if [ $exit_code -eq 0 ]; then
        run_syntax_check || exit_code=1
    fi

    if [ $exit_code -eq 0 ]; then
        run_ble_tests || exit_code=1
    fi

    generate_report $exit_code

    exit $exit_code
}

# Run main function
main
