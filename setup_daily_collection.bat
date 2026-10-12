@echo off
rem Registers two Windows scheduled tasks that save the Ben Gurion flight board
rem twice a day (07:30 and 19:30). Run once by double-clicking.
rem To remove:  schtasks /Delete /TN orit-flights-collect-morning /F
rem             schtasks /Delete /TN orit-flights-collect-evening /F

set PY=C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe
set SCRIPT=%~dp0collect.py

schtasks /Create /TN "orit-flights-collect-morning" /TR "\"%PY%\" -X utf8 \"%SCRIPT%\"" /SC DAILY /ST 07:30 /F
schtasks /Create /TN "orit-flights-collect-evening" /TR "\"%PY%\" -X utf8 \"%SCRIPT%\"" /SC DAILY /ST 19:30 /F

echo.
echo Running one collection now to check that it works...
"%PY%" -X utf8 "%SCRIPT%"
echo.
echo Done. You can close this window.
pause
