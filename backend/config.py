import os
from dotenv import load_dotenv

load_dotenv() # 加载 .env 文件中的环境变量

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here' # 用于JWT签名
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'XXX'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'clever_farming'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    # 千问API配置
    QWEN_API_KEY = os.environ.get('QWEN_API_KEY') or 'your-qwen-api-key-here'
    QWEN_API_URL = os.environ.get('QWEN_API_URL') or 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    
    # 高德天气API配置
    AMAP_API_KEY = os.environ.get('AMAP_API_KEY') or 'your-amap-api-key-here'

