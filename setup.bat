@echo off
title Essay Scoring System - Setup
color 0A

echo.
echo ================================================
echo  🚀 AI-Powered Essay Scoring System - Setup
echo  Author: Sardar Ahmed
echo ================================================
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo ✅ Python found!
python --version

echo.
echo 📦 Creating virtual environment...
python -m venv .venv

echo.
echo 🔌 Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo  🎉 Setup completed successfully!
echo ================================================
echo.
echo 🚀 To start the application:
echo    run_optimized_server.bat
echo.
echo 🌐 Then open: http://127.0.0.1:5000
echo.
echo ✨ Enjoy your AI-Powered Essay Scoring System!
echo ================================================
echo.
pause
