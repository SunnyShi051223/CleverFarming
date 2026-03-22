// api/js/user-info.js
// 用户信息和天气API调用模块

/**
 * 获取用户完整信息
 */
async function getUserProfile() {
    try {
        const response = await fetch('/api/user/info', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.user;
        } else {
            console.error('获取用户信息失败:', data.message);
            return null;
        }
    } catch (error) {
        console.error('获取用户信息出错:', error);
        return null;
    }
}

/**
 * 获取天气信息
 * @param {string} city - 城市名称
 * @param {string} adcode - 城市编码（可选，如果不提供会自动查找）
 */
async function getWeather(city = '武汉', adcode = null) {
    try {
        // 如果没有提供adcode，尝试从城市编码表获取
        if (!adcode && typeof getCityCode === 'function') {
            adcode = getCityCode(city);
        }
        
        // 如果还是没有，使用默认值
        if (!adcode) {
            adcode = '420100'; // 默认武汉
        }
        
        console.log(`获取天气: ${city} (${adcode})`);
        
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}&adcode=${adcode}`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            console.log('天气数据:', data.weather);
            if (data.note) {
                console.warn('天气数据说明:', data.note);
            }
            return data.weather;
        } else {
            console.error('获取天气信息失败:', data.message);
            return null;
        }
    } catch (error) {
        console.error('获取天气信息出错:', error);
        return null;
    }
}

/**
 * 获取用户统计信息
 */
async function getUserStats() {
    try {
        const response = await fetch('/api/user/stats', {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.stats;
        } else {
            console.error('获取统计信息失败:', data.message);
            return null;
        }
    } catch (error) {
        console.error('获取统计信息出错:', error);
        return null;
    }
}

/**
 * 更新用户信息
 * @param {Object} userData - 要更新的用户数据
 */
async function updateUserProfile(userData) {
    try {
        const response = await fetch('/api/user/info', {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            return true;
        } else {
            console.error('更新用户信息失败:', data.message);
            return false;
        }
    } catch (error) {
        console.error('更新用户信息出错:', error);
        return false;
    }
}

/**
 * 初始化用户界面信息
 * 自动更新页面上的用户信息和天气信息
 */
async function initUserInterface() {
    try {
        // 获取用户信息
        const user = await getUserProfile();
        
        if (user) {
            // 检查是否已完成初始化，若未完成，则弹出强制引导收集必要信息
            if (!user.is_initialized) {
                const initModal = document.getElementById('initProfileModal');
                if (initModal) {
                    initModal.style.display = 'flex';
                    
                    // 防止点击背景关闭模态框
                    initModal.addEventListener('click', function(e) {
                        if (e.target === initModal) {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                    });
                    
                    // 防止ESC键关闭模态框
                    document.addEventListener('keydown', function preventEsc(e) {
                        if (e.key === 'Escape' && initModal.style.display === 'flex') {
                            e.preventDefault();
                            e.stopPropagation();
                        }
                    });
                    
                    // 添加输入框焦点效果
                    const inputs = initModal.querySelectorAll('input, select');
                    inputs.forEach(input => {
                        input.addEventListener('focus', function() {
                            this.style.borderColor = 'var(--primary-color)';
                            this.style.boxShadow = '0 0 0 3px rgba(76,175,80,0.1)';
                        });
                        input.addEventListener('blur', function() {
                            this.style.borderColor = 'var(--border-color)';
                            this.style.boxShadow = 'none';
                        });
                    });
                }
            }

            // 更新用户名
            const usernameElements = document.querySelectorAll('.user-name, .username');
            usernameElements.forEach(el => {
                el.textContent = user.username || '农户';
            });
            
            // 更新头像
            const avatarElements = document.querySelectorAll('.user-avatar');
            if (user.avatar_url) {
                avatarElements.forEach(el => {
                    el.src = user.avatar_url;
                });
            }
            
            // 更新地区
            const locationElements = document.querySelectorAll('.user-location');
            locationElements.forEach(el => {
                el.textContent = user.city || '北京';
            });
            
            // 更新作物类型
            const cropElements = document.querySelectorAll('.user-crop');
            cropElements.forEach(el => {
                el.textContent = user.crop_type || '小麦';
            });
            
            // 更新农田面积
            const farmAreaElements = document.querySelectorAll('.user-farm-area');
            farmAreaElements.forEach(el => {
                const area = user.farm_area || 0;
                el.textContent = `${area}亩`;
            });
            
            // 更新统计信息
            if (user.stats) {
                // 未读预警数
                const alertCountElements = document.querySelectorAll('.alert-count, .unread-count');
                alertCountElements.forEach(el => {
                    el.textContent = user.stats.unread_alerts || 0;
                });
                
                // 使用天数
                const daysUsedElements = document.querySelectorAll('.days-used');
                daysUsedElements.forEach(el => {
                    el.textContent = `${user.stats.days_used || 0}天`;
                });
            }
            
            // 获取并更新天气信息
            const weather = await getWeather(user.city || '北京');
            if (weather) {
                updateWeatherUI(weather);
            }
        }
    } catch (error) {
        console.error('初始化用户界面失败:', error);
    }
}

/**
 * 更新天气UI
 * @param {Object} weather - 天气数据
 */
function updateWeatherUI(weather) {
    console.log('更新天气UI:', weather);
    
    // 更新温度
    const tempElements = document.querySelectorAll('.weather-temp, .temperature');
    tempElements.forEach(el => {
        el.textContent = `${weather.temperature}°C`;
    });
    
    // 更新天气状况
    const conditionElements = document.querySelectorAll('.weather-condition, .weather-desc');
    conditionElements.forEach(el => {
        el.textContent = weather.weather || '多云';
    });
    
    // 更新湿度
    const humidityElements = document.querySelectorAll('.weather-humidity');
    humidityElements.forEach(el => {
        el.textContent = `${weather.humidity}%`;
    });
    
    // 更新风速/风向
    const windElements = document.querySelectorAll('.weather-wind');
    windElements.forEach(el => {
        const windText = `${weather.wind_direction}风 ${weather.wind_power}`;
        el.textContent = windText;
    });
    
    // 更新气压（如果有）
    const pressureElements = document.querySelectorAll('.weather-pressure');
    if (weather.pressure) {
        pressureElements.forEach(el => {
            el.textContent = `${weather.pressure}hPa`;
        });
    } else {
        // 如果没有气压数据，显示报告时间
        pressureElements.forEach(el => {
            if (weather.report_time) {
                const time = weather.report_time.split(' ')[1] || weather.report_time;
                el.textContent = time;
            }
        });
    }
    
    // 根据天气更新图标
    updateWeatherIcon(weather.weather);
}

/**
 * 根据天气状况更新图标
 * @param {string} weatherCondition - 天气状况
 */
function updateWeatherIcon(weatherCondition) {
    const iconElements = document.querySelectorAll('.weather-icon');
    let iconClass = 'fa-cloud-sun'; // 默认图标
    
    if (weatherCondition.includes('晴')) {
        iconClass = 'fa-sun';
    } else if (weatherCondition.includes('雨')) {
        iconClass = 'fa-cloud-rain';
    } else if (weatherCondition.includes('雪')) {
        iconClass = 'fa-snowflake';
    } else if (weatherCondition.includes('阴')) {
        iconClass = 'fa-cloud';
    } else if (weatherCondition.includes('雷')) {
        iconClass = 'fa-bolt';
    }
    
    iconElements.forEach(el => {
        // 移除所有天气图标类
        el.className = el.className.replace(/fa-\w+/g, '');
        // 添加新图标类
        el.classList.add('fas', iconClass);
    });
}

/**
 * 定时刷新天气信息（每30分钟）
 */
function startWeatherAutoRefresh() {
    setInterval(async () => {
        const user = await getUserProfile();
        if (user && user.city) {
            const weather = await getWeather(user.city);
            if (weather) {
                updateWeatherUI(weather);
            }
        }
    }, 30 * 60 * 1000); // 30分钟
}

// 页面加载时自动初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initUserInterface();
        startWeatherAutoRefresh();
    });
} else {
    initUserInterface();
    startWeatherAutoRefresh();
}

/**
 * 提交初始化信息
 */
async function submitInitialization() {
    const city = document.getElementById('initCity').value.trim();
    const cropType = document.getElementById('initCropType').value;
    const farmArea = document.getElementById('initFarmArea').value;
    
    // 严格验证
    if (!city) {
        alert('请输入所在地区（城市）');
        document.getElementById('initCity').focus();
        return;
    }
    
    if (!cropType) {
        alert('请选择主要种植作物');
        document.getElementById('initCropType').focus();
        return;
    }
    
    if (!farmArea || isNaN(farmArea) || parseFloat(farmArea) <= 0) {
        alert('请输入有效的农田面积（必须大于0）');
        document.getElementById('initFarmArea').focus();
        return;
    }
    
    const submitBtn = document.getElementById('initSubmitBtn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '正在配置专属数据...';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';
    
    try {
        // 提交到后端并更新初始化标记为1 (true)
        const success = await updateUserProfile({
            city: city,
            crop_type: cropType,
            farm_area: parseFloat(farmArea),
            is_initialized: 1
        });
        
        if (success) {
            document.getElementById('initProfileModal').style.display = 'none';
            alert('初始化设置成功！系统已为您加载专属农业信息面板。');
            await initUserInterface(); // 重新加载用户最新数据
        } else {
            alert('信息保存失败，请检查网络并重试');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    } catch (error) {
        console.error('提交初始化信息失败:', error);
        alert('提交失败，请检查网络连接后重试');
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }
}
