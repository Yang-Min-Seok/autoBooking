#!/bin/bash

# Get current path
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Make logs dir if not exists
mkdir -p "$SCRIPT_DIR/logs"

# Use VENV_PYTHON if provided in environment, otherwise try ./venv/bin/python3
# You can override by exporting VENV_PYTHON="/path/to/venv/bin/python3" before running this script
: "${VENV_PYTHON:-}" >/dev/null 2>&1 || VENV_PYTHON="$SCRIPT_DIR/venv/bin/python3"

if [ ! -x "$VENV_PYTHON" ]; then
	echo "[WARN] Python executable not found at '$VENV_PYTHON'. Ensure you created a venv or set VENV_PYTHON."
	echo "Attempting to use system 'python3'..."
	VENV_PYTHON="$(command -v python3 || true)"
fi

"$VENV_PYTHON" "$SCRIPT_DIR/main.py"

