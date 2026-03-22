import requests
import json
import random

BASE_URL = "http://127.0.0.1:5000"

def test_register_with_personalization():
    """测试注册时收集个性化信息"""
    print("=" * 50)
    print("测试1: 注册新用户并收集个性化信息")
    print("=" * 50)
    
    # 注册新用户（使用随机用户名避免重复）
    random_num = random.randint(1000, 9999)
    register_data = {
        "username": f"test_user_{random_num}",
        "password": "test123456",
        "role": "user",
        "city": "深圳",
        "crop_type": "水果",
        "farm_area": 25.5,
        "is_initialized": 1
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/register", json=register_data)
        result = response.json()
        
        if response.status_code == 201:
            print("✓ 注册成功")
            print(f"  用户ID: {result['user']['id']}")
            print(f"  用户名: {result['user']['username']}")
            print(f"  城市: {result['user']['city']}")
            print(f"  作物类型: {result['user']['crop_type']}")
            print(f"  农田面积: {result['user']['farm_area']}")
            return result['user']['id']
        else:
            print(f"✗ 注册失败: {result.get('message', '未知错误')}")
            return None
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return None

def test_existing_users():
    """测试现有用户的个性化信息"""
    print("\n" + "=" * 50)
    print("测试2: 验证现有用户的个性化信息")
    print("=" * 50)
    
    # 测试登录并获取用户信息
    test_users = [
        {"username": "admin", "password": "admin123", "expected_city": "北京", "expected_crop": "小麦"},
        {"username": "farmer", "password": "farmer123", "expected_city": "武汉", "expected_crop": "水稻"},
        {"username": "test_yang", "password": "test123", "expected_city": "上海", "expected_crop": "玉米"},
        {"username": "111", "password": "111111", "expected_city": "广州", "expected_crop": "蔬菜"}
    ]
    
    for user in test_users:
        print(f"\n测试用户: {user['username']}")
        try:
            # 登录
            login_response = requests.post(f"{BASE_URL}/api/login", json={
                "username": user["username"],
                "password": user["password"],
                "role": "user" if user["username"] != "admin" else "admin"
            })
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                # 从cookie中获取token
                token = login_response.cookies.get('token')
                
                if not token:
                    print(f"  ✗ 未获取到token")
                    continue
                
                user_id = login_result['user']['id']
                
                # 获取用户信息（使用正确的端点）
                profile_response = requests.get(
                    f"{BASE_URL}/api/user/info",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    if profile.get('success'):
                        user_data = profile['user']
                        city = user_data.get('city', '未设置')
                        crop_type = user_data.get('crop_type', '未设置')
                        farm_area = user_data.get('farm_area', '未设置')
                        is_initialized = user_data.get('is_initialized', 0)
                        
                        # 验证个性化信息
                        city_match = city == user['expected_city']
                        crop_match = crop_type == user['expected_crop']
                        
                        if city_match and crop_match:
                            print(f"  ✓ 个性化信息正确")
                            print(f"    城市: {city} (预期: {user['expected_city']})")
                            print(f"    作物: {crop_type} (预期: {user['expected_crop']})")
                            print(f"    面积: {farm_area}亩")
                            print(f"    已初始化: {'是' if is_initialized else '否'}")
                        else:
                            print(f"  ✗ 个性化信息不匹配")
                            print(f"    城市: {city} (预期: {user['expected_city']}) - {'✓' if city_match else '✗'}")
                            print(f"    作物: {crop_type} (预期: {user['expected_crop']}) - {'✓' if crop_match else '✗'}")
                    else:
                        print(f"  ✗ 获取用户信息失败: {profile.get('message', '未知错误')}")
                else:
                    print(f"  ✗ 获取用户信息失败: HTTP {profile_response.status_code}")
                    print(f"  响应内容: {profile_response.text[:200]}")
            else:
                print(f"  ✗ 登录失败: {login_response.status_code}")
                print(f"  响应内容: {login_response.text[:200]}")
        except Exception as e:
            print(f"  ✗ 测试失败: {e}")

def test_weather_api():
    """测试天气API是否根据城市返回不同的天气"""
    print("\n" + "=" * 50)
    print("测试3: 验证天气API的个性化")
    print("=" * 50)
    
    cities = ["北京", "武汉", "上海", "广州"]
    
    for city in cities:
        try:
            response = requests.get(f"{BASE_URL}/api/weather", params={"city": city})
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    weather = result['weather']
                    print(f"\n城市: {city}")
                    print(f"  温度: {weather.get('temperature', 'N/A')}°C")
                    print(f"  天气: {weather.get('condition', 'N/A')}")
                    print(f"  湿度: {weather.get('humidity', 'N/A')}%")
                else:
                    print(f"\n城市: {city} - 获取天气失败: {result.get('message', '未知错误')}")
            else:
                print(f"\n城市: {city} - HTTP {response.status_code}")
        except Exception as e:
            print(f"\n城市: {city} - 请求失败: {e}")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("开始个性化功能测试")
    print("=" * 50)
    
    # 测试1: 注册新用户
    new_user_id = test_register_with_personalization()
    
    # 测试2: 验证现有用户
    test_existing_users()
    
    # 测试3: 验证天气API
    test_weather_api()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)