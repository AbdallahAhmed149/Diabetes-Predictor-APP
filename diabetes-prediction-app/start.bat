@echo off
echo.
echo ========================================
echo    Diabetes Prediction Application
echo    Quick Start Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not running.
    echo Please install Docker Desktop and try again.
    pause
    exit /b 1
)

echo [2/3] Creating environment file...
if not exist .env (
    copy .env.example .env
    echo Environment file created.
) else (
    echo Environment file already exists.
)

echo [3/3] Starting all services...
echo This may take several minutes on first run...
echo.
docker-compose up --build

pause
