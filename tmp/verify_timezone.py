import sys
import os

# Add backend and its packages to path first
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.append(backend_path)
sys.path.append(os.path.join(backend_path, 'packages'))

import pymysql
from app import get_db_connection
from utils import get_beijing_time

def verify():
    print(f"Current System Time: {get_beijing_time()}")
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT NOW() as db_now, @@session.time_zone as session_tz")
            result = cursor.fetchone()
            print(f"Database NOW(): {result['db_now']}")
            print(f"Database Session Timezone: {result['session_tz']}")
            
            # Check if they are close (within seconds)
            db_now = result['db_now']
            sys_now = get_beijing_time().replace(tzinfo=None) # NOW() returns a naive datetime usually
            
            diff = abs((db_now - sys_now).total_seconds())
            if diff < 10 and result['session_tz'] == '+08:00':
                print("SUCCESS: Database and System time are synchronized to Beijing Time!")
            else:
                print(f"WARNING: Time mismatch! Diff: {diff}s, TZ: {result['session_tz']}")
                
        conn.close()
    except Exception as e:
        print(f"Verification failed with error: {e}")

if __name__ == "__main__":
    verify()
