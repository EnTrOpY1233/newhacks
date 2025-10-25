# 🔑 API 密钥获取快速参考

## 🎯 需要的 API 密钥

| API | 必需性 | 用途 | 免费额度 |
|-----|--------|------|----------|
| Google Gemini | ✅ 必需 | 生成旅行行程 | 完全免费 |
| Google Maps | ✅ 必需 | 地图显示 | $200/月 |
| ElevenLabs | ⭐ 可选 | 语音讲解 | 10,000字符/月 |

## 📋 获取链接

### 1. Google Gemini API
🔗 **获取地址**: https://makersuite.google.com/app/apikey

**步骤**:
1. 登录 Google 账号
2. 点击 "Create API Key"
3. 复制密钥

**环境变量名**: `GEMINI_API_KEY`

**配置位置**: `backend/.env`

---

### 2. Google Maps API
🔗 **获取地址**: https://console.cloud.google.com/

**步骤**:
1. 创建项目
2. 启用 API:
   - Maps JavaScript API
   - Geocoding API
   - **Places API** ⭐ (新增 - 用于 Place Picker)
3. 创建凭据 → API 密钥

**环境变量名**: 
- 后端: `GOOGLE_MAPS_API_KEY` (在 `backend/.env`)
- 前端: `VITE_GOOGLE_MAPS_API_KEY` (在 `vue-project/.env`)

**重要**: 同一个密钥需要配置在两个地方！

---

### 3. ElevenLabs API
🔗 **获取地址**: https://elevenlabs.io/

**步骤**:
1. 注册账号
2. Profile → API Keys
3. 复制密钥

**环境变量名**: `ELEVENLABS_API_KEY`

**配置位置**: `backend/.env`

**注意**: 如不配置，将使用示例音频

---

## 📝 配置检查清单

### 后端 (`backend/.env`)
```env
✅ GEMINI_API_KEY=AIza...
✅ GOOGLE_MAPS_API_KEY=AIza...
⭐ ELEVENLABS_API_KEY=sk_...
```

### 前端 (`vue-project/.env`)
```env
✅ VITE_GOOGLE_MAPS_API_KEY=AIza...
✅ VITE_API_URL=http://localhost:5000
```

## 🔒 安全提示

- ⚠️ **永远不要**将 `.env` 文件提交到 Git
- ⚠️ **不要**在代码中硬编码 API 密钥
- ⚠️ **不要**公开分享你的 API 密钥
- ✅ 使用 API 密钥限制（IP、域名等）
- ✅ 定期检查 API 使用量
- ✅ 在生产环境使用环境变量

## 💰 费用说明

### Google Gemini
- **完全免费**
- 有速率限制（60 请求/分钟）

### Google Maps
- 每月 $200 免费额度
- 动态地图: $7/1000次加载
- 地理编码: $5/1000次请求
- Places API: $17/1000次请求（自动完成）
- **对于演示和开发完全够用**

### ElevenLabs
- 免费层: 10,000 字符/月
- 约 100+ 景点讲解
- **对于演示完全够用**

## 🧪 验证 API 配置

启动后端后，访问:
```
http://localhost:5000/api/health
```

应该看到:
```json
{
  "status": "ok",
  "gemini_configured": true,
  "elevenlabs_configured": true,
  "maps_configured": true
}
```

---

**💡 提示**: 将此文件保存为书签，方便快速查找 API 获取地址！

