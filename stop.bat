@echo off
chcp 65001 >nul

REM TripTeller Windows 停止脚本

echo 🛑 Stopping TripTeller services...
echo =================================

REM 关闭 Flask 后端 (端口 5000)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    echo    Stopping Flask backend (Port 5000, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
    echo    ✅ Backend stopped
)

REM 检查是否还有后端进程
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    echo    ℹ️  Backend process still running on port 5000
    goto :check_frontend
)
echo    ℹ️  No backend process found on port 5000

:check_frontend
REM 关闭 Vite 前端 (端口 5173)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
    echo    Stopping Vite dev server (Port 5173, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
    echo    ✅ Frontend stopped (port 5173)
)

REM 关闭 Vite 前端 (端口 5174)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5174') do (
    echo    Stopping Vite dev server (Port 5174, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
    echo    ✅ Frontend stopped (port 5174)
)

REM 通过进程名额外清理
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

echo.
echo ✅ All TripTeller services stopped!
echo =================================

pause
