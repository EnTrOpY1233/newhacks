#!/bin/bash

# TripTeller 停止脚本

echo "🛑 Stopping TripTeller services..."
echo "================================="

# 关闭 Flask 后端 (端口 5000)
PORT_5000_PID=$(lsof -ti:5000 2>/dev/null)
if [ ! -z "$PORT_5000_PID" ]; then
    echo "   Stopping Flask backend (Port 5000, PID: $PORT_5000_PID)"
    kill -9 $PORT_5000_PID 2>/dev/null
    echo "   ✅ Backend stopped"
else
    echo "   ℹ️  No backend process found on port 5000"
fi

# 关闭 Vite 前端 (端口 5173)
PORT_5173_PID=$(lsof -ti:5173 2>/dev/null)
if [ ! -z "$PORT_5173_PID" ]; then
    echo "   Stopping Vite dev server (Port 5173, PID: $PORT_5173_PID)"
    kill -9 $PORT_5173_PID 2>/dev/null
    echo "   ✅ Frontend stopped (port 5173)"
else
    echo "   ℹ️  No frontend process found on port 5173"
fi

# 关闭 Vite 前端 (端口 5174)
PORT_5174_PID=$(lsof -ti:5174 2>/dev/null)
if [ ! -z "$PORT_5174_PID" ]; then
    echo "   Stopping Vite dev server (Port 5174, PID: $PORT_5174_PID)"
    kill -9 $PORT_5174_PID 2>/dev/null
    echo "   ✅ Frontend stopped (port 5174)"
fi

# 通过进程名额外清理
pkill -f "python app.py" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo ""
echo "✅ All TripTeller services stopped!"
echo "================================="


