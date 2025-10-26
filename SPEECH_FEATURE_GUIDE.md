# 语音输入功能使用指南

## 功能概述

TripTeller 现在支持语音输入城市名称功能，用户可以通过语音来输入想要旅行的城市，无需手动打字。

## 功能特性

### 🎤 前端语音识别
- **浏览器原生语音识别**：使用 Web Speech API
- **中文支持**：支持中文语音输入
- **实时反馈**：录音状态和识别结果显示
- **错误处理**：友好的错误提示和权限管理

### 🔧 后端语音处理
- **Google 语音识别**：使用 Google Speech API 进行高精度识别
- **离线识别**：支持 PocketSphinx 离线语音识别
- **多语言支持**：可配置不同语言
- **音频处理**：自动噪音过滤和音频优化

## 使用方法

### 1. 安装依赖

运行安装脚本：
```bash
# Windows
install_speech_deps.bat

# 或者手动安装
cd backend
pip install SpeechRecognition==3.10.0
pip install PyAudio==0.2.11
pip install pocketsphinx==5.0.0
```

### 2. 使用语音输入

1. **点击语音按钮**：在城市输入框旁边点击"语音输入"按钮
2. **允许麦克风权限**：浏览器会请求麦克风权限，请点击"允许"
3. **开始说话**：清晰地说出城市名称，如"北京"、"东京"、"巴黎"
4. **查看结果**：语音识别结果会自动填入输入框
5. **搜索城市**：点击"Search"按钮开始搜索

### 3. 语音识别状态

- **准备状态**：显示"语音输入"按钮
- **录音状态**：按钮变红，显示"停止录音"
- **处理状态**：显示"处理中..."
- **识别结果**：显示识别出的文字

## 技术实现

### 前端组件 (SpeechInput.vue)

```vue
<SpeechInput 
  @speech-result="handleSpeechResult"
  language="zh-CN"
/>
```

**主要功能：**
- 浏览器语音识别 API 集成
- 录音状态管理
- 错误处理和用户反馈
- 支持多种浏览器

### 后端 API 端点

#### 1. 在线语音识别
```
POST /api/speech-to-text
Content-Type: multipart/form-data

参数：
- audio: 音频文件 (WAV 格式)

返回：
{
  "text": "识别结果",
  "confidence": 0.9,
  "language": "zh-CN"
}
```

#### 2. 离线语音识别
```
POST /api/speech-to-text-offline
Content-Type: multipart/form-data

参数：
- audio: 音频文件 (WAV 格式)

返回：
{
  "text": "识别结果",
  "confidence": 0.7,
  "language": "zh-CN",
  "method": "offline"
}
```

## 浏览器兼容性

### 支持的浏览器
- ✅ Chrome 25+
- ✅ Safari 14.1+
- ✅ Firefox 70+
- ✅ Edge 79+

### 不支持的浏览器
- ❌ Internet Explorer
- ❌ 旧版 Safari (< 14.1)

## 故障排除

### 常见问题

1. **麦克风权限被拒绝**
   - 解决方案：在浏览器设置中允许麦克风权限
   - 路径：浏览器设置 > 隐私和安全 > 网站设置 > 麦克风

2. **语音识别不准确**
   - 确保环境安静
   - 说话清晰，语速适中
   - 尝试使用标准普通话

3. **浏览器不支持语音识别**
   - 升级到最新版本的 Chrome、Safari 或 Firefox
   - 检查浏览器是否支持 Web Speech API

4. **后端语音识别失败**
   - 检查网络连接（Google API 需要网络）
   - 确认依赖包已正确安装
   - 查看后端日志获取详细错误信息

### 调试模式

在浏览器控制台中查看语音识别状态：
```javascript
// 检查浏览器支持
console.log('Speech Recognition supported:', 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window)

// 查看语音识别结果
window.speechRecognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)()
```

## 配置选项

### 语言设置
```javascript
// 在 SpeechInput 组件中修改
language: 'zh-CN'  // 中文
language: 'en-US'  // 英文
language: 'ja-JP'  // 日文
```

### 识别参数
```javascript
// 在 app.py 中修改识别参数
recognizer.energy_threshold = 300  # 能量阈值
recognizer.dynamic_energy_threshold = True  # 动态阈值
recognizer.pause_threshold = 0.8  # 暂停阈值
```

## 性能优化

### 前端优化
- 使用防抖处理避免重复识别
- 缓存语音识别结果
- 优化音频录制质量

### 后端优化
- 音频文件大小限制
- 临时文件自动清理
- 并发请求限制

## 安全考虑

1. **权限管理**：只在需要时请求麦克风权限
2. **数据隐私**：语音数据不存储，仅用于实时识别
3. **网络安全**：使用 HTTPS 确保数据传输安全

## 未来改进

- [ ] 支持更多语言
- [ ] 语音命令控制
- [ ] 离线语音识别优化
- [ ] 语音质量检测
- [ ] 多轮对话支持

---

如有问题，请查看控制台日志或联系技术支持。
