@echo off
chcp 65001 >nul
echo ========================================
echo  LinguaGraph Processing Workbench
echo ========================================
echo.
echo  Starting server...
echo.
echo  Open http://localhost:5000 in your browser
echo  Press Ctrl+C to stop
echo ========================================
echo.

C:\Users\rongj\AppData\Local\Programs\Python\Python312\python.exe "%~dp0workbench\server.py"
pause
