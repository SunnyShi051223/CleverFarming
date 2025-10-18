#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智禾慧研系统启动脚本
"""

import os
import sys
import subprocess

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        return False
    print(f"Python版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements"])
        print("依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖包安装失败: {e}")
        return False

def init_database():
    """初始化数据库"""
    print("正在初始化数据库...")
    try:
        from init_db import init_database
        if init_database():
            print("数据库初始化成功")
            return True
        else:
            print("数据库初始化失败")
            return False
    except Exception as e:
        print(f"数据库初始化出错: {e}")
        return False

def start_server():
    """启动Flask服务器"""
    print("正在启动服务器...")
    print("=" * 50)
    print("智禾慧研 - 智能农业管理系统")
    print("=" * 50)
    print("默认登录账号:")
    print("- 管理员: admin / admin123")
    print("- 农户: farmer / farmer123")
    print("=" * 50)
    print("服务器地址: http://localhost:5000")
    print("按 Ctrl+C 停止服务器")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"服务器启动失败: {e}")
        return False

def main():
    """主函数"""
    print("智禾慧研系统启动中...")
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 安装依赖
    if not install_dependencies():
        return
    
    # 初始化数据库
    if not init_database():
        return
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()
