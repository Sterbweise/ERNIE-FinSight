#!/bin/bash

echo "========================================"
echo "  ERNIE FinSight - Crypto Whitepaper Analyzer"
echo "  Starting Backend and Frontend..."
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "WARNING: backend/.env file not found!"
    echo "Please create backend/.env with your NOVITA_API_KEY"
    echo ""
    echo "Example:"
    echo "NOVITA_API_KEY=your_key_here"
    echo "MAX_FILE_SIZE_MB=10"
    echo "UPLOAD_DIR=./uploads"
    echo ""
    read -p "Press Enter to continue..."
fi

# Create uploads directory if it doesn't exist
mkdir -p backend/uploads

echo ""
echo "[1/4] Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install backend dependencies"
    exit 1
fi

echo "[2/4] Installing frontend dependencies..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    npm install
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install frontend dependencies"
        exit 1
    fi
else
    echo "Frontend dependencies already installed"
fi

echo ""
echo "[3/4] Starting Backend Server..."
cd ../backend
python3 main.py &
BACKEND_PID=$!
sleep 3

echo "[4/4] Starting Frontend Server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  ERNIE FinSight is Running!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

