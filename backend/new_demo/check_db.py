#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查数据库中新闻数据"""

import pymysql

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'shisannian1223',
    'database': 'clever_farming',
    'charset': 'utf8mb4'
}

def check_database():
    """检查数据库表结构和数据"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 检查表记录数
        cursor.execute('SELECT COUNT(*) FROM agri_news_articles')
        news_count = cursor.fetchone()[0]
        print(f'agri_news_articles 表记录数: {news_count}')
        
        cursor.execute('SELECT COUNT(*) FROM farming_alerts')
        alerts_count = cursor.fetchone()[0]
        print(f'farming_alerts 表记录数: {alerts_count}')
        
        # 检查表结构
        print('\nagri_news_articles 表结构:')
        cursor.execute('DESCRIBE agri_news_articles')
        for row in cursor.fetchall():
            print(f'  {row[0]}: {row[1]} ({row[2]})')
        
        # 检查最近的新闻
        cursor.execute('''
            SELECT id, title, url, category, created_at 
            FROM agri_news_articles 
            ORDER BY created_at DESC 
            LIMIT 10
        ''')
        
        print('\n最近10条新闻:')
        print('-' * 120)
        for row in cursor.fetchall():
            print(f'ID: {row[0]}, 标题: {row[1]}')
            print(f'  URL: {row[2]}')
            print(f'  分类: {row[3]}, 创建时间: {row[4]}')
            print()
        
        # 检查推送表（如果存在）
        try:
            cursor.execute('SELECT COUNT(*) FROM push_news')
            push_count = cursor.fetchone()[0]
            print(f'\npush_news 表记录数: {push_count}')
            
            cursor.execute('''
                SELECT id, news_id, user_id, score, created_at 
                FROM push_news 
                ORDER BY created_at DESC 
                LIMIT 5
            ''')
            
            print('\n最近5条推送记录:')
            for row in cursor.fetchall():
                print(f'ID: {row[0]}, 新闻ID: {row[1]}, 用户ID: {row[2]}, 分数: {row[3]}')
        except Exception as e:
            print(f'\n推送表检查失败: {e}')
        
        conn.close()
        print('\n✅ 数据库检查完成！')
        
    except Exception as e:
        print(f'❌ 错误: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    check_database()