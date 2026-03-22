import requests
import json

def test_formatting_update():
    """测试更新后的格式化功能"""
    url = "http://127.0.0.1:5000/api/ai-agent/ask"
    
    # 测试问题
    question = "我的小麦长势不好，叶子发黄，植株矮小，有什么解决办法？"
    
    print(f"测试问题: {question}")
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
                answer = result['data']['answer']
                print(answer)
                
                # 检查是否还有==================================================字符
                if '='*50 in answer:
                    print("\n❌ 仍然存在==================================================字符")
                else:
                    print("\n✅ 已成功将==================================================替换为换行")
            else:
                print(f"❌ 请求失败: {result.get('message')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_formatting_update()