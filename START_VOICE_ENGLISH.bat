@echo off



chcp 65001 > nul



title CMO Tactical Voice Advisor v1.2.14 (English)



color 0B







echo ======================================================================



echo    CMO TACTICAL VOICE ADVISOR - v1.2.14 [Community Edition]



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



:: Close any orphan previous instance to prevent overlapping audio



powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*tactical_voice*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1



timeout /t 1 /nobreak >nul 2>&1







set "PY_CMD="



:: 1. Check if python is directly available in Windows PATH

python --version >nul 2>&1

if %ERRORLEVEL% EQU 0 set "PY_CMD=python"



:: 2. Check if Python Launcher (py) is available

if "%PY_CMD%"=="" (

    py -3 --version >nul 2>&1

    if %ERRORLEVEL% EQU 0 set "PY_CMD=py -3"

)



:: 3. Check direct AppData installation paths

if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"

if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"

if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"

if "%PY_CMD%"=="" if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" set PY_CMD="%LOCALAPPDATA%\Programs\Python\Python314\python.exe"



:: 4. Check system Program Files

if "%PY_CMD%"=="" if exist "%ProgramFiles%\Python312\python.exe" set PY_CMD="%ProgramFiles%\Python312\python.exe"

if "%PY_CMD%"=="" if exist "%ProgramFiles%\Python311\python.exe" set PY_CMD="%ProgramFiles%\Python311\python.exe"

if "%PY_CMD%"=="" if exist "%ProgramFiles%\Python310\python.exe" set PY_CMD="%ProgramFiles%\Python310\python.exe"



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







:: Auto-preflight check: ensure piper-tts is installed in this Python environment



%PY_CMD% -c "import piper" >nul 2>&1



if %ERRORLEVEL% NEQ 0 (



    echo ======================================================================



    echo  [!] First run detected or Piper neural voice engine is missing.



    echo      Installing dependencies automatically via pip...



    echo      [This only happens once and takes ~30 seconds]



    echo ======================================================================



    echo.



    %PY_CMD% -m pip install -r requirements.txt



    if %ERRORLEVEL% NEQ 0 (



        echo.



        echo [ERROR] Failed to install dependencies automatically.



        echo Please run INSTALL_DEPENDENCIES.bat or execute:



        echo    pip install -r requirements.txt



        echo ======================================================================



        pause



        exit /b 1



    )



    echo.



    echo  [OK] Dependencies installed successfully! Starting voice advisor...



    echo ======================================================================



    echo.



)







%PY_CMD% cmo_tactical_voice.py --lang en



pause



