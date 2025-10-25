@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM TripTeller Windows 快速启动脚本

echo 🌍 Starting TripTeller - AI Travel Guide
echo =================================
echo.

REM 检查是否在正确的目录
if not exist "backend" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)
if not exist "vue-project" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

REM 🧹 清理之前的进程
echo 🧹 Cleaning up old processes...

REM 关闭占用 5000 端口的进程（Flask 后端）
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000') do (
    echo    Stopping Flask backend (Port 5000, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
)

REM 关闭占用 5173 和 5174 端口的进程（Vite 前端）
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
    echo    Stopping Vite dev server (Port 5173, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
)

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5174') do (
    echo    Stopping Vite dev server (Port 5174, PID: %%a)
    taskkill /PID %%a /F >nul 2>&1
)

REM 额外保险：通过进程名关闭
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

timeout /t 1 /nobreak >nul
echo ✅ Cleanup complete!
echo.

REM 启动后端
echo 📡 Starting Flask backend...
cd backend

REM 检查虚拟环境
if not exist "venv" (
    echo ⚠️  Creating virtual environment...
    python -m venv venv
)

REM 激活虚拟环境并安装依赖
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM 检查 .env 文件
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo    Run: copy env.example .env
    echo    Then edit .env to add your API keys
)

REM 后台启动 Flask
echo    Starting Flask server...
start /B python app.py
timeout /t 3 /nobreak >nul

REM 检查后端是否启动成功
curl -s http://localhost:5000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Backend started successfully - http://localhost:5000
) else (
    echo ⚠️  Backend may not be ready yet, please wait...
)

cd ..

REM 启动前端
echo.
echo 🎨 Starting Vue frontend...
cd vue-project

REM 检查 node_modules
if not exist "node_modules" (
    echo 📦 Installing frontend dependencies...
    npm install
)

REM 检查 .env 文件
if not exist ".env" (
    echo ⚠️  Warning: frontend .env file not found
    echo    Run: copy env.example .env
)

echo.
echo =================================
echo ✨ TripTeller Started Successfully!
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:5000
echo.
echo Press Ctrl+C to stop servers
echo =================================

REM 启动前端开发服务器
npm run dev
