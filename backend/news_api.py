# backend/news_api.py
from flask import Blueprint, jsonify
import json
import os
import re

# 创建蓝图
news_bp = Blueprint('news', __name__)

def extract_news_data():
    """从农情速递页面中提取新闻数据"""
    try:
        # 读取农情速递页面文件
        with open('api/agricultural-news/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找newsData数组
        start_marker = "const newsData = ["
        end_marker = "];"
        
        start_pos = content.find(start_marker)
        if start_pos == -1:
            return []
            
        start_pos += len(start_marker)
        end_pos = content.find(end_marker, start_pos)
        if end_pos == -1:
            return []
        
        # 提取新闻数据字符串
        news_data_str = content[start_pos:end_pos]
        
        # 简化的数据提取方法 - 直接返回原始数据
        # 在实际应用中，可能需要更复杂的解析方法
        return news_data_str
    except Exception as e:
        print(f"提取新闻数据时出错: {e}")
        return []

@news_bp.route('/api/news/list', methods=['GET'])
def get_news_list():
    """获取新闻列表"""
    try:
        # 读取农情速递页面文件
        with open('api/agricultural-news/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取newsData数组
        # 修正正则表达式以正确匹配当前HTML结构
        pattern = r'const newsData = \[\s*(.*?)\s*\];'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 提取新闻数据
            news_data_section = match.group(1)
            
            # 简化处理 - 返回原始数据字符串
            # 在实际应用中，应该将其解析为JSON对象
            news_items = []
            
            # 查找每个新闻项，使用更宽松的匹配模式
            # 考虑到可能存在的换行和空格
            item_pattern = r'\{\s*id:\s*(\d+),\s*title:\s*\'([^\']*)\',\s*category:\s*\'([^\']*)\',\s*summary:\s*\'([^\']*)\',.*?author:\s*\'([^\']*)\',\s*time:\s*\'([^\']*)\',\s*views:\s*(\d+)\s*\}'
            items = re.findall(item_pattern, news_data_section, re.DOTALL)
            
            # 如果上面的模式没有匹配到，尝试另一种模式
            if not items:
                # 更宽松的匹配模式，允许content字段的存在
                item_pattern = r'\{\s*id:\s*(\d+),\s*title:\s*\'([^\']*)\',\s*category:\s*\'([^\']*)\',\s*summary:\s*\'([^\']*)\',.*?author:\s*\'([^\']*)\',\s*time:\s*\'([^\']*)\',\s*views:\s*(\d+).*?\}'
                items = re.findall(item_pattern, news_data_section, re.DOTALL)
            
            for item in items:
                news_items.append({
                    'id': int(item[0]),
                    'title': item[1],
                    'category': item[2],
                    'summary': item[3],
                    'author': item[4],
                    'time': item[5],
                    'views': int(item[6])
                })
            
            return jsonify({
                'code': 200,
                'data': news_items,
                'message': 'success'
            })
        else:
            # 如果正则表达式匹配失败，尝试其他方法
            # 直接返回空数组而不是错误
            return jsonify({
                'code': 200,
                'data': [],
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
        # 读取农情速递页面文件
        with open('api/agricultural-news/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取newsData数组
        pattern = r'const newsData = \[(.*?)\];'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 提取新闻数据
            news_data_section = match.group(1)
            
            # 查找指定ID的新闻项
            item_pattern = r'\{\s*id:\s*' + str(news_id) + r'.*?\}'
            match_item = re.search(item_pattern, news_data_section, re.DOTALL)
            
            if match_item:
                # 找到完整新闻项
                full_item_pattern = r'\{\s*id:\s*' + str(news_id) + r',\s*title:\s*\'([^\']*)\',\s*category:\s*\'([^\']*)\',\s*summary:\s*\'([^\']*)\',\s*content:\s*`(.*?)`,\s*image:\s*\'([^\']*)\',\s*author:\s*\'([^\']*)\',\s*time:\s*\'([^\']*)\',\s*views:\s*(\d+)\s*\}'
                detail_match = re.search(full_item_pattern, news_data_section, re.DOTALL)
                
                if detail_match:
                    news_detail = {
                        'id': news_id,
                        'title': detail_match.group(1),
                        'category': detail_match.group(2),
                        'summary': detail_match.group(3),
                        'content': detail_match.group(4),
                        'image': detail_match.group(5),
                        'author': detail_match.group(6),
                        'time': detail_match.group(7),
                        'views': int(detail_match.group(8))
                    }
                    
                    return jsonify({
                        'code': 200,
                        'data': news_detail,
                        'message': 'success'
                    })
            
            return jsonify({
                'code': 404,
                'data': None,
                'message': '新闻不存在'
            })
        else:
            return jsonify({
                'code': 500,
                'data': None,
                'message': '无法解析新闻数据'
            })
    except Exception as e:
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'获取新闻详情失败: {str(e)}'
        })