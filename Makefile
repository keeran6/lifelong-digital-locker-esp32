.PHONY: help test lint format check hardware-test clean install deploy

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := pip3
PYTEST := pytest
PYLINT := pylint
BLACK := black
ESP32_PORT ?= /dev/ttyUSB0
VERSION := ultimate

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)ESP32 Safe Locker - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Examples:$(NC)"
	@echo "  make test              # Run all unit tests"
	@echo "  make check             # Run linting + tests"
	@echo "  make hardware-test     # Test on connected ESP32"
	@echo "  make deploy            # Deploy to ESP32"

install: ## Install development dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

test: ## Run unit tests
	@echo "$(BLUE)Running unit tests...$(NC)"
	$(PYTEST) tests/ -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-cov: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	$(PYTEST) tests/ -v --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated: htmlcov/index.html$(NC)"

test-watch: ## Run tests in watch mode
	@echo "$(BLUE)Running tests in watch mode...$(NC)"
	$(PYTEST) tests/ -v --looponfail

lint: ## Run code quality checks
	@echo "$(BLUE)Running pylint...$(NC)"
	$(PYLINT) --rcfile=.pylintrc *.py || true
	@echo "$(GREEN)✓ Linting completed$(NC)"

lint-strict: ## Run pylint with strict mode (must pass)
	@echo "$(BLUE)Running strict pylint...$(NC)"
	$(PYLINT) --rcfile=.pylintrc *.py

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	$(BLACK) *.py --line-length 100
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting without modifying
	@echo "$(BLUE)Checking code format...$(NC)"
	$(BLACK) --check --line-length 100 *.py
	@echo "$(GREEN)✓ Format check passed$(NC)"

security: ## Run security checks
	@echo "$(BLUE)Running security scan...$(NC)"
	bandit -r . -ll || true
	@echo "$(GREEN)✓ Security scan completed$(NC)"

deadcode: ## Check for dead code
	@echo "$(BLUE)Checking for dead code...$(NC)"
	vulture *.py --min-confidence 80 || true
	@echo "$(GREEN)✓ Dead code check completed$(NC)"

check: lint test ## Run all quality checks (lint + test)
	@echo "$(GREEN)✓ All checks passed!$(NC)"

hardware-test: ## Run hardware tests on connected ESP32
	@echo "$(BLUE)Running hardware tests on $(ESP32_PORT)...$(NC)"
	@if [ ! -e "$(ESP32_PORT)" ]; then \
		echo "$(RED)✗ ESP32 not found on $(ESP32_PORT)$(NC)"; \
		echo "Available ports:"; \
		ls -la /dev/tty* 2>/dev/null | grep -E "(USB|ACM)" || echo "No USB devices found"; \
		exit 1; \
	fi
	chmod +x scripts/hardware_test.sh
	./scripts/hardware_test.sh $(ESP32_PORT)
	@echo "$(GREEN)✓ Hardware tests completed$(NC)"
	@echo "Results: test-results/"

deploy: ## Deploy code to ESP32 (use VERSION=ultimate|battery|enhanced)
	@echo "$(BLUE)Deploying $(VERSION) version to $(ESP32_PORT)...$(NC)"
	@if [ ! -e "$(ESP32_PORT)" ]; then \
		echo "$(RED)✗ ESP32 not found on $(ESP32_PORT)$(NC)"; \
		exit 1; \
	fi
	@echo "Uploading BLE modules..."
	mpremote connect $(ESP32_PORT) fs cp ble_advertising.py : || exit 1
	mpremote connect $(ESP32_PORT) fs cp ble_simple_peripheral.py : || exit 1
	@if [ "$(VERSION)" = "ultimate" ]; then \
		echo "Uploading ultimate version..."; \
		mpremote connect $(ESP32_PORT) fs cp digital_safe_locker_ultimate.py :main.py; \
	elif [ "$(VERSION)" = "battery" ]; then \
		echo "Uploading battery optimized version..."; \
		mpremote connect $(ESP32_PORT) fs cp digital_safe_locker_T8_battery_optimized.py :main.py; \
	elif [ "$(VERSION)" = "enhanced" ]; then \
		echo "Uploading enhanced version..."; \
		mpremote connect $(ESP32_PORT) fs cp digital_safe_locker_T8_enhanced.py :main.py; \
	else \
		echo "$(RED)Invalid VERSION: $(VERSION)$(NC)"; \
		echo "Use: make deploy VERSION=ultimate|battery|enhanced"; \
		exit 1; \
	fi
	@echo "$(GREEN)✓ Deployment completed!$(NC)"
	@echo "Reset ESP32 to run the new code"

deploy-ampy: ## Deploy using ampy instead of mpremote
	@echo "$(BLUE)Deploying with ampy...$(NC)"
	ampy --port $(ESP32_PORT) put ble_advertising.py
	ampy --port $(ESP32_PORT) put ble_simple_peripheral.py
	@if [ "$(VERSION)" = "ultimate" ]; then \
		ampy --port $(ESP32_PORT) put digital_safe_locker_ultimate.py main.py; \
	elif [ "$(VERSION)" = "battery" ]; then \
		ampy --port $(ESP32_PORT) put digital_safe_locker_T8_battery_optimized.py main.py; \
	elif [ "$(VERSION)" = "enhanced" ]; then \
		ampy --port $(ESP32_PORT) put digital_safe_locker_T8_enhanced.py main.py; \
	fi
	@echo "$(GREEN)✓ Deployment completed!$(NC)"

monitor: ## Monitor ESP32 serial output
	@echo "$(BLUE)Monitoring $(ESP32_PORT)...$(NC)"
	@echo "Press Ctrl+C to exit"
	mpremote connect $(ESP32_PORT)

repl: ## Open REPL on ESP32
	@echo "$(BLUE)Opening REPL on $(ESP32_PORT)...$(NC)"
	@echo "Press Ctrl+D to soft reboot, Ctrl+C then Ctrl+D to exit"
	mpremote connect $(ESP32_PORT) repl

flash-info: ## Get ESP32 chip information
	@echo "$(BLUE)Getting ESP32 information...$(NC)"
	esptool.py --port $(ESP32_PORT) chip_id
	esptool.py --port $(ESP32_PORT) flash_id

erase-flash: ## Erase ESP32 flash (WARNING: deletes everything!)
	@echo "$(RED)WARNING: This will erase all data on ESP32!$(NC)"
	@read -p "Are you sure? (yes/no): " confirm && [ "$$confirm" = "yes" ] || exit 1
	@echo "$(BLUE)Erasing flash...$(NC)"
	esptool.py --port $(ESP32_PORT) erase_flash
	@echo "$(GREEN)✓ Flash erased$(NC)"

list-files: ## List files on ESP32
	@echo "$(BLUE)Files on ESP32:$(NC)"
	mpremote connect $(ESP32_PORT) fs ls

clean: ## Remove generated files and caches
	@echo "$(BLUE)Cleaning up...$(NC)"
	rm -rf test-results/ htmlcov/ .pytest_cache/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup completed$(NC)"

clean-all: clean ## Remove all generated files including dist
	@echo "$(BLUE)Deep cleaning...$(NC)"
	rm -rf dist/ build/ *.egg-info
	@echo "$(GREEN)✓ Deep cleanup completed$(NC)"

package: ## Create distribution package
	@echo "$(BLUE)Creating package...$(NC)"
	mkdir -p dist
	tar -czf dist/esp32-safe-locker-$(shell date +%Y%m%d).tar.gz \
		digital_safe_locker_ultimate.py \
		digital_safe_locker_T8_battery_optimized.py \
		digital_safe_locker_T8_enhanced.py \
		ble_simple_peripheral.py \
		ble_advertising.py \
		README.md \
		--transform 's,^,esp32-safe-locker/,'
	cd dist && sha256sum *.tar.gz > checksums.txt
	@echo "$(GREEN)✓ Package created: dist/$(NC)"
	@ls -lh dist/

pre-commit: format lint test ## Run all checks before commit
	@echo "$(GREEN)✓ All pre-commit checks passed!$(NC)"
	@echo "Ready to commit!"

ci-local: ## Run CI pipeline locally
	@echo "$(BLUE)Running CI pipeline locally...$(NC)"
	@echo "1. Linting..."
	@$(MAKE) lint
	@echo "2. Testing..."
	@$(MAKE) test
	@echo "3. Security scan..."
	@$(MAKE) security
	@echo "4. Hardware test..."
	@$(MAKE) hardware-test
	@echo "$(GREEN)✓ CI pipeline completed successfully!$(NC)"

docs: ## Generate documentation
	@echo "$(BLUE)Documentation available:$(NC)"
	@echo "  - CI/CD Setup: docs/CI_CD_SETUP.md"
	@echo "  - Quick Start: docs/QUICK_START_CI.md"
	@echo "  - README: README.md"

status: ## Show project status
	@echo "$(BLUE)Project Status:$(NC)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  Pytest: $(shell $(PYTEST) --version 2>&1 | head -1)"
	@echo "  Pylint: $(shell $(PYLINT) --version 2>&1 | head -1)"
	@echo "  ESP32 Port: $(ESP32_PORT)"
	@if [ -e "$(ESP32_PORT)" ]; then \
		echo "  $(GREEN)✓ ESP32 connected$(NC)"; \
	else \
		echo "  $(RED)✗ ESP32 not connected$(NC)"; \
	fi
	@echo ""
	@echo "$(BLUE)Git Status:$(NC)"
	@git status --short

.PHONY: test-cov test-watch lint-strict format-check security deadcode
.PHONY: deploy-ampy monitor repl flash-info erase-flash list-files
.PHONY: clean-all package pre-commit ci-local docs status
