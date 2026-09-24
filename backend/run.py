"""
LaTeX 速成训练器 - 应用入口文件
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app import create_app
from flask import request

# 根据环境变量选择配置
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

# 添加健康检查端点
@app.route('/api/health')
def health_check():
    return {'status': 'healthy', 'message': 'LaTeX Speed Trainer API is running'}


# 添加环境变量检查端点 - 用于排查部署配置，不输出任何密钥明文
@app.route('/api/env-check')
def env_check():
    uri = os.environ.get('MONGODB_URI', '')
    if uri.startswith('mongodb+srv://'):
        uri_prefix = 'mongodb+srv://***'
    elif uri.startswith('mongodb://'):
        uri_prefix = 'mongodb://***'
    elif uri:
        uri_prefix = 'UNKNOWN_FORMAT'
    else:
        uri_prefix = 'NOT SET'

    def is_set(name):
        return 'SET' if os.environ.get(name) else 'NOT SET'

    return {
        'environment_variables': {
            'FLASK_ENV': os.environ.get('FLASK_ENV', 'NOT SET'),
            'FLASK_DEBUG': os.environ.get('FLASK_DEBUG', 'NOT SET'),
            'FLASK_HOST': os.environ.get('FLASK_HOST', 'NOT SET'),
            'FLASK_PORT': os.environ.get('FLASK_PORT', 'NOT SET'),
            'MONGODB_URI_PREFIX': uri_prefix,
            'MONGODB_DB': os.environ.get('MONGODB_DB', 'NOT SET'),
            'CORS_ORIGINS': os.environ.get('CORS_ORIGINS', 'NOT SET'),
            'OAUTH_REDIRECT_URI': os.environ.get('OAUTH_REDIRECT_URI', 'NOT SET'),
            'SECRET_KEY': is_set('SECRET_KEY'),
            'JWT_SECRET_KEY': is_set('JWT_SECRET_KEY'),
            'ADMIN_PASSWORD': is_set('ADMIN_PASSWORD'),
            'GITHUB_CLIENT_ID': is_set('GITHUB_CLIENT_ID'),
            'GITHUB_CLIENT_SECRET': is_set('GITHUB_CLIENT_SECRET'),
            'INIT_DB_SECRET': is_set('INIT_DB_SECRET'),
            'DEV_RESET_SECRET': is_set('DEV_RESET_SECRET')
        },
        'config_loaded': app.config.get('MONGODB_URI') is not None
    }

# 添加数据库初始化端点
@app.route('/api/init-db')
def init_database():
    """初始化数据库 - 仅在生产环境首次部署时使用

    安全限制：
    1. 需要特定的初始化密钥
    2. 只允许在数据库为空时使用
    3. 有操作日志记录
    """
    # 安全检查：需要初始化密钥
    init_key = request.args.get('init_key', '')
    expected_key = os.getenv('INIT_DB_SECRET', '')

    if not expected_key:
        return {
            'error': 'Database initialization is disabled',
            'message': 'INIT_DB_SECRET environment variable is not set'
        }, 403

    if init_key != expected_key:
        return {
            'error': 'Invalid initialization key',
            'message': 'Please provide valid init_key parameter'
        }, 401

    # 检查数据库是否已有数据（防止意外重置）
    try:
        from app import get_db
        db = get_db()
        lesson_count = db.lessons.count_documents({})
        user_count = db.users.count_documents({})

        if lesson_count > 0 or user_count > 0:
            return {
                'error': 'Database already contains data',
                'message': f'Found {lesson_count} lessons and {user_count} users. Use reset-db for development or manual scripts for production.',
                'lesson_count': lesson_count,
                'user_count': user_count
            }, 409
    except Exception as e:
        return {'error': f'Database check failed: {str(e)}'}, 500

    try:
        from app import get_db
        from app.services.bank import seed_database

        result = seed_database(get_db(), reset=False)

        return {
            'message': 'Database initialized successfully',
            'lesson_count': result['lesson_count'],
            'practice_count': result['practice_count'],
            'translation_count': result['translation_count'],
            'admin_credentials': result['admin_credentials']
        }

    except Exception as e:
        return {'error': f'Database initialization failed: {str(e)}'}, 500

# 添加强制重新初始化端点 - 仅限开发环境
@app.route('/api/reset-db')
def reset_database():
    """强制重新初始化数据库 - 使用 data/latex_bank.json 中的完整课程数据

    安全限制：
    1. 仅在开发环境启用
    2. 生产环境直接拒绝访问
    3. 需要特定的开发环境标识
    """
    # 检查环境变量
    env = os.getenv('FLASK_ENV', 'production')
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    dev_secret = os.getenv('DEV_RESET_SECRET', '')

    # 生产环境直接拒绝
    if env == 'production' or not debug_mode:
        return {
            'error': 'Database reset is disabled in production environment',
            'message': 'This endpoint is only available in development mode'
        }, 403

    # 开发环境也需要特殊密钥（可选的额外保护）
    reset_key = request.args.get('dev_key', '')
    if dev_secret and reset_key != dev_secret:
        return {
            'error': 'Invalid development key',
            'message': 'Please provide valid dev_key parameter'
        }, 401

    try:
        from app import get_db
        from app.services.bank import seed_database

        db = get_db()
        if db is None:
            return {'error': 'Database connection failed'}, 500

        result = seed_database(db, reset=True)

        return {
            'message': 'Database reset with comprehensive lessons and translations successfully',
            'lesson_count': result['lesson_count'],
            'practice_count': result['practice_count'],
            'translation_count': result['translation_count'],
            'admin_created': True,
            'admin_credentials': result['admin_credentials']
        }

    except Exception as e:
        return {'error': f'Database reset failed: {str(e)}'}, 500

if __name__ == '__main__':
    # 从环境变量获取配置，默认为开发模式
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')  # 监听所有网络接口
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"Starting LaTeX Speed Trainer API server...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Debug mode: {debug}")
    print(f"Server: http://{host}:{port}")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
