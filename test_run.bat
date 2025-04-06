@echo off
cd /d %~dp0
call venv\Scripts\activate
python test_main.py