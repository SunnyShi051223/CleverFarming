import os
from openai import OpenAI

try:
    client = OpenAI(
        # 直接使用api_key参数，而不是os.getenv()
        api_key="sk-cc0a8af819144e0ca7333124f5f3181b",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': '我的小麦长势不好，我该如何处理？'}
        ]
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://www.alibabacloud.com/help/zh/model-studio/developer-reference/error-code")
