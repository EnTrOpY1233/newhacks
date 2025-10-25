# 🌐 ngrok 当前状况和解决方案

## ✅ 已完成
- ✅ ngrok 已安装并可用
- ✅ authtoken 已配置: `34Yssff1NCcB6R2IhiGcs7hQX9Q_4H1Wgs2g6Dmp4fC4ZdweQ`
- ✅ 网络连接正常
- ✅ 配置文件有效

## ❌ 当前问题
**错误**: ERR_NGROK_15013 - "Your account is requesting a dev domain that does not exist"

**原因**: 您的 ngrok 免费账户可能需要完成设置或有账户限制

---

## 🚀 立即可用的解决方案

### 方案 1: 使用命令行（推荐，最简单）

#### 只暴露前端（用于展示 UI）
```bash
# 终端 1: 启动应用
cd /home/grealish/newhacks
./start.sh

# 终端 2: 暴露前端
ngrok http 5173
```

复制显示的 URL（类似 `https://xxxx.ngrok-free.app`）分享给他人查看界面。

**限制**: 功能可能无法使用（因为后端在本地）

---

#### 只暴露后端（用于 API 测试）
```bash
# 终端 1: 启动后端
cd /home/grealish/newhacks/backend
source venv/bin/activate
python app.py

# 终端 2: 暴露后端
ngrok http 5000
```

可以通过 `https://xxxx.ngrok-free.app/api/health` 测试 API。

---

### 方案 2: 完整外网访问（需要两步）

**步骤 1**: 先获取后端 URL
```bash
# 启动后端
cd /home/grealish/newhacks/backend
source venv/bin/activate
python app.py &

# 暴露后端
ngrok http 5000
```

记下后端 URL: `https://BACKEND-URL.ngrok-free.app`

**步骤 2**: 配置前端使用外网后端，然后暴露前端
```bash
# 停止上面的 ngrok (Ctrl+C)

# 更新前端配置
echo "VITE_API_URL=https://BACKEND-URL.ngrok-free.app" > /home/grealish/newhacks/vue-project/.env
echo "VITE_GOOGLE_MAPS_API_KEY=你的Google_Maps_Key" >> /home/grealish/newhacks/vue-project/.env

# 启动前端
cd /home/grealish/newhacks/vue-project
npm run dev &

# 暴露前端
ngrok http 5173
```

**问题**: 后端的 ngrok 隧道会断开（免费版限制），所以这个方法不太实用。

---

### 方案 3: 使用替代工具 - Cloudflare Tunnel（免费且强大）

#### 安装 cloudflared
```bash
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

#### 使用（无需注册！）
```bash
# 暴露前端
cloudflared tunnel --url http://localhost:5173

# 或暴露后端
cloudflared tunnel --url http://localhost:5000
```

**优势**:
- ✅ 完全免费
- ✅ 无需注册
- ✅ 可以同时运行多个隧道
- ✅ 稳定可靠

---

### 方案 4: LocalTunnel（快速测试）

```bash
# 安装
npm install -g localtunnel

# 使用
lt --port 5173    # 前端
# 或
lt --port 5000    # 后端
```

---

## 🎯 我的建议（根据您的需求）

### 如果需要现在就演示：

**最快方案**:
```bash
# 1. 启动应用
cd /home/grealish/newhacks && ./start.sh

# 2. 在另一个终端
cloudflared tunnel --url http://localhost:5173
```

如果没有 cloudflared，用 ngrok:
```bash
ngrok http 5173
```

然后分享 URL，说明"这是 UI 界面演示，完整功能请查看本地运行"。

---

### 如果需要完整功能演示：

**选项 A**: 本地演示
- 不用内网穿透
- 直接在本地运行
- 使用屏幕共享演示

**选项 B**: 录制演示视频
- 录制完整功能演示
- 上传到 YouTube/Loom
- 分享视频链接

**选项 C**: 升级 ngrok 付费版
- 访问 https://dashboard.ngrok.com/billing
- Personal 计划 $8/月，支持 3 个隧道
- 可以同时暴露前端和后端

**选项 D**: 部署到云平台
- 前端: Vercel/Netlify（免费）
- 后端: Render/Railway（免费）
- 永久在线，无需内网穿透

---

## 📋 快速测试当前 ngrok

运行这个测试是否能工作：

```bash
# 启动前端
cd /home/grealish/newhacks/vue-project
npm run dev &

# 等待 3 秒
sleep 3

# 测试 ngrok（在另一个终端运行）
ngrok http 5173
```

如果能看到 ngrok 界面并显示 URL，说明可以使用！
如果还是报错，说明账户有限制，建议使用其他方案。

---

## 🔧 解决 ngrok 账户问题

访问 ngrok dashboard 完成以下步骤：

1. **登录**: https://dashboard.ngrok.com/login
2. **验证邮箱**（如果需要）
3. **检查 authtoken**: https://dashboard.ngrok.com/get-started/your-authtoken
4. **查看账户限制**: https://dashboard.ngrok.com/billing

如果显示需要完成某些设置，请按提示操作。

---

## 📞 需要帮助？

如果上述方案都不行，请提供：
1. ngrok dashboard 账户状态截图
2. 运行 `ngrok http 5173` 的完整错误信息
3. 您的演示时间（多紧急）

我会帮您找到最合适的解决方案！

---

## 🎉 总结

**当前可用**:
- ✅ 本地访问（localhost）
- ✅ ngrok 命令行（可能可用，需测试）
- ✅ Cloudflare Tunnel（推荐）
- ✅ LocalTunnel（备选）

**需要解决**:
- ⚠️ ngrok 多隧道配置（需要付费或账户设置）
- ⚠️ 账户 dev domain 问题

**建议行动**:
1. 先试试 `ngrok http 5173` 看是否能用
2. 如果不行，使用 Cloudflare Tunnel
3. 长期考虑部署到云平台

---

**现在就可以开始！选择一个方案并测试！** 🚀


