@echo off
echo Starting Personal Finance Assistant Web UI...
echo.

echo [1/2] Starting Backend API...
start "Backend API" cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend...
start "Frontend UI" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo  Personal Finance Assistant is starting!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:5173
echo.
echo Press any key to open browser...
pause > nul

start http://localhost:5173
