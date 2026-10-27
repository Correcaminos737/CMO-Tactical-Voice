@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor (English)
color 0B

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - (Community Edition)
echo    Author: Correcaminos / CMO War Room Community
echo ======================================================================
echo.
echo  Starting Tactical Voice Advisor in ENGLISH...
echo  Auto-detecting Command: Modern Operations installation...
echo.
echo  You can minimize this window while playing.
echo  To close the voice advisor at any time, simply close this window.
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
:: Close any orphan previous instance to prevent overlapping audio
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*tactical_voice*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
timeout /t 1 /nobreak >nul 2>&1

set "PY_CMD="

:: 1. Check if python is directly available in Windows PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 set "PY_CMD=python"

:: 2. Check if Python Launcher (py) is available
if "%PY_CMD%"=="" (
    py -3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 set "PY_CMD=py -3"
)

:: 3. Check default user installation folder (AppData\Local\Programs\Python)
if "%PY_CMD%"=="" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" set "PY_CMD="%%i\python.exe""
    )
)

:: 4. Check system Program Files
if "%PY_CMD%"=="" (
    for /d %%i in ("%ProgramFiles%\Python*") do (
        if exist "%%i\python.exe" set "PY_CMD="%%i\python.exe""
    )
)
if "%PY_CMD%"=="" (
    for /d %%i in ("%ProgramFiles(x86)%\Python*") do (
        if exist "%%i\python.exe" set "PY_CMD="%%i\python.exe""
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python was not found on your system!
    echo.
    echo Please install Python 3 from: https://www.python.org/downloads/
    echo Make sure to check the box: [X] "Add python.exe to PATH"
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

%PY_CMD% cmo_tactical_voice.py --lang en
pause
