# 数据库初始化脚本
import pymysql
import bcrypt
from datetime import datetime
from config import Config
from utils import get_beijing_time

def init_database():
    """初始化数据库和表结构"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=Config.MYSQL_PORT,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 创建数据库（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {Config.MYSQL_DB} 创建成功或已存在")
            
        connection.close()
        
        # 连接到指定数据库
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            charset='utf8mb4'
        )
        # 设置会话时区为北京时间 (UTC+8)
        with connection.cursor() as cursor:
            cursor.execute("SET time_zone = '+08:00'")
        
        with connection.cursor() as cursor:
            # 创建用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role ENUM('user', 'admin') NOT NULL DEFAULT 'user',
                    location VARCHAR(100) COMMENT '详细地址',
                    city VARCHAR(50) DEFAULT '北京' COMMENT '城市',
                    crop_type VARCHAR(50) DEFAULT '小麦' COMMENT '种植作物类型',
                    farm_area DECIMAL(10,2) COMMENT '农田面积（亩）',
                    avatar_url VARCHAR(255) COMMENT '头像URL',
                    last_login DATETIME COMMENT '最后登录时间',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("用户表创建成功或已存在")
            
            # 创建知识节点表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_nodes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    content TEXT,
                    summary TEXT,
                    keywords VARCHAR(500),
                    view_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("知识节点表创建成功或已存在")
            
            # 创建病虫害识别历史记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS disease_identification_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    disease_name VARCHAR(100) NOT NULL,
                    confidence DECIMAL(5,2) NOT NULL,
                    symptoms TEXT,
                    solutions TEXT,
                    image_path VARCHAR(500),
                    voice_input TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("病虫害识别历史记录表创建成功或已存在")
            
            # 创建农事预警表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS farming_alerts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    alert_type ENUM('weather', 'pest', 'farming') NOT NULL COMMENT '预警类型',
                    title VARCHAR(200) NOT NULL COMMENT '预警标题',
                    content TEXT NOT NULL COMMENT '预警内容',
                    priority ENUM('high', 'medium', 'low') DEFAULT 'medium' COMMENT '优先级',
                    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
                    location VARCHAR(100) COMMENT '地区',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    read_at DATETIME COMMENT '阅读时间',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_is_read (is_read),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("农事预警表创建成功或已存在")
            
            # 创建每日任务表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(200) NOT NULL COMMENT '任务标题',
                    description TEXT COMMENT '任务描述',
                    task_type VARCHAR(50) COMMENT '任务类型',
                    priority ENUM('high', 'medium', 'low') DEFAULT 'medium' COMMENT '优先级',
                    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending' COMMENT '任务状态',
                    scheduled_date DATE NOT NULL COMMENT '计划日期',
                    scheduled_time TIME COMMENT '计划时间',
                    location VARCHAR(100) COMMENT '任务地点',
                    completed_at DATETIME COMMENT '完成时间',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (status),
                    INDEX idx_scheduled_date (scheduled_date)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("每日任务表创建成功或已存在")
            
            # 检查是否有默认用户，如果没有则创建
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                # 创建默认管理员用户
                admin_password = "admin123"
                admin_hash = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role) 
                    VALUES (%s, %s, %s)
                """, ("admin", admin_hash, "admin"))
                
                # 创建默认农户用户
                farmer_password = "farmer123"
                farmer_hash = bcrypt.hashpw(farmer_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role, location, city, crop_type, farm_area, avatar_url) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, ("farmer", farmer_hash, "user", "北京市朝阳区", "北京", "小麦", 50.00, 
                     "https://ts1.tc.mm.bing.net/th/id/OIP-C.FZ6GQ0UcHCLgdPoHx-4UlgHaHa?rs=1&pid=ImgDetMain&o=7&rm=3"))
                
                print("默认用户创建成功:")
                print("- 管理员: admin / admin123")
                print("- 农户: farmer / farmer123")
                
                # 获取farmer用户ID
                cursor.execute("SELECT id FROM users WHERE username = 'farmer'")
                farmer_id = cursor.fetchone()[0]
                
                # 插入示例预警数据
                sample_alerts = [
                    (farmer_id, 'weather', '暴雨蓝色预警', '预计未来24小时内将有大到暴雨，请注意防范可能引发的洪涝灾害，及时疏通排水沟渠。', 'high', '北京市'),
                    (farmer_id, 'pest', '稻飞虱虫害预警', '近期气温适宜，稻飞虱繁殖加快，请及时检查田间虫情，必要时进行药剂防治。', 'medium', '北京市'),
                    (farmer_id, 'farming', '水稻分蘖期管理提醒', '当前正值水稻分蘖期，需保持浅水层，适时追施分蘖肥，促进有效分蘖。', 'low', '北京市'),
                    (farmer_id, 'weather', '高温橙色预警', '未来一周将持续高温天气，最高气温可达37℃以上，请注意防暑降温，合理安排农事活动。', 'high', '北京市'),
                    (farmer_id, 'pest', '玉米螟虫害预警', '近期发现玉米螟幼虫活动频繁，请及时检查玉米心叶，发现虫害立即防治。', 'medium', '北京市')
                ]
                
                for alert in sample_alerts:
                    cursor.execute("""
                        INSERT INTO farming_alerts (user_id, alert_type, title, content, priority, location)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, alert)
                
                print("示例预警数据插入成功")
                
                # 插入示例任务数据
                from datetime import date, time
                today = get_beijing_time().date()
                
                sample_tasks = [
                    (farmer_id, '小麦病虫害防治', '近期发现小麦叶片出现锈病症状，需要立即进行药剂喷洒防治。建议使用三唑酮或丙环唑，注意用药浓度和安全间隔期。', 
                     'pest_control', 'high', 'pending', today, time(8, 0), '东区田块'),
                    (farmer_id, '灌溉作业', '根据土壤墒情监测，西区田块需要进行灌溉。预计灌溉时间2小时，注意控制水量，避免积水。', 
                     'irrigation', 'medium', 'pending', today, time(14, 0), '西区田块'),
                    (farmer_id, '追肥作业', '小麦进入拔节期，需要追施拔节肥。建议每亩施用尿素10-15公斤，结合灌溉进行。', 
                     'fertilization', 'low', 'pending', today, time(16, 0), '南区田块'),
                    (farmer_id, '田间巡查', '对所有田块进行日常巡查，检查作物生长情况和病虫害发生情况。', 
                     'inspection', 'low', 'completed', today, time(6, 0), '全部田块')
                ]
                
                for task in sample_tasks:
                    cursor.execute("""
                        INSERT INTO daily_tasks (user_id, title, description, task_type, priority, status, 
                                                scheduled_date, scheduled_time, location)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, task)
                
                print("示例任务数据插入成功")
            
            # 插入一些示例知识数据
            cursor.execute("SELECT COUNT(*) FROM knowledge_nodes")
            knowledge_count = cursor.fetchone()[0]
            
            if knowledge_count == 0:
                sample_knowledge = [
                    {
                        'title': '水稻种植基础知识',
                        'category': '种植技术',
                        'summary': '详细介绍水稻从选种到收获的完整种植流程，包括育苗、移栽、田间管理等关键技术要点。',
                        'content': '''<h3>一、选种与育苗</h3>
                        <p>选择适合当地气候条件的优质水稻品种，进行种子处理。育苗时注意控制温度和湿度，确保苗期健康生长。</p>
                        
                        <h3>二、整地与移栽</h3>
                        <p>整地要求平整，保持适当水深。移栽时注意株行距，一般行距30cm，株距20cm。</p>
                        
                        <h3>三、田间管理</h3>
                        <p>包括水分管理、施肥、病虫害防治等。注意不同生长阶段的水肥需求。</p>
                        
                        <h3>四、收获与储存</h3>
                        <p>适时收获，避免过熟或欠熟。储存时注意防潮防虫。</p>''',
                        'keywords': '水稻,种植,育苗,移栽,田间管理'
                    },
                    {
                        'title': '水稻病虫害综合防治技术',
                        'category': '病虫害防治',
                        'summary': '全面介绍水稻常见病虫害的识别特征、发生规律和综合防治措施，包括农业防治、生物防治和化学防治。',
                        'content': '''<h3>一、主要病害防治</h3>
                        <p><strong>稻瘟病：</strong>选用抗病品种，合理施肥，及时排水。发病初期可用三环唑等药剂防治。</p>
                        <p><strong>纹枯病：</strong>控制田间湿度，合理密植。可用井冈霉素等药剂防治。</p>
                        
                        <h3>二、主要虫害防治</h3>
                        <p><strong>稻飞虱：</strong>采用灯光诱杀，保护天敌。可用吡虫啉等药剂防治。</p>
                        <p><strong>稻纵卷叶螟：</strong>合理密植，及时除草。可用阿维菌素等药剂防治。</p>
                        
                        <h3>三、综合防治策略</h3>
                        <p>以农业防治为基础，生物防治为重点，化学防治为辅助的综合防治体系。</p>''',
                        'keywords': '水稻,病虫害,防治,稻瘟病,稻飞虱,综合防治'
                    },
                    {
                        'title': '有机肥料制作与使用方法',
                        'category': '肥料管理',
                        'summary': '详细介绍有机肥料的制作工艺、养分特点和使用方法，包括堆肥、沤肥、绿肥等不同类型的有机肥料。',
                        'content': '''<h3>一、有机肥料类型</h3>
                        <p><strong>堆肥：</strong>利用秸秆、畜禽粪便等有机废弃物堆制而成。</p>
                        <p><strong>沤肥：</strong>将有机物料在厌氧条件下沤制而成。</p>
                        <p><strong>绿肥：</strong>种植豆科作物翻压入土作为肥料。</p>
                        
                        <h3>二、制作方法</h3>
                        <p>1. 选择合适的原料；2. 控制碳氮比；3. 调节水分和温度；4. 定期翻堆；5. 充分腐熟。</p>
                        
                        <h3>三、使用方法</h3>
                        <p>基肥施用为主，追肥为辅。注意与化肥配合使用，提高肥效。</p>''',
                        'keywords': '有机肥,堆肥,沤肥,绿肥,制作,使用'
                    },
                    {
                        'title': '土壤改良与培肥技术',
                        'category': '土壤管理',
                        'summary': '介绍土壤改良的基本原理和方法，包括深耕、增施有机肥、调节土壤pH值等技术措施。',
                        'content': '''<h3>一、土壤问题诊断</h3>
                        <p>通过土壤检测了解土壤养分状况、pH值、有机质含量等指标。</p>
                        
                        <h3>二、改良措施</h3>
                        <p><strong>深耕：</strong>改善土壤结构，增加耕作层厚度。</p>
                        <p><strong>增施有机肥：</strong>提高土壤有机质含量，改善土壤理化性质。</p>
                        <p><strong>调节pH值：</strong>酸性土壤施用石灰，碱性土壤施用石膏。</p>
                        
                        <h3>三、培肥技术</h3>
                        <p>轮作倒茬、种植绿肥、秸秆还田等措施。</p>''',
                        'keywords': '土壤改良,培肥,深耕,有机质,轮作,绿肥'
                    },
                    {
                        'title': '节水灌溉技术',
                        'category': '灌溉技术',
                        'summary': '介绍现代农业节水灌溉技术，包括滴灌、喷灌、微灌等高效节水灌溉方式及其适用条件。',
                        'content': '''<h3>一、节水灌溉原理</h3>
                        <p>通过减少水分损失，提高水分利用效率，实现农业可持续发展。</p>
                        
                        <h3>二、主要技术</h3>
                        <p><strong>滴灌：</strong>将水直接输送到作物根部，节水效果显著。</p>
                        <p><strong>喷灌：</strong>模拟自然降雨，适合大面积农田。</p>
                        <p><strong>微灌：</strong>介于滴灌和喷灌之间，适合设施农业。</p>
                        
                        <h3>三、管理要点</h3>
                        <p>根据作物需水规律、土壤墒情、天气预报等因素确定灌溉时间和水量。</p>''',
                        'keywords': '节水灌溉,滴灌,喷灌,微灌,水分利用效率'
                    },
                    {
                        'title': '温室蔬菜栽培技术',
                        'category': '设施农业',
                        'summary': '详细介绍温室蔬菜栽培的环境控制、品种选择、栽培管理等关键技术，提高温室蔬菜产量和品质。',
                        'content': '''<h3>一、温室环境控制</h3>
                        <p><strong>温度：</strong>根据作物需求调节温室温度，注意昼夜温差。</p>
                        <p><strong>湿度：</strong>控制空气湿度，防止病害发生。</p>
                        <p><strong>光照：</strong>合理设计温室结构，充分利用自然光。</p>
                        
                        <h3>二、品种选择</h3>
                        <p>选择适应性强、抗病性好、产量高的优质品种。</p>
                        
                        <h3>三、栽培管理</h3>
                        <p>合理密植、科学施肥、及时防治病虫害。</p>''',
                        'keywords': '温室,蔬菜,栽培,环境控制,品种选择,栽培管理'
                    },
                    {
                        'title': '智慧农业技术应用',
                        'category': '智慧农业',
                        'summary': '介绍物联网、大数据、人工智能等技术在现代农业中的应用，包括精准农业、智能监测、自动化控制等。',
                        'content': '''<h3>一、物联网技术</h3>
                        <p>通过传感器实时监测土壤、气候、作物生长状况，实现精准管理。</p>
                        
                        <h3>二、大数据分析</h3>
                        <p>收集和分析农业生产数据，为决策提供科学依据。</p>
                        
                        <h3>三、人工智能应用</h3>
                        <p>利用AI技术进行病虫害识别、产量预测、智能灌溉等。</p>
                        
                        <h3>四、自动化设备</h3>
                        <p>无人农机、自动喷药、智能温室等自动化设备提高生产效率。</p>''',
                        'keywords': '智慧农业,物联网,大数据,人工智能,精准农业,自动化'
                    },
                    {
                        'title': '农产品质量安全控制',
                        'category': '质量安全',
                        'summary': '介绍农产品质量安全控制体系，包括生产标准、检测方法、认证体系等，确保农产品质量安全。',
                        'content': '''<h3>一、生产标准</h3>
                        <p>建立完善的生产标准体系，规范农业生产过程。</p>
                        
                        <h3>二、检测方法</h3>
                        <p>采用先进的检测技术和设备，确保检测结果准确可靠。</p>
                        
                        <h3>三、认证体系</h3>
                        <p>建立有机食品、绿色食品、无公害食品等认证体系。</p>
                        
                        <h3>四、追溯系统</h3>
                        <p>建立农产品质量安全追溯系统，实现全程可追溯。</p>''',
                        'keywords': '农产品,质量安全,生产标准,检测,认证,追溯'
                    }
                ]
                
                for knowledge in sample_knowledge:
                    cursor.execute("""
                        INSERT INTO knowledge_nodes (title, category, content, summary, keywords)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (knowledge['title'], knowledge['category'], knowledge['content'], 
                         knowledge['summary'], knowledge['keywords']))
                
                print("示例知识数据插入成功")
            
            connection.commit()
            print("数据库初始化完成！")
            
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        return False
    finally:
        if 'connection' in locals() and connection:
            connection.close()
    
    return True

if __name__ == "__main__":
    init_database()
