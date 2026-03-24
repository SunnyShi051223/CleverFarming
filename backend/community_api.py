# backend/community_api.py
from flask import Blueprint, jsonify, request, current_app
import pymysql
import jwt

community_bp = Blueprint('community', __name__)

def get_db_connection():
    connection = pymysql.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
        port=current_app.config['MYSQL_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    # 设置会话时区为北京时间 (UTC+8)
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+08:00'")
    return connection

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

@community_bp.route('/community/posts', methods=['GET'])
@token_required
def get_posts(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.content, p.likes_count, 
                       DATE_FORMAT(p.created_at, '%%Y-%%m-%%d %%H:%%i') as created_at,
                       u.username, u.avatar_url,
                       EXISTS(SELECT 1 FROM post_likes pl WHERE pl.post_id = p.id AND pl.user_id = %s) as is_liked,
                       (SELECT COUNT(*) FROM community_comments cc WHERE cc.post_id = p.id) as comments_count
                FROM community_posts p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
            """, (current_user_id,))
            posts = cursor.fetchall()
            for p in posts:
                p['is_liked'] = bool(p['is_liked'])
            return jsonify({'success': True, 'data': posts})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@community_bp.route('/community/posts', methods=['POST'])
@token_required
def create_post(current_user_id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'success': False, 'message': '内容不能为空'}), 400
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO community_posts (user_id, content) VALUES (%s, %s)", (current_user_id, content))
            conn.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@community_bp.route('/community/posts/<int:post_id>/like', methods=['POST'])
@token_required
def toggle_like(current_user_id, post_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM post_likes WHERE user_id = %s AND post_id = %s", (current_user_id, post_id))
            liked = cursor.fetchone()
            if liked:
                cursor.execute("DELETE FROM post_likes WHERE user_id = %s AND post_id = %s", (current_user_id, post_id))
                cursor.execute("UPDATE community_posts SET likes_count = likes_count - 1 WHERE id = %s", (post_id,))
                action = 'unliked'
            else:
                cursor.execute("INSERT INTO post_likes (user_id, post_id) VALUES (%s, %s)", (current_user_id, post_id))
                cursor.execute("UPDATE community_posts SET likes_count = likes_count + 1 WHERE id = %s", (post_id,))
                action = 'liked'
            
            cursor.execute("SELECT likes_count FROM community_posts WHERE id = %s", (post_id,))
            new_count = cursor.fetchone()['likes_count']
            conn.commit()
            
            return jsonify({'success': True, 'action': action, 'likes_count': new_count})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@community_bp.route('/community/posts/<int:post_id>/comments', methods=['GET'])
@token_required
def get_comments(current_user_id, post_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.id, c.content, DATE_FORMAT(c.created_at, '%%Y-%%m-%%d %%H:%%i') as created_at,
                       u.username, u.avatar_url
                FROM community_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = %s
                ORDER BY c.created_at ASC
            """, (post_id,))
            comments = cursor.fetchall()
            return jsonify({'success': True, 'data': comments})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@community_bp.route('/community/posts/<int:post_id>/comments', methods=['POST'])
@token_required
def add_comment(current_user_id, post_id):
    data = request.json
    content = data.get('content')
    if not content:
        return jsonify({'success': False, 'message': '内容不能为空'}), 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO community_comments (post_id, user_id, content) VALUES (%s, %s, %s)", (post_id, current_user_id, content))
            conn.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
