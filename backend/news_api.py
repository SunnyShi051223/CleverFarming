# backend/news_api.py
from flask import Blueprint, jsonify
import json
import os

# 创建蓝图
news_bp = Blueprint('news', __name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'news.json')

def load_news_data():
    """从JSON文件加载新闻数据"""
    try:
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"读取新闻数据时出错: {e}")
        return []

@news_bp.route('/api/news/list', methods=['GET'])
def get_news_list():
    """获取新闻列表"""
    try:
        news_items = load_news_data()
        
        # 列表通常不需要返回完整的正文，以节省带宽
        # 但前端可能依赖部分结构，为了兼容，先完整返回或去除 content
        # original output had: id, title, category, summary, author, time, views
        filtered_items = []
        for item in news_items:
            filtered_items.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'category': item.get('category'),
                'summary': item.get('summary'),
                'author': item.get('author'),
                'time': item.get('time'),
                'views': item.get('views', 0)
            })
            
        return jsonify({
            'code': 200,
            'data': filtered_items,
            'message': 'success'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': [],
            'message': f'获取新闻列表失败: {str(e)}'
        })

@news_bp.route('/api/news/detail/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    """获取新闻详情"""
    try:
        news_items = load_news_data()
        for item in news_items:
            if item.get('id') == news_id:
                return jsonify({
                    'code': 200,
                    'data': item,
                    'message': 'success'
                })
        
        return jsonify({
            'code': 404,
            'data': None,
            'message': '新闻不存在'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取新闻详情失败: {str(e)}'
        })