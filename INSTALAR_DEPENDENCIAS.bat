@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor - Instalador de Librerias / Dependency Installer
color 0A

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - INSTALADOR DE DEPENDENCIAS
echo ======================================================================
echo.
echo  Instalando librerías oficiales de Python desde PyPI:
echo   - piper-tts  (Motor de voz neuronal local de código abierto)
echo   - numpy      (Operaciones de audio y memoria)
echo   - pedalboard (Filtros de radio militar táctica VHF/UHF)
echo.
echo  Este proceso solo se ejecuta una vez.
echo ======================================================================
echo.

cd /d "%~dp0"

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

echo Usando ejecutable de Python: %PY_CMD%
echo.
%PY_CMD% -m pip install -r requirements.txt

echo.
echo ======================================================================
if %ERRORLEVEL% EQU 0 (
    echo  Instalacion completada con exito.
    echo  Ya puedes ejecutar INICIAR_VOZ_ESPANOL.bat o START_VOICE_ENGLISH.bat
) else (
    echo  Hubo un problema instalando las dependencias.
    echo  Asegurate de tener conexion a internet y Python instalado.
)
echo ======================================================================
echo.
pause
