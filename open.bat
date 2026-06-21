@echo off
echo ========================================
echo  LinguaGraph — BWKI 2026 Submission Package
echo ========================================
echo.
echo Choose an option:
echo.
echo  1. Open CognitiveSpace (3D Knowledge Graph)
echo     File: cognitive-space\web\index.html
echo.
echo  2. Open LinguaGraph Research Workbench
echo     File: workbench\index.html
echo.
echo  3. Open Paper Drafts
echo     Folder: docs\paper\
echo.
echo  4. Project Documentation
echo     File: docs\PROJECT_LOG.md
echo.
echo ========================================
echo.
set /p opt="Enter number (1-4): "
if "%opt%"=="1" start "" "cognitive-space\web\index.html"
if "%opt%"=="2" start "" "workbench\index.html"
if "%opt%"=="3" start "" "docs\paper\"
if "%opt%"=="4" start "" "docs\PROJECT_LOG.md"
echo.
pause
