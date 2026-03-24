import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def verify_alerts():
    connection = pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '123456'),
        database=os.getenv('MYSQL_DB', 'clever_farming'),
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # Check table structure
            cursor.execute("DESCRIBE farming_alerts")
            columns = {col['Field']: col['Type'] for col in cursor.fetchall()}
            
            print("--- Table Structure ---")
            print(f"alert_type: {columns.get('alert_type')}")
            print(f"alert_subtype: {columns.get('alert_subtype')}")
            
            # Check data
            cursor.execute("SELECT alert_type, alert_subtype, title FROM farming_alerts")
            rows = cursor.fetchall()
            
            print("\n--- Seeded Data ---")
            for row in rows:
                print(f"Type: {row['alert_type']:<6} | Subtype: {row['alert_subtype']:<6} | Title: {row['title']}")
                
            # Verify counts
            cursor.execute("SELECT alert_type, COUNT(*) as count FROM farming_alerts GROUP BY alert_type")
            counts = cursor.fetchall()
            print("\n--- Counts ---")
            for c in counts:
                print(f"{c['alert_type']}: {c['count']}")
                
    finally:
        connection.close()

if __name__ == "__main__":
    verify_alerts()
