import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # 飞书应用配置
    FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID') or 'cli_a8004401f9fdd013'
    FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET') or 'IUKbsrkRwVaG686kwSvdQcTfZEFiMelA'
    
    # 多维表格配置
    BASE_ID = os.environ.get('BASE_ID') or 'TpKrbsbV6aIJ2fsBRi2cCHEqnFg'
    TABLE_ID = os.environ.get('TABLE_ID') or 'tbl60xA82n9YXO2Z'
    
    # 缓存配置
    CACHE_TIMEOUT = int(os.environ.get('CACHE_TIMEOUT', '300'))  # 5分钟缓存
    
    # 分页配置
    POSTS_PER_PAGE = int(os.environ.get('POSTS_PER_PAGE', '10'))
    
    # 文章预览长度
    PREVIEW_LENGTH = int(os.environ.get('PREVIEW_LENGTH', '100'))

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}