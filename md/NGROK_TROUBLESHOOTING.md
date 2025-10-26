# 🔧 ngrok 故障排查指南

## ❌ 当前问题：ERR_NGROK_15013

### 错误信息
```
ERROR: Your account is requesting a dev domain that does not exist.
ERROR: ERR_NGROK_15013
```

---

## 🔍 问题原因

这个错误通常是因为：
1. **ngrok 账户需要激活** - 新账户可能需要邮箱验证
2. **免费账户限制** - 免费版可能不支持配置文件中的某些选项
3. **需要在 dashboard 中配置 domain**

---

## ✅ 解决方案

### 方案 1: 验证账户（推荐）

1. **访问 ngrok dashboard**:
   ```
   https://dashboard.ngrok.com/
   ```

2. **完成账户设置**:
   - 验证邮箱（如果还没验证）
   - 查看 "Your Authtoken" 页面确认 token 正确
   - 检查账户状态

3. **获取新的 authtoken**（如果需要）:
   ```
   https://dashboard.ngrok.com/get-started/your-authtoken
   ```

---

### 方案 2: 使用简化版脚本

我们创建了一个简化版脚本，一次只启动一个隧道：

```bash
cd /home/grealish/newhacks
./start-ngrok-simple.sh
```

然后选择：
- **选项 1**: 只暴露前端（端口 5173）
- **选项 2**: 只暴露后端（端口 5000）
- **选项 3**: 尝试同时启动两个（可能失败）

---

### 方案 3: 直接使用命令行

#### 启动前端隧道
```bash
ngrok http 5173
```

#### 启动后端隧道
```bash
ngrok http 5000
```

**注意**: 免费账户一次只能运行一个隧道！

---

## 🎯 推荐工作流程（免费账户）

### 选择 A: 只暴露前端
```bash
# 1. 前端使用本地后端
# 确保 vue-project/.env 设置为:
VITE_API_URL=http://localhost:5000

# 2. 启动后端（本地）
cd backend && python app.py

# 3. 启动前端（本地）
cd vue-project && npm run dev

# 4. 用 ngrok 暴露前端
ngrok http 5173
```

**限制**: 外网用户只能看到界面，无法使用功能（因为后端在本地）

---

### 选择 B: 先暴露后端，再暴露前端（分两次）

#### 第一步：获取后端 URL
```bash
# 终端 1: 启动后端
cd backend && python app.py

# 终端 2: 暴露后端
ngrok http 5000
```

复制后端的 ngrok URL，例如：`https://xxxx.ngrok-free.app`

#### 第二步：配置并暴露前端
```bash
# 停止第一个 ngrok (Ctrl+C)

# 更新前端配置
echo "VITE_API_URL=https://xxxx.ngrok-free.app" > vue-project/.env

# 启动前端
cd vue-project && npm run dev

# 暴露前端
ngrok http 5173
```

**问题**: 后端的 ngrok URL 会失效，因为只能运行一个隧道

---

### 选择 C: 使用 ngrok 付费版（推荐用于演示）

升级到 ngrok 付费版：
- ✅ 可以同时运行多个隧道
- ✅ 固定的域名（不会每次变化）
- ✅ 更高的请求限制
- ✅ 无广告页面

访问: https://dashboard.ngrok.com/billing

**价格**: 
- Personal: $8/月 - 3 个隧道
- Pro: $20/月 - 无限隧道

---

### 选择 D: 使用其他内网穿透工具

免费替代方案：

#### 1. Cloudflare Tunnel (推荐)
```bash
# 安装
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# 使用
cloudflared tunnel --url http://localhost:5173
```

#### 2. LocalTunnel
```bash
# 安装
npm install -g localtunnel

# 使用
lt --port 5173
```

#### 3. Serveo (无需安装)
```bash
ssh -R 80:localhost:5173 serveo.net
```

---

## 🛠️ 临时解决方案（演示用）

如果您现在就需要演示，最简单的方法：

### 方案：只用一个隧道 + 模拟数据

```bash
# 1. 修改前端使用模拟数据（开发模式）
# 或者只展示 UI 界面

# 2. 启动前端
cd vue-project && npm run dev

# 3. 用 ngrok 暴露
ngrok http 5173
```

**或者只演示后端 API**:
```bash
# 1. 启动后端
cd backend && python app.py

# 2. 用 ngrok 暴露
ngrok http 5000

# 3. 用 curl 或 Postman 测试 API
curl https://xxxx.ngrok-free.app/api/health
```

---

## 📋 检查清单

尝试每个步骤：

- [ ] 访问 https://dashboard.ngrok.com/ 检查账户状态
- [ ] 验证邮箱（如果需要）
- [ ] 确认 authtoken 正确
- [ ] 尝试运行单个隧道：`ngrok http 5173`
- [ ] 如果单个隧道工作，考虑工作流程选择 B
- [ ] 如果都不工作，考虑使用替代工具

---

## 🆘 如果还是不行

### 创建新的 ngrok 账户

1. 访问: https://ngrok.com/signup
2. 使用不同的邮箱注册
3. 验证邮箱
4. 获取新的 authtoken
5. 更新配置

### 联系 ngrok 支持

访问: https://ngrok.com/support

---

## 💡 当前建议

**对于 Hackathon 演示**:

1. **本地演示**:
   - 不用 ngrok
   - 直接在本地运行并演示
   - 使用屏幕共享展示

2. **远程演示**:
   - 使用 Cloudflare Tunnel（免费且稳定）
   - 或者只暴露前端，后端保持本地
   - 或者录制演示视频

3. **长期使用**:
   - 考虑升级到 ngrok 付费版
   - 或者部署到云服务器（Vercel, Netlify 等）

---

## 📝 更新配置文件

如果问题解决了，记得更新：

```bash
# 更新 ngrok authtoken
ngrok config add-authtoken YOUR_NEW_TOKEN

# 测试
ngrok http 5173
```

---

**需要帮助？** 查看 [NGROK_SETUP.md](./NGROK_SETUP.md) 或提问！

**快速测试**: 运行 `./start-ngrok-simple.sh` 选择选项 1 测试前端隧道


