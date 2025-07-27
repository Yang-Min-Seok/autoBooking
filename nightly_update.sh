#!/bin/bash

# [1] Resolve the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/info1.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "[❌ ERROR] Env file not found: $ENV_FILE"
    exit 1
fi

# [2] Read PROJECT_DIR from env file
PROJECT_DIR=$(grep '^PROJECT_DIR=' "$ENV_FILE" | cut -d '=' -f2-)

if [ -z "$PROJECT_DIR" ]; then
    echo "[❌ ERROR] PROJECT_DIR not found in $ENV_FILE"
    exit 1
fi

echo "==============================="
echo "[🕒 DATE] $(date '+%Y-%m-%d %H:%M:%S')"
echo "[INFO] Starting nightly autoBooking update..."
echo "[INFO] Target directory: $PROJECT_DIR"
echo "==============================="

cd "$PROJECT_DIR" || {
    echo "[❌ ERROR] Failed to change directory: $PROJECT_DIR"
    exit 1
}

echo "[INFO] Checking out to main branch..."
git checkout main

echo "[INFO] Fetching from origin..."
git fetch origin

echo "[INFO] Pulling latest changes from origin/main..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "[✅ SUCCESS] Update completed successfully."
    echo "[INFO] Latest commit:"
    git log -1 --oneline
else
    echo "[❌ ERROR] An error occurred during update."
    exit 1
fi

echo "-------------------------------"
echo
