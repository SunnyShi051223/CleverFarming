# 智禾慧农 - 智能农业管理系统

## 系统简介

欢迎访问：https://cleverfarming.alwaysdata.net

智禾慧农是一个智能农业管理系统，为农户提供农作物病虫害识别、农时预警、知识库查询等功能。

## 功能特性

- 🔐 **用户认证系统**: 支持农户和管理员两种角色
- 👁️ **慧眼识病**: 上传农作物图片，智能识别病虫害
- ⏰ **农时预警**: 实时获取天气预警和农事提醒
- 👥 **智慧农友**: 农户交流社区
- 📚 **农识宝典**: 农业知识库查询
- 📰 **农情速递**: 农业资讯浏览

## 系统要求

- Python 3.7+
- MySQL 5.7+
- 现代浏览器（Chrome、Firefox、Safari、Edge）

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.7+
- MySQL数据库

### 2. 数据库配置

修改 `backend/config.py` 中的数据库配置：

```python
MYSQL_HOST = 'localhost'      # 数据库主机
MYSQL_USER = 'root'           # 数据库用户名
MYSQL_PASSWORD = 'your_password'  # 数据库密码
MYSQL_DB = 'CleverFarming'    # 数据库名称
MYSQL_PORT = 3306             # 数据库端口
```

### 3. 启动系统

进入backend目录，运行启动脚本：

```bash
cd backend
python start.py
```

或者手动启动：

```bash
cd backend
pip install -r requirements
python init_db.py  # 初始化数据库
python app.py      # 启动服务器
```

### 4. 访问系统

打开浏览器访问：http://localhost:5000

## 默认登录账号

- **管理员**: admin / admin123
- **农户**: farmer / farmer123

## 项目结构

```
CleverFarming/
├── api/                    # 前端页面
│   ├── login.html         # 登录页面
│   ├── farmer.html        # 农户中心
│   └── admin.html         # 管理员中心
├── backend/               # 后端代码
│   ├── app.py            # Flask应用主文件
│   ├── config.py         # 配置文件
│   ├── models.py         # 数据模型
│   ├── utils.py          # 工具函数
│   ├── init_db.py        # 数据库初始化脚本
│   ├── start.py          # 启动脚本
│   └── requirements      # 依赖包列表
└── README.md             # 项目说明
```

## 技术栈

### 后端
- Flask: Web框架
- PyMySQL: MySQL数据库连接
- bcrypt: 密码加密
- PyJWT: JWT令牌处理
- Flask-CORS: 跨域请求处理

### 前端
- HTML5/CSS3/JavaScript
- Font Awesome: 图标库
- 响应式设计

## 常见问题

### 1. 无法连接数据库
- 检查MySQL服务是否启动
- 确认数据库配置信息是否正确
- 确保数据库用户有足够权限

### 2. 登录后无法跳转
- 检查浏览器控制台是否有错误信息
- 确认Flask服务器正常运行
- 检查CORS配置

### 3. 页面显示异常
- 清除浏览器缓存
- 检查JavaScript控制台错误
- 确认所有静态资源加载正常

## 开发说明

### 添加新功能
1. 在 `backend/app.py` 中添加新的路由
2. 在前端页面中添加对应的UI组件
3. 更新数据库结构（如需要）

### 数据库操作
- 使用 `backend/init_db.py` 初始化数据库
- 修改表结构后需要更新初始化脚本

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题，请提交Issue或联系开发团队。
