#!/bin/bash
# this_file: scripts/build-and-test.sh
# Build and test script for uicu project
# Usage: ./scripts/build-and-test.sh [options]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CLEAN=false
COVERAGE=false
VERBOSE=false
PARALLEL=false
BENCHMARK=false
INSTALL_DEPS=false
PYTHON_VERSION="3.12"

# Function to print colored output
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to show help
show_help() {
    cat << EOF
Build and Test Script for uicu

Usage: $0 [OPTIONS]

OPTIONS:
    -h, --help          Show this help message
    -c, --clean         Clean build artifacts and cache
    -v, --verbose       Enable verbose output
    -p, --parallel      Run tests in parallel
    -b, --benchmark     Run benchmarks
    --coverage          Generate coverage report
    --install-deps      Install/update dependencies
    --python VERSION    Python version to use (default: 3.12)

EXAMPLES:
    $0                  Basic build and test
    $0 -c -v            Clean build with verbose output
    $0 --coverage -p    Run tests with coverage in parallel
    $0 --benchmark      Run performance benchmarks

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -b|--benchmark)
            BENCHMARK=true
            shift
            ;;
        --coverage)
            COVERAGE=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --python)
            PYTHON_VERSION="$2"
            shift 2
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    print_error "Must be run from project root directory"
    exit 1
fi

# Install UV if not present
if ! command -v uv &> /dev/null; then
    print_header "Installing UV package manager"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

# Ensure UV is in PATH
if ! command -v uv &> /dev/null; then
    if [[ -f "$HOME/.local/bin/uv" ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        print_error "UV not found in PATH"
        exit 1
    fi
fi

# Clean build artifacts
if [[ "$CLEAN" == true ]]; then
    print_header "Cleaning build artifacts"
    rm -rf dist/ build/ .pytest_cache/ .coverage
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "*.pyo" -delete 2>/dev/null || true
    find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
    print_success "Build artifacts cleaned"
fi

# Create virtual environment if it doesn't exist
if [[ ! -d ".venv" ]]; then
    print_header "Creating virtual environment"
    uv venv --python "$PYTHON_VERSION"
    print_success "Virtual environment created"
fi

# Install dependencies
if [[ "$INSTALL_DEPS" == true ]] || [[ ! -f ".venv/pyvenv.cfg" ]]; then
    print_header "Installing dependencies"
    source .venv/bin/activate
    uv pip install -e ".[dev,test,all]"
    print_success "Dependencies installed"
fi

# Activate virtual environment
source .venv/bin/activate

# Check Python version
print_header "Environment Information"
echo "Python version: $(python --version)"
echo "UV version: $(uv --version)"
echo "Virtual environment: $(which python)"

# Run linting
print_header "Running code quality checks"
if [[ "$VERBOSE" == true ]]; then
    uv run ruff check --output-format=github src/ tests/
    uv run ruff format --check --respect-gitignore src/ tests/
else
    uv run ruff check --output-format=github src/ tests/ --quiet
    uv run ruff format --check --respect-gitignore src/ tests/ --quiet
fi
print_success "Code quality checks passed"

# Run type checking
print_header "Running type checking"
if command -v mypy &> /dev/null; then
    uv run mypy src/uicu --ignore-missing-imports
    print_success "Type checking passed"
else
    print_warning "mypy not found, skipping type checking"
fi

# Build the package
print_header "Building package"
uv run python -m build --outdir dist/
print_success "Package built successfully"

# Verify package contents
print_header "Verifying package contents"
ls -la dist/
for file in dist/*; do
    if [[ "$file" == *.whl ]]; then
        echo "Wheel contents:"
        unzip -l "$file" | head -20
    fi
done
print_success "Package contents verified"

# Run tests
print_header "Running tests"
TEST_ARGS=""
if [[ "$PARALLEL" == true ]]; then
    TEST_ARGS="$TEST_ARGS -n auto"
fi
if [[ "$VERBOSE" == true ]]; then
    TEST_ARGS="$TEST_ARGS -v"
fi
if [[ "$COVERAGE" == true ]]; then
    TEST_ARGS="$TEST_ARGS --cov=src/uicu --cov-report=term-missing --cov-report=html --cov-report=xml"
fi

uv run pytest $TEST_ARGS tests/
print_success "Tests completed successfully"

# Run benchmarks if requested
if [[ "$BENCHMARK" == true ]]; then
    print_header "Running benchmarks"
    if [[ -f "tests/test_benchmark.py" ]]; then
        uv run pytest tests/test_benchmark.py --benchmark-only -v
        print_success "Benchmarks completed"
    else
        print_warning "No benchmark tests found"
    fi
fi

# Test package installation
print_header "Testing package installation"
TEMP_VENV=$(mktemp -d)
uv venv "$TEMP_VENV"
source "$TEMP_VENV/bin/activate"
uv pip install dist/*.whl
python -c "import uicu; print(f'uicu {uicu.__version__} installed successfully')"
rm -rf "$TEMP_VENV"
print_success "Package installation test passed"

# Final summary
print_header "Build Summary"
print_success "All checks passed!"
echo "Build artifacts:"
ls -la dist/
if [[ "$COVERAGE" == true ]]; then
    echo "Coverage report generated in htmlcov/"
fi

print_success "Build and test completed successfully!"