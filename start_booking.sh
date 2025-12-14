#!/bin/bash

# Cron-friendly environment
# Set HOME to the user's home dynamically (falls back to /Users/$(id -un))
# and provide a sane PATH so `command -v` works under cron
export HOME="${HOME:-/Users/$(id -un)}"
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# --- Optional user configuration (edit if needed) ---
# You can set `VENV_PYTHON` here to point to your virtualenv python,
# e.g. VENV_PYTHON="/Users/yourname/.virtualenvs/autoBooking/bin/python3"
# ----------------------------------------------------

# Get current path
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Make logs dir if not exists
mkdir -p "$SCRIPT_DIR/logs"

# Redirect stdout/stderr so cron output is captured in logs/cron.log
exec >> "$SCRIPT_DIR/logs/cron.log" 2>&1

# Use VENV_PYTHON if provided in environment, otherwise try ./venv/bin/python3
# You can override by exporting VENV_PYTHON="/path/to/venv/bin/python3" before running this script
VENV_PYTHON="${VENV_PYTHON:-$SCRIPT_DIR/venv/bin/python3}"

# in case the venv python is not found, try to find system python3
if [ ! -x "$VENV_PYTHON" ]; then
	echo "[WARN] Python executable not found at '$VENV_PYTHON'. Ensure you created a venv or set VENV_PYTHON."
	echo "Attempting to use system 'python3'..."
	VENV_PYTHON="$(command -v python3 || /usr/bin/python3 || /usr/local/bin/python3 || true)"
fi

# in case no python3 is found, exit with error
if [ -z "$VENV_PYTHON" ] || [ ! -x "$VENV_PYTHON" ]; then
	echo "[ERROR] No python3 executable found. Exiting."
	exit 1
fi

# incase the venv python is found, print its version
exec "$VENV_PYTHON" "$SCRIPT_DIR/main.py"