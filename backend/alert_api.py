from flask import Blueprint, jsonify, request
import pymysql
from config import Config
from functools import wraps
import jwt
from utils import get_beijing_time, get_db_connection, token_required

# 创建预警API蓝图
alert_bp = Blueprint('alert', __name__)


@alert_bp.route('/list', methods=['GET'])
@token_required
def get_alerts(current_user_id):
    """获取预警列表（支持分类过滤和个性化匹配）"""
    try:
        # 获取查询参数
        alert_type = request.args.get('type') # news 或 alert
        alert_subtype = request.args.get('subtype') # nyyw, nszd, nyqx, trsq, zwbch
        
        connection = get_db_connection()
        
        # 获取用户信息用于匹配
        with connection.cursor() as cursor:
            cursor.execute("SELECT city, crop_type FROM users WHERE id = %s", (current_user_id,))
            user = cursor.fetchone()
            
        user_city = user.get('city', '').replace('省', '').replace('市', '').replace('自治区', '') if user else ''
        user_crop = user.get('crop_type', '') if user else ''
        
        # 构建查询语句
        query = """
            SELECT id, alert_type, alert_subtype, title, content, priority, is_read, location, created_at 
            FROM farming_alerts 
            WHERE user_id = %s
        """
        params = [current_user_id]
        
        # 强制只返回 'alert' 类型的数据
        query += " AND alert_type = 'alert'"
        
        if alert_type and alert_type != 'all' and alert_type != 'alert':
            # 如果请求的是 news 类型，但在预警平台，我们还是返回 alert 或者返回空
            # 这里我们强制过滤为 alert 子类型
            pass
            
        if alert_subtype and alert_subtype != 'all':
            query += " AND alert_subtype = %s"
            params.append(alert_subtype)
        else:
            # 默认只显示农业气象、土壤墒情、植物病虫害
            query += " AND alert_subtype IN ('nyqx', 'trsq', 'zwbch')"
            
        query += " ORDER BY is_read ASC, created_at DESC"
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            alerts = cursor.fetchall()
            
            # 子类型映射
            subtype_map = {
                'nyyw': '农业要闻',
                'nszd': '农事指导',
                'nyqx': '农业气象',
                'trsq': '土壤墒情',
                'zwbch': '植物病虫害'
            }
            
            # 处理预警数据
            processed_alerts = []
            for alert in alerts:
                # 计算匹配分数
                match_score = 0
                content_str = alert.get('content', '') or ''
                if user_crop and user_crop in content_str:
                    match_score += 2
                if user_city and user_city in content_str:
                    match_score += 1
                
                processed_alerts.append({
                    'id': alert['id'],
                    'alert_type': alert['alert_type'],
                    'alert_subtype': alert['alert_subtype'],
                    'subtype_name': subtype_map.get(alert['alert_subtype'], alert['alert_subtype']),
                    'title': alert['title'],
                    'content': alert['content'],
                    'priority': alert['priority'],
                    'is_read': bool(alert['is_read']),
                    'location': alert['location'],
                    'created_at': alert['created_at'].strftime('%Y-%m-%d %H:%M:%S') if alert['created_at'] else '未知时间',
                    'match_score': match_score
                })
            
            # 按匹配分数排序
            processed_alerts.sort(key=lambda x: -x['match_score'])
            
            return jsonify({
                'code': 200,
                'message': 'success',
                'data': processed_alerts
            })
    
    except Exception as e:
        print(f"获取预警列表失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        })
    finally:
        if 'connection' in locals():
            connection.close()

@alert_bp.route('/detail/<int:alert_id>', methods=['GET'])
@token_required
def get_alert_detail(current_user_id, alert_id):
    """获取预警详情"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 查询预警详情
            query = """
            SELECT id, alert_type, alert_subtype, title, content, created_at 
            FROM farming_alerts 
            WHERE id = %s AND user_id = %s
            """
            cursor.execute(query, (alert_id, current_user_id))
            alert = cursor.fetchone()
            
            if not alert:
                return jsonify({
                    'code': 404,
                    'message': '预警不存在'
                })
            
            # 子类型映射
            subtype_map = {
                'nyyw': '农业要闻',
                'nszd': '农事指导',
                'nyqx': '农业气象',
                'trsq': '土壤墒情',
                'zwbch': '植物病虫害'
            }
            alert['subtype_name'] = subtype_map.get(alert['alert_subtype'], alert['alert_subtype'])
            
            # 格式化时间
            if alert['created_at']:
                alert['created_at'] = alert['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
            return jsonify({
                'code': 200,
                'message': 'success',
                'data': alert
            })
    
    except Exception as e:
        print(f"获取预警详情失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        })
    finally:
        if 'connection' in locals():
            connection.close()