import urllib.request
import json
import re

def req(url, method='GET', data=None, token=None):
    headers = {'Content-Type': 'application/json'}
    if token: headers['Cookie'] = f'token={token}'
    req_data = json.dumps(data).encode() if data else None
    r = urllib.request.Request(f'http://localhost:5000{url}', data=req_data, headers=headers, method=method)
    try:
        res = urllib.request.urlopen(r)
        return json.loads(res.read().decode()), res.headers
    except Exception as e:
        print(f"Error {url}:", e)
        return None, None

print("1. Login as farmer...")
body, headers = req('/api/login', method='POST', data={'username':'farmer', 'password':'farmer123'})
token = re.search(r'token=([^;]+)', headers.get('Set-Cookie')).group(1)

print("2. Create Community Post...")
res, _ = req('/api/community/posts', method='POST', data={'content': '我的麦田长势喜人！大家都用什么肥料？'}, token=token)
print(res)

print("3. Fetch Posts...")
res, _ = req('/api/community/posts', method='GET', token=token)
post_id = res['data'][0]['id']
print(f"Post ID: {post_id}")

print("4. Like Post...")
res, _ = req(f'/api/community/posts/{post_id}/like', method='POST', token=token)
print(res)

print("5. Comment on Post...")
res, _ = req(f'/api/community/posts/{post_id}/comments', method='POST', data={'content':'建议多用有机肥'}, token=token)
print(res)

print("6. Create Daily Task...")
res, _ = req('/api/tasks', method='POST', data={'title':'去田里喷洒农药', 'description':'二化螟防治', 'priority':'high', 'time':'08:00', 'location':'A区'}, token=token)
print(res)

print("7. Create Disease History...")
res, _ = req('/api/disease/history', method='POST', data={'disease_name':'稻瘟病', 'confidence':0.95, 'symptoms':'叶片黄', 'solutions':'喷药'}, token=token)
print(res)

print("8. Fetch Disease History...")
res, _ = req('/api/disease/history', method='GET', token=token)
print(f"Records count: {len(res['data'])}")
