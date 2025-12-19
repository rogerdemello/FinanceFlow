#!/bin/bash

echo "Starting Personal Finance Assistant Web UI..."
echo ""

echo "[1/2] Starting Backend API..."
cd backend
python main.py &
BACKEND_PID=$!
cd ..

sleep 3

echo "[2/2] Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo " Personal Finance Assistant is running!"
echo "========================================"
echo ""
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
