# backend/farming_api.py
from flask import Blueprint, jsonify, request, current_app
import pymysql
import jwt

farming_bp = Blueprint('farming', __name__)

def get_db_connection():
    return pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
        port=current_app.config['MYSQL_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        from utils import get_token_from_request
        token = get_token_from_request(request)
        if not token:
            return jsonify({'message': '未登录', 'success': False}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except tuple([jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception]):
            return jsonify({'message': 'Token无效', 'success': False}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

@farming_bp.route('/api/alerts', methods=['GET'])
@token_required
def get_alerts(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, alert_type as type, title, content, 
                       DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i') as date, location, is_read
                FROM farming_alerts 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (current_user_id,))
            alerts = cursor.fetchall()
            
            # Map is_read from tinyint
            for a in alerts:
                a['is_read'] = bool(a['is_read'])
                
            return jsonify({
                'success': True,
                'data': alerts
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@farming_bp.route('/api/alerts/<int:alert_id>/read', methods=['PUT'])
@token_required
def mark_alert_read(current_user_id, alert_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE farming_alerts 
                SET is_read = TRUE, read_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s
            """, (alert_id, current_user_id))
            conn.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@farming_bp.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, task_type as type, priority, status, 
                       DATE_FORMAT(scheduled_time, '%%H:%%i') as time, location
                FROM daily_tasks 
                WHERE user_id = %s
                ORDER BY scheduled_date ASC, scheduled_time ASC
            """, (current_user_id,))
            tasks = cursor.fetchall()
            return jsonify({
                'success': True,
                'data': tasks
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@farming_bp.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
@token_required
def complete_task(current_user_id, task_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE daily_tasks 
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s
            """, (task_id, current_user_id))
            conn.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@farming_bp.route('/api/tasks', methods=['POST'])
@token_required
def add_task(current_user_id):
    data = request.json
    title = data.get('title')
    description = data.get('description', '')
    priority = data.get('priority', 'medium')
    scheduled_time = data.get('time', '12:00')
    location = data.get('location', '')
    
    # We will assume today's date for scheduled_date
    import datetime
    scheduled_date = datetime.date.today().strftime('%Y-%m-%d')
    
    if not title:
        return jsonify({'success': False, 'message': '标题不能为空'}), 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO daily_tasks 
                (user_id, title, description, priority, scheduled_date, scheduled_time, location, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            """, (current_user_id, title, description, priority, scheduled_date, scheduled_time, location))
            conn.commit()
            return jsonify({'success': True, 'task_id': cursor.lastrowid})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@farming_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task_detail(current_user_id, task_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, title, description, task_type as type, priority, status, 
                       DATE_FORMAT(scheduled_time, '%%H:%%i') as time, location
                FROM daily_tasks 
                WHERE id = %s AND user_id = %s
            """, (task_id, current_user_id))
            task = cursor.fetchone()
            if not task:
                return jsonify({'success': False, 'message': '任务不存在或无权限'}), 404
            return jsonify({'success': True, 'data': task})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
