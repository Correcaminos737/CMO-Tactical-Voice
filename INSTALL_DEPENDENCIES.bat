@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor v1.2.14 - Dependency Installer
color 0A

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR v1.2.14 - DEPENDENCY INSTALLER
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
    echo Please download and install Python 3.12 (64-bit) from:
    echo https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
    echo.
    echo Make sure to check the box: [X] "Add python.exe to PATH"
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

:: Verify Python version compatibility (Requires Python 3.10 - 3.12)
%PY_CMD% -c "import sys; sys.exit(0 if (3, 9) <= sys.version_info < (3, 13) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ======================================================================
    echo [ERROR] Incompatible Python version detected!
    echo.
    echo The neural voice engine (Piper-TTS) requires Python 3.10, 3.11, or 3.12.
    echo (Python 3.13+ is not yet supported by the voice phonemizer library).
    echo.
    echo Please install Python 3.12 using the direct official installer:
    echo https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
    echo.
    echo Remember to check: [X] "Add python.exe to PATH"
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
    echo  Please ensure you have internet access and Python 3.12 installed.
)
echo ======================================================================
echo.
pause
