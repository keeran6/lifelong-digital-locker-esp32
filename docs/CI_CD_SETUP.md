# CI/CD Pipeline Setup Guide

## Overview

This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD). The pipeline automatically tests, validates, and packages code changes for the ESP32 Safe Locker project.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions Workflow                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Linting    │  │   Static     │  │   Unit Tests │     │
│  │   (pylint)   │  │   Analysis   │  │   (pytest)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                 │                 │              │
│         └─────────────────┴─────────────────┘              │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │  Hardware Tests │                       │
│                  │  (self-hosted)  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │  Build Package  │                       │
│                  └────────┬────────┘                       │
│                           │                                │
│                  ┌────────▼────────┐                       │
│                  │  Create Release │                       │
│                  │  (on tags)      │                       │
│                  └─────────────────┘                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Workflow Stages

### 1. Code Quality & Linting

**Runs on:** Every push and PR

**Tools:**
- **pylint**: Checks code quality and style for MicroPython code
- **black**: Verifies code formatting (optional)
- Configuration: `.pylintrc`

**How to run locally:**
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run pylint
pylint --rcfile=.pylintrc *.py

# Check formatting
black --check --line-length 100 *.py
```

### 2. Static Analysis

**Runs on:** Every push and PR

**Tools:**
- **bandit**: Security vulnerability scanner
- **vulture**: Dead code detector

**How to run locally:**
```bash
# Security scan
bandit -r . -ll

# Dead code detection
vulture *.py --min-confidence 80
```

### 3. Unit Tests

**Runs on:** Every push and PR

**Framework:** pytest with mocks for MicroPython modules

**Test files:**
- `tests/test_ble_advertising.py`
- `tests/test_ble_simple_peripheral.py`

**How to run locally:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run specific test file
pytest tests/test_ble_advertising.py -v

# Run tests with specific marker
pytest -m unit -v
```

### 4. Hardware Testing

**Runs on:** Self-hosted runner with ESP32 connected

**Requirements:**
- Physical ESP32 device connected via USB
- Self-hosted GitHub Actions runner
- Tools: esptool, mpremote, ampy

**Test script:** `scripts/hardware_test.sh`

**How to run locally:**
```bash
# Make script executable
chmod +x scripts/hardware_test.sh

# Run hardware tests (specify USB port)
./scripts/hardware_test.sh /dev/ttyUSB0

# Check results
ls -la test-results/
```

**Hardware test stages:**
1. Device detection and connection test
2. Upload files to ESP32
3. Syntax validation on device
4. BLE module import and function tests
5. Generate test report

### 5. Build & Package

**Runs on:** Push to main or release

**Outputs:**
- Compressed archive: `esp32-safe-locker-{version}.tar.gz`
- Deployment script: `deploy.sh`
- Checksums: `checksums.txt`

**Manual packaging:**
```bash
# Create package
tar -czf esp32-safe-locker.tar.gz \
  digital_safe_locker_ultimate.py \
  digital_safe_locker_T8_battery_optimized.py \
  ble_simple_peripheral.py \
  ble_advertising.py \
  README.md
```

### 6. Release Creation

**Trigger:** Git tag push (e.g., `v1.0.0`)

**Process:**
1. Builds deployment package
2. Generates release notes from commits
3. Uploads artifacts to GitHub Release
4. Creates checksums

**Creating a release:**
```bash
# Tag a release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# The CI/CD pipeline will automatically:
# - Build the package
# - Generate release notes
# - Create GitHub release
# - Upload artifacts
```

## Setting Up Self-Hosted Runner for Hardware Tests

### Prerequisites

1. Computer with ESP32 connected via USB
2. Python 3.11+ installed
3. USB permissions configured

### Installation Steps

#### 1. Install GitHub Actions Runner

```bash
# Create runner directory
mkdir -p ~/actions-runner && cd ~/actions-runner

# Download latest runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (get token from GitHub repo Settings > Actions > Runners)
./config.sh --url https://github.com/YOUR_USERNAME/lifelong-digital-locker-esp32 \
  --token YOUR_TOKEN \
  --labels self-hosted,esp32

# Install as service (optional)
sudo ./svc.sh install
sudo ./svc.sh start
```

#### 2. Configure USB Permissions

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Create udev rule for ESP32
sudo tee /etc/udev/rules.d/99-esp32.rules << EOF
SUBSYSTEMS=="usb", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", MODE="0666"
SUBSYSTEMS=="usb", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE="0666"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

# Logout and login for group changes to take effect
```

#### 3. Install ESP32 Tools

```bash
# Install Python tools
pip install esptool adafruit-ampy mpremote pyserial

# Verify installation
esptool.py version
mpremote --help

# Test ESP32 connection
mpremote connect /dev/ttyUSB0 exec "print('Hello from ESP32')"
```

#### 4. Verify Setup

```bash
# Check USB devices
ls -la /dev/ttyUSB*

# Test device connection
esptool.py --port /dev/ttyUSB0 chip_id

# Run hardware test script manually
cd ~/lifelong-digital-locker-esp32
./scripts/hardware_test.sh /dev/ttyUSB0
```

## Workflow Triggers

### Automatic Triggers

| Event | Branches | Actions |
|-------|----------|---------|
| Push | `main`, `claude/**` | Lint, Test, Build |
| Pull Request | `main` | Lint, Test |
| Release | Tag `v*` | Full pipeline + Release |

### Manual Trigger

```bash
# Trigger workflow manually via GitHub web interface
# Repository → Actions → Select workflow → Run workflow
```

## Environment Variables

Configure in GitHub Settings → Secrets and variables → Actions:

| Variable | Description | Required |
|----------|-------------|----------|
| `ESP32_PORT` | USB port for ESP32 | No (default: /dev/ttyUSB0) |
| `GITHUB_TOKEN` | Auto-provided by GitHub | Yes (automatic) |

## Artifacts & Reports

### Artifacts Generated

1. **Build artifacts**: Packaged releases
2. **Test results**: Hardware test logs
3. **Coverage reports**: Code coverage HTML
4. **Checksums**: SHA256 verification

### Accessing Artifacts

```bash
# Via GitHub Actions UI
# Repository → Actions → Select workflow run → Artifacts

# Download using GitHub CLI
gh run download RUN_ID

# List recent artifacts
gh api repos/:owner/:repo/actions/artifacts
```

## Deployment

### Automated Deployment (from CI)

The `deploy.sh` script is included in release packages:

```bash
# Extract release package
tar -xzf esp32-safe-locker-v1.0.0.tar.gz
cd esp32-safe-locker/

# Deploy to ESP32
chmod +x deploy.sh
./deploy.sh /dev/ttyUSB0 ultimate

# Options: ultimate | battery | enhanced
```

### Manual Deployment

```bash
# Using mpremote
mpremote connect /dev/ttyUSB0 fs cp ble_advertising.py :
mpremote connect /dev/ttyUSB0 fs cp ble_simple_peripheral.py :
mpremote connect /dev/ttyUSB0 fs cp digital_safe_locker_ultimate.py :main.py

# Using ampy
ampy --port /dev/ttyUSB0 put ble_advertising.py
ampy --port /dev/ttyUSB0 put ble_simple_peripheral.py
ampy --port /dev/ttyUSB0 put digital_safe_locker_ultimate.py main.py
```

## Troubleshooting

### Common Issues

#### 1. Hardware Tests Fail - Device Not Found

**Problem:** ESP32 not detected on expected port

**Solution:**
```bash
# Find ESP32 device
ls -la /dev/tty* | grep -E "(USB|ACM)"

# Check permissions
groups  # Should include 'dialout'

# Test connection
esptool.py --port /dev/ttyUSB0 chip_id
```

#### 2. Pylint Errors

**Problem:** Too many linting errors

**Solution:**
```bash
# Adjust .pylintrc to disable specific checks
# Or run with higher tolerance:
pylint --fail-under=7.0 *.py
```

#### 3. Import Errors in Tests

**Problem:** MicroPython modules not found

**Solution:**
```bash
# Tests use mocks - check test files have proper fixtures
# Ensure pytest is running from project root
pytest tests/ -v
```

#### 4. Self-Hosted Runner Offline

**Problem:** Hardware tests skipped

**Solution:**
```bash
# Check runner status
cd ~/actions-runner
./run.sh

# Or restart service
sudo ./svc.sh restart

# Check logs
journalctl -u actions.runner.* -f
```

## Best Practices

### For Contributors

1. **Run tests locally before pushing:**
   ```bash
   pytest tests/ -v
   pylint *.py
   ```

2. **Keep commits atomic** - one feature/fix per commit

3. **Write meaningful commit messages:**
   ```
   Fix LoadProhibited crash in BLE send()

   - Send response before blocking delay
   - Add connection validation
   - Update tests
   ```

4. **Add tests for new features:**
   - Unit tests with mocks
   - Hardware test cases if applicable

### For Releases

1. **Version numbering:** Use semantic versioning (v1.2.3)
2. **Tag format:** `v{major}.{minor}.{patch}`
3. **Release notes:** Auto-generated from commits
4. **Testing:** Ensure all tests pass before tagging

## CI/CD Metrics

Monitor pipeline health:

- **Build success rate:** Target >95%
- **Test coverage:** Target >70%
- **Build time:** Target <10 minutes
- **Hardware test success:** Target >90%

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [MicroPython Documentation](https://docs.micropython.org/)
- [ESP32 Testing Guide](https://github.com/micropython/micropython/wiki/ESP32-debugging)
- [pytest Documentation](https://docs.pytest.org/)
- [pylint Documentation](https://pylint.pycqa.org/)

## Support

For CI/CD issues:
1. Check workflow logs in GitHub Actions tab
2. Review test results and artifacts
3. Consult this documentation
4. Open an issue with logs and error details
