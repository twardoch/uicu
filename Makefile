# this_file: Makefile
# Makefile for uicu project

.PHONY: help install test test-cov lint format build clean release install-dev setup-dev binary docs

# Default target
.DEFAULT_GOAL := help

# Colors
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m

# Project variables
PROJECT_NAME := uicu
PYTHON_VERSION := 3.12
VENV_DIR := .venv

help: ## Show this help message
	@echo "$(GREEN)uicu - Development Commands$(NC)"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup-dev: ## Set up development environment
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	@if ! command -v uv &> /dev/null; then \
		echo "$(YELLOW)Installing UV...$(NC)"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		export PATH="$$HOME/.local/bin:$$PATH"; \
	fi
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(YELLOW)Creating virtual environment...$(NC)"; \
		uv venv --python $(PYTHON_VERSION); \
	fi
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@. $(VENV_DIR)/bin/activate && uv pip install -e ".[dev,test,all]"
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "$(YELLOW)To activate: source $(VENV_DIR)/bin/activate$(NC)"

install: ## Install package in development mode
	@echo "$(YELLOW)Installing package in development mode...$(NC)"
	@. $(VENV_DIR)/bin/activate && uv pip install -e ".[dev,test,all]"

install-dev: setup-dev ## Alias for setup-dev

test: ## Run tests
	@echo "$(YELLOW)Running tests...$(NC)"
	@. $(VENV_DIR)/bin/activate && pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	@. $(VENV_DIR)/bin/activate && pytest tests/ --cov=src/uicu --cov-report=term-missing --cov-report=html --cov-report=xml

test-parallel: ## Run tests in parallel
	@echo "$(YELLOW)Running tests in parallel...$(NC)"
	@. $(VENV_DIR)/bin/activate && pytest tests/ -n auto -v

benchmark: ## Run benchmarks
	@echo "$(YELLOW)Running benchmarks...$(NC)"
	@if [ -f "tests/test_benchmark.py" ]; then \
		. $(VENV_DIR)/bin/activate && pytest tests/test_benchmark.py --benchmark-only -v; \
	else \
		echo "$(RED)No benchmark tests found$(NC)"; \
	fi

lint: ## Run linting
	@echo "$(YELLOW)Running linting...$(NC)"
	@. $(VENV_DIR)/bin/activate && ruff check src/ tests/
	@. $(VENV_DIR)/bin/activate && ruff format --check src/ tests/

format: ## Format code
	@echo "$(YELLOW)Formatting code...$(NC)"
	@. $(VENV_DIR)/bin/activate && ruff format src/ tests/
	@. $(VENV_DIR)/bin/activate && ruff check --fix src/ tests/

type-check: ## Run type checking
	@echo "$(YELLOW)Running type checking...$(NC)"
	@. $(VENV_DIR)/bin/activate && mypy src/uicu --ignore-missing-imports

build: ## Build package
	@echo "$(YELLOW)Building package...$(NC)"
	@. $(VENV_DIR)/bin/activate && python -m build --outdir dist/
	@echo "$(GREEN)Package built successfully!$(NC)"
	@ls -la dist/

binary: ## Build binary executable
	@echo "$(YELLOW)Building binary...$(NC)"
	@chmod +x scripts/build-binary.sh
	@./scripts/build-binary.sh
	@echo "$(GREEN)Binary built successfully!$(NC)"

full-build: ## Run full build pipeline
	@echo "$(YELLOW)Running full build pipeline...$(NC)"
	@chmod +x scripts/build-and-test.sh
	@./scripts/build-and-test.sh --coverage --parallel

clean: ## Clean build artifacts
	@echo "$(YELLOW)Cleaning build artifacts...$(NC)"
	@rm -rf dist/ build/ .pytest_cache/ .coverage htmlcov/ coverage.xml
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)Build artifacts cleaned!$(NC)"

clean-all: clean ## Clean everything including venv
	@echo "$(YELLOW)Cleaning virtual environment...$(NC)"
	@rm -rf $(VENV_DIR)
	@echo "$(GREEN)Everything cleaned!$(NC)"

release: ## Create a release (interactive)
	@echo "$(YELLOW)Creating release...$(NC)"
	@chmod +x scripts/release.sh
	@./scripts/release.sh

release-dry: ## Dry run release
	@echo "$(YELLOW)Dry run release...$(NC)"
	@chmod +x scripts/release.sh
	@./scripts/release.sh --dry-run

docs: ## Build documentation (placeholder)
	@echo "$(YELLOW)Building documentation...$(NC)"
	@echo "$(RED)Documentation build not yet implemented$(NC)"

install-icu: ## Install ICU dependencies (Ubuntu/Debian)
	@echo "$(YELLOW)Installing ICU dependencies...$(NC)"
	@if command -v apt-get &> /dev/null; then \
		sudo apt-get update && sudo apt-get install -y libicu-dev pkg-config; \
	elif command -v brew &> /dev/null; then \
		brew install icu4c pkg-config; \
	else \
		echo "$(RED)Please install ICU development libraries manually$(NC)"; \
		exit 1; \
	fi

check: lint type-check test ## Run all checks

all: clean install lint type-check test build ## Run complete workflow

# Development workflow shortcuts
dev: setup-dev ## Quick development setup
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. source $(VENV_DIR)/bin/activate"
	@echo "  2. make test"
	@echo "  3. make build"

ci: ## Run CI-like checks locally
	@echo "$(YELLOW)Running CI-like checks...$(NC)"
	@make lint
	@make type-check
	@make test-cov
	@make build
	@echo "$(GREEN)All CI checks passed!$(NC)"

# Show environment info
info: ## Show environment information
	@echo "$(GREEN)Environment Information:$(NC)"
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python version: $(PYTHON_VERSION)"
	@echo "Virtual environment: $(VENV_DIR)"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment status: $(GREEN)Active$(NC)"; \
		if [ -f "$(VENV_DIR)/bin/python" ]; then \
			echo "Python path: $(VENV_DIR)/bin/python"; \
			echo "Python version: $$($(VENV_DIR)/bin/python --version)"; \
		fi; \
	else \
		echo "Virtual environment status: $(RED)Not found$(NC)"; \
	fi
	@if command -v uv &> /dev/null; then \
		echo "UV version: $$(uv --version)"; \
	else \
		echo "UV: $(RED)Not installed$(NC)"; \
	fi