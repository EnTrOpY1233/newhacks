# 🚀 ngrok 快速开始

## ✅ 您的固定域名

**域名**: `tonisha-chiropodical-sharonda.ngrok-free.dev`

这是您的专属域名，每次使用时 URL 都不会变！

---

## 三步启动外网访问

### 📋 第一步：启动应用（终端 1）
```bash
cd /home/grealish/newhacks
./start.sh
```
等待看到：
- ✅ Backend: http://localhost:5000
- ✅ Frontend: http://localhost:5173

---

### 🌐 第二步：启动 ngrok（终端 2）

**使用固定域名**（推荐）:
```bash
cd /home/grealish/newhacks
./start-ngrok-frontend.sh
```

**或者使用随机域名**:
```bash
ngrok http 5173
```

**保持这个终端运行！不要关闭！**

您的应用将在以下地址可用：
- 固定域名: `https://tonisha-chiropodical-sharonda.ngrok-free.dev`
- 或随机域名: `https://xxxx-xxxx.ngrok-free.app`（每次都会变）

---

### 🔧 第三步：完成！

**如果使用固定域名**: 已完成！直接访问：
```
https://tonisha-chiropodical-sharonda.ngrok-free.dev
```

**如果使用随机域名**: 需要配置后端（如果需要完整功能）
```bash
cd /home/grealish/newhacks

# 查看 ngrok URLs
./get-ngrok-urls.sh

# 如果需要完整功能，更新前端配置
./update-frontend-url.sh

# 然后重启前端
```

---

## ✅ 验证成功

### 检查后端
```bash
# 复制您的后端 ngrok URL 并访问
curl https://YOUR-BACKEND-URL.ngrok-free.app/api/health
```

### 访问前端
在浏览器打开前端 ngrok URL：
```
https://YOUR-FRONTEND-URL.ngrok-free.app
```

---

## 📱 分享给他人

**分享您的固定域名**（永不改变！）：
```
https://tonisha-chiropodical-sharonda.ngrok-free.dev
```

**优势**:
- ✅ URL 永不改变
- ✅ 可以保存书签
- ✅ 适合长期分享
- ✅ 看起来更专业

他们就可以：
- 搜索城市
- 确认地点
- 生成 AI 旅行行程
- 查看地图
- 听语音讲解

---

## 🛑 停止 ngrok

在 ngrok 终端（终端 2）按 `Ctrl+C`

恢复本地配置：
```bash
# 编辑 vue-project/.env，改回：
VITE_API_URL=http://localhost:5000

# 重启前端
cd vue-project && npm run dev
```

---

## 🔍 查看实时请求

访问 ngrok 管理界面：
```
http://localhost:4040
```

可以看到：
- 所有 HTTP 请求
- 请求/响应详情
- 流量统计

---

## ⚡ 常用命令速查

```bash
# 查看 ngrok URLs
./get-ngrok-urls.sh

# 更新前端配置
./update-frontend-url.sh

# 启动 ngrok
./start-ngrok.sh

# 启动应用
./start.sh
```

---

## 💡 重要提示

1. **URL 每次都会变化**  
   每次重启 ngrok，URL 都不同

2. **需要重启前端**  
   更新配置后必须重启前端

3. **三个终端**  
   - 终端 1: 应用（后端+前端）
   - 终端 2: ngrok
   - 终端 3: 执行命令

4. **免费版限制**  
   - 每分钟 40 个请求
   - 会显示 ngrok 提示页（可跳过）

---

## 🎯 完整流程（复制粘贴）

### 使用固定域名（最简单！）

**终端 1**: 启动应用
```bash
cd /home/grealish/newhacks && ./start.sh
```

**终端 2**: 启动 ngrok
```bash
cd /home/grealish/newhacks && ./start-ngrok-frontend.sh
```

**完成！** 🎉

直接访问并分享：
```
https://tonisha-chiropodical-sharonda.ngrok-free.dev
```

---

### 使用随机域名（备选）

**终端 1**:
```bash
cd /home/grealish/newhacks && ./start.sh
```

**终端 2**:
```bash
cd /home/grealish/newhacks && ngrok http 5173
```

查看显示的 URL 并分享！

