#!/bin/bash

# set log
LOG_FILE="/Users/yourPathTo/autoBooking/cron.log"
echo "Script started" >> "$LOG_FILE"

# set env
export PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin

# project path
PROJECT_DIR="/Users/yourPathTo/autoBooking"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
SCRIPT="$PROJECT_DIR/auto_booking.py"
ENV_FILE="$PROJECT_DIR/info.env"

# call .env
if [ -f "$ENV_FILE" ]; then
  export $(cat "$ENV_FILE" | xargs)
  echo ".env loaded" >> "$LOG_FILE"
else
  echo "WARNING: .env not found" >> "$LOG_FILE"
fi

# execute
"$VENV_PYTHON" "$SCRIPT" >> "$LOG_FILE" 2>&1