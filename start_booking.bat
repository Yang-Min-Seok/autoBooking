@echo off
REM Activate virtual environment
call venv\Scripts\activate

REM Run the Python Playwright reservation script
python auto_booking.py

REM Deactivate virtual environment
call venv\Scripts\deactivate