import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
import re

# 农业农村部新闻页面URL
BASE_URL = "https://www.moa.gov.cn/xw/zwdt/"
NEWS_URL = "https://www.moa.gov.cn/xw/zwdt/202509/t20250925_6477769.htm"

def scrape_moa_news():
    """爬取农业农村部新闻内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 获取新闻页面内容
        response = requests.get(NEWS_URL, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # 设置编码
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取新闻标题
        title_elem = soup.find('meta', attrs={'name': 'ArticleTitle'})
        title = title_elem.get('content').strip() if title_elem else "未找到标题"
        
        # 提取新闻发布时间
        time_elem = soup.find('meta', attrs={'name': 'PubDate'})
        publish_time = time_elem.get('content').strip() if time_elem else "未知时间"
        
        # 提取新闻内容
        # 根据分析的HTML结构，新闻内容在<div class="content_body_box">中
        content_div = soup.find('div', class_='content_body_box')
        content = ""
        if content_div:
            # 移除script和style标签
            for script in content_div(["script", "style"]):
                script.decompose()
            # 获取文本内容
            content = content_div.get_text().strip()
        
        # 提取图片链接
        images = []
        if content_div:
            img_tags = content_div.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if src:
                    # 处理相对链接
                    full_url = urljoin(NEWS_URL, src)
                    images.append(full_url)
        
        # 如果没有找到内容，尝试其他可能的选择器
        if not content:
            # 查找所有p标签作为备选
            p_tags = soup.find_all('p')
            content = '\n'.join([p.get_text().strip() for p in p_tags if p.get_text().strip()])
        
        # 构造新闻对象
        news_item = {
            "id": 4,  # 新的ID
            "title": title if title else "未找到标题",
            "category": "政务动态",
            "summary": content[:100] + "..." if len(content) > 100 else content,
            "content": f"<p>{content.replace(chr(10), '</p><p>')}</p>" if content else "<p>无法获取新闻内容</p>",
            "image": images[0] if images else "https://via.placeholder.com/400x250",
            "author": "农业农村部",
            "time": publish_time if publish_time else "未知时间",
            "views": random.randint(5000, 15000)  # 随机浏览量
        }
        
        return news_item
    
    except Exception as e:
        print(f"爬取新闻时出错: {e}")
        return None

def update_news_data(news_item):
    """更新农情速递模块的新闻数据"""
    if not news_item:
        print("没有获取到新闻数据")
        return False
    
    # 读取现有的index.html文件
    try:
        with open('api/agricultural-news/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找newsData数组的位置
        start_marker = "// 资讯数据\n    const newsData = ["
        end_marker = "    ];"
        
        start_pos = content.find(start_marker)
        if start_pos == -1:
            print("未找到newsData数组的开始位置")
            return False
            
        start_pos += len(start_marker)
        end_pos = content.find(end_marker, start_pos)
        if end_pos == -1:
            print("未找到newsData数组的结束位置")
            return False
        
        # 提取现有的新闻数据
        news_data_str = content[start_pos:end_pos].strip()
        
        # 将现有数据转换为Python对象
        # 这里简化处理，直接在字符串层面操作
        
        # 将新的新闻项转换为JavaScript对象字符串
        new_item_str = f"""
      {{
        id: {news_item['id']},
        title: '{news_item['title']}',
        category: '{news_item['category']}',
        summary: '{news_item['summary']}',
        content: `{news_item['content']}`,
        image: '{news_item['image']}',
        author: '{news_item['author']}',
        time: '{news_item['time']}',
        views: {news_item['views']}
      }},"""
        
        # 在第一个新闻项之前插入新项
        insert_pos = news_data_str.find("{")
        if insert_pos != -1:
            updated_news_data = news_data_str[:insert_pos] + new_item_str + "\n      " + news_data_str[insert_pos:]
        else:
            updated_news_data = new_item_str + "\n      " + news_data_str
        
        # 更新整个文件内容
        updated_content = content[:start_pos] + updated_news_data + content[end_pos:]
        
        # 写入更新后的内容
        with open('api/agricultural-news/index.html', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("成功更新农情速递模块的新闻数据")
        return True
        
    except Exception as e:
        print(f"更新新闻数据时出错: {e}")
        return False

def main():
    """主函数"""
    print("开始爬取农业农村部新闻...")
    news_item = scrape_moa_news()
    
    if news_item:
        print("成功获取新闻:")
        print(f"标题: {news_item['title']}")
        print(f"时间: {news_item['time']}")
        print(f"摘要: {news_item['summary']}")
        
        # 更新到农情速递模块
        if update_news_data(news_item):
            print("新闻已成功添加到农情速递模块")
        else:
            print("更新农情速递模块失败")
    else:
        print("未能获取新闻内容")

if __name__ == "__main__":
    main()