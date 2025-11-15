@echo off
:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :launch
) else (
    powershell -Command "Start-Process '%~f0' -Verb RunAs" -WindowStyle Hidden
    exit /b
)

:launch
cd /d "%~dp0..\gui"
pythonw meshroom-control-center.py
exit

