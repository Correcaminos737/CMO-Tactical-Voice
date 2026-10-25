@echo off
chcp 65001 > nul
title CMO Tactical Voice Advisor v1.2 (English)
color 0B

echo ======================================================================
echo    CMO TACTICAL VOICE ADVISOR - v1.2 (Community Edition)
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
python cmo_tactical_voice.py --lang en
pause
