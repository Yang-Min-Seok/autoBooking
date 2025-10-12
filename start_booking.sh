#!/bin/bash

# Log file path
LOG_FILE="$(dirname "$0")/booking.log"

# Activate virtual environment (if needed)
# source venv/bin/activate

# Run main.py
python3 main.py >> "$LOG_FILE" 2>&1

# Deactivate virtual environment (if needed)
# deactivate
