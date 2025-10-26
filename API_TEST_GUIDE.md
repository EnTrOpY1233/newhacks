# API 测试指南

## 概述

`test_apis.py` 是一个全面的API测试脚本，用于测试 TripTeller 后端的所有API端点，确保所有功能正常工作。

## 功能

该测试脚本会测试以下API端点：

1. **Health Check** (`/api/health`) - 健康检查和配置状态
2. **Search Places** (`/api/search-places`) - 地点搜索
3. **Generate Itinerary** (`/api/generate-itinerary`) - 生成旅行计划
4. **Generate Audio** (`/api/generate-audio`) - 生成音频
5. **Weather API** (`/api/weather`) - 天气信息
6. **Events API** (`/api/events`) - 活动信息
7. **Speech to Text** (`/api/speech-to-text`) - 语音转文字

## 使用方法

### 前提条件

1. **启动后端服务器**
   ```bash
   cd backend
   python app.py
   ```
   后端服务器应该在 `http://localhost:5000` 上运行

2. **安装依赖**
   ```bash
   pip install requests
   ```

### 运行测试

```bash
python test_apis.py
```

或者（如果已设置为可执行）：

```bash
./test_apis.py
```

## 测试输出

测试脚本会显示彩色输出，包括：

- ✓ 绿色：测试通过
- ✗ 红色：测试失败
- ⚠ 黄色：警告信息
- ℹ 蓝色：信息提示

### 示例输出

```
============================================================
              TripTeller API Test Suite              
============================================================

ℹ Testing API at: http://localhost:5000

Testing: Health Check
✓ Health check passed
ℹ AI Service: cerebras
ℹ Configured Services:
  ✓ cerebras_configured
  ✓ openrouter_configured
  ✗ gemini_configured
  ✓ elevenlabs_configured
  ✓ maps_configured
  ✓ weather_configured

Testing: Search Places
✓ Search for 'Paris' returned 1 result(s)
...

============================================================
                      Test Summary                      
============================================================

✓ PASS - Health Check
✓ PASS - Search Places
✓ PASS - Generate Itinerary
...

Results: 7/7 tests passed
```

## 配置

如果需要修改测试配置，可以编辑脚本开头的配置：

```python
BASE_URL = "http://localhost:5000"  # 后端服务器地址
TIMEOUT = 30  # 请求超时时间（秒）
```

## 故障排除

### 1. 无法连接到服务器

**错误信息：**
```
✗ Cannot connect to server. Is the backend running?
```

**解决方案：**
- 确保后端服务器正在运行
- 检查后端是否在正确的端口上运行
- 确认防火墙设置

### 2. API密钥未配置

某些API可能需要API密钥才能正常工作：

- **Google Maps API**: 用于地点搜索
- **ElevenLabs API**: 用于音频生成
- **OpenWeather API**: 用于天气信息
- **AI Service API**: 用于生成旅行计划

如果相应的API密钥未配置，相关测试会失败，但不会影响其他功能的测试。

### 3. 测试超时

如果某些测试超时（尤其是生成旅行计划或音频），可以增加超时时间：

```python
TIMEOUT = 60  # 增加到60秒
```

## 测试详细信息

### Health Check
检查服务器状态和配置的API服务

### Search Places
测试三个地点搜索：
- Paris
- Tokyo
- New York

### Generate Itinerary
生成一个3天的东京旅行计划，包含历史和美食偏好

### Generate Audio
生成一段示例音频

### Weather API
获取东京明天的天气信息

### Events API
获取东京下周的活动信息

### Speech to Text
跳过实际测试（需要上传音频文件）

## 手动测试

某些功能（如语音转文字）需要手动测试：

```bash
# 测试语音转文字
curl -X POST http://localhost:5000/api/speech-to-text \
  -F "audio=@your_audio_file.wav"
```

## 持续集成

可以将此测试脚本集成到CI/CD流程中：

```yaml
# .github/workflows/test.yml
name: API Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install requests
      - name: Start backend
        run: |
          cd backend
          python app.py &
          sleep 5
      - name: Run tests
        run: python test_apis.py
```

## 贡献

如果添加了新的API端点，请更新此测试脚本以包含相应的测试。

## 许可证

此测试脚本与主项目共享相同的许可证。
