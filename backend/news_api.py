# backend/news_api.py
from flask import Blueprint, jsonify, request
import pymysql
from config import Config
from functools import wraps
import jwt
from datetime import datetime

# 创建蓝图
news_bp = Blueprint('news', __name__)

from utils import get_db_connection, token_required, get_beijing_time

@news_bp.route('/api/news/list', methods=['GET'])
@token_required
def get_news_list(current_user_id):
    """获取新闻列表（根据用户信息个性化推送）"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'code': 500,
                'data': [],
                'message': '数据库连接失败'
            })
        
        # 获取用户信息
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT city, crop_type FROM users WHERE id = %s",
                (current_user_id,)
            )
            user = cursor.fetchone()
        
        if not user:
            return jsonify({
                'code': 404,
                'data': [],
                'message': '用户不存在'
            })
        
        user_city = user.get('city', '北京').replace('省', '').replace('市', '').replace('自治区', '')
        user_crop = user.get('crop_type', '小麦')
        
        with connection.cursor() as cursor:
            # 查询所有农业要闻 (nyyw)
            sql = """
            SELECT id, nid, title, category, entities, url, publish_time as time
            FROM agri_news_articles
            WHERE category = 'nyyw'
            ORDER BY publish_time DESC
            """
            cursor.execute(sql)
            nyyw_news = cursor.fetchall()

            # 查询所有农事指导类新闻 (nszd)
            sql = """
            SELECT id, nid, title, category, entities, url, publish_time as time
            FROM agri_news_articles
            WHERE category = 'nszd'
            ORDER BY publish_time DESC
            """
            cursor.execute(sql)
            nszd_news = cursor.fetchall()
        
        # 转换类别显示
        category_map = {
            'nyyw': '农业要闻',
            'nszd': '农事指导'
        }
        
        # 处理农事指导类新闻 - 个性化推荐
        nszd_items = []
        for item in nszd_news:
            entities = item.get('entities', '') or ''
            entity_list = [e.strip() for e in entities.split(',') if e.strip()]
            
            # 计算匹配分数
            match_score = 0
            if user_crop:
                if user_crop in item['title']:
                    match_score += 3
                for entity in entity_list:
                    if entity in user_crop or user_crop in entity:
                        match_score += 2
            
            # 地区匹配
            if user_city and (user_city in item['title'] or user_city in entities):
                match_score += 2
            
            nszd_items.append({
                'item': item,
                'score': match_score
            })
        
        # 构造返回数据
        filtered_items = []
        
        # 1. 添加农事指导类新闻 (已按内容匹配)
        # 按匹配分数排序，分数相同的按时间排序
        nszd_sorted = sorted(nszd_items, key=lambda x: (x['score'], x['item'].get('time') or datetime.min), reverse=True)

        for nszd_item in nszd_sorted:
            item = nszd_item['item']
            filtered_items.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'category': category_map.get(item.get('category'), item.get('category')),
                'content': item.get('title'), # 数据库无内容，暂用标题
                'summary': item.get('title'),
                'author': '农业农村部',
                'date': item.get('time').strftime('%Y-%m-%d %H:%M:%S') if item.get('time') else '未知时间',
                'url': item.get('url'),
                'images': [], # 数据库暂无图片
                'match_score': nszd_item['score']
            })
        
        # 2. 添加农业要闻 (nyyw)
        for item in nyyw_news:
            filtered_items.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'category': category_map.get(item.get('category'), item.get('category')),
                'content': item.get('title'),
                'summary': item.get('title'),
                'author': '农业农村部',
                'date': item.get('time').strftime('%Y-%m-%d %H:%M:%S') if item.get('time') else '未知时间',
                'url': item.get('url'),
                'images': [],
                'match_score': 0
            })
            
        return jsonify({
            'code': 200,
            'data': filtered_items,
            'message': 'success'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'data': [],
            'message': f'获取新闻列表失败: {str(e)}'
        })
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@news_bp.route('/api/news/detail/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    """获取新闻详情（跳转到原始URL）"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'code': 500,
                'data': None,
                'message': '数据库连接失败'
            })
        
        with connection.cursor() as cursor:
            # 查询新闻详情
            sql = """
            SELECT id, nid, title, category, url, publish_time as time
            FROM agri_news_articles
            WHERE id = %s
            """
            cursor.execute(sql, (news_id,))
            news = cursor.fetchone()
        
        if not news:
            return jsonify({
                'code': 404,
                'data': None,
                'message': '新闻不存在'
            })
        
        # 直接跳转到原始URL
        return jsonify({
            'code': 200,
            'data': {
                'url': news.get('url'),
                'title': news.get('title'),
                'category': news.get('category')
            },
            'message': 'success'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取新闻详情失败: {str(e)}'
        })
    finally:
        if 'connection' in locals() and connection:
            connection.close()