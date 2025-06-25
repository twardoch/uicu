#!/usr/bin/env bash
# this_file: release.sh
# ============================================================================
# UICU RELEASE SCRIPT
# ----------------------------------------------------------------------------
# A script to handle the release process for uicu.
# ----------------------------------------------------------------------------
#  • Runs all tests and checks
#  • Builds documentation
#  • Updates version
#  • Creates git tag
#  • Builds and uploads to PyPI
# ============================================================================

set -euo pipefail
IFS=$'\n\t'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# ------------------------------- helpers ------------------------------------
usage() {
    cat <<'EOF'
Usage: ./release.sh <version>

Arguments:
  version     The version to release (e.g. 1.0.0)

Example:
  ./release.sh 1.0.0
EOF
}

# ----------------------------- main script --------------------------------
if [ $# -ne 1 ]; then
    usage
    exit 1
fi

VERSION="$1"

echo "[release.sh] Starting release process for version ${VERSION}..."

# Run all checks and tests
echo "[release.sh] Running build script with all checks..."
./build.sh all

# Build documentation
echo "[release.sh] Building documentation..."
./build.sh docs

# Create git tag
echo "[release.sh] Creating git tag v${VERSION}..."
git tag -a "v${VERSION}" -m "Release version ${VERSION}"

# Build distribution
echo "[release.sh] Building distribution..."
./build.sh build

# Upload to PyPI
echo "[release.sh] Uploading to PyPI..."
hatch publish

echo "[release.sh] Release ${VERSION} completed successfully!"
echo
echo "Next steps:"
echo "1. Push the tag: git push origin v${VERSION}"
echo "2. Create a GitHub release: https://github.com/adamchainz/uicu/releases/new"
echo "3. Update the documentation site"
echo "4. Announce the release"
