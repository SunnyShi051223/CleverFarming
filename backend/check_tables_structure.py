import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'shisannian1223',
    'database': 'clever_farming',
    'charset': 'utf8mb4'
}

def check_tables():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SHOW TABLES LIKE 'agri_news_articles'")
        agri_exists = cursor.fetchone() is not None
        print(f"agri_news_articles 表存在: {agri_exists}")
        
        cursor.execute("SHOW TABLES LIKE 'farming_alerts'")
        alerts_exists = cursor.fetchone() is not None
        print(f"farming_alerts 表存在: {alerts_exists}")
        
        # 检查 agri_news_articles 表结构
        if agri_exists:
            print("\n=== agri_news_articles 表结构 ===")
            cursor.execute("DESCRIBE agri_news_articles")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        
        # 检查 farming_alerts 表结构
        if alerts_exists:
            print("\n=== farming_alerts 表结构 ===")
            cursor.execute("DESCRIBE farming_alerts")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[0]}: {col[1]}")
        
        # 检查当前数据量
        if agri_exists:
            cursor.execute("SELECT COUNT(*) FROM agri_news_articles")
            count = cursor.fetchone()[0]
            print(f"\nagri_news_articles 表中数据量: {count} 条")
            
            # 查看最近几条数据
            cursor.execute("SELECT id, title, category, url, publish_time, entities FROM agri_news_articles ORDER BY publish_time DESC LIMIT 3")
            rows = cursor.fetchall()
            if rows:
                print("\n最近3条新闻:")
                for row in rows:
                    print(f"  ID: {row[0]}, 标题: {row[1][:30]}..., 类别: {row[2]}, URL: {row[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    check_tables()