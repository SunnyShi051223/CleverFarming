import pymysql
from config import Config

conn = pymysql.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB,
    port=Config.MYSQL_PORT,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    cursor.execute('SELECT DISTINCT alert_type FROM farming_alerts')
    alert_types = cursor.fetchall()
    print('预警类型:', alert_types)
    
    # 也查询一些预警数据来了解完整结构
    cursor.execute('SELECT * FROM farming_alerts LIMIT 5')
    alerts = cursor.fetchall()
    print('预警数据示例:', alerts)

conn.close()