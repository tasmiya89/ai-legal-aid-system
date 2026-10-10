@echo off
chcp 65001 >nul
REM ═══════════════════════════════════════════════════════════════════════
REM  AI Legal Aid Multi-Agent System - Windows Launcher
REM  Powered by IBM Granite LLM | IBM watsonx.ai
REM ═══════════════════════════════════════════════════════════════════════

title AI Legal Aid System — IBM Granite

echo.
echo  ============================================================
echo   AI Legal Aid Multi-Agent System
echo   Powered by IBM Granite LLM ^| IBM watsonx.ai
echo  ============================================================
echo.

REM ── Check Python is available ─────────────────────────────────────────
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python 3.9+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo  [OK] Python found.
python --version

REM ── Create virtual environment if it doesn't exist ────────────────────
if not exist ".venv" (
    echo.
    echo  [SETUP] Creating Python virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo  [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created.
)

REM ── Activate virtual environment ──────────────────────────────────────
echo.
echo  [SETUP] Activating virtual environment...
call .venv\Scripts\activate.bat

REM ── Install / update dependencies ────────────────────────────────────
echo.
echo  [SETUP] Installing required dependencies...
echo  (This may take a few minutes on first run)
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Failed to install dependencies.
    echo  Please check your internet connection and requirements.txt
    pause
    exit /b 1
)
echo  [OK] All dependencies installed.

REM ── Check .env file ───────────────────────────────────────────────────
echo.
if not exist ".env" (
    echo  [WARNING] .env file not found. Creating from .env.example...
    copy .env.example .env >nul
    echo  [INFO] Please edit .env and add your IBM watsonx.ai credentials.
    echo  [INFO] Running in DEMO MODE until credentials are configured.
) else (
    echo  [OK] .env file found.
)

REM ── Display configuration info ────────────────────────────────────────
echo.
echo  ============================================================
echo   Configuration
echo  ============================================================
echo   - Edit .env to add your IBM watsonx.ai API key
echo   - Get a free IBM Cloud account: https://cloud.ibm.com
echo   - Get your API key: https://cloud.ibm.com/iam/apikeys
echo   - Set DEMO_MODE=false in .env to enable live AI responses
echo  ============================================================

REM ── Start Flask application ───────────────────────────────────────────
echo.
echo  [START] Launching AI Legal Aid System...
echo.
echo  ============================================================
echo   Open your browser at: http://127.0.0.1:5000
echo   Press Ctrl+C to stop the server
echo  ============================================================
echo.

set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM NOTE: No log files are created — output goes directly to this window.
REM       server_out.log / server_err.log should NEVER appear in this project.
python app.py

REM ── If the server exits ───────────────────────────────────────────────
echo.
echo  [INFO] Server stopped.
pause
