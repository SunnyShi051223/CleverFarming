import sys
import os
from datetime import datetime, timezone, timedelta

# Add backend/packages to path for pymysql
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.append(os.path.join(backend_path, 'packages'))

import pymysql

def get_beijing_time():
    return datetime.now(timezone(timedelta(hours=8)))

def verify():
    print(f"Current System Time (Beijing): {get_beijing_time()}")
    
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='shisannian1223',
            database='clever_farming',
            port=3306,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Manually set the timezone like we do in the app
            cursor.execute("SET time_zone = '+08:00'")
            
            cursor.execute("SELECT NOW() as db_now, @@session.time_zone as session_tz")
            result = cursor.fetchone()
            print(f"Database NOW(): {result['db_now']}")
            print(f"Database Session Timezone: {result['session_tz']}")
            
            db_now = result['db_now']
            sys_now = get_beijing_time().replace(tzinfo=None)
            
            diff = abs((db_now - sys_now).total_seconds())
            if diff < 60 and result['session_tz'] == '+08:00':
                print("SUCCESS: Database session is confirmed to be Beijing Time (+08:00)!")
            else:
                print(f"WARNING: Potential mismatch. Diff: {diff}s, TZ: {result['session_tz']}")
        
        connection.close()
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify()
