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
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set "PY_CMD=python"
) else (
    py -3 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PY_CMD=py -3"
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
