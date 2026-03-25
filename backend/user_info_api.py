# backend/user_info_api.py
# 用户信息和天气API
from flask import Blueprint, jsonify, request
import requests
import pymysql
from functools import wraps
import jwt
from utils import get_beijing_time, get_db_connection, token_required

user_info_bp = Blueprint('user_info', __name__)

# 高德天气API配置


# Token验证装饰器
def token_required_simple(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from utils import get_token_from_request
        token = get_token_from_request(request)
        if not token:
            return jsonify({'success': False, 'message': '未登录'}), 401
        
        try:
            from flask import current_app
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user_id = data['user_id']
            return f(user_id, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': '登录已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': '无效的登录信息'}), 401
    
    return decorated

# 获取用户完整信息（包括地理位置、作物等）
@user_info_bp.route('/user/profile', methods=['GET'])
@token_required_simple
def get_user_profile(user_id):
    """获取用户完整信息"""
    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            # 查询用户基本信息
            sql = """
                SELECT id, username, role, location, city, crop_type, 
                       farm_area, avatar_url, created_at, last_login, is_initialized
                FROM users 
                WHERE id = %s
            """
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'success': False, 'message': '用户不存在'}), 404
            
            # 格式化日期
            if user.get('created_at'):
                user['created_at'] = user['created_at'].strftime('%Y-%m-%d')
            if user.get('last_login'):
                user['last_login'] = user['last_login'].strftime('%Y-%m-%d %H:%M:%S')
            
            # 统计用户数据
            # 获取预警数量
            cursor.execute("SELECT COUNT(*) as count FROM farming_alerts WHERE user_id = %s AND is_read = 0", (user_id,))
            alert_count = cursor.fetchone()['count']
            
            # 获取使用天数
            cursor.execute("SELECT DATEDIFF(NOW(), created_at) as days FROM users WHERE id = %s", (user_id,))
            days_used = cursor.fetchone()['days']
            
            user['stats'] = {
                'unread_alerts': alert_count,
                'days_used': days_used if days_used else 0
            }
            
            return jsonify({
                'success': True,
                'user': user
            }), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库错误'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# 更新用户信息
@user_info_bp.route('/user/profile', methods=['PUT'])
@token_required_simple
def update_user_profile(user_id):
    """更新用户信息"""
    try:
        data = request.get_json()
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            # 构建更新语句
            update_fields = []
            params = []
            
            if 'location' in data:
                update_fields.append("location = %s")
                params.append(data['location'])
            
            if 'city' in data:
                update_fields.append("city = %s")
                params.append(data['city'])
            
            if 'crop_type' in data:
                update_fields.append("crop_type = %s")
                params.append(data['crop_type'])
            
            if 'farm_area' in data:
                update_fields.append("farm_area = %s")
                params.append(data['farm_area'])
            
            if 'is_initialized' in data:
                update_fields.append("is_initialized = %s")
                params.append(data['is_initialized'])
            
            if not update_fields:
                return jsonify({'success': False, 'message': '没有要更新的字段'}), 400
            
            params.append(user_id)
            sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            
            cursor.execute(sql, params)
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': '用户信息更新成功'
            }), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库错误'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# 获取天气信息
@user_info_bp.route('/weather', methods=['GET'])
def get_weather():
    """获取天气信息"""
    try:
        # 获取城市参数
        city_name = request.args.get('city', '武汉')
        adcode = request.args.get('adcode', '420100')  # 城市编码
        
        # 调用高德天气API
        from flask import current_app
        amap_api_key = current_app.config.get('AMAP_API_KEY')
        params = {
            'key': amap_api_key,
            'city': adcode,
            'extensions': 'base'  # base=实况天气, all=预报天气
        }
        
        print(f"正在获取天气信息: city={city_name}, adcode={adcode}")
        
        amap_weather_url = current_app.config['AMAP_WEATHER_URL']
        response = requests.get(amap_weather_url, params=params, timeout=10)
        data = response.json()
        
        print(f"高德天气API响应: {data}")
        
        # 检查API响应状态
        if data.get('status') == '1' and data.get('lives'):
            weather_data = data['lives'][0]
            
            result = {
                'success': True,
                'weather': {
                    'province': weather_data.get('province', ''),
                    'city': weather_data.get('city', city_name),
                    'adcode': weather_data.get('adcode', adcode),
                    'temperature': weather_data.get('temperature', '26'),
                    'weather': weather_data.get('weather', '多云'),
                    'wind_direction': weather_data.get('winddirection', '东南'),
                    'wind_power': weather_data.get('windpower', '≤3'),
                    'humidity': weather_data.get('humidity', '65'),
                    'report_time': weather_data.get('reporttime', ''),
                    'temperature_float': weather_data.get('temperature_float', '26.0'),
                    'humidity_float': weather_data.get('humidity_float', '65.0')
                }
            }
            
            print(f"天气信息获取成功: {result['weather']['city']} {result['weather']['weather']} {result['weather']['temperature']}°C")
            return jsonify(result), 200
        else:
            # API返回错误
            error_msg = data.get('info', '未知错误')
            print(f"高德天气API错误: {error_msg}")
            
            # 返回模拟数据作为降级方案
            return jsonify({
                'success': True,
                'weather': {
                    'city': city_name,
                    'temperature': '26',
                    'weather': '多云',
                    'wind_direction': '东南',
                    'wind_power': '≤3',
                    'humidity': '65',
                    'report_time': '2025-10-18 01:00:00',
                    'temperature_float': '26.0',
                    'humidity_float': '65.0'
                },
                'note': f'使用模拟数据（API错误: {error_msg}）'
            }), 200
        
    except requests.RequestException as e:
        print(f"Weather API 请求错误: {e}")
        # 返回模拟数据作为降级方案
        return jsonify({
            'success': True,
            'weather': {
                'city': request.args.get('city', '武汉'),
                'temperature': '26',
                'weather': '多云',
                'wind_direction': '东南',
                'wind_power': '≤3',
                'humidity': '65',
                'report_time': '2025-10-18 01:00:00',
                'temperature_float': '26.0',
                'humidity_float': '65.0'
            },
            'note': f'使用模拟数据（网络错误: {str(e)}）'
        }), 200
    except Exception as e:
        print(f"获取天气信息错误: {e}")
        return jsonify({
            'success': False, 
            'message': f'获取天气信息失败: {str(e)}'
        }), 500

# 获取用户统计信息
@user_info_bp.route('/user/stats', methods=['GET'])
@token_required_simple
def get_user_stats(user_id):
    """获取用户统计信息"""
    try:
        connection = get_db_connection()
        
        with connection.cursor() as cursor:
            stats = {}
            
            # 未读预警数量
            cursor.execute(
                "SELECT COUNT(*) as count FROM farming_alerts WHERE user_id = %s AND is_read = 0",
                (user_id,)
            )
            stats['unread_alerts'] = cursor.fetchone()['count']
            
            # 本周完成任务数
            cursor.execute(
                """SELECT COUNT(*) as count FROM daily_tasks 
                   WHERE user_id = %s AND status = 'completed' 
                   AND WEEK(completed_at) = WEEK(NOW())""",
                (user_id,)
            )
            stats['weekly_completed_tasks'] = cursor.fetchone()['count']
            
            # 待办任务数
            cursor.execute(
                "SELECT COUNT(*) as count FROM daily_tasks WHERE user_id = %s AND status = 'pending'",
                (user_id,)
            )
            stats['pending_tasks'] = cursor.fetchone()['count']
            
            # 使用天数
            cursor.execute(
                "SELECT DATEDIFF(NOW(), created_at) as days FROM users WHERE id = %s",
                (user_id,)
            )
            result = cursor.fetchone()
            stats['days_used'] = result['days'] if result['days'] else 0
            
            return jsonify({
                'success': True,
                'stats': stats
            }), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库错误'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': '服务器错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()
