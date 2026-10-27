@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor (Español)
color 0B

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - (Edición de la Comunidad)
echo    Autor: Correcaminos / CMO War Room Community
echo ======================================================================
echo.
echo  Iniciando Asesor Táctico por Voz en ESPAÑOL...
echo  Localizando instalación de Command: Modern Operations...
echo.
echo  Puedes minimizar esta ventana mientras juegas.
echo  Para detener el asesor en cualquier momento, cierra esta ventana.
echo.
echo ======================================================================
echo.

cd /d "%~dp0"
:: Cerrar cualquier instancia previa para evitar voces duplicadas
powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*tactical_voice*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
timeout /t 1 /nobreak >nul 2>&1

set "PY_CMD="

:: 1. Comprobar si python está en el PATH
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 set "PY_CMD=python"

:: 2. Comprobar lanzador py de Windows
if "%PY_CMD%"=="" (
    py -3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 set "PY_CMD=py -3"
)

:: 3. Comprobar ruta por defecto de instalación de usuario (AppData\Local\Programs\Python)
if "%PY_CMD%"=="" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
        if exist "%%i\python.exe" set "PY_CMD="%%i\python.exe""
    )
)

:: 4. Comprobar Program Files
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
    echo [ERROR] No se ha encontrado Python en el sistema.
    echo.
    echo Por favor, instala Python 3 desde: https://www.python.org/downloads/
    echo Recuerda marcar la casilla: [X] "Add python.exe to PATH"
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

%PY_CMD% cmo_tactical_voice.py --lang es
pause
