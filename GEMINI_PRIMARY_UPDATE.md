# Gemini API 作为主要 AI 服务更新

## 更新概述

已将 TripTeller 的 AI 服务优先级调整为：
1. **Gemini API** (主要选项)
2. **Cerebras API** (备选项)
3. **OpenRouter API** (最后备选)

## 更改内容

### 1. 后端代码更新 (`backend/app.py`)

#### API 初始化优先级调整
- **之前**: Cerebras -> OpenRouter -> Gemini
- **现在**: Gemini -> Cerebras -> OpenRouter

#### 新增 Gemini API 函数
```python
def call_gemini_api(prompt):
    """Call Gemini API using new google-genai SDK"""
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt,
    )
    return response.text
```

#### 更新的调用逻辑
```python
if AI_SERVICE == 'gemini':
    response_text = call_gemini_api(prompt)
elif AI_SERVICE == 'cerebras':
    response_text = call_cerebras_api(prompt)
elif AI_SERVICE == 'openrouter':
    response_text = call_openrouter_api(prompt)
```

### 2. 依赖更新 (`backend/requirements.txt`)

**更改:**
```diff
- google-generativeai==0.3.2
+ google-genai
```

使用新的 `google-genai` SDK，支持最新的 Gemini 2.0 模型。

### 3. 环境变量示例更新 (`backend/env.example`)

添加了清晰的优先级说明：
```env
# AI API Keys (Priority: Gemini -> Cerebras -> OpenRouter)

# Gemini API Key (Primary - get from Google AI Studio)
GEMINI_API_KEY=your_gemini_api_key_here

# Cerebras API Key (Backup - get from cerebras.ai)
CEREBRAS_API_KEY=your_cerebras_api_key_here

# OpenRouter API Key (Fallback - get from openrouter.ai)
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## 安装和配置

### 1. 安装新依赖

```bash
cd backend
pip install -r requirements.txt
```

或单独安装：
```bash
pip install google-genai
```

### 2. 配置 API Key

在 `backend/.env` 文件中添加您的 Gemini API Key：

```env
GEMINI_API_KEY=AIzaSyCOl5CnAYAfLvBf2LlE9Sdi_LrThI6im-I
```

### 3. 获取 Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/apikey)
2. 登录您的 Google 账号
3. 点击 "Get API Key" 或 "Create API Key"
4. 复制生成的 API Key
5. 粘贴到 `.env` 文件中

## 测试 API Key

使用提供的测试脚本验证 Gemini API Key：

```bash
python test_gemini_key.py
```

**预期输出：**
```
============================================================
                    Gemini API Key Test                     
============================================================

📝 Testing API Key: AIzaSyCOl5CnAYAfLvBf...LrThI6im-I

✓ google.genai library found

------------------------------------------------------------
Testing API Connection...
------------------------------------------------------------

✓ Client initialized
✓ Model: gemini-2.0-flash-exp

Sending test prompt: 'Explain how AI works in a few words'
✓ Response received:
  'AI uses algorithms and data to learn patterns and make decisions.'

============================================================
        ✅ SUCCESS: API Key is VALID and WORKING!        
============================================================
```

## 使用的 Gemini 模型

- **模型名称**: `gemini-2.0-flash-exp`
- **特点**: 
  - 快速响应
  - 成本效益高
  - 支持长文本生成
  - 适合旅行规划等复杂任务

## 备选方案

如果 Gemini API 不可用或出错，系统会自动切换到：

1. **Cerebras API** - 如果配置了 `CEREBRAS_API_KEY`
2. **OpenRouter API** - 如果配置了 `OPENROUTER_API_KEY`
3. **示例数据** - 如果没有配置任何 API

## 运行服务器

```bash
cd backend
python app.py
```

**启动日志应显示：**
```
✅ Using Gemini API (Primary)
```

如果看到其他信息：
- `✅ Using Cerebras API (Backup)` - Gemini 不可用，使用 Cerebras
- `⚠️ No AI API configured` - 没有配置任何 AI API

## API 响应时间对比

| API | 平均响应时间 | 成本 |
|-----|-------------|------|
| Gemini 2.0 Flash | ~2-3秒 | 免费（有配额） |
| Cerebras | ~1-2秒 | 按使用付费 |
| OpenRouter | ~3-5秒 | 部分免费模型 |

## 故障排除

### 问题：导入错误
```
ImportError: No module named 'google.genai'
```

**解决方案：**
```bash
pip install google-genai
```

### 问题：API Key 无效
```
❌ Error: 403 API key not valid
```

**解决方案：**
1. 检查 `.env` 文件中的 API Key 是否正确
2. 确保 API Key 已启用 Gemini API
3. 访问 [Google AI Studio](https://aistudio.google.com/apikey) 重新生成

### 问题：配额超限
```
❌ Error: 429 Quota exceeded
```

**解决方案：**
1. 等待配额重置（通常每天重置）
2. 升级到付费计划
3. 系统会自动切换到 Cerebras 备选

## 优势

使用 Gemini 作为主要 AI 服务的优势：

1. **免费配额充足** - 适合开发和演示
2. **响应质量高** - Google 最新的 AI 模型
3. **JSON 格式支持好** - 适合结构化数据生成
4. **多语言支持** - 支持多种语言的旅行规划
5. **上下文理解强** - 能更好理解复杂的旅行需求

## 相关文件

- `backend/app.py` - 主要后端逻辑
- `backend/requirements.txt` - Python 依赖
- `backend/env.example` - 环境变量示例
- `test_gemini_key.py` - API Key 测试脚本

## 更新日期

2025-01-26

---

**注意**: 如果您已经在使用 Cerebras API，它仍然作为备选方案保留，无需删除相关配置。

