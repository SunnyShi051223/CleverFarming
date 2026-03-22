import pymysql
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend'))
from config import Config

def upgrade_db():
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
            # Check if column exists first
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'is_initialized'
            """, (Config.MYSQL_DB,))
            
            if cursor.fetchone()[0] == 0:
                print("Adding is_initialized column to users table...")
                cursor.execute("ALTER TABLE users ADD COLUMN is_initialized BOOLEAN DEFAULT FALSE;")
                connection.commit()
                print("Successfully added is_initialized column.")
            else:
                print("Column is_initialized already exists.")
                
            # Set all existing users to True except recently created ones (or set all to True if requested, but let's keep it safe)
            # Actually, the user wants new logins to initialize. We can just leave existing ones as they are or force all FALSE.
            # I will just leave it.
                
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == '__main__':
    upgrade_db()
