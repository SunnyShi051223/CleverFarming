# utils.py
import jwt
from datetime import datetime, timezone, timedelta

# 尝试导入bcrypt，如果失败则使用模拟实现
try:
    import bcrypt
except ImportError as e:
    print(f"Warning: bcrypt import failed: {e}")
    print("Using simulated bcrypt implementation for development")
    
    # 模拟bcrypt实现
    class MockBcrypt:
        @staticmethod
        def gensalt():
            return b"mock_salt"
        
        @staticmethod
        def hashpw(password, salt):
            return f"mock_hash_{password.decode('utf-8')}".encode('utf-8')
        
        @staticmethod
        def checkpw(password, hashed_password):
            return f"mock_hash_{password.decode('utf-8')}".encode('utf-8') == hashed_password
    
    bcrypt = MockBcrypt()

def get_beijing_time():
    """获取北京时间 (UTC+8)"""
    return datetime.now(timezone(timedelta(hours=8)))

def hash_password(password):
    """对密码进行哈希处理"""
    # 生成盐值并哈希密码
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8') # 返回字符串格式，方便存储

def check_password(hashed_password, user_password):
    """验证密码是否正确"""
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password.encode('utf-8'))

def verify_token(token, secret_key):
    """
    验证JWT token
    返回: (is_valid, payload)
    """
    try:
        if not token:
            return False, None
        # 移除可能的 'Bearer ' 前缀
        if token.startswith('Bearer '):
            token = token[7:]
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, {'error': 'Token已过期'}
    except jwt.InvalidTokenError:
        return False, {'error': '无效的Token'}
    except Exception as e:
        return False, {'error': str(e)}

def get_token_from_request(request):
    """从请求中获取Token（先后从Header和Cookie中尝试提取）"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
    if not token:
        token = request.cookies.get('token')
    return token