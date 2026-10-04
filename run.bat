@echo off
title StockPulse AI - Keywords & Trends Crawler
echo ========================================================
echo   StockPulse AI - Stock & Digital Product Intelligence
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
