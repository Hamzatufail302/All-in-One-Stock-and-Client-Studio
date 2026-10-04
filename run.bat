@echo off
title All-In-One Stock & Client Studio
echo ========================================================
echo   All-In-One Stock & Client Studio
echo ========================================================
echo.
echo Starting local web server on http://localhost:8000 ...
echo.
start "" http://localhost:8000
where py >nul 2>nul
if %errorlevel% equ 0 (
    py app.py
) else (
    python app.py
)
pause
