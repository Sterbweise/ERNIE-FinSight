@echo off
echo ========================================
echo   ERNIE FinSight - Crypto Whitepaper Analyzer
echo   Starting Backend and Frontend...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if backend .env exists
if not exist "backend\.env" (
    echo.
    echo WARNING: backend/.env file not found!
    echo Please create backend/.env with your NOVITA_API_KEY
    echo.
    echo Example:
    echo NOVITA_API_KEY=your_key_here
    echo MAX_FILE_SIZE_MB=10
    echo UPLOAD_DIR=./uploads
    echo.
    pause
)

REM Create uploads directory if it doesn't exist
if not exist "backend\uploads" mkdir "backend\uploads"

echo.
echo [1/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)

echo [2/4] Installing frontend dependencies...
cd ..\frontend
if not exist "node_modules" (
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
) else (
    echo Frontend dependencies already installed
)

echo.
echo [3/4] Starting Backend Server...
cd ..\backend
start "ERNIE FinSight Backend" cmd /k "python main.py"
timeout /t 3 /nobreak >nul

echo [4/4] Starting Frontend Server...
cd ..\frontend
start "ERNIE FinSight Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   ERNIE FinSight is Starting!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo The application will open in new windows.
echo Wait a few seconds for servers to start...
echo.
echo Press any key to close this window (servers will keep running)
pause >nul

