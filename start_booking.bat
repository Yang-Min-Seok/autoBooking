@echo off
setlocal

REM 실행 로그 파일 경로
set LOG_FILE=%~dp0booking.log

REM 가상환경 활성화 (필요시)
REM call venv\Scripts\activate

REM main.py 실행
python main.py >> %LOG_FILE% 2>&1

REM 가상환경 비활성화 (필요시)
REM call venv\Scripts\deactivate
