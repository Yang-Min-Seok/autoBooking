@echo off
setlocal enabledelayedexpansion

REM Set base directory and log file
set BASE_DIR=%~dp0
set LOG_FILE=%BASE_DIR%booking.log

REM Log start
echo [%date% %time%] Booking script started. >> %LOG_FILE%

REM Activate virtual environment
if exist %BASE_DIR%venv\Scripts\activate (
    call %BASE_DIR%venv\Scripts\activate
    echo [%date% %time%] Virtual environment activated. >> %LOG_FILE%
) else (
    echo [%date% %time%] ERROR: Virtual environment not found at %BASE_DIR%venv >> %LOG_FILE%
    exit /b 1
)

REM Loop through up to 3 booking targets
for %%i in (1 2 3) do (
    set "ENV_FILE=%BASE_DIR%info%%i.env"

    if exist !ENV_FILE! (
        REM Read values from .env file
        for /f "tokens=2 delims==" %%A in ('findstr "^USE=" !ENV_FILE!') do set "USE=%%A"
        for /f "tokens=2 delims==" %%B in ('findstr "^GYM=" !ENV_FILE!') do set "GYM=%%B"
        for /f "tokens=2 delims==" %%C in ('findstr "^COURT_NO=" !ENV_FILE!') do set "COURT_NO=%%C"
        for /f "tokens=2 delims==" %%D in ('findstr "^TIME=" !ENV_FILE!') do set "TIME=%%D"

        REM Clean values (remove potential trailing characters)
        set "USE=!USE:~0,2!"
        set "GYM=!GYM:~0,50!"
        set "COURT_NO=!COURT_NO:~0,10!"
        set "TIME=!TIME:~0,20!"

        REM Conditional booking execution
        if /I "!USE!"=="ON" (
            echo [%date% %time%] Booking %%i started (Gym: !GYM!, Court: !COURT_NO!, Time: !TIME!) >> %LOG_FILE%
            python auto_booking.py --env !ENV_FILE! --court !COURT_NO! --time "!TIME!" >> %LOG_FILE% 2>&1
        ) else (
            echo [%date% %time%] Booking %%i skipped (USE=OFF) >> %LOG_FILE%
        )
    ) else (
        echo [%date% %time%] info%%i.env not found, skipping. >> %LOG_FILE%
    )
)

REM Deactivate virtual environment
call %BASE_DIR%venv\Scripts\deactivate
echo [%date% %time%] Virtual environment deactivated. >> %LOG_FILE%

echo [%date% %time%] All booking tasks completed. >> %LOG_FILE%
pause
