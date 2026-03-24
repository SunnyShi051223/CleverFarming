import requests
from bs4 import BeautifulSoup
import re
import json
import os
from datetime import datetime
import pymysql
from config import Config

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        port=Config.MYSQL_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def scrape_moa_news():
    # 农业农村部网站地址
    url = "http://www.moa.gov.cn/xw/bmdt/"
    
    # 发送请求
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    response.encoding = 'utf-8'
    
    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到新闻列表
    news_list = soup.find('ul', class_='news_list')
    if not news_list:
        print("未找到新闻列表")
        return []
    
    # 提取新闻链接
    news_items = news_list.find_all('li')
    news_data = []
    
    # 只爬取最新的10条新闻
    for item in news_items[:10]:
        try:
            # 找到链接
            link = item.find('a')
            if not link:
                continue
            
            # 获取标题和链接
            title = link.get_text(strip=True)
            href = link.get('href')
            
            # 构建完整链接
            if href.startswith('http'):
                full_url = href
            else:
                full_url = f"http://www.moa.gov.cn{href}"
            
            # 找到时间
            time_span = item.find('span')
            date_str = time_span.get_text(strip=True) if time_span else ""
            
            # 解析日期
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except:
                date = datetime.now().date()
            
            # 爬取新闻详情
            detail_response = requests.get(full_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            detail_response.encoding = 'utf-8'
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
            
            # 提取新闻内容
            content_div = detail_soup.find('div', class_='TRS_Editor') or detail_soup.find('div', class_='content')
            content = ""
            if content_div:
                # 移除所有脚本和样式
                for script in content_div(['script', 'style']):
                    script.decompose()
                content = content_div.get_text(separator='\n', strip=True)
            
            # 提取图片
            images = []
            img_tags = detail_soup.find_all('img')
            for img in img_tags:
                img_src = img.get('src')
                if img_src:
                    if img_src.startswith('http'):
                        images.append(img_src)
                    else:
                        images.append(f"http://www.moa.gov.cn{img_src}")
            
            # 生成nid（使用时间戳和随机数）
            nid = f"{int(datetime.now().timestamp())}{hash(title) % 1000:03d}"
            
            # 分类（简单分类）
            category = "政策" if "政策" in title else "资讯"
            
            news_data.append({
                'nid': nid,
                'title': title,
                'url': full_url,
                'date': date_str,
                'content': content,
                'images': images,
                'category': category
            })
            
            print(f"爬取成功: {title}")
            
        except Exception as e:
            print(f"爬取失败: {str(e)}")
            continue
    
    return news_data

def save_news_to_database(news_data):
    """将新闻数据保存到数据库"""
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 清空旧数据（可选，根据需求决定）
            # cursor.execute("TRUNCATE TABLE agri_news_articles")
            
            # 插入新闻数据
            for news in news_data:
                # 检查是否已存在相同标题的新闻
                cursor.execute(
                    "SELECT id FROM agri_news_articles WHERE title = %s",
                    (news['title'],)
                )
                if cursor.fetchone():
                    print(f"新闻已存在: {news['title']}")
                    continue
                
                # 插入新闻
                sql = """
                INSERT INTO agri_news_articles (nid, title, url, category, publish_time)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    news['nid'],
                    news['title'],
                    news['url'],
                    news['category'],
                    news['date']
                ))
            
            # 提交事务
            connection.commit()
            print(f"成功保存 {len(news_data)} 条新闻到数据库")
    except Exception as e:
        print(f"保存新闻到数据库失败: {str(e)}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    print("开始爬取农业农村部新闻...")
    news_data = scrape_moa_news()
    if news_data:
        save_news_to_database(news_data)
        print(f"爬取完成，共获取 {len(news_data)} 条新闻")
    else:
        print("未获取到新闻数据")