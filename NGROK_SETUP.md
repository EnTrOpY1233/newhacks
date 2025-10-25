# 🌐 ngrok 内网穿透设置指南

## 概述

通过 ngrok，您可以让外网用户访问运行在本地的 TripTeller 应用。

---

## ✅ 已完成的配置

- ✅ ngrok 已安装
- ✅ API token 已配置
- ✅ 配置文件已创建 (`ngrok.yml`)
- ✅ 启动脚本已准备好

---

## 🚀 快速开始

### 步骤 1: 启动应用服务

**在终端 1 - 启动后端和前端**:
```bash
cd /home/grealish/newhacks
./start.sh
```

等待服务启动完成，确认：
- ✅ Backend: http://localhost:5000
- ✅ Frontend: http://localhost:5173

---

### 步骤 2: 启动 ngrok 隧道

**在终端 2 - 启动 ngrok**:
```bash
cd /home/grealish/newhacks
./start-ngrok.sh
```

您会看到 ngrok 界面，显示两个公网 URL：
```
Session Status    online
Account           your-account
Version           3.x.x

Forwarding        https://xxxx-xx-xx-xxx-xx.ngrok-free.app -> http://localhost:5173
Forwarding        https://yyyy-yy-yy-yyy-yy.ngrok-free.app -> http://localhost:5000
```

---

### 步骤 3: 获取 ngrok URL

**在终端 3 - 查看 URL**:
```bash
cd /home/grealish/newhacks
./get-ngrok-urls.sh
```

这会显示：
- 🎨 **Frontend URL**: 前端公网访问地址
- 📡 **Backend URL**: 后端 API 公网地址

---

### 步骤 4: 更新前端配置（重要！）

**自动更新**（推荐）:
```bash
cd /home/grealish/newhacks
./update-frontend-url.sh
```

**然后重启前端**:
```bash
# 在前端终端按 Ctrl+C 停止
cd vue-project
npm run dev
```

---

## 📋 三种访问模式

### 模式 1: 本地访问（默认）
- 前端: http://localhost:5173
- 后端: http://localhost:5000
- **适合**: 本地开发和测试

### 模式 2: 前端外网访问 + 本地后端
- 前端: https://xxxx.ngrok-free.app
- 后端: http://localhost:5000
- **问题**: 外网用户无法访问后端
- **不推荐**: 功能不完整

### 模式 3: 全外网访问（推荐用于演示）
- 前端: https://xxxx.ngrok-free.app
- 后端: https://yyyy.ngrok-free.app
- **适合**: 向外部用户展示、远程演示
- **需要**: 运行 `./update-frontend-url.sh` 并重启前端

---

## 🎯 完整操作流程

```bash
# 终端 1: 启动应用
cd /home/grealish/newhacks
./start.sh

# 终端 2: 启动 ngrok
cd /home/grealish/newhacks
./start-ngrok.sh

# 终端 3: 获取 URL 并更新配置
cd /home/grealish/newhacks
./get-ngrok-urls.sh
./update-frontend-url.sh

# 然后返回终端 1，重启前端（Ctrl+C 后重新运行）
cd vue-project
npm run dev
```

---

## 🌐 访问您的应用

### 本地访问
- **前端**: http://localhost:5173
- **后端**: http://localhost:5000/api/health

### 外网访问（ngrok URL）
- **前端**: https://xxxx-xxxx-xxxx.ngrok-free.app
- **后端**: https://yyyy-yyyy-yyyy.ngrok-free.app/api/health

### ngrok Web 界面
- **管理界面**: http://localhost:4040
- **功能**: 查看请求日志、流量统计、重放请求

---

## 📊 可用脚本

| 脚本 | 功能 | 用法 |
|------|------|------|
| `start-ngrok.sh` | 启动 ngrok 隧道 | `./start-ngrok.sh` |
| `get-ngrok-urls.sh` | 显示当前 ngrok URL | `./get-ngrok-urls.sh` |
| `update-frontend-url.sh` | 更新前端配置使用 ngrok 后端 | `./update-frontend-url.sh` |

---

## 🔍 验证设置

### 1. 检查后端健康状态
```bash
# 本地
curl http://localhost:5000/api/health

# ngrok（替换为您的实际 URL）
curl https://yyyy-yyyy-yyyy.ngrok-free.app/api/health
```

### 2. 检查前端配置
```bash
cat vue-project/.env
# 应该显示：
# VITE_API_URL=https://yyyy-yyyy-yyyy.ngrok-free.app
```

### 3. 测试地点确认功能
1. 访问前端 ngrok URL
2. 输入城市名称（如 "Tokyo"）
3. 点击 Search
4. 检查是否成功调用后端 API

---

## ⚠️ 重要注意事项

### ngrok 免费版限制
- ✅ 每次启动 URL 会变化
- ✅ 每分钟 40 个请求限制
- ✅ 会显示 ngrok 警告页面（可跳过）
- ⚠️ 隧道空闲 8 小时后断开

### 安全建议
- 🔒 不要公开分享 ngrok authtoken
- 🔒 演示结束后关闭 ngrok
- 🔒 不要在生产环境使用 ngrok

### CORS 问题
- ✅ Flask 已配置 CORS，无需额外设置
- ✅ 支持跨域请求

---

## 🛠️ 故障排查

### 问题 1: ngrok 启动失败
```bash
# 检查 authtoken 是否配置
cat ~/.config/ngrok/ngrok.yml

# 重新配置
ngrok config add-authtoken 34ZhRleGd8RCQo2sIxZ2q7TtDwQ_7TFhsRLgWbg33Sf3E8XGH
```

### 问题 2: 前端无法连接后端
```bash
# 1. 确认后端 URL 正确
./get-ngrok-urls.sh

# 2. 更新前端配置
./update-frontend-url.sh

# 3. 重启前端
cd vue-project && npm run dev
```

### 问题 3: 外网访问显示 502
- 确认本地服务正在运行
- 检查端口是否正确（前端 5173，后端 5000）

### 问题 4: ngrok URL 变化了
```bash
# 每次重启 ngrok，URL 都会变化
# 需要重新运行：
./update-frontend-url.sh
# 然后重启前端
```

---

## 📝 配置文件说明

### `ngrok.yml`
```yaml
version: "2"
authtoken: YOUR_TOKEN_HERE

tunnels:
  frontend:
    addr: 5173      # Vue 前端端口
    proto: http
    
  backend:
    addr: 5000      # Flask 后端端口
    proto: http
```

### `vue-project/.env`
```bash
# 本地开发
VITE_API_URL=http://localhost:5000

# 外网访问（ngrok）
VITE_API_URL=https://yyyy-yyyy-yyyy.ngrok-free.app
```

---

## 🎓 演示场景

### 场景 1: 本地演示
直接使用 localhost，无需 ngrok

### 场景 2: 远程演示 / Hackathon 评审
1. 启动 ngrok
2. 分享前端 ngrok URL
3. 评委可以直接访问

### 场景 3: 移动设备测试
1. 启动 ngrok
2. 在手机上访问 ngrok URL
3. 测试响应式设计

---

## 📱 分享给他人

当您想让别人访问您的应用时：

1. **启动所有服务** (应用 + ngrok)
2. **获取 URL**:
   ```bash
   ./get-ngrok-urls.sh
   ```
3. **分享前端 URL**:
   ```
   🌐 请访问: https://xxxx-xxxx-xxxx.ngrok-free.app
   ```
4. **注意**: 确保前端已配置使用 ngrok 后端 URL

---

## 🔄 停止 ngrok

**停止 ngrok**:
- 在 ngrok 终端按 `Ctrl+C`

**恢复本地配置**:
```bash
# 编辑 vue-project/.env
VITE_API_URL=http://localhost:5000

# 重启前端
cd vue-project && npm run dev
```

---

## 💡 小贴士

### 保持 URL 稳定（付费功能）
升级到 ngrok 付费版本可以获得：
- 固定的自定义域名
- 更高的请求限制
- 更多并发隧道

### 快速切换配置
创建两个 .env 文件：
- `.env.local` - 本地开发配置
- `.env.ngrok` - ngrok 配置

```bash
# 使用本地配置
cp .env.local vue-project/.env

# 使用 ngrok 配置
cp .env.ngrok vue-project/.env
```

---

## ✅ 检查清单

使用前确认：
- [ ] 后端运行在 http://localhost:5000
- [ ] 前端运行在 http://localhost:5173
- [ ] ngrok 已启动并显示两个 URL
- [ ] 运行了 `./update-frontend-url.sh`
- [ ] 重启了前端服务
- [ ] 测试后端健康检查 API
- [ ] 测试前端页面加载
- [ ] 测试地点确认功能

---

## 🎉 完成！

您的 TripTeller 应用现在可以通过外网访问了！

**前端 URL**: 分享给用户访问  
**后端 URL**: API 端点（前端会自动使用）  
**管理界面**: http://localhost:4040（仅本地）

享受您的全球可访问的 AI 旅行助手！🌍✈️


