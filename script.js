// 简单项目的主要JavaScript文件

/**
 * 项目初始化函数
 */
function initProject() {
    console.log('🚀 项目初始化中...');
    
    // 设置当前时间
    updateCurrentTime();
    
    // 每秒更新时间
    setInterval(updateCurrentTime, 1000);
    
    console.log('✅ 项目初始化完成！');
}

/**
 * 更新当前时间显示
 */
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleString('zh-CN');
    
    // 如果页面有时间显示元素，则更新它
    const timeElement = document.getElementById('current-time');
    if (timeElement) {
        timeElement.textContent = timeString;
    }
}

/**
 * 显示欢迎消息
 * @param {string} name - 用户名称
 */
function showWelcomeMessage(name = '访客') {
    const message = `🎉 欢迎 ${name} 来到我的项目！`;
    console.log(message);
    
    // 如果有消息显示区域，则显示消息
    const messageArea = document.getElementById('message-area');
    if (messageArea) {
        messageArea.innerHTML = `<div class="welcome-message">${message}</div>`;
    }
}

/**
 * 简单的工具函数集合
 */
const Utils = {
    /**
     * 生成随机颜色
     */
    getRandomColor() {
        const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'];
        return colors[Math.floor(Math.random() * colors.length)];
    },
    
    /**
     * 格式化数字
     * @param {number} num - 要格式化的数字
     */
    formatNumber(num) {
        return num.toLocaleString('zh-CN');
    },
    
    /**
     * 检查是否为移动设备
     */
    isMobile() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }
};

/**
 * 页面加载完成后执行
 */
document.addEventListener('DOMContentLoaded', function() {
    initProject();
    showWelcomeMessage();
    
    // 检测设备类型
    if (Utils.isMobile()) {
        console.log('📱 检测到移动设备');
        document.body.classList.add('mobile-device');
    } else {
        console.log('💻 检测到桌面设备');
        document.body.classList.add('desktop-device');
    }
});

// 导出函数供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initProject,
        showWelcomeMessage,
        Utils
    };
}