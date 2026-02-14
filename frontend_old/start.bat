@echo off
echo Starting Data Challenge Generator Frontend...
echo.

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting Vite dev server...
echo Frontend will be available at: http://localhost:3000
echo.
call npm run dev
