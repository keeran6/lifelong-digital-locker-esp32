# CI/CD Quick Start Guide

## Local Development Setup

### 1. Install Development Tools

```bash
# Install all development dependencies
pip install -r requirements-dev.txt

# Verify installation
pylint --version
pytest --version
esptool.py version
```

### 2. Run Pre-Commit Checks

```bash
# Run all checks before committing
make check  # If Makefile exists

# Or run manually:
pylint *.py
pytest tests/ -v
black --check *.py
```

### 3. Test on Hardware

```bash
# Connect ESP32 via USB
# Find device
ls /dev/ttyUSB*

# Run hardware tests
./scripts/hardware_test.sh /dev/ttyUSB0

# View results
cat test-results/summary_*.txt
```

## GitHub Actions Workflows

### Workflow Overview

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **ci.yml** | Push, PR | Full CI pipeline |
| *(future)* deploy.yml | Tag | Deployment |
| *(future)* nightly.yml | Schedule | Nightly tests |

### Current CI Pipeline (ci.yml)

```yaml
Jobs:
  1. lint           ✓ Code quality checks
  2. static-analysis ✓ Security & dead code
  3. unit-tests     ✓ Pytest with coverage
  4. hardware-test  ⚡ Requires self-hosted runner
  5. build-package  📦 Creates releases
  6. release-notes  📝 Auto-generates changelog
```

## Common Commands

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html

# Run specific test
pytest tests/test_ble_advertising.py::test_name -v

# Run hardware tests
./scripts/hardware_test.sh /dev/ttyUSB0
```

### Linting

```bash
# Check code quality
pylint *.py

# Auto-format code
black *.py --line-length 100

# Security scan
bandit -r . -ll

# Dead code detection
vulture *.py
```

### Deployment

```bash
# Deploy to ESP32
./dist/deploy.sh /dev/ttyUSB0 ultimate

# Or manually with mpremote
mpremote connect /dev/ttyUSB0 fs cp file.py :
```

## Creating a Release

### Step 1: Prepare

```bash
# Ensure all tests pass
pytest tests/ -v
./scripts/hardware_test.sh /dev/ttyUSB0

# Commit all changes
git add .
git commit -m "Prepare release v1.0.0"
git push
```

### Step 2: Tag Release

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- Added deep sleep support
- Fixed BLE crash issues
- Improved battery life

Bug fixes:
- Fixed wake configuration
- Corrected pin levels
"

# Push tag to trigger release
git push origin v1.0.0
```

### Step 3: Verify

1. Go to GitHub Actions tab
2. Watch the pipeline run
3. Check for green checkmarks ✓
4. Review the created release under Releases

## Self-Hosted Runner (Hardware Tests)

### Quick Setup

```bash
# 1. Download runner
mkdir ~/actions-runner && cd ~/actions-runner
curl -L -o runner.tar.gz \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf runner.tar.gz

# 2. Configure (get token from repo Settings > Actions)
./config.sh --url https://github.com/USER/REPO --token TOKEN

# 3. Start runner
./run.sh
# Or install as service:
sudo ./svc.sh install && sudo ./svc.sh start
```

### USB Permissions

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Create udev rule
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", MODE="0666"' | \
  sudo tee /etc/udev/rules.d/99-esp32.rules

# Reload
sudo udevadm control --reload-rules
```

### Verify Setup

```bash
# Check runner status
cd ~/actions-runner && ./run.sh

# Test ESP32 connection
esptool.py --port /dev/ttyUSB0 chip_id

# Run test script
cd /path/to/repo
./scripts/hardware_test.sh /dev/ttyUSB0
```

## Troubleshooting

### Tests Failing

```bash
# Check pytest output
pytest tests/ -v -s

# Run with debugging
pytest tests/ -v --pdb

# Check mocks are working
pytest tests/ -v --setup-show
```

### Hardware Test Issues

```bash
# Device not found?
ls -la /dev/tty* | grep USB

# Permission denied?
sudo chmod 666 /dev/ttyUSB0
# Or add to dialout group (permanent)

# Connection timeout?
# - Check USB cable
# - Press reset button on ESP32
# - Try different USB port
```

### CI Pipeline Stuck

```bash
# Check workflow status
gh run list

# View specific run
gh run view RUN_ID

# Cancel stuck run
gh run cancel RUN_ID

# Re-run failed jobs
gh run rerun RUN_ID --failed
```

### Self-Hosted Runner Offline

```bash
# Check runner service
sudo systemctl status actions.runner.*

# Restart runner
cd ~/actions-runner
sudo ./svc.sh restart

# View logs
sudo journalctl -u actions.runner.* -f
```

## GitHub CLI Commands

```bash
# Install GitHub CLI
# See: https://cli.github.com/

# List workflow runs
gh run list

# Watch current run
gh run watch

# View run details
gh run view

# Download artifacts
gh run download RUN_ID

# List releases
gh release list

# View release
gh release view v1.0.0
```

## Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run tests before commit

echo "Running pre-commit checks..."

# Run pylint
echo "Checking code quality..."
pylint *.py || exit 1

# Run tests
echo "Running tests..."
pytest tests/ -v || exit 1

echo "✓ All checks passed!"
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Makefile (Optional)

Create `Makefile`:

```makefile
.PHONY: test lint check format clean hardware-test

test:
	pytest tests/ -v

lint:
	pylint *.py

format:
	black *.py --line-length 100

check: lint test

hardware-test:
	./scripts/hardware_test.sh /dev/ttyUSB0

clean:
	rm -rf test-results/ htmlcov/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

install:
	pip install -r requirements-dev.txt

help:
	@echo "Available commands:"
	@echo "  make test          - Run unit tests"
	@echo "  make lint          - Run code quality checks"
	@echo "  make format        - Format code with black"
	@echo "  make check         - Run lint + test"
	@echo "  make hardware-test - Test on ESP32"
	@echo "  make clean         - Remove generated files"
	@echo "  make install       - Install dependencies"
```

## Environment Variables

### Local Development

```bash
# .env file (not committed)
ESP32_PORT=/dev/ttyUSB0
PYTHON_VERSION=3.11
```

### GitHub Secrets

Set in: Repository Settings → Secrets and variables → Actions

```
# Optional secrets (if needed)
ESP32_WIFI_SSID=your_wifi
ESP32_WIFI_PASSWORD=your_password
```

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│                   CI/CD QUICK REFERENCE                 │
├─────────────────────────────────────────────────────────┤
│ Run Tests:     pytest tests/ -v                         │
│ Lint Code:     pylint *.py                              │
│ Format Code:   black *.py                               │
│ HW Test:       ./scripts/hardware_test.sh /dev/ttyUSB0  │
│ Create Tag:    git tag -a v1.0.0 -m "Release"           │
│ Push Tag:      git push origin v1.0.0                   │
│ View Runs:     gh run list                              │
│ Download:      gh run download RUN_ID                   │
└─────────────────────────────────────────────────────────┘
```

## Next Steps

1. ✓ Read full documentation: `docs/CI_CD_SETUP.md`
2. ✓ Set up self-hosted runner (for hardware tests)
3. ✓ Configure GitHub repository settings
4. ✓ Run first pipeline
5. ✓ Create first release

## Support & Resources

- **Documentation**: `docs/CI_CD_SETUP.md`
- **GitHub Actions**: Repository → Actions tab
- **Issues**: Repository → Issues tab
- **Releases**: Repository → Releases tab
