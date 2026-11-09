#!/bin/bash
# Sets up a basic python dev environment (python3, pip, jupyter)
# Usage: ./env_install.sh [--dry-run] [--quiet]

set -euo pipefail

DRY_RUN=false
QUIET=false
LOG_FILE="install.log"

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --quiet) QUIET=true ;;
        *) echo "Unknown option: $arg"; exit 1 ;;
    esac
done

GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

pretty_print() {
    # $1 = message, $2 = level (info / warn / error)
    local color="$GREEN"
    if [ "${2:-info}" = "warn" ]; then color="$YELLOW"; fi
    if [ "${2:-info}" = "error" ]; then color="$RED"; fi
    if [ "$QUIET" = false ] || [ "${2:-info}" = "error" ]; then
        printf "\n${color}%s${NC}\n\n" "$1"
    fi
    echo "$(date '+%Y-%m-%d %H:%M:%S') [${2:-info}] $1" >> "$LOG_FILE"
}

run() {
    # runs a command (or just prints it in dry-run mode)
    if [ "$DRY_RUN" = true ]; then
        pretty_print "[dry-run] $*" warn
        return 0
    fi
    echo "$(date '+%Y-%m-%d %H:%M:%S') [cmd] $*" >> "$LOG_FILE"
    if ! "$@"; then
        pretty_print "Command failed: $*" error
        exit 1
    fi
}

# --- 1. detect the OS ---
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
else
    pretty_print "Unsupported OS: $OSTYPE" error
    exit 1
fi
pretty_print "Detected OS: $OS"

# --- 2. python3 ---
if command -v python3 > /dev/null 2>&1; then
    pretty_print "Python already installed: $(python3 --version)"
else
    pretty_print "Python3 not found, installing it..." warn
    if [ "$OS" = "macos" ]; then
        run brew install python
    else
        run sudo apt update
        run sudo apt install -y python3 python3-pip
    fi
fi

# --- 3. pip ---
if python3 -m pip --version > /dev/null 2>&1; then
    pretty_print "pip version: $(python3 -m pip --version)"
else
    pretty_print "pip is missing" error
    exit 1
fi

# --- 4. jupyter ---
if [ "$OS" = "macos" ]; then
    run brew install jupyterlab
else
    run python3 -m pip install --user notebook
fi
pretty_print "Jupyter installed, launch it with: jupyter notebook"

# --- 5. brew health check (mac only) ---
if [ "$OS" = "macos" ]; then
    pretty_print "Running brew doctor..."
    brew doctor || pretty_print "brew doctor found some issues, check the output above" warn
fi

pretty_print "All done! (log written in $LOG_FILE)"
