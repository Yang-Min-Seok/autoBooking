#!/bin/bash

# Log file path
LOG_FILE="$(dirname "$0")/nightly_update.log"

cd "$(dirname "$0")"

echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') Start nightly update" >> "$LOG_FILE"

git checkout main >> "$LOG_FILE" 2>&1

git fetch origin >> "$LOG_FILE" 2>&1

git pull origin main >> "$LOG_FILE" 2>&1

echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') Update finished" >> "$LOG_FILE"
