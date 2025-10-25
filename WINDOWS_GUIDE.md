# 🖥️ Windows 运行指南

本指南专门为Windows用户提供详细的运行说明，确保项目在Windows环境下正常运行。

## 📋 Windows 前置要求

### 1. 安装 Node.js
- 访问 https://nodejs.org/
- 下载并安装 LTS 版本（推荐 20.19.0 或更高）
- 安装完成后，打开命令提示符验证：
```cmd
node --version
npm --version
```

### 2. 安装 Python
- 访问 https://python.org/downloads/
- 下载并安装 Python 3.8 或更高版本
- **重要**：安装时勾选 "Add Python to PATH"
- 安装完成后验证：
```cmd
python --version
pip --version
```

## 🚀 Windows 快速启动

### 方法 1：使用批处理脚本（推荐）

1. **双击运行 `start.bat`**
   - 脚本会自动处理所有配置
   - 自动安装依赖
   - 自动启动前后端服务

2. **停止服务**
   - 双击运行 `stop.bat`
   - 或按 `Ctrl+C` 停止服务

### 方法 2：手动启动

#### 启动后端
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
REM 编辑 .env 文件添加API密钥
python app.py
```

#### 启动前端（新开命令提示符）
```cmd
cd vue-project
npm install
copy env.example .env
REM 编辑 .env 文件添加Google Maps API密钥
npm run dev
```

## 🔧 Windows 特殊配置

### 1. 环境变量配置

#### 后端环境变量 (`backend\.env`)
```env
GEMINI_API_KEY=你的_Gemini_密钥
ELEVENLABS_API_KEY=你的_ElevenLabs_密钥（可选）
GOOGLE_MAPS_API_KEY=你的_GoogleMaps_密钥
FLASK_ENV=development
FLASK_DEBUG=True
```

#### 前端环境变量 (`vue-project\.env`)
```env
VITE_GOOGLE_MAPS_API_KEY=你的_GoogleMaps_密钥
VITE_API_URL=http://localhost:5000
```

### 2. Windows 防火墙设置

如果遇到连接问题，可能需要允许Python和Node.js通过Windows防火墙：

1. 打开"Windows Defender 防火墙"
2. 点击"允许应用或功能通过Windows Defender防火墙"
3. 找到Python和Node.js，确保勾选"专用"和"公用"

### 3. 端口占用问题

如果端口被占用，Windows脚本会自动处理。也可以手动检查：

```cmd
netstat -ano | findstr :5000
netstat -ano | findstr :5173
```

## 🐛 Windows 常见问题

### 问题 1：Python 命令未找到
**解决方案**：
- 重新安装Python，确保勾选"Add Python to PATH"
- 或手动添加Python到系统PATH环境变量

### 问题 2：npm 命令未找到
**解决方案**：
- 重新安装Node.js
- 重启命令提示符

### 问题 3：虚拟环境激活失败
**解决方案**：
```cmd
cd backend
python -m venv venv --clear
venv\Scripts\activate
```

### 问题 4：权限错误
**解决方案**：
- 以管理员身份运行命令提示符
- 或使用PowerShell替代命令提示符

### 问题 5：编码问题
**解决方案**：
- 确保命令提示符使用UTF-8编码
- Windows脚本已设置 `chcp 65001` 来处理中文显示

## 📁 Windows 项目结构

```
newhacks/
├── start.bat              # Windows启动脚本
├── stop.bat               # Windows停止脚本
├── start.sh               # Linux/Mac启动脚本
├── stop.sh                # Linux/Mac停止脚本
├── backend/
│   ├── venv/              # Python虚拟环境
│   │   └── Scripts/       # Windows激活脚本
│   ├── app.py
│   ├── requirements.txt
│   └── .env               # 后端环境变量
└── vue-project/
    ├── node_modules/      # Node.js依赖
    ├── package.json
    └── .env               # 前端环境变量
```

## ✅ Windows 验证步骤

1. **检查后端**：访问 http://localhost:5000/api/health
2. **检查前端**：访问 http://localhost:5173
3. **测试功能**：输入城市名称，测试AI生成功能

## 🔄 从Linux迁移到Windows

如果你之前在Linux上运行过项目：

1. **保留配置文件**：`.env` 文件可以直接使用
2. **重新安装依赖**：Windows脚本会自动处理
3. **使用Windows脚本**：`start.bat` 和 `stop.bat`

## 📞 Windows 技术支持

- 确保使用最新版本的Node.js和Python
- 如果遇到问题，查看命令提示符的错误信息
- Windows脚本包含详细的错误处理和提示信息

---

**🎯 Windows用户现在可以像Linux用户一样轻松运行TripTeller项目！**
