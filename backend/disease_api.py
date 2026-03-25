# backend/disease_api.py
from flask import Blueprint, jsonify, request, current_app
import pymysql
import jwt
from utils import get_beijing_time

disease_bp = Blueprint('disease', __name__)

from utils import get_db_connection, token_required, get_beijing_time

@disease_bp.route('/api/disease/history', methods=['POST'])
@token_required
def save_history(current_user_id):
    data = request.json
    disease_name = data.get('disease_name')
    confidence = data.get('confidence')
    symptoms = data.get('symptoms', '')
    solutions = data.get('solutions', '')
    
    if not disease_name or confidence is None:
        return jsonify({'success': False, 'message': '识别结果不完整'}), 400
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO disease_identification_history 
                (user_id, disease_name, confidence, symptoms, solutions, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (current_user_id, disease_name, confidence, symptoms, solutions, get_beijing_time()))
            conn.commit()
            return jsonify({'success': True, 'record_id': cursor.lastrowid})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()

@disease_bp.route('/api/disease/history', methods=['GET'])
@token_required
def get_history(current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, disease_name, confidence, symptoms, solutions, 
                       DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i') as time
                FROM disease_identification_history 
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (current_user_id,))
            records = cursor.fetchall()
            return jsonify({'success': True, 'data': records})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        conn.close()
