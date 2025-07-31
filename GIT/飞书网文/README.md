# 飞书博客网站

基于 Flask 的个人博客网站，数据来源于飞书多维表格。网站采用深色科技风格设计，提供简洁优雅的阅读体验。

## 功能特点

### 🎨 现代化设计
- 深色科技风格界面
- 响应式布局，支持多设备访问
- 流畅的动画效果和交互体验
- 基于 CSS Grid 和 Flexbox 的现代布局

### 📝 内容管理
- **首页展示**：博客标题、精选金句、文章预览
- **文章详情页**：完整文章内容、金句展示、点评内容
- **实时同步**：从飞书多维表格获取最新数据
- **缓存机制**：提升页面加载速度

### 🔗 飞书集成
- 通过飞书 API 获取多维表格数据
- 支持实时数据更新
- 安全的访问令牌管理

## 技术栈

- **后端**：Python Flask 3.0.0
- **前端**：原生 HTML/CSS/JavaScript
- **数据源**：飞书多维表格 API
- **样式**：深色科技风格，参考微信聊天记录可视化设计
- **图标**：Font Awesome 6.0

## 项目结构

```
feishu-blog/
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖包
├── config.py             # 配置文件
├── app.py               # 主应用文件
├── .env.example         # 环境变量模板
├── venv/               # Python 虚拟环境
├── templates/          # HTML 模板
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页模板
│   ├── detail.html    # 文章详情页模板
│   ├── 404.html       # 404 错误页面
│   └── 500.html       # 500 错误页面
└── static/            # 静态文件
    ├── css/          # 样式文件
    ├── js/           # JavaScript 文件
    └── images/       # 图片文件
```

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8+：

```bash
python --version
```

### 2. 激活虚拟环境

```bash
# Windows
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置飞书应用

#### 4.1 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`
4. 开启权限：`bitable:record:read`（多维表格读取权限）

#### 4.2 创建多维表格

在飞书中创建多维表格，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 标题 | 单行文本 | 文章标题 |
| 金句输出 | 多行文本 | 精选金句内容 |
| 黄叔点评 | 多行文本 | 点评内容 |
| 概要内容输出 | 多行文本 | 文章正文内容 |

#### 4.3 配置环境变量

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 飞书应用配置
FEISHU_APP_ID=your_app_id_here
FEISHU_APP_SECRET=your_app_secret_here

# 多维表格配置
BASE_ID=your_base_id_here
TABLE_ID=your_table_id_here

# Flask 配置
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

### 5. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 查看网站。

## 配置说明

### 飞书配置获取

#### 获取 App ID 和 App Secret
1. 在飞书开放平台的应用详情页面可以找到
2. App ID 格式：`cli_xxxxxxxxx`
3. App Secret 格式：长字符串

#### 获取 Base ID 和 Table ID
1. 打开飞书多维表格
2. 在浏览器地址栏中可以看到：
   ```
   https://example.feishu.cn/base/BaseId?table=TableId
   ```
3. `BaseId` 就是 BASE_ID
4. `TableId` 就是 TABLE_ID

### 权限配置

在飞书开放平台的应用管理中，需要开启以下权限：

- `bitable:record:read` - 读取多维表格记录

## API 接口

### 获取文章列表
```
GET /api/articles
```

返回格式：
```json
{
  "code": 0,
  "data": [
    {
      "id": "record_id",
      "title": "文章标题",
      "quote": "精选金句",
      "review": "黄叔点评",
      "content": "文章内容",
      "preview": "内容预览"
    }
  ],
  "message": "success"
}
```

### 刷新缓存
```
GET /api/refresh
```

返回格式：
```json
{
  "code": 0,
  "message": "缓存已刷新",
  "count": 10
}
```

## 部署说明

### 生产环境部署

1. 设置环境变量：
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
```

2. 使用 Gunicorn 运行：
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker 部署

创建 `Dockerfile`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建和运行：
```bash
docker build -t feishu-blog .
docker run -p 5000:5000 --env-file .env feishu-blog
```

## 常见问题

### 1. 数据显示异常

**问题**：页面显示空白或数据加载失败

**解决方案**：
- 检查飞书应用权限是否正确开启
- 验证 App ID 和 App Secret 是否正确
- 确认多维表格的字段名称与代码中完全一致
- 检查表格中是否有数据

### 2. 权限错误

**问题**：API 返回权限不足错误

**解决方案**：
- 确认已开启 `bitable:record:read` 权限
- 检查应用是否已发布
- 验证 Base ID 和 Table ID 是否正确

### 3. 样式显示问题

**问题**：页面样式异常或布局错乱

**解决方案**：
- 确保所有模板文件都在 `templates` 目录下
- 检查浏览器是否支持现代 CSS 特性
- 清除浏览器缓存

### 4. 性能问题

**问题**：页面加载缓慢

**解决方案**：
- 调整缓存时间（CACHE_TIMEOUT）
- 减少单页显示的文章数量
- 优化图片和静态资源

## 开发指南

### 本地开发

1. 启用调试模式：
```python
app.run(debug=True)
```

2. 修改代码后自动重载
3. 详细的错误信息显示

### 自定义样式

1. 修改 `templates/base.html` 中的 CSS 变量
2. 在各页面模板中添加自定义样式
3. 创建独立的 CSS 文件放在 `static/css/` 目录

### 扩展功能

1. **添加分类功能**：在多维表格中添加分类字段
2. **实现搜索功能**：添加搜索接口和前端搜索框
3. **添加评论系统**：集成第三方评论服务
4. **优化移动端**：进一步优化移动端体验

## 注意事项

### 数据安全
- 不要在代码中直接硬编码飞书应用凭证
- 使用环境变量管理敏感信息
- 定期更新 App Secret

### 性能优化
- 合理设置缓存时间
- 避免频繁调用飞书 API
- 优化图片和静态资源加载

### 错误处理
- 实现完善的错误处理机制
- 记录详细的错误日志
- 提供友好的错误页面

## 更新日志

### v1.0.0 (2025-01-31)
- 初始版本发布
- 基础博客功能实现
- 飞书多维表格集成
- 深色科技风格设计
- 响应式布局支持

## 许可证

MIT License

## 联系方式

如需帮助或报告问题，请提供以下信息：
1. 完整的错误信息
2. 飞书应用配置截图（隐藏敏感信息）
3. 多维表格的结构说明
4. 浏览器和操作系统信息

---

**享受使用飞书博客网站！** 🚀