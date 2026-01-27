@echo off
title Roblox RPC - Launcher
color 0A

:: --- PATHS ---
set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
set "SCRIPT_FILE=%~dp0main.pyw"

echo =========================================
echo   STARTING ROBLOX AND PRESENCE
echo =========================================

:: 1. Start Roblox
echo [1/2] Launching Roblox...
start roblox://

:: 2. Start Script
echo [2/2] Launching Presence Script...
if exist "%PYTHON_EXE%" (
    start "" "%PYTHON_EXE%" "%SCRIPT_FILE%"
    echo [SUCCESS] Script is running in background.
) else (
    color 0C
    echo [ERROR] Virtual Environment not found! 
    echo Please run Setup.bat first.
    pause
    exit
)

timeout /t 5
exit