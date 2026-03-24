# backend/app.py
# 推荐使用命令: C:\Users\32874\AppData\Local\Programs\Python\Python38\python.exe app.py
import sys
import os
# 优先使用本地包路径，然后才是系统环境中的包
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'packages'))

from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, send_from_directory
from flask_cors import CORS
import pymysql
import jwt
from datetime import datetime, timedelta
from functools import wraps
from config import Config
from utils import hash_password, verify_token, get_beijing_time
from news_api import news_bp
from ai_agent import ai_agent_bp
from user_info_api import user_info_bp
from farming_api import farming_bp
from community_api import community_bp
from disease_api import disease_bp

# 尝试导入bcrypt，如果失败则使用模拟实现
try:
    import bcrypt
except ImportError as e:
    print(f"Warning: bcrypt import failed: {e}")
    print("Using simulated bcrypt implementation for development")
    
    class bcrypt:
        @staticmethod
        def checkpw(provided_password, stored_password_hash):
            # 在开发环境中简化密码验证
            # 注意：这仅用于开发环境，不应在生产环境中使用
            return provided_password.decode('utf-8') == "password123"  # 默认密码用于测试
            
        @staticmethod
        def gensalt():
            return b'$2b$12$K7DQ6r8r7P5tF3nR9vW3K.'
            
        @staticmethod
        def hashpw(password, salt):
            # 简化的哈希实现
            return password

app = Flask(__name__,
            template_folder='../frontend',
            static_folder='../frontend',
            static_url_path='')
app.config.from_object(Config)

# 配置CORS
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:5000"],
     supports_credentials=True)

# 注册新闻API蓝图
app.register_blueprint(news_bp)
app.register_blueprint(ai_agent_bp, url_prefix='/api')  # 注册AI问答模块蓝图
app.register_blueprint(user_info_bp, url_prefix='/api')  # 注册用户信息API蓝图
app.register_blueprint(farming_bp)  # Farming API
app.register_blueprint(community_bp, url_prefix='/api')
app.register_blueprint(disease_bp)

# 处理OPTIONS预检请求
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# 数据库连接函数
def get_db_connection():
    connection = pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT'],
        cursorclass=pymysql.cursors.DictCursor
    )
    # 设置会话时区为北京时间 (UTC+8)
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+08:00'")
    return connection

# 添加根路径路由，渲染登录页面
@app.route('/')
def home():
    return render_template('login.html') # 直接渲染frontend文件夹下的login.html

# 农户中心页面路由
@app.route('/api/farmer.html')
def farmer():
    return render_template('farmer.html')

# 各个功能模块路由
@app.route('/api/disease-identification/index.html')
def disease_identification():
    return render_template('disease-identification/index.html')

# 为病虫害识别模块的静态文件添加路由
@app.route('/api/disease-identification/<path:filename>')
def disease_identification_static(filename):
    return send_from_directory('../frontend/disease-identification', filename)

@app.route('/api/farming-alert/index.html')
def farming_alert():
    return render_template('farming-alert/index.html')

# 为农事提醒模块的静态文件添加路由
@app.route('/api/farming-alert/<path:filename>')
def farming_alert_static(filename):
    return send_from_directory('../frontend/farming-alert', filename)

@app.route('/api/smart-community/index.html')
def smart_community():
    return render_template('smart-community/index.html')

# 为智慧社区模块的静态文件添加路由
@app.route('/api/smart-community/<path:filename>')
def smart_community_static(filename):
    return send_from_directory('../frontend/smart-community', filename)

@app.route('/api/farming-almanac/index.html')
def farming_almanac():
    return render_template('farming-almanac/index.html')

# 为农事历模块的静态文件添加路由
@app.route('/api/farming-almanac/<path:filename>')
def farming_almanac_static(filename):
    return send_from_directory('../frontend/farming-almanac', filename)

@app.route('/api/agricultural-news/index.html')
def agricultural_news():
    return render_template('agricultural-news/index.html')

# 为农业资讯模块的静态文件添加路由
@app.route('/api/agricultural-news/<path:filename>')
def agricultural_news_static(filename):
    return send_from_directory('../frontend/agricultural-news', filename)

@app.route('/api/daily-farming/<path:filename>')
def daily_farming_static(filename):
    return send_from_directory('../frontend/daily-farming', filename)

# 测试页面路由
@app.route('/test')
def test():
    return render_template('test.html')

# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    try:
        # 记录请求数据（不记录密码）
        data = request.get_json()
        app.logger.info(f"Login attempt for username: {data.get('username')}")

        if not data or not data.get('username') or not data.get('password'):
            app.logger.warning("Login failed: Username or password missing")
            return jsonify({
                'success': False, 
                'message': '用户名和密码不能为空',
                'error': 'missing_credentials'
            }), 400

        username = data['username']
        password = data['password']
        expected_role = data.get('role', '').lower()

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
                cursor.execute(sql, (username,))
                user = cursor.fetchone()

                if not user:
                    app.logger.warning(f"Login failed: User not found - {username}")
                    return jsonify({
                        'success': False, 
                        'message': '用户名或密码错误',
                        'error': 'invalid_credentials'
                    }), 401

                # 检查角色是否匹配
                if expected_role and user['role'] != expected_role:
                    app.logger.warning(f"Role mismatch for user {username}: expected {expected_role}, got {user['role']}")
                    return jsonify({
                        'success': False, 
                        'message': '角色不匹配',
                        'error': 'role_mismatch'
                    }), 403

                # 验证密码
                stored_password_hash = user['password_hash'].encode('utf-8')
                provided_password = password.encode('utf-8')

                if not bcrypt.checkpw(provided_password, stored_password_hash):
                    app.logger.warning(f"Invalid password for user: {username}")
                    return jsonify({
                        'success': False, 
                        'message': '用户名或密码错误',
                        'error': 'invalid_credentials'
                    }), 401

                # 生成JWT令牌
                payload = {
                    'user_id': user['id'],
                    'username': user['username'],
                    'role': user['role'],
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }
                
                try:
                    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
                except Exception as e:
                    app.logger.error(f"JWT token generation failed: {str(e)}")
                    return jsonify({
                        'success': False,
                        'message': '服务器内部错误',
                        'error': 'token_generation_failed'
                    }), 500
                
                # 创建响应
                response_data = {
                    'success': True,
                    'message': '登录成功',
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'role': user['role']
                    }
                }
                
                resp = jsonify(response_data)
                
                # 设置HTTP-only cookie
                resp.set_cookie(
                    'token',
                    token,
                    httponly=True,
                    secure=app.config.get('ENV') == 'production',
                    samesite='Strict',
                    max_age=24 * 60 * 60,  # 24小时
                    path='/'  # 确保cookie在整个站点都有效
                )
                
                app.logger.info(f"User {username} logged in successfully")
                return resp, 200

        except pymysql.MySQLError as e:
            app.logger.error(f"Database error during login: {str(e)}")
            return jsonify({
                'success': False, 
                'message': '数据库连接失败',
                'error': 'database_error'
            }), 500
        except Exception as e:
            app.logger.error(f"Unexpected error during login: {str(e)}")
            return jsonify({
                'success': False, 
                'message': '服务器内部错误',
                'error': 'server_error'
            }), 500
        finally:
            if 'connection' in locals() and connection:
                connection.close()
    
    except Exception as e:
        app.logger.error(f"Error in login endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'message': '请求处理失败',
            'error': 'request_processing_error'
        }), 500

# 获取用户信息接口
def token_required(f):
    def decorated(*args, **kwargs):
        from utils import get_token_from_request
        token = get_token_from_request(request)
        if not token:
            return jsonify({'message': '缺少认证令牌'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': '令牌已过期'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': '无效的令牌'}), 401

        return f(current_user_id, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


# 病虫害识别历史记录接口
@app.route('/api/disease-identification/history', methods=['POST'])
@token_required
def save_disease_identification_history(current_user_id):
    """保存病虫害识别历史记录"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': '缺少请求数据'}), 400
            
        # 验证必填字段
        required_fields = ['disease_name', 'confidence']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'message': f'缺少必填字段: {field}'}), 400
        
        disease_name = data['disease_name']
        confidence = float(data['confidence'])
        symptoms = data.get('symptoms', '')
        solutions = data.get('solutions', '')
        image_path = data.get('image_path', '')
        voice_input = data.get('voice_input', '')
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 插入历史记录
            sql = """
                INSERT INTO disease_identification_history 
                (user_id, disease_name, confidence, symptoms, solutions, image_path, voice_input, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                current_user_id, 
                disease_name, 
                confidence, 
                symptoms, 
                solutions, 
                image_path,
                voice_input,
                get_beijing_time()
            ))
            
            connection.commit()
            
            return jsonify({
                'success': True, 
                'message': '历史记录保存成功',
                'record_id': cursor.lastrowid
            }), 201
            
    except ValueError:
        return jsonify({'success': False, 'message': '置信度格式错误'}), 400
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库操作失败'}), 500
    except Exception as e:
        print(f"Error saving disease identification history: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()


@app.route('/api/disease-identification/history', methods=['GET'])
@token_required
def get_disease_identification_history(current_user_id):
    """获取用户的病虫害识别历史记录"""
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 查询历史记录总数
            count_sql = "SELECT COUNT(*) as total FROM disease_identification_history WHERE user_id = %s"
            cursor.execute(count_sql, (current_user_id,))
            total = cursor.fetchone()['total']
            
            # 查询历史记录
            sql = """
                SELECT id, disease_name, confidence, symptoms, solutions, image_path, voice_input, created_at
                FROM disease_identification_history 
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (current_user_id, limit, offset))
            records = cursor.fetchall()
            
            # 格式化日期
            for record in records:
                if 'created_at' in record and record['created_at']:
                    record['created_at'] = record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({
                'success': True,
                'records': records,
                'total': total,
                'page': page,
                'limit': limit,
                'total_pages': (total + limit - 1) // limit
            }), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库操作失败'}), 500
    except Exception as e:
        print(f"Error retrieving disease identification history: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()


@app.route('/api/disease-identification/history/<int:record_id>', methods=['DELETE'])
@token_required
def delete_disease_identification_history(current_user_id, record_id):
    """删除指定的历史记录"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 检查记录是否存在且属于当前用户
            check_sql = """
                SELECT id FROM disease_identification_history 
                WHERE id = %s AND user_id = %s
            """
            cursor.execute(check_sql, (record_id, current_user_id))
            record = cursor.fetchone()
            
            if not record:
                return jsonify({'success': False, 'message': '记录不存在或无权限删除'}), 404
            
            # 删除记录
            delete_sql = "DELETE FROM disease_identification_history WHERE id = %s"
            cursor.execute(delete_sql, (record_id,))
            connection.commit()
            
            return jsonify({'success': True, 'message': '历史记录删除成功'}), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库操作失败'}), 500
    except Exception as e:
        print(f"Error deleting disease identification history: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/api/user/info', methods=['GET'])
@token_required
def get_user_info(current_user_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, username, role, city, crop_type, farm_area, is_initialized, created_at FROM users WHERE id = %s"
            cursor.execute(sql, (current_user_id,))
            user = cursor.fetchone()

            if user:
                # 计算已使用天数
                from datetime import datetime
                if user.get('created_at'):
                    created_date = user['created_at']
                    if isinstance(created_date, str):
                        created_date = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
                    days_used = (datetime.now() - created_date).days
                else:
                    days_used = 0
                
                # 添加统计信息
                user['stats'] = {
                    'days_used': days_used
                }
                
                # 获取未读预警数量
                cursor.execute(
                    "SELECT COUNT(*) as unread_count FROM farming_alerts WHERE user_id = %s AND is_read = FALSE",
                    (current_user_id,)
                )
                alert_result = cursor.fetchone()
                user['stats']['unread_alerts'] = alert_result['unread_count'] if alert_result else 0
                
                return jsonify({
                    'success': True,
                    'user': user
                }), 200
            else:
                return jsonify({'success': False, 'message': '用户不存在'}), 404

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库连接失败'}), 500
    finally:
        connection.close()


@app.route('/api/user/info', methods=['PUT'])
@token_required
def update_user_info(current_user_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': '没有提供更新数据'}), 400
        
        # 构建更新SQL语句
        update_fields = []
        update_values = []
        
        if 'city' in data:
            update_fields.append("city = %s")
            update_values.append(data['city'])
        
        if 'crop_type' in data:
            update_fields.append("crop_type = %s")
            update_values.append(data['crop_type'])
        
        if 'farm_area' in data:
            update_fields.append("farm_area = %s")
            update_values.append(data['farm_area'])
        
        if 'is_initialized' in data:
            update_fields.append("is_initialized = %s")
            update_values.append(data['is_initialized'])
        
        if not update_fields:
            return jsonify({'success': False, 'message': '没有有效的更新字段'}), 400
        
        # 添加用户ID到参数列表
        update_values.append(current_user_id)
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s"
            cursor.execute(sql, update_values)
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': '用户信息更新成功'
            }), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': '数据库操作失败'}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        connection.close()


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证必填字段
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'success': False, 'message': '请提供用户名、密码和角色'}), 400
    
    username = data['username'].strip()
    password = data['password']
    role = data['role'].lower()
    
    # 验证角色是否有效
    if role not in ['user', 'admin']:
        return jsonify({'success': False, 'message': '无效的角色，角色必须为 user 或 admin'}), 400
    
    # 验证密码长度
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码长度至少为6位'}), 400
    
    # 获取个性化信息（可选字段）
    city = data.get('city', '北京').strip()  # 默认北京
    crop_type = data.get('crop_type', '小麦').strip()  # 默认小麦
    farm_area = data.get('farm_area')  # 可选
    is_initialized = data.get('is_initialized', 0)  # 默认未初始化
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 检查用户名是否已存在
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone() is not None:
                return jsonify({'success': False, 'message': '用户名已存在'}), 400
            
            # 密码哈希处理
            hashed_password = hash_password(password)
            
            # 插入新用户（包含个性化信息）
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, role, city, crop_type, farm_area, is_initialized, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (username, hashed_password, role, city, crop_type, farm_area, is_initialized, get_beijing_time())
            )
            
            # 获取新创建的用户ID
            user_id = cursor.lastrowid
            
            # 提交事务
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': '注册成功',
                'user': {
                    'id': user_id,
                    'username': username,
                    'role': role,
                    'city': city,
                    'crop_type': crop_type,
                    'farm_area': farm_area
                }
            }), 201
            
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        connection.rollback()
        return jsonify({'success': False, 'message': '数据库操作失败'}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# Token验证装饰器
def role_required(roles=None):
    if roles is None:
        roles = ['user']
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from utils import get_token_from_request
            token = get_token_from_request(request)
            if not token:
                return redirect(url_for('home'))
                
            is_valid, payload = verify_token(token, app.config['SECRET_KEY'])
            if not is_valid or 'role' not in payload:
                resp = make_response(redirect(url_for('home')))
                resp.delete_cookie('token')
                return resp
                
            if payload['role'] not in roles:
                return jsonify({'success': False, 'message': '权限不足'}), 403
                
            return f(payload, *args, **kwargs)
        return decorated_function
    return decorator

# 管理员仪表盘
@app.route('/admin')
@role_required(roles=['admin'])
def admin_dashboard(payload):
    return render_template('admin.html', user=payload)

# 农户仪表盘
@app.route('/farmer')
@role_required(roles=['user'])  # 只允许普通用户(农户)访问
def farmer_dashboard(payload):
    return render_template('farmer.html', user=payload)

# 登出
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('home')))
    resp.delete_cookie('token')
    return resp

# 知识库API
@app.route('/api/knowledge/categories', methods=['GET'])
@role_required(['admin', 'farmer'])
def get_knowledge_categories(payload):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT DISTINCT category FROM knowledge_nodes"
            cursor.execute(sql)
            categories = [row['category'] for row in cursor.fetchall()]
            return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        print(f"获取分类失败: {e}")
        return jsonify({'success': False, 'message': '获取分类失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/api/knowledge/items', methods=['GET'])
@role_required(['admin', 'farmer'])
def get_knowledge_items(payload):
    try:
        category = request.args.get('category')
        search = request.args.get('search', '')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        sort_by = request.args.get('sort', 'created_at')
        offset = (page - 1) * limit
        
        # 验证排序字段
        allowed_sorts = ['created_at', 'view_count', 'title', 'updated_at']
        if sort_by not in allowed_sorts:
            sort_by = 'created_at'
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 构建查询条件和参数
            conditions = []
            params = []
            
            if category:
                conditions.append("category = %s")
                params.append(category)
                
            if search:
                conditions.append("(title LIKE %s OR content LIKE %s OR keywords LIKE %s OR summary LIKE %s)")
                search_term = f"%{search}%"
                params.extend([search_term, search_term, search_term, search_term])
            
            # 构建基础查询
            where_clause = " AND ".join(conditions) if conditions else "1=1"
            count_sql = f"SELECT COUNT(*) as total FROM knowledge_nodes WHERE {where_clause}"
            
            # 获取总数
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 构建排序子句
            order_clause = "DESC" if sort_by in ['created_at', 'view_count', 'updated_at'] else "ASC"
            
            # 获取分页数据
            sql = f"""
                SELECT id, title, category, summary, keywords, created_at, updated_at, view_count
                FROM knowledge_nodes 
                WHERE {where_clause}
                ORDER BY {sort_by} {order_clause}
                LIMIT %s OFFSET %s
            """
            params.extend([limit, offset])
            
            cursor.execute(sql, params)
            items = cursor.fetchall()
            
            # 转换日期格式和添加额外信息
            for item in items:
                if 'created_at' in item and item['created_at']:
                    item['created_at'] = item['created_at'].strftime('%Y-%m-%d')
                if 'updated_at' in item and item['updated_at']:
                    item['updated_at'] = item['updated_at'].strftime('%Y-%m-%d')
                # 确保所有字段都有值
                item['view_count'] = item.get('view_count', 0)
                item['summary'] = item.get('summary', '')
                item['keywords'] = item.get('keywords', '')
            
            return jsonify({
                'success': True, 
                'items': items,
                'total': total,
                'page': page,
                'total_pages': (total + limit - 1) // limit,
                'has_next': page < (total + limit - 1) // limit,
                'has_prev': page > 1
            })
            
    except Exception as e:
        print(f"获取知识点失败: {e}")
        return jsonify({'success': False, 'message': '获取知识点失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/api/knowledge/item/<int:item_id>', methods=['GET'])
@role_required(['admin', 'farmer'])
def get_knowledge_item(payload, item_id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 获取知识点详情
            sql = """
                SELECT id, title, category, content, summary, keywords, 
                       created_at, updated_at, view_count
                FROM knowledge_nodes 
                WHERE id = %s
            """
            cursor.execute(sql, (item_id,))
            item = cursor.fetchone()
            
            if not item:
                return jsonify({'success': False, 'message': '未找到该知识点'}), 404
            
            # 更新查看次数
            update_sql = "UPDATE knowledge_nodes SET view_count = view_count + 1 WHERE id = %s"
            cursor.execute(update_sql, (item_id,))
            connection.commit()
            
            # 转换日期格式
            if 'created_at' in item and item['created_at']:
                item['created_at'] = item['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if 'updated_at' in item and item['updated_at']:
                item['updated_at'] = item['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
                
            return jsonify({'success': True, 'item': item})
    except Exception as e:
        print(f"获取知识点详情失败: {e}")
        return jsonify({'success': False, 'message': '获取知识点详情失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# 管理员API：获取用户列表
@app.route('/api/admin/users', methods=['GET'])
@role_required(roles=['admin'])
def admin_get_users(payload):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, username, role, location, city, crop_type, farm_area, created_at, last_login FROM users ORDER BY id DESC"
            cursor.execute(sql)
            users = cursor.fetchall()
            
            # 格式化日期
            for user in users:
                if user.get('created_at'):
                    user['created_at'] = user['created_at'].strftime('%Y-%m-%d %H:%M')
                if user.get('last_login'):
                    user['last_login'] = user['last_login'].strftime('%Y-%m-%d %H:%M')
                    
            return jsonify({'success': True, 'users': users})
    except Exception as e:
        print(f"Admin get users failed: {e}")
        return jsonify({'success': False, 'message': '获取用户列表失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# 管理员API：获取概览统计
@app.route('/api/admin/stats', methods=['GET'])
@role_required(roles=['admin'])
def admin_get_stats(payload):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 总数
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()['count']
            
            # 今日新增
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE DATE(created_at) = CURDATE()")
            new_today = cursor.fetchone()['count']
            
            # 最近活跃 (24小时内)
            cursor.execute("SELECT COUNT(*) as count FROM users WHERE last_login >= NOW() - INTERVAL 1 DAY")
            active_24h = cursor.fetchone()['count']
            
            # 各角色数量
            cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
            roles = cursor.fetchall()
            
            return jsonify({
                'success': True, 
                'stats': {
                    'total_users': total_users,
                    'new_today': new_today,
                    'active_24h': active_24h,
                    'roles': roles
                }
            })
    except Exception as e:
        print(f"Admin get stats failed: {e}")
        return jsonify({'success': False, 'message': '获取统计数据失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# 管理员API：删除用户
@app.route('/api/admin/user/<int:user_id>', methods=['DELETE'])
@role_required(roles=['admin'])
def admin_delete_user(payload, user_id):
    if user_id == payload['user_id']:
        return jsonify({'success': False, 'message': '不能删除自己'}), 400
        
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "DELETE FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            connection.commit()
            return jsonify({'success': True, 'message': '用户删除成功'})
    except Exception as e:
        print(f"Admin delete user failed: {e}")
        return jsonify({'success': False, 'message': '删除用户失败'}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
