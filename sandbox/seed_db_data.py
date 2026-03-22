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

def seed_db():
    print("正在向数据库添加初始基础内容...")
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
            # 1. 确保有可以关联的用户
            cursor.execute("SELECT id FROM users LIMIT 1")
            user = cursor.fetchone()
            if not user:
                print("未找到用户，请确保先运行并插入了测试用户")
                return
            user_id = user[0]
            
            # 2. 添加社区帖子
            cursor.execute("SELECT COUNT(*) FROM community_posts")
            post_count = cursor.fetchone()[0]
            
            if post_count == 0:
                print("添加社区帖子初始数据...")
                posts = [
                    (user_id, "今天试验了新的水稻品种，抗病性确实比去年的好很多！", 5),
                    (user_id, "请问大家，最近多雨天气，玉米地里除草有什么好建议吗？", 2),
                    (user_id, "分享一个自制的简易灌溉系统，成本不到200元，非常实用。", 10)
                ]
                cursor.executemany(
                    "INSERT INTO community_posts (user_id, content, likes_count) VALUES (%s, %s, %s)",
                    posts
                )
                
                # 获取插入的帖子ID用于添加评论
                cursor.execute("SELECT id FROM community_posts ORDER BY id DESC LIMIT 3")
                post_ids = [row[0] for row in cursor.fetchall()]
                
                if post_ids:
                    # 添加评论
                    comments = [
                        (post_ids[0], user_id, "确实，我也试了那个品种，长势喜人。"),
                        (post_ids[1], user_id, "可以用些低毒环保的除草剂，注意用量。")
                    ]
                    cursor.executemany(
                        "INSERT INTO community_comments (post_id, user_id, content) VALUES (%s, %s, %s)",
                        comments
                    )
            else:
                print("社区帖子已有数据，跳过...")

            # 3. 添加病虫害识别历史
            cursor.execute("SELECT COUNT(*) FROM disease_identification_history")
            disease_count = cursor.fetchone()[0]
            
            if disease_count == 0:
                print("添加病虫害识别历史记录...")
                histories = [
                    (user_id, "水稻稻瘟病", 0.95, "叶片出现暗绿色小斑点，逐渐变成菱形或纺锤形病斑", "1. 选用抗病品种 2. 合理施肥 3. 喷洒三环唑等药剂", None, None),
                    (user_id, "玉米大斑病", 0.88, "叶片上出现长梭形青灰色病斑", "1. 摘除底部病叶 2. 使用代森锰锌或百菌清进行防治", None, None)
                ]
                cursor.executemany(
                    """INSERT INTO disease_identification_history 
                       (user_id, disease_name, confidence, symptoms, solutions, image_path, voice_input) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    histories
                )
            else:
                print("病虫害识别记录已有数据，跳过...")

        connection.commit()
        connection.close()
        print("数据库基础内容填充完毕！")
    except Exception as e:
        print(f"数据填充出错: {e}")

if __name__ == '__main__':
    seed_db()
