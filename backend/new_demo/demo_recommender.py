import pymysql
import math
from datetime import datetime

# ==========================================
# 🛑 数据库配置 (请修改为你的本地 MySQL 密码)
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'shisannian1223',  # 替换为你的密码
    'database': 'clever_farming',
    'charset': 'utf8mb4'
}

# ==========================================
# 🧠 IP2 隐式特征图谱 (模拟神经网络的 Embedding 联想)
# ==========================================
# 真实大模型能自己学出来，我们在 Demo 中用字典来模拟这种“举一反三”的隐式兴趣
IP2_KNOWLEDGE_GRAPH = {
    "小麦": ["化肥", "尿素", "赤霉病", "干旱", "收割机", "霜冻"],
    "水稻": ["暴雨", "抽水", "稻瘟病", "插秧", "农药"],
    "玉米": ["复合肥", "秋收", "玉米锈病", "大风", "倒伏"],
    "蔬菜": ["大棚", "农膜", "保暖", "市场价格", "农药残留"],
    "水果": ["修剪", "套袋", "果蝇", "冷链", "冰雹"],
    "棉花": ["采棉机", "打顶", "蚜虫", "高温"]
}


def calculate_time_decay(publish_time):
    """时间衰减函数：越老的新闻，权重越低"""
    if not publish_time:
        return 0.5
    now = datetime.now()
    days_old = (now - publish_time).days
    # 使用指数衰减公式模拟推荐系统的时效性：e^(-λt)
    # 新闻在 0 天衰减系数为 1.0，7天后大约衰减到 0.5
    decay_weight = math.exp(-0.1 * max(0, days_old))
    return max(0.1, decay_weight)  # 保底给0.1的权重


def run_recommendation_engine():
    print("=" * 50)
    print(" 🚀 CleverFarming 双塔+IP2 推荐引擎启动 ")
    print("=" * 50)

    connection = pymysql.connect(**DB_CONFIG)

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 1. 获取所有用户 
            cursor.execute("SELECT id, username, city, crop_type FROM users")
            users = cursor.fetchall()

            # 2. 获取近期的候选新闻池 (最近30天的资讯)
            cursor.execute("""
                SELECT id, title, category, entities, publish_time 
                FROM agri_news_articles 
                ORDER BY publish_time DESC LIMIT 50
            """)
            news_pool = cursor.fetchall()

            if not news_pool:
                print("⚠️ 资讯库为空，请先运行爬虫抓取数据！")
                return

            # 3. 为每个用户进行双塔打分与推送
            for user in users:
                user_id = user['id']
                crop = user.get('crop_type', '')
                city = user.get('city', '')

                print(f"\n🎯 正在为用户 [ID:{user_id} {user['username']}] (地区:{city}, 作物:{crop}) 计算推荐流...")

                best_news = None
                highest_score = -1.0

                # 获取该作物的隐式兴趣词表
                implicit_interests = IP2_KNOWLEDGE_GRAPH.get(crop, [])

                for news in news_pool:
                    title_entities = str(news['entities'] or '') + str(news['title'])

                    # ------ [算法核心：模拟打分机制] ------
                    score = 0.0

                    # A. 显式兴趣匹配 (Two-Tower Base: 作物直接命中)
                    if crop and crop in title_entities:
                        score += 5.0

                    # B. 隐式兴趣挖掘 (IP2 Algorithm: 没提作物，但提了相关的病害/农药)
                    for implicit_word in implicit_interests:
                        if implicit_word in title_entities:
                            score += 3.0  # IP2 隐式加分！

                    # C. 地区属性加持 (如果新闻刚好带有用户所在城市，加急分)
                    if city and city in title_entities:
                        score += 2.0

                    # D. 时效性衰减 (Time Weight)
                    time_weight = calculate_time_decay(news['publish_time'])
                    final_score = score * time_weight

                    # 记录最高分的新闻
                    if final_score > highest_score:
                        highest_score = final_score
                        best_news = news

                # 4. 将得分最高的新闻作为预警/推荐推送到 farming_alerts 表
                if best_news and highest_score > 0:
                    # 根据新闻分类确定 alert_type
                    # 农业资讯新闻 -> 'news'，气象预警 -> 'alert'
                    if best_news['category'] == 'nyqx':
                        alert_type = 'alert'  # 气象预警
                    else:
                        alert_type = 'news'   # 农业资讯新闻
                    
                    content = f"【系统智能推荐】基于您的种植作物({crop})与所在地区({city})，为您精选资讯：{best_news['title']}"

                    # 插入到 farming_alerts 表中
                    insert_sql = """
                        INSERT INTO farming_alerts 
                        (user_id, alert_type, alert_subtype, title, content, priority, location)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    # 设置 alert_subtype，根据新闻分类
                    category_map = {
                        'trsq': 'soil_moisture',      # 土壤墒情
                        'zwbch': 'disaster',          # 灾害预警
                        'nyqx': 'weather',            # 气象预警
                        'bch': 'pest',                # 病虫害
                        'nyyw': 'agriculture'         # 农业要闻
                    }
                    alert_subtype = category_map.get(best_news['category'], 'general')
                    
                    cursor.execute(insert_sql, (
                        user_id, 
                        alert_type, 
                        alert_subtype,
                        best_news['title'], 
                        content, 
                        'high', 
                        city
                    ))

                    print(f"   => 🌟 [推送成功] 最终得分: {highest_score:.2f}")
                    print(f"   => 📰 推送类型: {alert_type} | 分类: {best_news['category']} | {best_news['title']}")
                else:
                    print("   => 🤷‍♂️ 暂无高匹配度资讯，本次不推送，避免打扰。")

        connection.commit()
        print("\n✅ 所有用户的推荐预警流处理完毕！请检查 farming_alerts 表。")

    finally:
        connection.close()


if __name__ == "__main__":
    run_recommendation_engine()