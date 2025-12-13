@echo off
setlocal

REM Use VENV_PYTHON if set, otherwise try .\venv\Scripts\python.exe, otherwise system python
if defined VENV_PYTHON (
	set "PY_EXE=%VENV_PYTHON%"
) else (
	if exist "%~dp0venv\Scripts\python.exe" (
		set "PY_EXE=%~dp0venv\Scripts\python.exe"
	) else (
		for %%I in (python.exe) do if exist "%%~$PATH:I" set "PY_EXE=%%~$PATH:I"
	)
)

if not defined PY_EXE (
	echo [WARN] Python executable not found. Please create a venv or set VENV_PYTHON environment variable.
	exit /b 1
)

REM Run main.py with selected python
"%PY_EXE%" "%~dp0main.py"
