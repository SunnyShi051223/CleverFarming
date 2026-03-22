import requests
import json

# 测试AI问答功能
def test_ai_question():
    url = "http://127.0.0.1:5000/api/ai-agent/ask"
    headers = {
        "Content-Type": "application/json"
    }
    
    # 测试问题
    data = {
        "question": "我的小麦长势不好，我该如何处理？"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Status Code:", response.status_code)
        print("Response:", response.json())
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_ai_question()