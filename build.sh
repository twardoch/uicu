#!/usr/bin/env bash
# this_file: build.sh
# ============================================================================
# UICU BUILD SCRIPT
# ----------------------------------------------------------------------------
# A single entry-point for common development tasks.  Run `./build.sh help` to
# see available commands.
# ----------------------------------------------------------------------------
#  • Installs missing tools (uv, hatch) automatically
#  • Wraps Hatch scripts defined in pyproject.toml for linting, tests, docs …
#  • Provides convenience targets like `all` that run the full CI pipeline
#  • Regenerates llms.txt via repomix
#  • Cleans build artifacts
# ============================================================================

set -euo pipefail
IFS=$'\n\t'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

repomix -o llms.txt . -i research

# ------------------------------- helpers ------------------------------------
usage() {
    cat <<'EOF'
Usage: ./build.sh <command>

Commands:
  deps         Install/update dev dependencies (uv, hatch)
  lint         Run Ruff linting and formatting checks
  format       Run Ruff formatter and autofixes
  type-check   Run mypy static type checking
  test         Run pytest test suite
  test-cov     Run tests with coverage report
  build        Build wheel and sdist using Hatch
  docs         Build Sphinx HTML documentation
  clean        Remove build artefacts (build/, dist/, *.egg-info …)
  llms         Regenerate llms.txt using repomix (requires Node + npx)
  all          Run deps → format → lint → type-check → test-cov → build
  help         Show this help message
EOF
}

command_exists() { command -v "$1" >/dev/null 2>&1; }

ensure_uv() {
    if ! command_exists uv; then
        echo "[build.sh] Installing uv…"
        python3 -m pip install --quiet --upgrade pip
        python3 -m pip install --quiet uv
    fi
}

ensure_hatch() {
    if ! command_exists hatch; then
        ensure_uv
        echo "[build.sh] Installing hatch…"
        uv pip install --quiet hatch
    fi
}

run_hatch() {
    ensure_hatch
    hatch "$@"
}

clean() {
    echo "[build.sh] Cleaning build artefacts…"
    rm -rf build dist .pytest_cache .mypy_cache .coverage coverage.xml \
        "$(git ls-files -o -i --exclude-standard | grep -E '\\.egg-info$' || true)"
}

llms() {
    echo "[build.sh] Regenerating llms.txt with repomix…"
    npx repomix -o llms.txt .
}

# ----------------------------- command router -------------------------------
CMD="${1:-help}"
shift || true # remove first arg so remaining $@ are passed to hatch/pytest …

case "$CMD" in
deps)
    ensure_uv && ensure_hatch
    ;;
lint)
    run_hatch run lint "${@:-}"
    ;;
format)
    run_hatch run fmt "${@:-}"
    ;;
type-check)
    run_hatch run type-check "${@:-}"
    ;;
test)
    run_hatch run test "${@:-}"
    ;;
test-cov)
    run_hatch run test-cov "${@:-}"
    ;;
build)
    run_hatch build "${@:-}"
    ;;
docs)
    run_hatch run docs:build "${@:-}"
    ;;
clean)
    clean
    ;;
llms)
    llms
    ;;
all)
    "$0" deps
    "$0" format
    "$0" lint
    "$0" type-check
    "$0" test-cov
    "$0" build
    ;;
help | -h | --help)
    usage
    ;;
*)
    echo "Error: Unknown command '$CMD'\n" >&2
    usage
    exit 1
    ;;
esac
