# TripTeller Backend API

Flask 后端服务，提供 AI 旅行规划、语音生成等功能。

## 功能

- 🗺️ 使用 Gemini AI 生成旅行行程
- 🔊 使用 ElevenLabs 生成景点语音讲解
- 🎨 生成目的地海报图片（可选）
- 📍 Google Maps 集成

## 安装步骤

### 1. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入以下信息：

- **GEMINI_API_KEY**: 从 [Google AI Studio](https://makersuite.google.com/app/apikey) 获取
- **ELEVENLABS_API_KEY**: 从 [ElevenLabs](https://elevenlabs.io/) 获取
- **GOOGLE_MAPS_API_KEY**: 从 [Google Cloud Console](https://console.cloud.google.com/) 获取

### 4. 运行服务器

```bash
python app.py
```

服务器将在 `http://localhost:5000` 启动

## API 接口

### 1. 健康检查

```
GET /api/health
```

### 2. 生成行程

```
POST /api/generate-itinerary
Content-Type: application/json

{
    "city": "Tokyo",
    "days": 3
}
```

### 3. 生成语音

```
POST /api/generate-audio
Content-Type: application/json

{
    "place_name": "东京塔",
    "description": "东京的标志性建筑..."
}
```

### 4. 生成海报

```
POST /api/generate-poster
Content-Type: application/json

{
    "city": "Paris"
}
```

## 开发模式

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## 生产部署

使用 Gunicorn：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 注意事项

- 确保所有 API 密钥都已正确配置
- ElevenLabs 有免费额度限制，注意使用量
- Google Maps API 需要启用 Maps JavaScript API 和 Geocoding API
- Gemini API 目前免费使用，但有速率限制

## 故障排除

### 问题：CORS 错误

确保 `flask-cors` 已安装并在 `app.py` 中启用。

### 问题：API 密钥无效

检查 `.env` 文件中的密钥是否正确，并确保已加载环境变量。

### 问题：音频生成失败

检查 ElevenLabs API 配额，确保账户有足够的额度。

