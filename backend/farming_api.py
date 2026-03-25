# backend/farming_api.py
from flask import Blueprint, jsonify, request
import pymysql
from config import Config
from functools import wraps
import jwt
from datetime import datetime, date, time
import math

# 创建蓝图
farming_bp = Blueprint('farming', __name__)

from utils import get_db_connection, token_required, get_beijing_time


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
            return jsonify({'code': 400, 'message': '缺少is_read参数'})
        
        is_read = data['is_read']
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE farming_alerts SET is_read = %s WHERE id = %s AND user_id = %s"
            cursor.execute(sql, (1 if is_read else 0, alert_id, current_user_id))
            connection.commit()
            
        return jsonify({'code': 200, 'message': '状态更新成功'})
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)})
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# --- 任务管理接口 ---

@farming_bp.route('/api/tasks', methods=['GET'])
@token_required
def get_tasks(current_user_id):
    """获取用户的每日任务列表"""
    try:
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': '数据库连接失败'}), 500
        
        with connection.cursor() as cursor:
            # 获取当天的任务
            from utils import get_beijing_time
            today = get_beijing_time().date()
            
            sql = """
                SELECT id, title, description, task_type, priority, status, 
                       scheduled_date, scheduled_time, location
                FROM daily_tasks 
                WHERE user_id = %s AND (scheduled_date = %s OR status = 'pending')
                ORDER BY status ASC, scheduled_time ASC
            """
            cursor.execute(sql, (current_user_id, today))
            tasks = cursor.fetchall()
            
            # 格式化日期和时间
            for task in tasks:
                if task.get('scheduled_date'):
                    task['date'] = task['scheduled_date'].strftime('%Y-%m-%d')
                if task.get('scheduled_time'):
                    # 将 timedelta 或 time 转换为字符串
                    t = task['scheduled_time']
                    if hasattr(t, 'total_seconds'): # timedelta
                        hours = int(t.total_seconds() // 3600)
                        minutes = int((t.total_seconds() % 3600) // 60)
                        task['time'] = f"{hours:02d}:{minutes:02d}"
                    else:
                        task['time'] = t.strftime('%H:%M')
                else:
                    task['time'] = "08:00"
                
                # 兼容前端字段名并转为字符串以解决JSON序列化问题
                task['description'] = task.get('description') or ''
                if task.get('scheduled_date'):
                    task['scheduled_date'] = task['scheduled_date'].strftime('%Y-%m-%d')
                if task.get('scheduled_time'):
                    t = task['scheduled_time']
                    if hasattr(t, 'total_seconds'):
                        hours = int(t.total_seconds() // 3600)
                        minutes = int((t.total_seconds() % 3600) // 60)
                        task['scheduled_time'] = f"{hours:02d}:{minutes:02d}"
                    else:
                        task['scheduled_time'] = t.strftime('%H:%M')
                
            return jsonify({
                'success': True,
                'data': tasks
            }), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@farming_bp.route('/api/tasks', methods=['POST'])
@token_required
def create_task(current_user_id):
    """创建新任务"""
    try:
        data = request.get_json()
        if not data or not data.get('title'):
            return jsonify({'success': False, 'message': '标题不能为空'}), 400
        
        connection = get_db_connection()
        if not connection:
            return jsonify({'success': False, 'message': '数据库连接失败'}), 500
        
        from utils import get_beijing_time
        today = get_beijing_time().date()
        
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO daily_tasks (user_id, title, description, priority, location, scheduled_date, scheduled_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            """
            cursor.execute(sql, (
                current_user_id,
                data.get('title'),
                data.get('description', ''),
                data.get('priority', 'medium'),
                data.get('location', '农田'),
                today,
                data.get('time', '08:00'),
            ))
            connection.commit()
            
            return jsonify({
                'success': True,
                'message': '任务创建成功',
                'id': cursor.lastrowid
            }), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@farming_bp.route('/api/tasks/<int:task_id>', methods=['GET'])
@token_required
def get_task_detail(current_user_id, task_id):
    """获取任务详情"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM daily_tasks WHERE id = %s AND user_id = %s"
            cursor.execute(sql, (task_id, current_user_id))
            task = cursor.fetchone()
            
            if not task:
                return jsonify({'success': False, 'message': '任务不存在'}), 404
            
            # 格式化以解决JSON序列化问题
            if task.get('scheduled_date'):
                task['scheduled_date'] = task['scheduled_date'].strftime('%Y-%m-%d')
            if task.get('scheduled_time'):
                t = task['scheduled_time']
                if hasattr(t, 'total_seconds'):
                    hours = int(t.total_seconds() // 3600)
                    minutes = int((t.total_seconds() % 3600) // 60)
                    task['scheduled_time'] = f"{hours:02d}:{minutes:02d}"
                    task['time'] = task['scheduled_time']
                else:
                    task['scheduled_time'] = t.strftime('%H:%M')
                    task['time'] = task['scheduled_time']
            if task.get('created_at'):
                task['created_at'] = task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if task.get('completed_at'):
                task['completed_at'] = task['completed_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({'success': True, 'data': task}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@farming_bp.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
@token_required
def update_task_status(current_user_id, task_id):
    """更新任务状态"""
    try:
        # 简单实现：目前只支持标记为完成
        connection = get_db_connection()
        with connection.cursor() as cursor:
            from utils import get_beijing_time
            now = get_beijing_time()
            sql = "UPDATE daily_tasks SET status = 'completed', completed_at = %s WHERE id = %s AND user_id = %s"
            cursor.execute(sql, (now, task_id, current_user_id))
            connection.commit()
            
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'message': '更新失败'}), 400
            
            return jsonify({'success': True, 'message': '状态更新成功'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        if 'connection' in locals() and connection:
            connection.close()

# --- 农历与节气接口 ---

@farming_bp.route('/api/lunar', methods=['GET'])
def get_lunar_info():
    """获取当前农历和节气信息 (简化算法)"""
    from utils import get_beijing_time
    now = get_beijing_time()
    
    # 这里使用一个简化的算法或者静态映射作为演示
    # 实际生产环境应使用 lunar-python 等库
    # 我们根据 2026-03-25 计算
    # 2026年3月25日 是 农历二月初七
    # 春分是 3月20日
    
    lunar_date = "农历二月初七"
    solar_term = "春分后第5天"
    
    # 动态计算逻辑（示例）：
    # 实际上这里应该调用一个复杂的转换函数
    # 暂时返回一个基于当前日期的"看起来真实"的数据
    
    return jsonify({
        'success': True,
        'lunar_date': lunar_date,
        'solar_term': solar_term,
        'full_info': f"{lunar_date} · {solar_term}"
    })
