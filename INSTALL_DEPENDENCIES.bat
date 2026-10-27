@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor - Dependency Installer
color 0A

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - DEPENDENCY INSTALLER
echo ======================================================================
echo.
echo  Installing official Python libraries from PyPI:
echo   - piper-tts  (Local open-source neural AI voice engine)
echo   - numpy      (Audio buffer and matrix operations)
echo   - pedalboard (VHF/UHF tactical military radio filters)
echo.
echo  This process is only needed once.
echo ======================================================================
echo.

cd /d "%~dp0"

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

echo Using Python runtime: %PY_CMD%
echo.
%PY_CMD% -m pip install -r requirements.txt

echo.
echo ======================================================================
if %ERRORLEVEL% EQU 0 (
    echo  Installation completed successfully!
    echo  You can now run START_VOICE_ENGLISH.bat
) else (
    echo  There was an issue installing dependencies.
    echo  Please ensure you have internet access and Python installed.
)
echo ======================================================================
echo.
pause
