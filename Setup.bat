@echo off
title Roblox RPC - Initializer
color 0B

echo =========================================
echo   SETTING UP PROJECT ENVIRONMENT
echo =========================================

:: 1. Create Virtual Environment
if not exist "venv" (
    echo [1/3] Creating Virtual Environment...
    python -m venv venv
) else (
    echo [SKIP] venv already exists.
)

:: 2. Upgrade Pip and Install Requirements
echo [2/3] Installing/Updating Libraries...
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\pip install pypresence requests psutil python-dotenv

:: 3. Create .env template if it doesn't exist
if not exist ".env" (
    echo [3/3] Creating .env template...
    echo ROBLOX_USER_ID=0 > .env
    echo ROBLOSECURITY=PASTE_COOKIE_HERE >> .env
    echo [IMPORTANT] Please edit the .env file with your info!
)

echo -----------------------------------------
echo SETUP COMPLETE! You can now run Start.bat
echo -----------------------------------------
pause