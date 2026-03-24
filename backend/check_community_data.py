#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查社区数据库中的真实帖子数据
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def check_community_data():
    """检查社区数据"""
    print("=" * 60)
    print("检查社区数据库中的真实数据")
    print("=" * 60)
    
    # 测试用户登录
    test_users = [
        {'username': 'admin', 'password': 'admin123'},
        {'username': 'farmer', 'password': 'farmer123'}
    ]
    
    for user_info in test_users:
        print(f"\n{'=' * 60}")
        print(f"测试用户: {user_info['username']}")
        print(f"{'=' * 60}")
        
        # 1. 登录获取token
        print("\n1. 登录...")
        login_response = requests.post(
            f"{BASE_URL}/api/login",
            json={
                'username': user_info['username'],
                'password': user_info['password']
            }
        )
        
        if login_response.status_code == 200:
            print(f"✓ 登录成功")
            # 从cookie中获取token
            token = login_response.cookies.get('token')
            if not token:
                print("✗ 未获取到token")
                continue
        else:
            print(f"✗ 登录失败: {login_response.status_code}")
            print(f"  响应: {login_response.text}")
            continue
        
        # 2. 获取社区帖子列表
        print("\n2. 获取社区帖子列表...")
        posts_response = requests.get(
            f"{BASE_URL}/api/community/posts",
            cookies={'token': token}
        )
        
        if posts_response.status_code == 200:
            data = posts_response.json()
            if data.get('success'):
                posts = data.get('data', [])
                print(f"✓ 获取帖子成功，共 {len(posts)} 条帖子")
                
                if posts:
                    print(f"\n  帖子详情:")
                    for i, post in enumerate(posts[:5]):  # 只显示前5条
                        print(f"    {i+1}. {post.get('username')} - {post.get('content', '')[:50]}...")
                        print(f"       点赞数: {post.get('likes_count', 0)}, 评论数: {post.get('comments_count', 0)}")
                        print(f"       发布时间: {post.get('created_at')}")
                        print(f"       是否已点赞: {post.get('is_liked', False)}")
                        print()
                else:
                    print("  暂无帖子数据")
            else:
                print(f"✗ 获取帖子失败: {data.get('message')}")
        else:
            print(f"✗ 请求失败: {posts_response.status_code}")
            print(f"  响应: {posts_response.text}")
        
        # 3. 尝试发布测试帖子
        print("\n3. 发布测试帖子...")
        test_content = f"测试帖子 - {user_info['username']} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        create_response = requests.post(
            f"{BASE_URL}/api/community/posts",
            cookies={'token': token},
            headers={'Content-Type': 'application/json'},
            json={'content': test_content}
        )
        
        if create_response.status_code == 200:
            result = create_response.json()
            if result.get('success'):
                print(f"✓ 发布测试帖子成功")
                print(f"  内容: {test_content}")
            else:
                print(f"✗ 发布失败: {result.get('message')}")
        else:
            print(f"✗ 请求失败: {create_response.status_code}")
            print(f"  响应: {create_response.text}")
    
    print(f"\n{'=' * 60}")
    print("检查完成！")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    check_community_data()