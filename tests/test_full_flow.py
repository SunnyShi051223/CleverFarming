import requests
import json

def test_ai_flow():
    """测试完整的AI问答流程"""
    url = "http://127.0.0.1:5000/api/ai-agent/ask"
    
    # 测试问题
    test_questions = [
        "我的小麦长势不好，叶子发黄，植株矮小，有什么解决办法？",
        "水稻稻瘟病怎么防治？",
        "小麦赤霉病的症状和防治方法？"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*50}")
        print(f"测试问题 {i}: {question}")
        print('='*50)
        
        payload = {
            "question": question
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print("✅ 请求成功!")
                    print("\nAI回答:")
                    print('-' * 30)
                    print(result['data']['answer'])
                else:
                    print(f"❌ 请求失败: {result.get('message')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_ai_flow()