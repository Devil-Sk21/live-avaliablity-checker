@echo off
echo Stopping background stock sniper...
taskkill /f /im python.exe /fi "WINDOWTITLE eq *" >nul 2>&1
echo Done!
pause
