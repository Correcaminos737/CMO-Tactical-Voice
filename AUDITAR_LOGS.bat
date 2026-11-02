@echo off
chcp 65001 > nul
title CMO Tactical Voice - Auditor de Logs
color 0A

echo ======================================================================
echo    CMO TACTICAL VOICE - AUDITOR MASIVO DE LOGS DE COMBATE
echo ======================================================================
echo.

cd /d "%~dp0"
python audit_cmo_logs.py --verbose
echo.
pause
