@echo off
chcp 65001 >nul
echo ========================================
echo  LinguaGraph — BWKI 2026 Submission Package
echo ========================================
echo.
echo Choose an option:
echo.
echo  1. Open CognitiveSpace (3D Knowledge Graph)
echo     File: cognitive-space\web\index.html
echo.
echo  2. Open LinguaGraph Workbench (Static Dashboard)
echo     File: workbench\index.html
echo.
echo  3. START Workbench Server (Text → Analyze → 3D)
echo     Opens: http://localhost:5000
echo     Run: start_workbench.bat
echo.
echo  4. Open Paper Drafts
echo     Folder: docs\paper\
echo.
echo  5. Project Documentation
echo     File: docs\PROJECT_LOG.md
echo.
echo ========================================
echo.
set /p opt="Enter number (1-5): "
if "%opt%"=="1" start "" "cognitive-space\web\index.html"
if "%opt%"=="2" start "" "workbench\index.html"
if "%opt%"=="3" start "Workbench Server" cmd /c start_workbench.bat
if "%opt%"=="4" start "" "docs\paper\"
if "%opt%"=="5" start "" "docs\PROJECT_LOG.md"
echo.
pause
