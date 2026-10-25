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
python -m pip install -r requirements.txt

echo.
echo ======================================================================
if %ERRORLEVEL% EQU 0 (
    echo  Instalacion completada con exito.
    echo  Ya puedes ejecutar INICIAR_VOZ_ESPANOL.bat o START_VOICE_ENGLISH.bat
) else (
    echo  Hubo un problema instalando las dependencias.
    echo  Asegurate de tener Python instalado y anadido al PATH de Windows.
)
echo ======================================================================
echo.
pause
