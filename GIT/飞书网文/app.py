from flask import Flask, render_template, request, jsonify
import requests
import json
import time
from datetime import datetime, timedelta
import markdown
from config import config
import os

# 创建Flask应用
def create_app(config_name=None):
    app = Flask(__name__)
    
    # 加载配置
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    return app

app = create_app()

# 全局变量用于缓存
cache = {
    'data': None,
    'timestamp': None
}

class FeishuAPI:
    """飞书API操作类"""
    
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self):
        """获取访问令牌"""
        if self.access_token and self.token_expires_at and datetime.now() < self.token_expires_at:
            return self.access_token
        
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if result.get('code') == 0:
                self.access_token = result['tenant_access_token']
                # 令牌有效期为2小时，提前10分钟刷新
                self.token_expires_at = datetime.now() + timedelta(seconds=result['expire'] - 600)
                return self.access_token
            else:
                print(f"获取访问令牌失败: {result}")
                return None
        except Exception as e:
            print(f"获取访问令牌异常: {e}")
            return None
    
    def get_table_records(self, base_id, table_id):
        """获取多维表格记录"""
        access_token = self.get_access_token()
        if not access_token:
            return []
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_id}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        try:
            response = requests.get(url, headers=headers)
            result = response.json()
            
            if result.get('code') == 0:
                return result.get('data', {}).get('items', [])
            else:
                print(f"获取表格记录失败: {result}")
                return []
        except Exception as e:
            print(f"获取表格记录异常: {e}")
            return []

# 初始化飞书API
feishu_api = FeishuAPI(app.config['FEISHU_APP_ID'], app.config['FEISHU_APP_SECRET'])

def get_blog_data():
    """获取博客数据，带缓存机制"""
    global cache
    
    # 检查缓存是否有效
    if (cache['data'] is not None and 
        cache['timestamp'] is not None and 
        time.time() - cache['timestamp'] < app.config['CACHE_TIMEOUT']):
        return cache['data']
    
    # 从飞书获取数据
    records = feishu_api.get_table_records(app.config['BASE_ID'], app.config['TABLE_ID'])
    
    # 处理数据
    articles = []
    for record in records:
        fields = record.get('fields', {})
        
        # 从链接字段中提取标题
        link_field = fields.get('链接', {})
        title = ''
        if isinstance(link_field, dict):
            title = link_field.get('text', '') or link_field.get('link', '')
        elif isinstance(link_field, str):
            title = link_field
        
        # 如果没有标题，使用总结的前50个字符作为标题
        if not title:
            summary = fields.get('总结', '')
            title = summary[:50] + '...' if len(summary) > 50 else summary
        
        # 使用实际的字段名
        content = fields.get('全文内容提取', '') or fields.get('总结', '')
        
        article = {
            'id': record.get('record_id'),
            'title': title,
            'quote': fields.get('小白解读', ''),  # 使用小白解读作为金句
            'review': fields.get('总结', ''),     # 使用总结作为点评
            'content': content,
            'preview': content[:app.config['PREVIEW_LENGTH']] + '...' if len(content) > app.config['PREVIEW_LENGTH'] else content
        }
        
        # 只添加有内容的文章
        if article['title'] and (article['content'] or article['quote'] or article['review']):
            articles.append(article)
    
    # 更新缓存
    cache['data'] = articles
    cache['timestamp'] = time.time()
    
    return articles

@app.route('/')
def index():
    """首页"""
    articles = get_blog_data()
    return render_template('index.html', articles=articles)

@app.route('/article/<article_id>')
def article_detail(article_id):
    """文章详情页"""
    articles = get_blog_data()
    article = next((a for a in articles if a['id'] == article_id), None)
    
    if not article:
        return render_template('404.html'), 404
    
    # 处理Markdown内容
    if article['content']:
        article['content_html'] = markdown.markdown(article['content'])
    else:
        article['content_html'] = article['content']
    
    return render_template('detail.html', article=article)

@app.route('/api/articles')
def api_articles():
    """API接口：获取文章列表"""
    articles = get_blog_data()
    return jsonify({
        'code': 0,
        'data': articles,
        'message': 'success'
    })

@app.route('/api/refresh')
def api_refresh():
    """API接口：刷新缓存"""
    global cache
    cache['data'] = None
    cache['timestamp'] = None
    articles = get_blog_data()
    return jsonify({
        'code': 0,
        'message': '缓存已刷新',
        'count': len(articles)
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Vercel需要的应用导出
app_instance = app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])