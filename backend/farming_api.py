# backend/farming_api.py
from flask import Blueprint, jsonify, request
import pymysql
from config import Config
from functools import wraps
import jwt
from datetime import datetime

# 创建蓝图
farming_bp = Blueprint('farming', __name__)

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            port=Config.MYSQL_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        print(f"数据库连接失败: {e}")
        return None

def token_required(f):
    """Token验证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        from utils import get_token_from_request
        token = get_token_from_request(request)
        if not token:
            return jsonify({'message': '未登录', 'success': False}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user_id = data['user_id']
        except tuple([jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception]):
            return jsonify({'message': 'Token无效', 'success': False}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

@farming_bp.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts(current_user_id):
    """获取预警列表（根据用户信息个性化推送）"""
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
        
        # 获取预警列表，支持分类过滤
        alert_type = request.args.get('type') # news 或 alert
        alert_subtype = request.args.get('subtype') # nyyw, nszd, nyqx, trsq, zwbch
        
        query = """
            SELECT id, user_id, alert_type, alert_subtype, title, content, 
                   priority, is_read, location, created_at
            FROM farming_alerts 
            WHERE user_id = %s
        """
        params = [current_user_id]
        
        if alert_type and alert_type != 'all':
            query += " AND alert_type = %s"
            params.append(alert_type)
        if alert_subtype and alert_subtype != 'all':
            query += " AND alert_subtype = %s"
            params.append(alert_subtype)
            
        query += " ORDER BY is_read ASC, created_at DESC"
        
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(params))
            alerts = cursor.fetchall()
            
        # 格式化返回值
        formatted_alerts = []
        for item in alerts:
            # 计算匹配分数（基于用户作物类型和城市）
            match_score = 0
            content_str = item.get('content', '') or ''
            if user_crop and user_crop in content_str:
                match_score += 2
            if user_city and user_city in content_str:
                match_score += 1
                
            formatted_alerts.append({
                'id': item['id'],
                'alert_type': item['alert_type'],
                'alert_subtype': item['alert_subtype'],
                'title': item['title'],
                'content': item['content'],
                'priority': item['priority'],
                'is_read': bool(item['is_read']),
                'location': item['location'],
                'created_at': item['created_at'].strftime('%Y-%m-%d %H:%M:%S') if item['created_at'] else '未知时间',
                'match_score': match_score
            })
            
        # 按匹配分数排序
        formatted_alerts.sort(key=lambda x: -x['match_score'])
            
        return jsonify({
            'code': 200,
            'data': formatted_alerts,
            'message': 'success'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'data': [],
            'message': f'获取预警列表失败: {str(e)}'
        })
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@farming_bp.route('/api/alerts/<int:alert_id>', methods=['PUT'])
@token_required
def update_alert_status(current_user_id, alert_id):
    """更新预警状态（标记为已读/未读）"""
    try:
        data = request.get_json()
        if not data or 'is_read' not in data:
            return jsonify({
                'code': 400,
                'data': None,
                'message': '缺少is_read参数'
            })
        
        is_read = data['is_read']
        if not isinstance(is_read, bool):
            return jsonify({
                'code': 400,
                'data': None,
                'message': 'is_read参数必须为布尔值'
            })
        
        connection = get_db_connection()
        if not connection:
            return jsonify({
                'code': 500,
                'data': None,
                'message': '数据库连接失败'
            })
        
        with connection.cursor() as cursor:
            # 更新预警状态
            sql = """
            UPDATE farming_alerts 
            SET is_read = %s 
            WHERE id = %s AND user_id = %s
            """
            cursor.execute(sql, (1 if is_read else 0, alert_id, current_user_id))
            connection.commit()
            
            if cursor.rowcount == 0:
                return jsonify({
                    'code': 404,
                    'data': None,
                    'message': '预警不存在或无权限修改'
                })
        
        return jsonify({
            'code': 200,
            'data': None,
            'message': '状态更新成功'
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'code': 500,
            'data': None,
            'message': f'更新预警状态失败: {str(e)}'
        })
    finally:
        if 'connection' in locals() and connection:
            connection.close()
