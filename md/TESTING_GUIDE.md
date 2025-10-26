# 🧪 TripTeller 测试指南

## 🚀 快速测试 Place Picker 新功能

### 前置条件

确保已完成：
- ✅ 获取 Google Maps API Key
- ✅ 在 Google Cloud Console 启用 **Places API**
- ✅ 配置前端 `.env` 文件
- ✅ 安装所有依赖

### 测试步骤

#### 1. 启动项目

```bash
# 后端
cd backend
source venv/bin/activate
python app.py

# 新终端 - 前端
cd vue-project
npm run dev
```

访问：http://localhost:5173

#### 2. 测试 Place Picker 自动完成

**测试用例 1：完整城市名**
1. 在输入框输入：`Tok`
2. 应该看到下拉建议：
   - Tokyo, Japan
   - Tokushima, Japan
   - ...
3. 选择 "Tokyo, Japan"
4. 点击 "🔍 搜索"
5. 验证：AI 生成 Tokyo 的行程

**测试用例 2：著名景点**
1. 输入：`Eiffel`
2. 选择：Eiffel Tower, Paris, France
3. 点击搜索
4. 验证：自动提取 "Paris" 并生成行程

**测试用例 3：地址**
1. 输入：`301 Front St W, Toronto`
2. 选择建议的地址
3. 验证：提取 "Toronto" 并生成行程

**测试用例 4：热门城市快捷按钮**
1. 直接点击 "Tokyo" 按钮
2. 验证：立即搜索无需输入

#### 3. 测试地图功能

1. 生成行程后
2. 检查右侧地图是否显示
3. 验证景点标记（1, 2, 3...）
4. 点击标记查看信息窗口

#### 4. 测试语音功能

1. 点击任意景点的 "🔊 播放讲解"
2. 验证：弹出音频播放器
3. 检查音频播放
4. （如未配置 ElevenLabs，会使用示例音频）

### 控制台检查

打开浏览器开发者工具（F12），查看控制台：

**正常输出：**
```
Selected place: {name: "Tokyo", formatted_address: "Tokyo, Japan", ...}
Extracted city: Tokyo
Successfully generated itinerary for Tokyo
```

**警告（可忽略）：**
```
Google Maps API Key 未配置，Place Picker 可能无法正常工作
```
→ 确保 `.env` 文件中有 `VITE_GOOGLE_MAPS_API_KEY`

### 功能检查清单

#### Place Picker
- [ ] 输入时显示自动完成建议
- [ ] 可以选择建议项
- [ ] 正确提取城市名
- [ ] 样式与整体 UI 协调

#### 行程生成
- [ ] 点击搜索后显示加载状态
- [ ] 成功生成 3 天行程
- [ ] 每天显示多个景点
- [ ] 景点包含描述和详细信息

#### 地图显示
- [ ] 地图自动加载
- [ ] 标记所有景点位置
- [ ] 标记有正确的编号
- [ ] 点击标记显示信息窗口
- [ ] 地图自动缩放到合适范围

#### 语音播放
- [ ] 点击 🔊 按钮弹出播放器
- [ ] 显示景点名称
- [ ] 音频可以播放
- [ ] 可以关闭播放器

#### 响应式设计
- [ ] 在桌面浏览器正常显示
- [ ] 在移动设备正常显示（F12 → 设备模拟）
- [ ] 搜索框在移动端垂直排列

### 常见问题排查

#### 问题 1：Place Picker 不显示建议

**可能原因：**
- Places API 未启用
- API Key 未配置
- API Key 无效

**解决方法：**
1. 访问 Google Cloud Console
2. 确认 Places API 已启用
3. 检查 API Key 限制设置
4. 查看浏览器控制台错误

#### 问题 2：选择地点后没反应

**检查：**
1. 打开控制台，查看是否有错误
2. 确认 `handlePlaceChange` 事件被触发
3. 检查 `cityName` 是否被正确设置

**调试：**
```javascript
// 在 CityInput.vue 中添加调试日志
console.log('Place selected:', event.detail.place)
```

#### 问题 3：提取的城市名不正确

**原因：**
某些地点可能没有标准的城市信息

**解决：**
城市提取逻辑会按优先级尝试：
1. locality（城市）
2. administrative_area_level_1（州/省）
3. name（地点名）
4. formatted_address（完整地址）

可以手动调整提取逻辑。

#### 问题 4：地图标记位置不准确

**原因：**
Geocoding API 对某些景点的定位可能不够精确

**这是正常的：**
- 地理编码基于文本地址
- 不同景点可能有相似名称
- 系统会尽力匹配最佳位置

### 性能测试

#### 加载速度
- Place Picker 组件：< 1秒
- 行程生成：3-10秒（取决于 Gemini API）
- 地图加载：1-2秒
- 语音生成：2-5秒（取决于 ElevenLabs API）

#### API 调用次数
一次完整流程：
- Place Picker: 1-5 次（自动完成）
- 行程生成: 1 次（Gemini）
- 地理编码: N 次（N = 景点数量）
- 语音生成: 按需调用

### 浏览器兼容性

**已测试：**
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**已知问题：**
- IE 11 不支持（Vue 3 要求）

### API 额度监控

测试时注意监控 API 使用量：

**Google Cloud Console:**
1. 访问：https://console.cloud.google.com/
2. 导航到：APIs & Services → Dashboard
3. 查看 Places API 使用量

**建议：**
- 设置使用量警报
- 限制每日配额（测试期间）
- 使用 API Key 限制（HTTP referrer）

### 测试数据

推荐测试城市：
- **亚洲**: Tokyo, Seoul, Singapore, Bangkok
- **欧洲**: Paris, London, Barcelona, Rome
- **北美**: Toronto, New York, Los Angeles, Vancouver
- **其他**: Dubai, Sydney, Cairo, Rio de Janeiro

### 单元测试（可选）

如果需要编写自动化测试：

```javascript
// CityInput.test.js
import { mount } from '@vue/test-utils'
import CityInput from './CityInput.vue'

describe('CityInput', () => {
  it('should emit search event on button click', async () => {
    const wrapper = mount(CityInput)
    // 测试代码...
  })
})
```

### 截图检查

记录测试结果时，建议截图：
1. Place Picker 自动完成下拉
2. 生成的行程显示
3. 地图标记
4. 音频播放器
5. 移动端显示

---

## ✅ 测试完成确认

完成以上所有测试后，你的 TripTeller 应该：
- ✅ 能够智能搜索地点
- ✅ 正确提取城市信息
- ✅ AI 生成合理行程
- ✅ 地图显示景点位置
- ✅ 语音播放正常工作
- ✅ 在各种设备上良好显示

**准备好演示了！** 🎉

---

*测试有问题？查看 `UPDATES.md` 了解详细功能说明。*

