# backend/ai_agent.py
# 智能农业问答AI代理模块

from flask import Blueprint, request, jsonify, current_app
import json
import re
import requests
from openai import OpenAI

# 创建蓝图
ai_agent_bp = Blueprint('ai_agent', __name__)

# 模拟农业知识库数据
AGRICULTURAL_KNOWLEDGE_BASE = {
    "水稻病害": {
        "稻瘟病": {
            "症状": "叶片出现梭形或椭圆形病斑，中央灰白色，边缘褐色；严重时叶片枯死。",
            "防治方法": "1. 选用抗病品种；2. 合理施肥，避免氮肥过量；3. 发病初期喷施三环唑、稻瘟灵等药剂。"
        },
        "纹枯病": {
            "症状": "叶鞘和叶片出现云纹状病斑，边缘褐色，中央灰白色，后期形成菌核。",
            "防治方法": "1. 浅水勤灌，适时晒田；2. 合理密植；3. 药剂防治可选用井冈霉素、己唑醇等。"
        }
    },
    "小麦病害": {
        "赤霉病": {
            "症状": "穗部出现粉红色霉层，籽粒皱缩，有霉味。",
            "防治方法": "1. 选用抗病品种；2. 合理施肥，避免后期贪青晚熟；3. 抽穗扬花期喷施多菌灵、咪鲜胺等药剂。"
        }
    },
    "施肥管理": {
        "水稻施肥": {
            "基肥": "每亩施用腐熟有机肥1500-2000公斤，配合施用复合肥30-40公斤。",
            "分蘖肥": "移栽后5-7天，每亩追施尿素8-10公斤，促进分蘖。",
            "穗肥": "拔节期和孕穗期分别追施尿素5-8公斤，钾肥3-5公斤。"
        }
    },
    "种植技术": {
        "水稻育秧": {
            "湿润育秧": "选择背风向阳、排灌方便的田块做秧田，每亩秧田播种量30-40公斤。",
            "旱育秧": "在旱地或湿润秧田采用旱育技术，播种量可适当增加。"
        }
    }
}

# 调用千问API函数
def call_qwen_api(question):
    """
    调用千问API获取答案
    """
    try:
        # 导入openai库
        from openai import OpenAI
        
        # 创建客户端实例
        client = OpenAI(
            api_key="sk-cc0a8af819144e0ca7333124f5f3181b",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # 调用千问API
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的农业专家助手，专门帮助农民解答有关作物种植、病虫害防治、施肥管理、农业技术等方面的问题。请用专业且易懂的语言回答用户的问题。"
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            max_tokens=1500,
            temperature=0.7,
            top_p=0.8
        )
        
        # 返回API响应内容
        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling Qwen API: {str(e)}")
        return None

# 格式化AI返回的文本
def format_ai_response(text):
    """
    对AI返回的文本进行格式化处理，使其更易于阅读
    """
    if not text:
        return text
    
    import re
    
    # 将多个连续的换行符替换为两个换行符（段落分隔）
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 处理标题（### 标题形式）
    text = re.sub(r'(?<=\n)### (.+?)(?=\n)', r'\n【\1】\n', text)
    text = re.sub(r'^### (.+?)(?=\n)', r'【\1】\n', text)
    
    # 处理次级标题（#### 标题形式）
    text = re.sub(r'(?<=\n)#### (.+?)(?=\n)', r'\n\1\n', text)
    text = re.sub(r'^#### (.+?)(?=\n)', r'\1\n', text)
    
    # 处理列表项
    text = re.sub(r'(?<=\n)\d+\. (.+?)(?=\n)', r'  \1\n', text)
    text = re.sub(r'^\d+\. (.+?)(?=\n)', r'  \1\n', text)
    text = re.sub(r'(?<=\n)- (.+?)(?=\n)', r'  \1\n', text)
    text = re.sub(r'^- (.+?)(?=\n)', r'  \1\n', text)
    
    # 处理强调内容（**内容**形式）
    text = re.sub(r'\*\*(.+?)\*\*', r'【\1】', text)
    
    # 处理表格行，添加分隔线
    lines = text.split('\n')
    formatted_lines = []
    in_table = False
    
    for line in lines:
        if '|' in line and line.count('|') >= 3:
            if not in_table:
                # 添加表格标题行的分隔线
                formatted_lines.append(line)
                # 添加分隔线
                separator = '|' + '|'.join(['---' for _ in range(line.count('|') - 2)]) + '|'
                formatted_lines.append(separator)
                in_table = True
            else:
                formatted_lines.append(line)
        else:
            if in_table:
                in_table = False
            formatted_lines.append(line)
    
    text = '\n'.join(formatted_lines)
    
    # 处理提示信息（✅ 形式）
    text = re.sub(r'(?<=\n)✅ (.+?)(?=\n)', r'\n提示：\1\n', text)
    text = re.sub(r'^✅ (.+?)(?=\n)', r'提示：\1\n', text)
    
    # 处理分隔线（将==================================================替换为换行）
    text = re.sub(r'\n=+\n', '\n\n', text)
    text = re.sub(r'^=+\n', '\n', text)
    text = re.sub(r'\n=+$', '\n', text)
    
    # 处理短分隔线（---形式）
    text = re.sub(r'\n---\n', '\n\n', text)
    text = re.sub(r'^---\n', '\n', text)
    
    # 去除行首行尾的多余空格
    lines = text.split('\n')
    formatted_lines = [line.strip() for line in lines]
    text = '\n'.join(formatted_lines)
    
    return text.strip()

# 模拟AI问答处理函数
def process_question(question):
    """
    处理用户问题，返回相关答案
    """
    # 首先尝试调用千问API
    qwen_answer = call_qwen_api(question)
    if qwen_answer:
        # 对AI返回的文本进行格式化处理
        return format_ai_response(qwen_answer)
    
    # 如果千问API调用失败，使用本地知识库
    # 简单的关键词匹配逻辑（实际应用中会使用更复杂的NLP模型）
    question = question.lower()
    
    # 关键词匹配
    if "稻瘟病" in question or "叶瘟" in question:
        disease_info = AGRICULTURAL_KNOWLEDGE_BASE["水稻病害"]["稻瘟病"]
        return f"稻瘟病的症状：{disease_info['症状']} 防治方法：{disease_info['防治方法']}"
    
    if "纹枯病" in question or "水稻纹枯病" in question:
        disease_info = AGRICULTURAL_KNOWLEDGE_BASE["水稻病害"]["纹枯病"]
        return f"纹枯病的症状：{disease_info['症状']} 防治方法：{disease_info['防治方法']}"
    
    if "赤霉病" in question or "小麦赤霉病" in question:
        disease_info = AGRICULTURAL_KNOWLEDGE_BASE["小麦病害"]["赤霉病"]
        return f"赤霉病的症状：{disease_info['症状']} 防治方法：{disease_info['防治方法']}"
    
    if "水稻施肥" in question:
        fertilization_info = AGRICULTURAL_KNOWLEDGE_BASE["施肥管理"]["水稻施肥"]
        return f"水稻施肥技术：基肥-{fertilization_info['基肥']} 分蘖肥-{fertilization_info['分蘖肥']} 穗肥-{fertilization_info['穗肥']}"
    
    if "水稻育秧" in question:
        technique_info = AGRICULTURAL_KNOWLEDGE_BASE["种植技术"]["水稻育秧"]
        return f"水稻育秧技术：湿润育秧-{technique_info['湿润育秧']} 旱育秧-{technique_info['旱育秧']}"
    
    # 如果没有匹配到具体问题，返回通用提示
    return "您好！我是农业智能助手，可以帮您解答有关作物种植、病虫害防治、施肥管理等方面的问题。请具体描述您遇到的问题，我会尽力为您解答。"

# AI问答接口
@ai_agent_bp.route('/ai-agent/ask', methods=['POST'])
def ask_question():
    """
    AI问答接口
    """
    try:
        # 获取请求数据
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'success': False,
                'message': '问题不能为空'
            }), 400
        
        # 处理问题并获取答案
        answer = process_question(question)
        
        # 返回结果
        return jsonify({
            'success': True,
            'data': {
                'question': question,
                'answer': answer
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'处理问题时发生错误: {str(e)}'
        }), 500

# 获取热门问题接口
@ai_agent_bp.route('/ai-agent/hot-questions', methods=['GET'])
def get_hot_questions():
    """
    获取热门问题列表
    """
    try:
        hot_questions = [
            "水稻稻瘟病怎么防治？",
            "小麦赤霉病的症状和防治方法？",
            "水稻施肥技术有哪些？",
            "水稻纹枯病如何识别和防治？",
            "水稻育秧技术要点是什么？"
        ]
        
        return jsonify({
            'success': True,
            'data': hot_questions
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取热门问题时发生错误: {str(e)}'
        }), 500