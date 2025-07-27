@echo off
setlocal enabledelayedexpansion

REM [1] Move to the directory where this script is located
cd /d %~dp0

REM [2] Load PROJECT_DIR from info1.env
set "PROJECT_DIR="
for /f "usebackq tokens=1,* delims==" %%A in ("info1.env") do (
    if /i "%%A"=="PROJECT_DIR" (
        set "PROJECT_DIR=%%B"
    )
)

if not defined PROJECT_DIR (
    echo [❌ ERROR] PROJECT_DIR not found in info1.env
    exit /b 1
)

REM [3] Print date and time
echo ========================================
echo [🕒 DATE] %date% %time%
echo [INFO] Starting nightly autoBooking update...
echo [INFO] Target directory: %PROJECT_DIR%
echo ========================================

REM [4] Move to the project directory
cd /d "%PROJECT_DIR%" || (
    echo [❌ ERROR] Failed to change directory to %PROJECT_DIR%
    exit /b 1
)

REM [5] Run git update commands
echo [INFO] Checking
