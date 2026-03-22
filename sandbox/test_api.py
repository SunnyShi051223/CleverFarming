import pymysql
import os
import sys

# Setup imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
from config import Config

def test():
    conn = pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    current_user_id = 1
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.content, p.likes_count, 
                       DATE_FORMAT(p.created_at, '%%Y-%%m-%%d %%H:%%i') as created_at,
                       u.username, u.avatar_url,
                       EXISTS(SELECT 1 FROM post_likes pl WHERE pl.post_id = p.id AND pl.user_id = %s) as is_liked,
                       (SELECT COUNT(*) FROM community_comments cc WHERE cc.post_id = p.id) as comments_count
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
            """, (current_user_id,))
            posts = cursor.fetchall()
            print("Posts returned:", len(posts))
            for p in posts:
                print(p)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    test()
