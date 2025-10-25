#!/bin/bash

# TripTeller 快速启动脚本

echo "🌍 启动 TripTeller - AI 语音导游"
echo "================================="
echo ""

# 检查是否在正确的目录
if [ ! -d "backend" ] || [ ! -d "vue-project" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 启动后端
echo "📡 启动 Flask 后端..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠️  未找到虚拟环境，正在创建..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install -q -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到 .env 文件，请从 env.example 复制并配置"
    echo "   cp env.example .env"
    echo "   然后编辑 .env 文件填入 API 密钥"
fi

# 后台启动 Flask
python app.py &
BACKEND_PID=$!
echo "✅ 后端已启动 (PID: $BACKEND_PID) - http://localhost:5000"

cd ..

# 启动前端
echo ""
echo "🎨 启动 Vue 前端..."
cd vue-project

# 检查 node_modules
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到前端 .env 文件，请配置 Google Maps API Key"
    echo "   cp env.example .env"
fi

echo ""
echo "================================="
echo "✨ TripTeller 启动成功！"
echo ""
echo "前端: http://localhost:5173"
echo "后端: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================="

# 启动前端开发服务器
npm run dev

