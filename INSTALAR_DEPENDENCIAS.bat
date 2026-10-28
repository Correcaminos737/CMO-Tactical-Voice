@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor v1.2.14 - Instalador de Dependencias
color 0A

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR v1.2.14 - INSTALADOR DE DEPENDENCIAS
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

:: 3. Comprobar ruta por defecto de instalacion de usuario (AppData\Local\Programs\Python)
if "%PY_CMD%"=="" (
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe""
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe""
    if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set "PY_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe""
)

:: 4. Comprobar Program Files
if "%PY_CMD%"=="" (
    if exist "%ProgramFiles%\Python312\python.exe" set "PY_CMD="%ProgramFiles%\Python312\python.exe""
    if exist "%ProgramFiles%\Python311\python.exe" set "PY_CMD="%ProgramFiles%\Python311\python.exe""
    if exist "%ProgramFiles%\Python310\python.exe" set "PY_CMD="%ProgramFiles%\Python310\python.exe""
)
if "%PY_CMD%"=="" (
    if exist "%ProgramFiles(x86)%\Python312\python.exe" set "PY_CMD="%ProgramFiles(x86)%\Python312\python.exe""
    if exist "%ProgramFiles(x86)%\Python311\python.exe" set "PY_CMD="%ProgramFiles(x86)%\Python311\python.exe""
    if exist "%ProgramFiles(x86)%\Python310\python.exe" set "PY_CMD="%ProgramFiles(x86)%\Python310\python.exe""
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
    echo Por favor, descarga e instala Python 3.12 (64-bit) desde:
    echo https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
    echo.
    echo Recuerda marcar la casilla: [X] "Add python.exe to PATH"
    echo ======================================================================
    echo.
    pause
    exit /b 1
)

:: Comprobar versión compatible de Python (3.10 - 3.12)
%PY_CMD% -c "import sys; sys.exit(0 if (3, 9) <= sys.version_info < (3, 13) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ======================================================================
    echo [ERROR] Version de Python no compatible detectada.
    echo.
    echo El motor de voz neuronal (Piper-TTS) requiere Python 3.10, 3.11 o 3.12.
    echo (Python 3.13+ aun no dispone de librerias de fonemas precompiladas).
    echo.
    echo Por favor, instala Python 3.12 usando el instalador oficial directo:
    echo https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
    echo.
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
    echo  Asegurate de tener conexion a internet y Python 3.12 instalado.
)
echo ======================================================================
echo.
pause
