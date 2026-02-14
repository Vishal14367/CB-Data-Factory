@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Codebasics Data Factory v2.0
echo ========================================
echo.

REM Add standard paths just in case
set "PATH=%PATH%;C:\Program Files\Python312;C:\Program Files\Python312\Scripts;C:\Program Files\nodejs"

echo [1/4] Checking environment...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. I installed it in C:\Program Files\Python312.
    echo Please make sure C:\Program Files\Python312 is in your PATH.
    pause
    exit /b 1
)

node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js not found. I installed it in C:\Program Files\nodejs.
    echo Please make sure C:\Program Files\nodejs is in your PATH.
    pause
    exit /b 1
)

echo [2/4] Starting Backend (FastAPI)...
cd backend
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
echo Updating dependencies...
pip install -r requirements.txt --quiet
start "CB Data Factory - Backend" cmd /k "venv\Scripts\activate && cd src && python main.py"
cd ..

timeout /t 3 /nobreak >nul

echo [3/4] Starting Frontend (Next.js)...
cd frontend_new
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
)
start "CB Data Factory - Frontend" cmd /k "npm run dev -- -p 3000"
cd ..

echo [4/4] Launching Application...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo ========================================
echo System is now running!
echo ========================================
echo Backend:  http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo Close the two terminal windows to stop the servers.
echo.
pause
