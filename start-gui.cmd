@echo off
setlocal
cd /d "%~dp0"
uv run python -m modem_controller.app
set "exit_code=%errorlevel%"
endlocal & exit /b %exit_code%