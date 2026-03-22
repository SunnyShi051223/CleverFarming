import pymysql
from config import Config

# 连接数据库
conn = pymysql.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB,
    port=Config.MYSQL_PORT
)
cursor = conn.cursor()

# 为每个用户设置不同的个性化信息
updates = [
    (1, '北京', '小麦', 100.00, 1),  # admin
    (2, '武汉', '水稻', 50.00, 1),   # farmer
    (3, '上海', '玉米', 80.00, 1),   # test_yang
    (4, '广州', '蔬菜', 30.00, 1)    # 111
]

print("开始更新用户个性化信息...")
for user_id, city, crop_type, farm_area, is_initialized in updates:
    cursor.execute(
        'UPDATE users SET city = %s, crop_type = %s, farm_area = %s, is_initialized = %s WHERE id = %s',
        (city, crop_type, farm_area, is_initialized, user_id)
    )
    conn.commit()
    print(f'用户 {user_id} 更新成功: 城市={city}, 作物={crop_type}, 面积={farm_area}亩, 已初始化={is_initialized}')

# 验证更新结果
print('\n更新后的用户数据:')
cursor.execute('SELECT id, username, city, crop_type, farm_area, is_initialized FROM users')
for row in cursor.fetchall():
    print(f'ID: {row[0]}, 用户名: {row[1]}, 城市: {row[2]}, 作物: {row[3]}, 面积: {row[4]}亩, 已初始化: {row[5]}')

conn.close()
print('\n所有用户个性化信息更新完成！')