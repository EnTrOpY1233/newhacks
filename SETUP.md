# 🚀 TripTeller 安装配置指南

完整的步骤说明，帮助你快速启动 TripTeller 项目。

## 📋 前置要求检查

### 1. Node.js
```bash
node --version  # 应该 >= 20.19.0
npm --version
```
test adawadaw
如果没安装：
- 访问 https://nodejs.org/
- 下载并安装 LTS 版本

### 2. Python
```bash
python3 --version  # 应该 >= 3.8
pip3 --version
```

如果没安装：
- **Linux/Mac**: 使用系统包管理器（apt, brew）
- **Windows**: 访问 https://python.org/downloads/

## 🔑 第一步：获取 API 密钥

### 1. Google Gemini API（必需）

**用途**：生成旅行行程

**步骤**：
1. 访问 https://makersuite.google.com/app/apikey
2. 使用 Google 账号登录
3. 点击 "Create API Key"
4. 选择项目或创建新项目
5. 复制生成的 API 密钥

**费用**：✅ 完全免费（有速率限制）

### 2. Google Maps API（必需）

**用途**：显示地图和景点位置

**步骤**：
1. 访问 https://console.cloud.google.com/
2. 创建新项目或选择现有项目
3. 启用以下 API：
   - **Maps JavaScript API**
   - **Geocoding API**
4. 前往 "凭据" > "创建凭据" > "API 密钥"
5. 复制 API 密钥
6. （可选）设置 API 密钥限制以提高安全性

**费用**：✅ 有免费额度（$200/月）

### 3. ElevenLabs API（可选）

**用途**：生成景点语音讲解

**步骤**：
1. 访问 https://elevenlabs.io/
2. 注册账号
3. 进入 "Profile" > "API Keys"
4. 复制 API 密钥

**费用**：✅ 有免费额度（10,000 字符/月）

**注意**：如果不配置此 API，语音功能将使用示例音频。

## 💾 第二步：配置项目

### 1. 后端配置

```bash
cd backend

# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件（使用你喜欢的编辑器）
nano .env
# 或
vim .env
# 或
code .env
```

在 `.env` 文件中填入：

```env
GEMINI_API_KEY=你的_Gemini_密钥
ELEVENLABS_API_KEY=你的_ElevenLabs_密钥（可选）
GOOGLE_MAPS_API_KEY=你的_GoogleMaps_密钥
FLASK_ENV=development
FLASK_DEBUG=True
```

### 2. 前端配置

```bash
cd ../vue-project

# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件
nano .env
```

在 `.env` 文件中填入：

```env
VITE_GOOGLE_MAPS_API_KEY=你的_GoogleMaps_密钥
VITE_API_URL=http://localhost:5000
```

## 📦 第三步：安装依赖

### 1. 后端依赖

```bash
cd backend

# 创建 Python 虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 前端依赖

```bash
cd ../vue-project

# 安装 npm 包
npm install
```

## 🎮 第四步：启动项目

### 方法 1：使用启动脚本（推荐）

#### Linux/Mac 用户
```bash
cd newhacks
chmod +x start.sh
./start.sh
```

#### Windows 用户
```cmd
cd newhacks
start.bat
```

### 方法 2：手动启动

**终端 1 - 启动后端**：
```bash
cd backend
source venv/bin/activate  # Linux/Mac - 激活虚拟环境
# 或 venv\Scripts\activate  # Windows - 激活虚拟环境
python app.py
```

**终端 2 - 启动前端**：
```bash
cd vue-project
npm run dev
```

## 🌐 第五步：访问应用

打开浏览器访问：
- **前端界面**: http://localhost:5173
- **后端 API**: http://localhost:5000
- **健康检查**: http://localhost:5000/api/health

## ✅ 验证安装

### 1. 检查后端

访问 http://localhost:5000/api/health

应该看到类似输出：
```json
{
  "status": "ok",
  "gemini_configured": true,
  "elevenlabs_configured": true,
  "maps_configured": true
}
```

### 2. 测试功能

1. 在前端输入框输入 "Tokyo"
2. 点击 "🔍 搜索"
3. 等待 AI 生成行程（5-10秒）
4. 查看行程列表和地图
5. 点击任意景点的 "🔊 播放讲解"

## 🐛 常见问题

### 问题 1：后端启动失败

**错误**: `ModuleNotFoundError`

**解决**:
```bash
# 确保虚拟环境已激活
source venv/bin/activate
# 重新安装依赖
pip install -r requirements.txt
```

### 问题 2：前端无法连接后端

**错误**: 浏览器控制台显示 CORS 错误

**解决**:
1. 确认后端正在运行
2. 检查前端 `.env` 中的 `VITE_API_URL`
3. 确认 flask-cors 已安装

### 问题 3：地图不显示

**可能原因**:
- Google Maps API Key 未配置
- API 未启用

**解决**:
1. 检查 `.env` 文件中的 API 密钥
2. 访问 Google Cloud Console 确认已启用 Maps JavaScript API
3. 查看浏览器控制台是否有错误信息

### 问题 4：语音生成失败

**如果显示**："ElevenLabs API未配置"

**这是正常的**！语音功能是可选的，不配置会使用示例音频。

**如需启用**：
1. 获取 ElevenLabs API 密钥
2. 添加到后端 `.env` 文件
3. 重启后端服务器

### 问题 5：AI 生成失败

**错误**: "生成行程失败"

**检查**:
1. Gemini API Key 是否正确
2. 网络是否可以访问 Google AI 服务
3. 查看后端日志获取详细错误信息

## 🎯 下一步

- 📖 阅读完整文档：`README.md`
- 🔧 自定义配置：修改行程天数、地图样式、语音选项
- 🚀 部署到生产：参考 `backend/README.md`

## 📞 获取帮助

- 查看项目 Issues
- 阅读 API 文档
- 检查后端日志：`backend/app.py` 的输出

---

**祝你使用愉快！如有问题，随时查看文档或提交 Issue。**

