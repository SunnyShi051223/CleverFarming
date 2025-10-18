// voice-input.js
// 语音输入功能实现

class VoiceInputManager {
    constructor() {
        this.recognition = null;
        this.isListening = false;
        this.resultCallback = null;
        this.errorCallback = null;
        
        // 检查浏览器是否支持语音识别
        this.isSupported = this.checkSupport();
        
        if (this.isSupported) {
            this.initRecognition();
        }
    }
    
    // 检查浏览器是否支持语音识别
    checkSupport() {
        return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    }
    
    // 初始化语音识别
    initRecognition() {
        const SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false; // 只识别一次
        this.recognition.interimResults = false; // 不返回临时结果
        this.recognition.lang = 'zh-CN'; // 设置语言为中文
        
        // 事件监听
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            console.log('识别结果:', transcript);
            
            if (this.resultCallback) {
                this.resultCallback(transcript);
            }
            
            this.isListening = false;
        };
        
        this.recognition.onerror = (event) => {
            console.error('语音识别错误:', event.error);
            
            if (this.errorCallback) {
                this.errorCallback(event.error);
            }
            
            this.isListening = false;
        };
        
        this.recognition.onend = () => {
            console.log('语音识别结束');
            this.isListening = false;
        };
    }
    
    // 开始语音识别
    startListening(resultCallback, errorCallback) {
        if (!this.isSupported) {
            if (errorCallback) {
                errorCallback('浏览器不支持语音识别功能');
            }
            return;
        }
        
        if (this.isListening) {
            console.warn('语音识别已在进行中');
            return;
        }
        
        this.resultCallback = resultCallback;
        this.errorCallback = errorCallback;
        
        try {
            this.recognition.start();
            this.isListening = true;
            console.log('开始语音识别...');
        } catch (error) {
            console.error('启动语音识别失败:', error);
            if (errorCallback) {
                errorCallback('启动语音识别失败: ' + error.message);
            }
        }
    }
    
    // 停止语音识别
    stopListening() {
        if (this.isListening && this.recognition) {
            this.recognition.stop();
            this.isListening = false;
            console.log('停止语音识别');
        }
    }
    
    // 获取支持状态
    getSupportStatus() {
        return this.isSupported;
    }
}

// 创建全局实例
const voiceInputManager = new VoiceInputManager();

// 导出类和实例
window.VoiceInputManager = VoiceInputManager;
window.voiceInputManager = voiceInputManager;