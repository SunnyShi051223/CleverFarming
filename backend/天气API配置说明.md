# 高德天气API配置说明

## ✅ 已完成配置

### 1. API Key 配置
已在 `backend/user_info_api.py` 中配置：
```python
AMAP_API_KEY = "01e17e6256c8768ad0f7961437bda3fc"
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
```

### 2. API接口实现
- ✅ 调用高德天气API获取实时天气
- ✅ 支持城市编码查询
- ✅ 自动降级到模拟数据
- ✅ 详细的日志输出

### 3. 前端集成
- ✅ 自动获取用户城市天气
- ✅ 支持80+个城市编码
- ✅ 动态更新天气UI
- ✅ 30分钟自动刷新

## 🌐 API调用示例

### 请求格式
```
GET /api/weather?city=武汉&adcode=420100
```

### 响应格式
```json
{
  "success": true,
  "weather": {
    "province": "湖北",
    "city": "武汉市",
    "adcode": "420100",
    "temperature": "17",
    "weather": "阴",
    "wind_direction": "北",
    "wind_power": "≤3",
    "humidity": "91",
    "report_time": "2025-10-18 01:01:54",
    "temperature_float": "17.0",
    "humidity_float": "91.0"
  }
}
```

## 📋 支持的城市

### 直辖市
- 北京 (110000)
- 上海 (310000)
- 天津 (120000)
- 重庆 (500000)

### 省会城市
- 武汉 (420100)
- 广州 (440100)
- 深圳 (440300)
- 成都 (510100)
- 杭州 (330100)
- 南京 (320100)
- 西安 (610100)
- 郑州 (410100)
- 长沙 (430100)
- 济南 (370100)
- 等80+个城市...

完整列表见 `api/js/city-codes.js`

## 🧪 测试方法

### 方法1：使用专用测试页面
访问：`http://localhost:5000/test-weather.html`

功能：
- ✅ 快速选择常用城市
- ✅ 自定义城市查询
- ✅ 实时天气显示
- ✅ API响应日志

### 方法2：使用综合测试页面
访问：`http://localhost:5000/test-api.html`

点击"天气API测试"按钮

### 方法3：直接API调用
```bash
# 武汉天气
curl "http://localhost:5000/api/weather?city=武汉&adcode=420100"

# 北京天气
curl "http://localhost:5000/api/weather?city=北京&adcode=110000"
```

## 📊 数据字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| province | string | 省份 | "湖北" |
| city | string | 城市 | "武汉市" |
| adcode | string | 城市编码 | "420100" |
| temperature | string | 温度(整数) | "17" |
| temperature_float | string | 温度(浮点) | "17.0" |
| weather | string | 天气状况 | "阴" |
| wind_direction | string | 风向 | "北" |
| wind_power | string | 风力 | "≤3" |
| humidity | string | 湿度(整数) | "91" |
| humidity_float | string | 湿度(浮点) | "91.0" |
| report_time | string | 更新时间 | "2025-10-18 01:01:54" |

## 🔧 前端使用

### 1. 引入必要文件
```html
<script src="/js/city-codes.js"></script>
<script src="/js/user-info.js"></script>
```

### 2. 调用天气API
```javascript
// 自动获取（会根据用户城市）
const weather = await getWeather();

// 指定城市
const weather = await getWeather('武汉', '420100');

// 只提供城市名（自动查找编码）
const weather = await getWeather('北京');
```

### 3. 添加CSS类名
```html
<!-- 温度 -->
<div class="weather-temp">26°C</div>

<!-- 天气状况 -->
<div class="weather-condition">多云</div>

<!-- 湿度 -->
<div class="weather-humidity">65%</div>

<!-- 风向风力 -->
<div class="weather-wind">东南风 2级</div>

<!-- 天气图标 -->
<i class="weather-icon fas fa-cloud-sun"></i>
```

页面加载时会自动更新这些元素。

## ⚙️ 配置选项

### 修改默认城市
在 `user_info_api.py` 中：
```python
city_name = request.args.get('city', '武汉')  # 修改默认城市
adcode = request.args.get('adcode', '420100')  # 修改默认编码
```

### 修改刷新频率
在 `user-info.js` 中：
```javascript
setInterval(async () => {
    // ...
}, 30 * 60 * 1000); // 修改刷新间隔（毫秒）
```

### 添加新城市
在 `city-codes.js` 中：
```javascript
const CITY_CODES = {
    '你的城市': '城市编码',
    // ...
};
```

## 🛡️ 错误处理

### 1. API调用失败
- 自动降级到模拟数据
- 在响应中添加 `note` 字段说明原因
- 控制台输出详细错误日志

### 2. 网络超时
- 设置10秒超时
- 超时后返回模拟数据
- 不影响页面正常显示

### 3. 城市编码错误
- 自动使用默认城市（武汉）
- 控制台警告提示
- 建议检查城市编码表

## 📈 性能优化

### 1. 缓存机制
建议在前端添加缓存：
```javascript
const CACHE_DURATION = 30 * 60 * 1000; // 30分钟
let weatherCache = {
    data: null,
    timestamp: 0
};

async function getWeatherWithCache(city, adcode) {
    const now = Date.now();
    if (weatherCache.data && (now - weatherCache.timestamp) < CACHE_DURATION) {
        return weatherCache.data;
    }
    
    const weather = await getWeather(city, adcode);
    weatherCache = { data: weather, timestamp: now };
    return weather;
}
```

### 2. 请求合并
如果多个组件需要天气数据，使用单例模式避免重复请求。

### 3. 懒加载
非首屏天气信息可以延迟加载。

## 🔍 调试技巧

### 1. 查看API响应
打开浏览器控制台（F12），查看：
```
正在获取天气信息: city=武汉, adcode=420100
高德天气API响应: {...}
天气信息获取成功: 武汉市 阴 17°C
```

### 2. 检查网络请求
在Network标签中查看：
- 请求URL
- 响应状态码
- 响应内容

### 3. 测试不同城市
使用测试页面快速切换城市测试。

## 📝 注意事项

1. **API Key安全**
   - 不要将API Key提交到公开仓库
   - 生产环境建议使用环境变量

2. **请求频率**
   - 高德API有调用次数限制
   - 建议添加缓存减少调用

3. **城市编码**
   - 必须使用正确的adcode
   - 错误的编码会导致查询失败

4. **时区问题**
   - API返回的时间为服务器时间
   - 注意时区转换

## 🆘 常见问题

### Q1: 天气数据不更新？
**A:** 检查：
- API Key是否正确
- 网络连接是否正常
- 浏览器控制台是否有错误

### Q2: 显示模拟数据？
**A:** 可能原因：
- API调用失败
- 城市编码错误
- 网络超时
查看控制台日志了解详情

### Q3: 如何添加更多城市？
**A:** 编辑 `city-codes.js`，添加城市和对应编码

### Q4: 天气图标不正确？
**A:** 检查 `updateWeatherIcon()` 函数的匹配规则

## 🔗 相关链接

- 高德开放平台：https://lbs.amap.com/
- 天气查询API文档：https://lbs.amap.com/api/webservice/guide/api/weatherinfo
- 城市编码查询：https://lbs.amap.com/api/webservice/guide/api/district

## ✨ 功能扩展建议

1. **天气预报**
   - 使用 `extensions=all` 获取未来天气
   - 显示3-7天预报

2. **天气预警**
   - 解析预警信息
   - 推送重要预警

3. **历史天气**
   - 记录历史天气数据
   - 生成天气趋势图表

4. **多语言支持**
   - 支持英文天气描述
   - 国际化城市名称

祝您使用愉快！🌤️
