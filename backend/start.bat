@echo off
echo Starting Data Challenge Generator Backend...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.

REM Check if .env exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your Anthropic API key.
    echo.
    pause
    exit /b 1
)

REM Start the server
echo Starting FastAPI server...
echo Server will be available at: http://127.0.0.1:8000
echo API documentation at: http://127.0.0.1:8000/docs
echo.
cd src
python main.py
