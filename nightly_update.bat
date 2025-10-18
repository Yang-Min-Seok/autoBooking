@echo off
setlocal

REM Log file path
set LOG_DIR=%~dp0logs
set LOG_FILE=%LOG_DIR%\nightly_update.log

rem Ensure logs directory exists
if not exist "%LOG_DIR%" (
	mkdir "%LOG_DIR%"
)

cd /d %~dp0

echo [INFO] %date% %time% Start nightly update >> %LOG_FILE%

git checkout main >> %LOG_FILE% 2>&1

git fetch origin >> %LOG_FILE% 2>&1

git pull origin main >> %LOG_FILE% 2>&1

echo [INFO] %date% %time% Update finished >> %LOG_FILE%
