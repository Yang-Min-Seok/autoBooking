#!/bin/bash

# Get current path
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Make logs dir if not exists
mkdir -p "$SCRIPT_DIR/logs"

# Execute python3
/usr/local/bin/python3 "$SCRIPT_DIR/main.py"

