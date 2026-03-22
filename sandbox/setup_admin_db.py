import pymysql
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from backend.config import Config
except ImportError:
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
        from config import Config
    except ImportError as e:
        print(f"Error importing Config: {e}")
        sys.exit(1)

def create_admin_tables():
    print("正在创建系统配置与操作日志相关的表...")
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # 系统配置表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_configs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    config_key VARCHAR(100) UNIQUE NOT NULL,
                    config_value TEXT NOT NULL,
                    description VARCHAR(255),
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("system_configs 表创建成功")

            # 操作日志表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS operation_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    admin_id INT,
                    action VARCHAR(100) NOT NULL,
                    module VARCHAR(50) NOT NULL,
                    details TEXT,
                    ip_address VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("operation_logs 表创建成功")
            
            # 添加系统配置基础数据
            cursor.execute("SELECT COUNT(*) FROM system_configs")
            if cursor.fetchone()[0] == 0:
                configs = [
                    ("site_name", "智禾慧农管理系统", "系统主站名称"),
                    ("maintenance_mode", "0", "是否开启维护模式 (0: 否, 1: 是)"),
                    ("max_upload_size", "10", "最大上传文件大小 (MB)"),
                    ("registration_open", "1", "是否开放新用户注册 (0: 否, 1: 是)")
                ]
                cursor.executemany(
                    "INSERT INTO system_configs (config_key, config_value, description) VALUES (%s, %s, %s)",
                    configs
                )
                print("系统配置基础数据填充成功")
            
            # 确保有管理员用户以插入示例日志
            cursor.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1")
            admin = cursor.fetchone()
            if admin:
                admin_id = admin[0]
                cursor.execute("SELECT COUNT(*) FROM operation_logs")
                if cursor.fetchone()[0] == 0:
                    logs = [
                        (admin_id, admin_id, "admin_login", "auth", "管理员登入系统", "127.0.0.1"),
                        (admin_id, admin_id, "update_config", "system", "更新系统名称", "127.0.0.1"),
                        (admin_id, admin_id, "view_users", "user_management", "查看用户列表", "127.0.0.1")
                    ]
                    cursor.executemany(
                        "INSERT INTO operation_logs (user_id, admin_id, action, module, details, ip_address) VALUES (%s, %s, %s, %s, %s, %s)",
                        logs
                    )
                    print("操作日志示例数据填充成功")
                
        connection.commit()
        connection.close()
        print("所有管理后台数据表与基础内容创建完毕。")
    except Exception as e:
        print(f"执行出错: {e}")

if __name__ == '__main__':
    create_admin_tables()
