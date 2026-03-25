import requests
import jwt
from datetime import datetime, timedelta
import os
import sys

# Add backend to path to import Config
sys.path.append(os.getcwd())
from config import Config

def test_apis():
    payload = {
        'user_id': 4,
        'role': 'user',
        'exp': datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    headers = {
        'Cookie': f'token={token}'
    }
    
    base_url = "http://127.0.0.1:5001"
    
    print("Testing Lunar API...")
    try:
        r = requests.get(f"{base_url}/api/lunar", headers=headers)
        print(f"Lunar: {r.status_code} - {r.json()}")
    except Exception as e:
        print(f"Lunar Error: {e}")
        
    print("\nTesting Tasks API...")
    try:
        r = requests.get(f"{base_url}/api/tasks", headers=headers)
        tasks = r.json().get('data', [])
        print(f"Tasks: {r.status_code} - Found {len(tasks)} items")
    except Exception as e:
        print(f"Tasks Error: {e}")
        
    print("\nTesting Weather API...")
    try:
        r = requests.get(f"{base_url}/api/weather", headers=headers)
        weather = r.json().get('weather', {}).get('weather', 'N/A')
        print(f"Weather: {r.status_code} - {weather}")
    except Exception as e:
        print(f"Weather Error: {e}")

if __name__ == "__main__":
    test_apis()
