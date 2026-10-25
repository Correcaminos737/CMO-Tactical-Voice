@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor v1.2 (Español)
color 0B

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - v1.2 (Edición de la Comunidad)
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
python cmo_tactical_voice.py --lang es
pause
