import requests
from bs4 import BeautifulSoup
import pymysql
import uuid
from urllib.parse import urljoin
from datetime import datetime
import re

# ==========================================
# 🛑 数据库配置 (请根据你的本地 MySQL 修改密码)
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'shisannian1223',  # 替换为你的 MySQL 密码
    'database': 'clever_farming',
    'charset': 'utf8mb4'
}

# ==========================================
# 🎯 5大目标数据源矩阵
# ==========================================
TARGET_URLS = {
    "nyqx": "http://www.agri.cn/sc/nyqx/",  # 农业气象
    "nszd": "http://www.agri.cn/sc/nszd/",  # 农事指导
    "trsq": "http://www.agri.cn/sc/zxjc/trsq/",  # 土壤墒情
    "zwbch": "http://www.agri.cn/sc/zxjc/zwbch/",  # 植物病虫害
    "nyyw": "http://www.agri.cn/zx/nyyw/"  # 农业要闻 
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36"
}


def extract_entities(title):
    """旗舰版 NLP 实体提取 (融合微观农技与宏观政策)"""
    keywords = [
        # 作物类
        "苹果", "玉米", "小麦", "水稻", "大豆", "棉花", "蔬菜", "水果",
        # 病害与环境类
        "锈病", "台风", "干旱", "降雨", "施肥", "病虫害", "土壤", "墒情",
        "灌溉", "草害", "霜冻", "赤霉病", "虫害", "倒春寒",
        # 宏观政策与农机类 (为农业要闻特化)
        "无人机", "补贴", "政策", "丰收", "产量", "市场", "机械化", "春耕", "秋收"
    ]
    entities = [kw for kw in keywords if kw in title]
    return ",".join(entities)


def fetch_agri_data(category_code, base_url):
    print(f"\n🕸️ 正在抓取频道: 【{category_code}】 -> {base_url}")
    try:
        res = requests.get(base_url, headers=HEADERS, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        valid_links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            title = a_tag.get('title') or a_tag.text.strip()

            # 过滤逻辑：包含 htm，且标题有实质内容
            if len(title) > 8 and '.htm' in href:
                full_url = urljoin(base_url, href)

                # 尝试从 URL 提取官方发布日期 (如 t20240324_...)
                date_match = re.search(r'202\d{5}', href)
                pub_time = None
                if date_match:
                    date_str = date_match.group()
                    pub_time = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]} 12:00:00"
                else:
                    pub_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                valid_links.append({
                    "title": title,
                    "url": full_url,
                    "pub_time": pub_time
                })

        # 去重处理
        unique_links = {v['url']: v for v in valid_links}.values()
        print(f" -> 页面解析完成，共发现 {len(unique_links)} 条有效资讯。")
        return list(unique_links)

    except Exception as e:
        print(f"❌ 抓取【{category_code}】失败: {e}")
        return []


def store_to_mysql(news_list, category_code):
    connection = pymysql.connect(**DB_CONFIG)
    insert_count = 0
    try:
        with connection.cursor() as cursor:
            for item in news_list:
                nid = "N_" + uuid.uuid4().hex[:8]
                entities = extract_entities(item['title'])

                sql = """
                INSERT IGNORE INTO agri_news_articles 
                (nid, title, url, category, publish_time, entities) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                affected_rows = cursor.execute(sql, (
                    nid, item['title'], item['url'], category_code,
                    item['pub_time'], entities
                ))

                if affected_rows > 0:
                    insert_count += 1
                    print(f"   [新增] {item['title'][:20]}...")

        connection.commit()
    finally:
        connection.close()

    print(f"✅ 【{category_code}】入库完毕！新增入库 {insert_count} 条，忽略已存在 {len(news_list) - insert_count} 条。")


def run_pipeline():
    print("=" * 50)
    print(" 🚀 CleverFarming 5通道资讯爬虫引擎启动 ")
    print("=" * 50)
    for category, url in TARGET_URLS.items():
        scraped_data = fetch_agri_data(category, url)
        if scraped_data:
            store_to_mysql(scraped_data, category)


if __name__ == "__main__":
    run_pipeline()