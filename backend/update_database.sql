-- 更新数据库表结构，添加用户位置、作物等信息字段

-- 1. 更新 users 表，添加地理位置和农业相关字段
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS location VARCHAR(100) COMMENT '详细地址',
ADD COLUMN IF NOT EXISTS city VARCHAR(50) DEFAULT '北京' COMMENT '城市',
ADD COLUMN IF NOT EXISTS crop_type VARCHAR(50) DEFAULT '小麦' COMMENT '种植作物类型',
ADD COLUMN IF NOT EXISTS farm_area DECIMAL(10,2) COMMENT '农田面积（亩）',
ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(255) COMMENT '头像URL',
ADD COLUMN IF NOT EXISTS last_login DATETIME COMMENT '最后登录时间';

-- 2. 创建农事预警表（如果不存在）
CREATE TABLE IF NOT EXISTS farming_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='农事预警表';

-- 3. 创建每日任务表（如果不存在）
CREATE TABLE IF NOT EXISTS daily_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日任务表';

-- 4. 插入示例预警数据
INSERT INTO farming_alerts (user_id, alert_type, title, content, priority, location) VALUES
(1, 'weather', '暴雨蓝色预警', '预计未来24小时内将有大到暴雨，请注意防范可能引发的洪涝灾害，及时疏通排水沟渠。', 'high', '北京市'),
(1, 'pest', '稻飞虱虫害预警', '近期气温适宜，稻飞虱繁殖加快，请及时检查田间虫情，必要时进行药剂防治。', 'medium', '北京市'),
(1, 'farming', '水稻分蘖期管理提醒', '当前正值水稻分蘖期，需保持浅水层，适时追施分蘖肥，促进有效分蘖。', 'low', '北京市'),
(1, 'weather', '高温橙色预警', '未来一周将持续高温天气，最高气温可达37℃以上，请注意防暑降温，合理安排农事活动。', 'high', '北京市'),
(1, 'pest', '玉米螟虫害预警', '近期发现玉米螟幼虫活动频繁，请及时检查玉米心叶，发现虫害立即防治。', 'medium', '北京市');

-- 5. 插入示例任务数据
INSERT INTO daily_tasks (user_id, title, description, task_type, priority, status, scheduled_date, scheduled_time, location) VALUES
(1, '小麦病虫害防治', '近期发现小麦叶片出现锈病症状，需要立即进行药剂喷洒防治。建议使用三唑酮或丙环唑，注意用药浓度和安全间隔期。', 'pest_control', 'high', 'pending', CURDATE(), '08:00:00', '东区田块'),
(1, '灌溉作业', '根据土壤墒情监测，西区田块需要进行灌溉。预计灌溉时间2小时，注意控制水量，避免积水。', 'irrigation', 'medium', 'pending', CURDATE(), '14:00:00', '西区田块'),
(1, '追肥作业', '小麦进入拔节期，需要追施拔节肥。建议每亩施用尿素10-15公斤，结合灌溉进行。', 'fertilization', 'low', 'pending', CURDATE(), '16:00:00', '南区田块'),
(1, '田间巡查', '对所有田块进行日常巡查，检查作物生长情况和病虫害发生情况。', 'inspection', 'low', 'completed', CURDATE(), '06:00:00', '全部田块');

-- 6. 更新示例用户数据
UPDATE users SET 
    location = '北京市朝阳区',
    city = '北京',
    crop_type = '小麦',
    farm_area = 50.00,
    avatar_url = 'https://ts1.tc.mm.bing.net/th/id/OIP-C.FZ6GQ0UcHCLgdPoHx-4UlgHaHa?rs=1&pid=ImgDetMain&o=7&rm=3'
WHERE id = 1;
