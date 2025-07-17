#!/bin/bash
# this_file: scripts/release.sh
# Release script for uicu project
# Usage: ./scripts/release.sh [version]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
Release Script for uicu

Usage: $0 [VERSION] [OPTIONS]

ARGUMENTS:
    VERSION             Version to release (e.g., 1.0.0, 1.0.1, 2.0.0-beta.1)
                       If not provided, will prompt for input

OPTIONS:
    -h, --help          Show this help message
    -d, --dry-run       Perform a dry run without making changes
    -f, --force         Force release without confirmation
    --skip-tests        Skip running tests (not recommended)
    --skip-build        Skip building package (not recommended)

EXAMPLES:
    $0 1.0.0            Release version 1.0.0
    $0 1.0.1 --dry-run  Preview release 1.0.1 without making changes
    $0 --force          Release with auto-generated version

NOTES:
    - This script will create a git tag and push it to trigger CI/CD
    - Ensure you have push permissions to the repository
    - The version should follow semantic versioning (semver)

EOF
}

# Default values
VERSION=""
DRY_RUN=false
FORCE=false
SKIP_TESTS=false
SKIP_BUILD=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        -*)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$VERSION" ]]; then
                VERSION="$1"
            else
                print_error "Too many arguments"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if we're in the project root
if [[ ! -f "pyproject.toml" ]]; then
    print_error "Must be run from project root directory"
    exit 1
fi

# Check if git is clean
if [[ -n "$(git status --porcelain)" ]]; then
    print_error "Git working directory is not clean"
    echo "Please commit or stash your changes before releasing"
    exit 1
fi

# Check if we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    print_warning "Not on main branch (currently on: $CURRENT_BRANCH)"
    if [[ "$FORCE" != true ]]; then
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

# Get current version from git
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
CURRENT_VERSION=${CURRENT_VERSION#v}  # Remove 'v' prefix

# If no version provided, prompt for it
if [[ -z "$VERSION" ]]; then
    print_header "Current version: $CURRENT_VERSION"
    read -p "Enter new version (e.g., 1.0.0): " VERSION
    if [[ -z "$VERSION" ]]; then
        print_error "Version cannot be empty"
        exit 1
    fi
fi

# Validate version format (basic semver check)
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9.-]+)?$ ]]; then
    print_error "Invalid version format: $VERSION"
    echo "Version should follow semantic versioning (e.g., 1.0.0, 1.0.1, 2.0.0-beta.1)"
    exit 1
fi

# Check if version already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    print_error "Version v$VERSION already exists"
    exit 1
fi

# Confirm release
if [[ "$FORCE" != true ]]; then
    print_header "Release Summary"
    echo "Current version: $CURRENT_VERSION"
    echo "New version: $VERSION"
    echo "Git branch: $CURRENT_BRANCH"
    echo "Repository: $(git config --get remote.origin.url)"
    echo ""
    if [[ "$DRY_RUN" == true ]]; then
        echo "This is a DRY RUN - no changes will be made"
    else
        echo "This will create a git tag and push it to trigger CI/CD"
    fi
    echo ""
    read -p "Proceed with release? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Release cancelled"
        exit 1
    fi
fi

# Run tests unless skipped
if [[ "$SKIP_TESTS" != true ]]; then
    print_header "Running tests"
    if [[ -f "scripts/build-and-test.sh" ]]; then
        ./scripts/build-and-test.sh --coverage
    else
        # Fallback to direct pytest
        source .venv/bin/activate 2>/dev/null || true
        uv run pytest tests/ -v
    fi
    print_success "Tests passed"
fi

# Build package unless skipped
if [[ "$SKIP_BUILD" != true ]]; then
    print_header "Building package"
    if [[ ! -d ".venv" ]]; then
        uv venv
    fi
    source .venv/bin/activate
    uv pip install build hatchling hatch-vcs
    uv run python -m build --outdir dist/
    print_success "Package built"
fi

# Update changelog
print_header "Updating changelog"
if [[ -f "CHANGELOG.md" ]]; then
    # Add new version entry to changelog
    CHANGELOG_ENTRY="## [$VERSION] - $(date +%Y-%m-%d)\n\n### Added\n- Version $VERSION release\n\n"
    
    if [[ "$DRY_RUN" != true ]]; then
        # Create backup
        cp CHANGELOG.md CHANGELOG.md.bak
        
        # Insert new entry after the first line (assuming it's the title)
        sed -i "1a\\$CHANGELOG_ENTRY" CHANGELOG.md
        
        # Stage the changelog
        git add CHANGELOG.md
        
        print_success "Changelog updated"
    else
        print_warning "DRY RUN: Would update CHANGELOG.md"
    fi
else
    print_warning "CHANGELOG.md not found"
fi

# Create git tag
print_header "Creating git tag"
TAG_MESSAGE="Release version $VERSION"

if [[ "$DRY_RUN" != true ]]; then
    # Commit changelog if it was updated
    if [[ -f "CHANGELOG.md" ]]; then
        git commit -m "Update changelog for v$VERSION" || true
    fi
    
    # Create annotated tag
    git tag -a "v$VERSION" -m "$TAG_MESSAGE"
    
    # Push tag to origin
    git push origin "v$VERSION"
    
    print_success "Git tag v$VERSION created and pushed"
else
    print_warning "DRY RUN: Would create and push tag v$VERSION"
fi

# Show next steps
print_header "Release Status"
if [[ "$DRY_RUN" != true ]]; then
    print_success "Release v$VERSION completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Check GitHub Actions for build status"
    echo "2. Monitor PyPI for package publication"
    echo "3. Create GitHub release notes if needed"
    echo ""
    echo "Links:"
    echo "- GitHub Actions: https://github.com/twardoch/uicu/actions"
    echo "- PyPI: https://pypi.org/project/uicu/"
    echo "- GitHub Releases: https://github.com/twardoch/uicu/releases"
else
    print_success "DRY RUN completed successfully!"
    echo ""
    echo "To perform the actual release, run:"
    echo "  $0 $VERSION"
fi

# Clean up
if [[ -f "CHANGELOG.md.bak" ]]; then
    rm -f CHANGELOG.md.bak
fi

print_success "Release script completed!"