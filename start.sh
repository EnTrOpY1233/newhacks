#!/bin/bash

# TripTeller 快速启动脚本

echo "🌍 Starting TripTeller - AI Travel Guide"
echo "================================="
echo ""

# 检查是否在正确的目录
if [ ! -d "backend" ] || [ ! -d "vue-project" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# 🧹 清理之前的进程
echo "🧹 Cleaning up old processes..."

# 关闭占用 5000 端口的进程（Flask 后端）
PORT_5000_PID=$(lsof -ti:5000 2>/dev/null)
if [ ! -z "$PORT_5000_PID" ]; then
    echo "   Stopping Flask backend (Port 5000, PID: $PORT_5000_PID)"
    kill -9 $PORT_5000_PID 2>/dev/null
fi

# 关闭占用 5173 和 5174 端口的进程（Vite 前端）
PORT_5173_PID=$(lsof -ti:5173 2>/dev/null)
if [ ! -z "$PORT_5173_PID" ]; then
    echo "   Stopping Vite dev server (Port 5173, PID: $PORT_5173_PID)"
    kill -9 $PORT_5173_PID 2>/dev/null
fi

PORT_5174_PID=$(lsof -ti:5174 2>/dev/null)
if [ ! -z "$PORT_5174_PID" ]; then
    echo "   Stopping Vite dev server (Port 5174, PID: $PORT_5174_PID)"
    kill -9 $PORT_5174_PID 2>/dev/null
fi

# 额外保险：通过进程名关闭
pkill -f "python app.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

sleep 1
echo "✅ Cleanup complete!"
echo ""

# 启动后端
echo "📡 Starting Flask backend..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠️  Creating virtual environment..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Run: cp env.example .env"
    echo "   Then edit .env to add your API keys"
fi

# 后台启动 Flask
python app.py &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) - http://localhost:5000"

cd ..

# 启动前端
echo ""
echo "🎨 Starting Vue frontend..."
cd vue-project

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: frontend .env file not found"
    echo "   Run: cp env.example .env"
fi

echo ""
echo "================================="
echo "✨ TripTeller Started Successfully!"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop servers"
echo "================================="

# 启动前端开发服务器
npm run dev

