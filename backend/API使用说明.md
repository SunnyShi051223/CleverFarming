# 用户信息和天气API使用说明

## 概述

本系统实现了通过后端API动态获取用户信息和天气数据的功能，替代了前端硬编码的静态信息。

## 功能特性

### 1. 用户信息管理
- 获取用户完整资料（姓名、地区、作物类型、农田面积等）
- 更新用户信息
- 获取用户统计数据（未读预警、使用天数等）

### 2. 天气信息
- 实时获取天气数据
- 支持多城市查询
- 自动30分钟刷新

### 3. 自动更新UI
- 页面加载时自动获取并更新用户信息
- 动态更新天气显示
- 根据天气状况自动切换图标

## API接口

### 1. 获取用户资料
```
GET /api/user/profile
```

**响应示例：**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "张三",
    "location": "北京市朝阳区",
    "city": "北京",
    "crop_type": "小麦",
    "farm_area": 50.00,
    "avatar_url": "https://...",
    "stats": {
      "unread_alerts": 5,
      "days_used": 128
    }
  }
}
```

### 2. 更新用户资料
```
PUT /api/user/profile
Content-Type: application/json

{
  "location": "北京市朝阳区",
  "city": "北京",
  "crop_type": "小麦",
  "farm_area": 50.00
}
```

### 3. 获取天气信息
```
GET /api/weather?city=北京&adcode=110000
```

**响应示例：**
```json
{
  "success": true,
  "weather": {
    "city": "北京",
    "temperature": "26",
    "weather": "多云转晴",
    "wind_direction": "东南风",
    "wind_power": "2级",
    "humidity": "65",
    "pressure": "1013"
  }
}
```

### 4. 获取用户统计
```
GET /api/user/stats
```

**响应示例：**
```json
{
  "success": true,
  "stats": {
    "unread_alerts": 5,
    "weekly_completed_tasks": 12,
    "pending_tasks": 3,
    "days_used": 128
  }
}
```

## 数据库更新

### 执行SQL脚本

运行 `update_database.sql` 文件来更新数据库结构：

```bash
mysql -u root -p farming_system < update_database.sql
```

### 新增字段

**users 表：**
- `location` - 详细地址
- `city` - 城市
- `crop_type` - 种植作物类型
- `farm_area` - 农田面积
- `avatar_url` - 头像URL
- `last_login` - 最后登录时间

**新增表：**
- `farming_alerts` - 农事预警表
- `daily_tasks` - 每日任务表

## 前端集成

### 1. 引入JavaScript文件

在HTML页面中添加：
```html
<script src="/js/user-info.js"></script>
```

### 2. 添加CSS类名

为需要动态更新的元素添加特定类名：

**用户信息：**
- `.user-name` - 用户名
- `.user-avatar` - 用户头像
- `.user-location` - 地区
- `.user-crop` - 作物类型
- `.alert-count` - 预警数量
- `.days-used` - 使用天数

**天气信息：**
- `.weather-temp` - 温度
- `.weather-condition` - 天气状况
- `.weather-humidity` - 湿度
- `.weather-wind` - 风速
- `.weather-pressure` - 气压
- `.weather-icon` - 天气图标

### 3. 自动初始化

页面加载时会自动调用 `initUserInterface()` 函数，无需手动调用。

### 4. 手动刷新

如需手动刷新数据：
```javascript
// 刷新用户信息
const user = await getUserProfile();

// 刷新天气信息
const weather = await getWeather('北京', '110000');

// 刷新统计信息
const stats = await getUserStats();
```

## 天气API配置

### 使用高德天气API（推荐）

1. 注册高德开放平台账号：https://lbs.amap.com/
2. 创建应用获取API Key
3. 在 `user_info_api.py` 中配置：
```python
AMAP_API_KEY = "your_actual_api_key"
```

### 使用模拟数据

如果不配置API Key，系统会自动返回模拟天气数据作为降级方案。

## 城市编码对照表

常用城市的adcode：
- 北京：110000
- 上海：310000
- 广州：440100
- 深圳：440300
- 武汉：420100
- 成都：510100

完整编码表：https://lbs.amap.com/api/webservice/guide/api/district

## 注意事项

1. **认证要求**：所有用户相关API需要登录后才能访问
2. **跨域配置**：已在后端配置CORS，支持跨域请求
3. **数据刷新**：天气数据每30分钟自动刷新一次
4. **降级方案**：天气API失败时自动使用模拟数据
5. **性能优化**：用户信息会在页面加载时一次性获取

## 示例页面

已更新的页面：
- `farmer.html` - 农户中心（已集成动态数据）
- `daily-farming/index.html` - 今日农事（可参考集成）

## 扩展建议

1. **缓存机制**：可以在前端添加localStorage缓存，减少API调用
2. **实时推送**：可以使用WebSocket实现预警信息的实时推送
3. **离线支持**：可以使用Service Worker实现离线访问
4. **数据可视化**：可以添加图表展示历史天气和农事数据

## 故障排查

### 问题1：用户信息不显示
- 检查是否已登录
- 查看浏览器控制台是否有错误
- 确认数据库已更新

### 问题2：天气信息不更新
- 检查API Key是否配置正确
- 查看后端日志是否有API调用错误
- 确认网络连接正常

### 问题3：数据库错误
- 确认已执行update_database.sql
- 检查数据库连接配置
- 查看后端错误日志

## 联系支持

如有问题，请查看：
- 后端日志：`backend/app.log`
- 浏览器控制台：F12 -> Console
- 数据库日志：MySQL错误日志
