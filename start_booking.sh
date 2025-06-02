#!/bin/bash

# set base dir
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# log file
LOG_FILE="$BASE_DIR/cron.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script started" >> "$LOG_FILE"

# env path
ENV_FILE="$BASE_DIR/info.env"

# export env from file
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] .env loaded from $ENV_FILE" >> "$LOG_FILE"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: .env not found" >> "$LOG_FILE"
  exit 1
fi

# validate PROJECT_DIR
if [ -z "$PROJECT_DIR" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: PROJECT_DIR is not set in .env" >> "$LOG_FILE"
  exit 1
fi

# PATH
export PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin

# execute
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
SCRIPT="$PROJECT_DIR/auto_booking.py"

if [ ! -x "$VENV_PYTHON" ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Python not found at $VENV_PYTHON" >> "$LOG_FILE"
  exit 1
fi

"$VENV_PYTHON" "$SCRIPT" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Script finished successfully." >> "$LOG_FILE"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Script failed with exit code $EXIT_CODE" >> "$LOG_FILE"
fi
