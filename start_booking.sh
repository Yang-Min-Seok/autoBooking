#!/bin/bash

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="$BASE_DIR/cron.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Booking script started." >> "$LOG_FILE"

export PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin

VENV_DIR="$BASE_DIR/venv"
VENV_PYTHON="$VENV_DIR/bin/python"
SCRIPT="$BASE_DIR/auto_booking.py"

# Activate virtual environment
if [ -d "$VENV_DIR" ]; then
  source "$VENV_DIR/bin/activate"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment activated." >> "$LOG_FILE"
else
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Virtual environment not found at $VENV_DIR" >> "$LOG_FILE"
  exit 1
fi

# Loop through up to 3 booking targets
for i in 1 2 3; do
  ENV_FILE="$BASE_DIR/info${i}.env"
  
  if [ -f "$ENV_FILE" ]; then
    # Parse USE, COURT_NO, TIME safely
    USE=$(grep '^USE=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r')
    GYM=$(grep '^GYM=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r')
    COURT_NO=$(grep '^COURT_NO=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r')
    TIME=$(grep '^TIME=' "$ENV_FILE" | cut -d '=' -f2 | tr -d '\r')
    
    if [ "$USE" = "ON" ]; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] Booking $i started (Gym: $GYM, Court: $COURT_NO, Time: $TIME)" >> "$LOG_FILE"
      "$VENV_PYTHON" "$SCRIPT" --env "$ENV_FILE" --court "$COURT_NO" --time "$TIME" >> "$LOG_FILE" 2>&1 &
    else
      echo "[$(date '+%Y-%m-%d %H:%M:%S')] Booking $i skipped (USE=OFF)" >> "$LOG_FILE"
    fi
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] info_${i}.env not found, skipping." >> "$LOG_FILE"
  fi
done

# Wait for all background processes
wait

# Deactivate virtual environment
deactivate
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Virtual environment deactivated." >> "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] All booking tasks completed." >> "$LOG_FILE"
