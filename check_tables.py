import pymysql

# 硬编码数据库连接信息
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='XXX',
    database='CleverFarming',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

print('=== farming_alerts表结构 ===')
cursor.execute('DESCRIBE farming_alerts')
rows = cursor.fetchall()
for row in rows:
    print(row)

print('\n=== agri_news_articles表结构 ===')
cursor.execute('DESCRIBE agri_news_articles')
rows = cursor.fetchall()
for row in rows:
    print(row)

print('\n=== 检查farming_alerts表数据 ===')
cursor.execute('SELECT * FROM farming_alerts LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)

print('\n=== 检查agri_news_articles表数据 ===')
cursor.execute('SELECT * FROM agri_news_articles LIMIT 5')
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()