@echo off
echo Setting up TECHBEAT...

:: Get Desktop path
set DESKTOP=%USERPROFILE%\Desktop
set TARGET=%DESKTOP%\TECHBEAT

:: Create folder if not exists
if not exist "%TARGET%" mkdir "%TARGET%"

:: Download v2.py using PowerShell (IWR)
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/KTGP007/TECHBEAT26/main/v2.py' -OutFile '%TARGET%\v2.py'"

echo.
echo Done! File downloaded to %TARGET%
pause
