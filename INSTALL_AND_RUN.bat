@echo off
echo ========================================
echo Data Challenge Generator - Auto Setup
echo ========================================
echo.

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo Opening Python download page in your browser...
    echo Please install Python and check "Add Python to PATH"
    echo Then run this script again.
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Python found!
python --version
echo.

REM Check if Node.js is installed
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Node.js is not installed or not in PATH.
    echo.
    echo Opening Node.js download page in your browser...
    echo Please install Node.js (LTS version)
    echo Then run this script again.
    echo.
    start https://nodejs.org/
    pause
    exit /b 1
)

echo [2/5] Node.js found!
node --version
echo.

REM Setup backend
echo [3/5] Setting up backend...
cd backend

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
echo Installing Python packages...
pip install -r requirements.txt --quiet --disable-pip-version-check

cd ..
echo Backend ready!
echo.

REM Setup frontend
echo [4/5] Setting up frontend...
cd frontend

if not exist "node_modules\" (
    echo Installing Node packages (this may take a minute)...
    call npm install --silent
)

cd ..
echo Frontend ready!
echo.

REM Start both servers
echo [5/5] Starting servers...
echo.
echo Backend will run on: http://127.0.0.1:8000
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C in either window to stop.
echo.
pause

REM Open two command windows
start "Backend Server" cmd /k "cd backend && venv\Scripts\activate && cd src && python main.py"
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Servers are starting!
echo ========================================
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul
start http://localhost:3000

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
pause
