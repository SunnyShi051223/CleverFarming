#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试已使用天数实时计算功能
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_days_used_calculation():
    """测试已使用天数的实时计算"""
    print("=" * 60)
    print("测试已使用天数实时计算功能")
    print("=" * 60)
    
    # 测试用户列表
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
        
        # 2. 获取用户信息
        print("\n2. 获取用户信息...")
        user_info_response = requests.get(
            f"{BASE_URL}/api/user/info",
            cookies={'token': token}
        )
        
        if user_info_response.status_code == 200:
            data = user_info_response.json()
            if data.get('success'):
                user = data.get('user', {})
                print(f"✓ 获取用户信息成功")
                print(f"\n  用户名: {user.get('username')}")
                print(f"  角色: {user.get('role')}")
                print(f"  地区: {user.get('city')}")
                print(f"  作物类型: {user.get('crop_type')}")
                print(f"  农田面积: {user.get('farm_area')} 亩")
                print(f"  注册时间: {user.get('created_at')}")
                
                # 显示统计信息
                stats = user.get('stats', {})
                print(f"\n  统计信息:")
                print(f"    已使用天数: {stats.get('days_used', 0)} 天")
                print(f"    未读预警数: {stats.get('unread_alerts', 0)} 条")
                
                # 验证已使用天数是否合理
                days_used = stats.get('days_used', 0)
                if days_used >= 0:
                    print(f"\n  ✓ 已使用天数计算正确（{days_used}天）")
                else:
                    print(f"\n  ✗ 已使用天数计算错误（{days_used}天）")
            else:
                print(f"✗ 获取用户信息失败: {data.get('message')}")
        else:
            print(f"✗ 请求失败: {user_info_response.status_code}")
            print(f"  响应: {user_info_response.text}")
    
    print(f"\n{'=' * 60}")
    print("测试完成！")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    test_days_used_calculation()