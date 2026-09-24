"""
管理后台路由模块
"""
from flask import Blueprint, request, session, redirect, url_for, flash, render_template_string, jsonify
from bson import ObjectId
from datetime import datetime
import json
from .auth import admin_required, verify_admin_password, get_current_admin
from app.models.admin import Admin
from app import get_db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    """管理后台首页"""
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """管理员登录"""
    if request.method == 'POST':
        password = request.form.get('password')
        is_valid, admin = verify_admin_password(password)
        if is_valid:
            session['admin_logged_in'] = True
            session['admin_id'] = str(admin._id)
            flash('登录成功！', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('密码错误！', 'error')
    
    # 简单的登录表单HTML
    login_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>管理后台登录</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 50px; }
            .login-container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
            .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%; }
            .btn:hover { background: #0056b3; }
            .alert { padding: 10px; margin-bottom: 20px; border-radius: 4px; }
            .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
            .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            h2 { text-align: center; color: #333; margin-bottom: 30px; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 4px; margin-bottom: 20px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h2>LaTeX训练器管理后台</h2>
            
            <div class="info">
                <strong>默认密码：</strong> admin123
            </div>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'error' if category == 'error' else 'success' }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="post">
                <div class="form-group">
                    <label for="password">管理员密码：</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit" class="btn">登录</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return render_template_string(login_html)


@admin_bp.route('/logout')
def logout():
    """管理员登出"""
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    flash('已退出登录', 'success')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """管理后台仪表板"""
    db = get_db()
    
    # 统计数据
    stats = {
        'total_users': db.users.count_documents({}),
        'total_lessons': db.lessons.count_documents({}),
        'total_practice_records': db.practice_records.count_documents({}),
        'total_reviews': db.reviews.count_documents({})
    }
    
    # 最近注册的用户
    recent_users = list(db.users.find({}).sort('created_at', -1).limit(5))
    
    dashboard_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>管理后台仪表板</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>
        
        <div class="container mt-4">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <h1>管理后台仪表板</h1>
            
            <div class="row mt-4">
                <div class="col-md-3">
                    <div class="card text-white bg-primary">
                        <div class="card-body">
                            <h5 class="card-title">总用户数</h5>
                            <h2>{{ stats.total_users }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-white bg-success">
                        <div class="card-body">
                            <h5 class="card-title">总课程数</h5>
                            <h2>{{ stats.total_lessons }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-white bg-info">
                        <div class="card-body">
                            <h5 class="card-title">练习记录</h5>
                            <h2>{{ stats.total_practice_records }}</h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card text-white bg-warning">
                        <div class="card-body">
                            <h5 class="card-title">复习记录</h5>
                            <h2>{{ stats.total_reviews }}</h2>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>系统管理</h5>
                        </div>
                        <div class="card-body">
                            <button id="updateLessonsBtn" class="btn btn-success mb-2" onclick="updateLessons()">
                               📚 更新课程数据
                            </button><br>
                            <a href="/admin/reset-database" class="btn btn-danger mb-2"
                               onclick="return confirm('确定要重置整个数据库吗？这将删除所有数据！')">
                               🔄 重置数据库
                            </a><br>
                            <a href="/admin/reset-users" class="btn btn-warning mb-2"
                               onclick="return confirm('确定要重置所有用户学习数据吗？')">
                               👥 重置用户学习数据
                            </a><br>
                            <a href="/admin/users" class="btn btn-primary mb-2">👤 用户管理</a><br>
                            <a href="/admin/lessons" class="btn btn-success mb-2">📚 课程管理</a><br>
                            <a href="/admin/translations/import" class="btn btn-info mb-2">🌐 导入翻译数据</a><br>
                            <a href="/admin/change-password" class="btn btn-secondary mb-2">🔑 修改密码</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5>最近注册用户</h5>
                        </div>
                        <div class="card-body">
                            {% if recent_users %}
                                <ul class="list-group list-group-flush">
                                    {% for user in recent_users %}
                                    <li class="list-group-item d-flex justify-content-between">
                                        <span>{{ user.email }}</span>
                                        <small class="text-muted">{{ user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A' }}</small>
                                    </li>
                                    {% endfor %}
                                </ul>
                            {% else %}
                                <p class="text-muted">暂无用户</p>
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 课程更新状态模态框 -->
        <div class="modal fade" id="updateModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">课程数据更新</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="updateStatus">
                            <div class="text-center">
                                <div class="spinner-border" role="status">
                                    <span class="visually-hidden">更新中...</span>
                                </div>
                                <p class="mt-2">正在更新课程数据，请稍候...</p>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" id="closeModalBtn" style="display:none;">关闭</button>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
        // 课程更新功能
        async function updateLessons() {
            // 显示确认对话框
            if (!confirm('确定要更新课程数据吗？\\n\\n这将使用最新的课程内容覆盖数据库中的现有课程。')) {
                return;
            }

            // 显示更新模态框
            const modal = new bootstrap.Modal(document.getElementById('updateModal'));
            modal.show();

            // 禁用更新按钮
            const updateBtn = document.getElementById('updateLessonsBtn');
            updateBtn.disabled = true;
            updateBtn.innerHTML = '🔄 更新中...';

            try {
                const response = await fetch('/admin/update-lessons', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const result = await response.json();

                if (result.success) {
                    const updateResult = result.update_result;
                    let detailsHtml = '';

                    if (updateResult.updated_lessons.length > 0) {
                        detailsHtml += `<p><strong>📝 更新的课程 (${updateResult.updated_lessons.length})：</strong></p><ul>`;
                        updateResult.updated_lessons.forEach(lesson => {
                            detailsHtml += `<li>第${lesson.sequence}课：${lesson.title}</li>`;
                        });
                        detailsHtml += '</ul>';
                    }

                    if (updateResult.new_lessons.length > 0) {
                        detailsHtml += `<p><strong>🆕 新增的课程 (${updateResult.new_lessons.length})：</strong></p><ul>`;
                        updateResult.new_lessons.forEach(lesson => {
                            detailsHtml += `<li>第${lesson.sequence}课：${lesson.title}</li>`;
                        });
                        detailsHtml += '</ul>';
                    }

                    if (updateResult.unchanged_lessons.length > 0) {
                        detailsHtml += `<p><strong>✅ 无变化的课程：</strong> ${updateResult.unchanged_lessons.length} 个</p>`;
                    }

                    if (updateResult.errors.length > 0) {
                        detailsHtml += `<p><strong>⚠️ 错误：</strong></p><ul>`;
                        updateResult.errors.forEach(error => {
                            const title = error.title || error.sequence || 'Unknown';
                            const errorMsg = error.error || error.general_error || 'Unknown error';
                            detailsHtml += `<li>${title}: ${errorMsg}</li>`;
                        });
                        detailsHtml += '</ul>';
                    }

                    document.getElementById('updateStatus').innerHTML = `
                        <div class="alert alert-success">
                            <h6>✅ 增量更新成功！</h6>
                            <p><strong>源课程总数：</strong> ${updateResult.total_source_lessons}</p>
                            <p><strong>更新时间：</strong> ${new Date(result.timestamp).toLocaleString()}</p>
                            ${detailsHtml}
                        </div>
                    `;
                } else {
                    document.getElementById('updateStatus').innerHTML = `
                        <div class="alert alert-danger">
                            <h6>❌ 更新失败</h6>
                            <p>${result.message}</p>
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('updateStatus').innerHTML = `
                    <div class="alert alert-danger">
                        <h6>❌ 更新失败</h6>
                        <p>网络错误：${error.message}</p>
                    </div>
                `;
            } finally {
                // 恢复更新按钮
                updateBtn.disabled = false;
                updateBtn.innerHTML = '📚 更新课程数据';

                // 显示关闭按钮
                document.getElementById('closeModalBtn').style.display = 'block';

                // 3秒后自动刷新页面
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            }
        }

        // 页面加载时检查课程更新状态
        document.addEventListener('DOMContentLoaded', async function() {
            try {
                const response = await fetch('/admin/update-lessons-status');
                const result = await response.json();

                if (result.success && result.needs_update) {
                    const updateBtn = document.getElementById('updateLessonsBtn');
                    updateBtn.classList.remove('btn-success');
                    updateBtn.classList.add('btn-warning');
                    updateBtn.innerHTML = '📚 更新课程数据 (有新版本)';
                }
            } catch (error) {
                console.log('检查更新状态失败:', error);
            }
        });
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(dashboard_html, stats=stats, recent_users=recent_users)


@admin_bp.route('/reset-database')
@admin_required
def reset_database():
    """重置数据库"""
    try:
        # 导入重置函数
        from run import reset_database
        reset_database()
        flash('数据库重置成功！', 'success')
    except Exception as e:
        flash(f'数据库重置失败：{str(e)}', 'error')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/update-lessons', methods=['POST'])
@admin_required
def update_lessons():
    """智能增量更新课程数据"""
    try:
        db = get_db()

        # 从题库单一源头加载课程数据
        from app.services.bank import load_bank, lessons_zh, lessons_en

        bank = load_bank()
        lessons = lessons_zh(bank)
        lessons_en_US = lessons_en(bank)

        # 执行增量更新
        update_result = perform_incremental_update(db, lessons, lessons_en_US)

        # 记录操作日志
        admin = get_current_admin()
        log_entry = {
            'action': 'incremental_update_lessons',
            'admin_id': str(admin._id) if admin else 'unknown',
            'admin_username': admin.username if admin else 'unknown',
            'timestamp': datetime.utcnow(),
            'update_result': update_result,
            'success': True
        }
        db.admin_logs.insert_one(log_entry)

        return jsonify({
            'success': True,
            'message': '课程数据增量更新成功！',
            'update_result': update_result,
            'timestamp': datetime.utcnow().isoformat()
        }), 200

    except Exception as e:
        # 记录错误日志
        try:
            admin = get_current_admin()
            log_entry = {
                'action': 'incremental_update_lessons',
                'admin_id': str(admin._id) if admin else 'unknown',
                'admin_username': admin.username if admin else 'unknown',
                'timestamp': datetime.utcnow(),
                'error': str(e),
                'success': False
            }
            db.admin_logs.insert_one(log_entry)
        except:
            pass

        return jsonify({
            'success': False,
            'message': f'课程数据更新失败：{str(e)}'
        }), 500


def perform_incremental_update(db, source_lessons, source_lessons_en):
    """执行增量更新"""
    update_result = {
        'total_source_lessons': len(source_lessons),
        'updated_lessons': [],
        'new_lessons': [],
        'unchanged_lessons': [],
        'errors': []
    }

    try:
        # 获取当前数据库中的所有课程
        current_lessons = {lesson['sequence']: lesson for lesson in db.lessons.find({})}

        # 创建英文翻译映射
        en_translations = {}
        for lesson in source_lessons_en:
            if 'sequence' in lesson:
                en_translations[lesson['sequence']] = lesson

        for source_lesson in source_lessons:
            # 确保课程有sequence字段
            if 'sequence' not in source_lesson:
                update_result['errors'].append({
                    'title': source_lesson.get('title', 'Unknown Lesson'),
                    'error': 'Missing sequence field'
                })
                continue

            sequence = source_lesson['sequence']

            try:
                # 检查课程是否存在
                if sequence in current_lessons:
                    current_lesson = current_lessons[sequence]

                    # 比较课程内容是否有变化
                    if lesson_content_changed(current_lesson, source_lesson):
                        # 准备更新数据
                        update_data = prepare_lesson_update_data(source_lesson, en_translations.get(sequence))

                        # 更新课程
                        db.lessons.update_one(
                            {'sequence': sequence},
                            {'$set': update_data}
                        )

                        update_result['updated_lessons'].append({
                            'sequence': sequence,
                            'title': source_lesson['title']
                        })
                    else:
                        update_result['unchanged_lessons'].append({
                            'sequence': sequence,
                            'title': source_lesson['title']
                        })
                else:
                    # 新课程，直接插入
                    new_lesson_data = prepare_lesson_insert_data(source_lesson, en_translations.get(sequence))
                    db.lessons.insert_one(new_lesson_data)

                    update_result['new_lessons'].append({
                        'sequence': sequence,
                        'title': source_lesson['title']
                    })

            except Exception as e:
                update_result['errors'].append({
                    'sequence': sequence,
                    'title': source_lesson.get('title', 'Unknown'),
                    'error': str(e)
                })

        return update_result

    except Exception as e:
        update_result['errors'].append({
            'title': 'General Error',
            'error': str(e)
        })
        return update_result


def lesson_content_changed(current_lesson, source_lesson):
    """检查课程内容是否有变化"""
    # 比较关键字段
    fields_to_compare = ['title', 'description', 'cards']

    for field in fields_to_compare:
        if current_lesson.get(field) != source_lesson.get(field):
            return True

    return False


def prepare_lesson_update_data(source_lesson, en_translation=None):
    """准备课程更新数据"""
    update_data = {
        'title': source_lesson['title'],
        'description': source_lesson['description'],
        'cards': source_lesson['cards'],
        'updated_at': datetime.utcnow()
    }

    # 添加英文翻译
    if en_translation:
        update_data.update({
            'title_en': en_translation.get('title'),
            'description_en': en_translation.get('description'),
            'cards_en': en_translation.get('cards', [])
        })

    return update_data


def prepare_lesson_insert_data(source_lesson, en_translation=None):
    """准备新课程插入数据"""
    lesson_data = {
        '_id': ObjectId(),
        'title': source_lesson['title'],
        'sequence': source_lesson['sequence'],
        'description': source_lesson['description'],
        'cards': source_lesson['cards'],
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    # 添加英文翻译
    if en_translation:
        lesson_data.update({
            'title_en': en_translation.get('title'),
            'description_en': en_translation.get('description'),
            'cards_en': en_translation.get('cards', [])
        })

    return lesson_data


@admin_bp.route('/update-lessons-status')
@admin_required
def update_lessons_status():
    """获取课程更新状态信息"""
    try:
        db = get_db()

        # 获取当前课程统计
        current_stats = {
            'total_lessons': db.lessons.count_documents({}),
            'last_updated': None
        }

        # 查找最近的更新日志
        latest_log = db.admin_logs.find_one(
            {'action': {'$in': ['update_lessons', 'incremental_update_lessons']}, 'success': True},
            sort=[('timestamp', -1)]
        )

        if latest_log:
            current_stats['last_updated'] = latest_log['timestamp'].isoformat()

        # 获取源课程数据并检查是否需要更新
        try:
            from app.services.bank import load_bank, lessons_zh

            lessons = lessons_zh(load_bank())
            source_lesson_count = len(lessons)

            # 检查是否有课程内容变化
            needs_update = check_lessons_need_update(db, lessons)

        except Exception:
            source_lesson_count = 'unknown'
            needs_update = False

        return jsonify({
            'success': True,
            'current_stats': current_stats,
            'source_lesson_count': source_lesson_count,
            'needs_update': needs_update
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取状态失败：{str(e)}'
        }), 500


def check_lessons_need_update(db, source_lessons):
    """检查是否有课程需要更新"""
    try:
        # 获取当前数据库中的课程
        current_lessons = {lesson['sequence']: lesson for lesson in db.lessons.find({})}

        # 检查数量是否不同
        if len(current_lessons) != len(source_lessons):
            return True

        # 检查每个课程的内容
        for source_lesson in source_lessons:
            sequence = source_lesson['sequence']

            if sequence not in current_lessons:
                return True  # 有新课程

            if lesson_content_changed(current_lessons[sequence], source_lesson):
                return True  # 有内容变化

        return False

    except Exception:
        return False  # 检查失败时假设不需要更新


@admin_bp.route('/users')
@admin_required
def users():
    """用户管理页面"""
    db = get_db()

    # 获取所有用户
    users_list = list(db.users.find({}).sort('created_at', -1))

    # 计算每个用户的完成课程数
    for user in users_list:
        progress = user.get('progress', {})
        completed_lessons = progress.get('completed_lessons', [])
        user['completed_lessons_count'] = len(completed_lessons)

    users_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>用户管理</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <h1>用户管理</h1>

            <div class="card mt-3">
                <div class="card-header">
                    <h5>用户列表 (共 {{ users_list|length }} 个用户)</h5>
                </div>
                <div class="card-body">
                    {% if users_list %}
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>邮箱</th>
                                        <th>注册时间</th>
                                        <th>管理员</th>
                                        <th>完成课程数</th>
                                        <th>操作</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for user in users_list %}
                                    <tr>
                                        <td>{{ user.email }}</td>
                                        <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else 'N/A' }}</td>
                                        <td>
                                            {% if user.get('is_admin') %}
                                                <span class="badge bg-success">是</span>
                                            {% else %}
                                                <span class="badge bg-secondary">否</span>
                                            {% endif %}
                                        </td>
                                        <td>{{ user.completed_lessons_count }}</td>
                                        <td>
                                            <a href="/admin/users/{{ user._id }}/reset" class="btn btn-sm btn-warning"
                                               onclick="return confirm('确定要重置该用户的学习数据吗？')">
                                               重置学习数据
                                            </a>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">暂无用户</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(users_html, users_list=users_list)


@admin_bp.route('/users/<user_id>/reset')
@admin_required
def reset_user(user_id):
    """重置单个用户的学习数据"""
    try:
        db = get_db()

        # 重置用户的学习进度
        result = db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'progress': {
                        'current_lesson_id': None,
                        'completed_lessons': []
                    },
                    'practice_stats': {
                        'total_attempts': 0,
                        'correct_answers': 0,
                        'accuracy_rate': 0.0
                    }
                }
            }
        )

        if result.modified_count > 0:
            # 删除该用户的练习记录
            db.practice_records.delete_many({'user_id': user_id})

            # 删除该用户的复习记录
            db.reviews.delete_many({'user_id': user_id})

            flash('用户学习数据重置成功！', 'success')
        else:
            flash('用户不存在或数据未发生变化', 'warning')

    except Exception as e:
        flash(f'重置用户数据失败：{str(e)}', 'error')

    return redirect(url_for('admin.users'))


@admin_bp.route('/lessons')
@admin_required
def lessons():
    """课程管理页面"""
    db = get_db()

    # 获取所有课程
    lessons_list = list(db.lessons.find({}).sort('sequence', 1))

    # 计算每个课程的卡片数量和翻译状态
    for lesson in lessons_list:
        cards = lesson.get('cards', [])
        lesson['cards_count'] = len(cards)
        lesson['knowledge_count'] = sum(1 for card in cards if card.get('type') == 'knowledge')
        lesson['practice_count'] = sum(1 for card in cards if card.get('type') == 'practice')

        # 计算翻译完成状态
        lesson['has_chinese'] = bool(lesson.get('title') and lesson.get('description'))
        lesson['has_english'] = bool(lesson.get('title_en') and lesson.get('description_en'))
        lesson['has_english_cards'] = bool(lesson.get('cards_en'))

        # 计算翻译完成度
        translation_score = 0
        if lesson['has_chinese']:
            translation_score += 40  # 中文基础信息
        if lesson['has_english']:
            translation_score += 40  # 英文基础信息
        if lesson['has_english_cards']:
            translation_score += 20  # 英文卡片内容
        lesson['translation_percentage'] = translation_score

    lessons_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>课程管理</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <h1>课程管理</h1>

            <div class="card mt-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5>课程列表 (共 {{ lessons_list|length }} 个课程)</h5>
                    <a href="/admin/lessons/create" class="btn btn-primary">新建课程</a>
                </div>
                <div class="card-body">
                    {% if lessons_list %}
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>序号</th>
                                        <th>课程标题</th>
                                        <th>描述</th>
                                        <th>知识点</th>
                                        <th>练习题</th>
                                        <th>总卡片</th>
                                        <th>翻译状态</th>
                                        <th>操作</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for lesson in lessons_list %}
                                    <tr>
                                        <td>{{ lesson.sequence }}</td>
                                        <td>
                                            {{ lesson.title }}
                                            {% if lesson.title_en %}
                                                <br><small class="text-muted">{{ lesson.title_en }}</small>
                                            {% endif %}
                                        </td>
                                        <td>{{ lesson.description[:50] }}{% if lesson.description|length > 50 %}...{% endif %}</td>
                                        <td><span class="badge bg-info">{{ lesson.knowledge_count }}</span></td>
                                        <td><span class="badge bg-success">{{ lesson.practice_count }}</span></td>
                                        <td><span class="badge bg-primary">{{ lesson.cards_count }}</span></td>
                                        <td>
                                            <div class="d-flex align-items-center gap-1">
                                                <!-- 中文状态 -->
                                                {% if lesson.has_chinese %}
                                                    <span class="badge bg-success" title="中文版本完整">🇨🇳</span>
                                                {% else %}
                                                    <span class="badge bg-danger" title="中文版本缺失">🇨🇳</span>
                                                {% endif %}

                                                <!-- 英文状态 -->
                                                {% if lesson.has_english %}
                                                    <span class="badge bg-success" title="英文版本完整">🇺🇸</span>
                                                {% else %}
                                                    <span class="badge bg-secondary" title="英文版本缺失">🇺🇸</span>
                                                {% endif %}

                                                <!-- 翻译完成度 -->
                                                <small class="text-muted">{{ lesson.translation_percentage }}%</small>
                                            </div>
                                        </td>
                                        <td>
                                            <div class="btn-group" role="group">
                                                <a href="/admin/lessons/{{ lesson._id }}" class="btn btn-sm btn-info">查看</a>
                                                <button type="button" class="btn btn-sm btn-warning dropdown-toggle" data-bs-toggle="dropdown">
                                                    编辑
                                                </button>
                                                <ul class="dropdown-menu">
                                                    <li><a class="dropdown-item" href="/admin/lessons/{{ lesson._id }}/edit?lang=zh-CN">🇨🇳 编辑中文</a></li>
                                                    <li><a class="dropdown-item" href="/admin/lessons/{{ lesson._id }}/edit?lang=en-US">🇺🇸 编辑英文</a></li>
                                                </ul>
                                            </div>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">暂无课程</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(lessons_html, lessons_list=lessons_list)


@admin_bp.route('/lessons/<lesson_id>')
@admin_required
def lesson_detail(lesson_id):
    """课程详情页面"""
    db = get_db()

    # 获取课程详情
    lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})
    if not lesson:
        flash('课程不存在', 'error')
        return redirect(url_for('admin.lessons'))

    lesson_detail_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>课程详情 - {{ lesson.title }}</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .card-content { max-height: 200px; overflow-y: auto; }
            .json-content { font-family: monospace; font-size: 12px; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/lessons">课程管理</a>
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>课程详情</h1>
                <div>
                    <a href="/admin/lessons/{{ lesson._id }}/edit" class="btn btn-warning">编辑课程</a>
                    <a href="/admin/lessons" class="btn btn-secondary">返回列表</a>
                </div>
            </div>

            <div class="card mt-3">
                <div class="card-header">
                    <h5>基本信息</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>序号：</strong>{{ lesson.sequence }}</p>
                            <p><strong>标题：</strong>{{ lesson.title }}</p>
                            <p><strong>描述：</strong>{{ lesson.description }}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>创建时间：</strong>{{ lesson.created_at.strftime('%Y-%m-%d %H:%M') if lesson.created_at else 'N/A' }}</p>
                            <p><strong>卡片总数：</strong>{{ lesson.cards|length }}</p>
                            <p><strong>知识点：</strong>{{ lesson.cards|selectattr('type', 'equalto', 'knowledge')|list|length }}</p>
                            <p><strong>练习题：</strong>{{ lesson.cards|selectattr('type', 'equalto', 'practice')|list|length }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card mt-3">
                <div class="card-header">
                    <h5>课程卡片 ({{ lesson.cards|length }} 个)</h5>
                </div>
                <div class="card-body">
                    {% if lesson.cards %}
                        {% for card in lesson.cards %}
                        <div class="card mb-3 {% if card.type == 'knowledge' %}border-info{% else %}border-success{% endif %}">
                            <div class="card-header d-flex justify-content-between">
                                <span>
                                    <strong>卡片 {{ loop.index }}</strong> -
                                    {% if card.type == 'knowledge' %}
                                        <span class="badge bg-info">知识点</span>
                                    {% else %}
                                        <span class="badge bg-success">练习题</span>
                                    {% endif %}
                                </span>
                                <small class="text-muted">{{ card.type }}</small>
                            </div>
                            <div class="card-body">
                                {% if card.type == 'knowledge' %}
                                    {% if card.get('title') %}
                                        <h6>{{ card.title }}</h6>
                                    {% endif %}
                                    {% if card.get('content') %}
                                        <div class="card-content">
                                            <pre>{{ card.content }}</pre>
                                        </div>
                                    {% endif %}
                                    {% if card.get('titleKey') or card.get('contentKey') %}
                                        <small class="text-muted">
                                            翻译键: {{ card.get('titleKey', '') }} / {{ card.get('contentKey', '') }}
                                        </small>
                                    {% endif %}
                                {% else %}
                                    <p><strong>问题：</strong>{{ card.get('question', 'N/A') }}</p>
                                    <p><strong>答案：</strong><code>{{ card.get('target_formula', 'N/A') }}</code></p>
                                    <p><strong>难度：</strong>{{ card.get('difficulty', 'N/A') }}</p>
                                    {% if card.get('hints') %}
                                        <p><strong>提示：</strong></p>
                                        <ul>
                                            {% for hint in card.hints %}
                                                <li>{{ hint }}</li>
                                            {% endfor %}
                                        </ul>
                                    {% endif %}
                                {% endif %}
                            </div>
                        </div>
                        {% endfor %}
                    {% else %}
                        <p class="text-muted">该课程暂无卡片</p>
                    {% endif %}
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(lesson_detail_html, lesson=lesson)


@admin_bp.route('/lessons/<lesson_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_lesson(lesson_id):
    """编辑课程"""
    db = get_db()

    # 获取课程详情
    lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})
    if not lesson:
        flash('课程不存在', 'error')
        return redirect(url_for('admin.lessons'))

    # 获取当前编辑的语言，默认为中文
    current_lang = request.args.get('lang', 'zh-CN')

    if request.method == 'POST':
        try:
            # 获取表单数据
            title = request.form.get('title', '').strip()
            sequence = request.form.get('sequence', type=int)
            description = request.form.get('description', '').strip()
            edit_lang = request.form.get('edit_lang', 'zh-CN')

            if not title or not sequence or not description:
                flash('请填写所有必填字段', 'error')
                return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id, lang=edit_lang))

            # 根据编辑的语言更新对应字段
            update_data = {'sequence': sequence}

            if edit_lang == 'en-US':
                update_data['title_en'] = title
                update_data['description_en'] = description
            else:
                update_data['title'] = title
                update_data['description'] = description

            # 更新课程基本信息
            result = db.lessons.update_one(
                {'_id': ObjectId(lesson_id)},
                {'$set': update_data}
            )

            if result.modified_count > 0:
                flash(f'课程{"英文" if edit_lang == "en-US" else "中文"}版本更新成功！', 'success')
            else:
                flash('课程数据未发生变化', 'info')

            return redirect(url_for('admin.lesson_detail', lesson_id=lesson_id))

        except Exception as e:
            flash(f'更新课程失败：{str(e)}', 'error')

    edit_lesson_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>编辑课程 - {{ lesson.title }}</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/lessons">课程管理</a>
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>编辑课程 - 多语言版本</h1>
                <div class="d-flex gap-2">
                    <div class="btn-group" role="group">
                        <a href="/admin/lessons/{{ lesson._id }}/edit?lang=zh-CN"
                           class="btn btn-outline-primary {{ 'active' if current_lang == 'zh-CN' else '' }}">
                            🇨🇳 中文
                        </a>
                        <a href="/admin/lessons/{{ lesson._id }}/edit?lang=en-US"
                           class="btn btn-outline-primary {{ 'active' if current_lang == 'en-US' else '' }}">
                            🇺🇸 English
                        </a>
                    </div>
                    <a href="/admin/lessons/{{ lesson._id }}" class="btn btn-info">查看详情</a>
                    <a href="/admin/lessons" class="btn btn-secondary">返回列表</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' if category == 'success' else 'info' }} alert-dismissible fade show mt-3">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <!-- 语言选择标签页 -->
            <div class="card mt-3">
                <div class="card-header">
                    <ul class="nav nav-tabs card-header-tabs" id="languageTabs" role="tablist">
                        <li class="nav-item" role="presentation">
                            <button class="nav-link {{ 'active' if current_lang == 'zh-CN' else '' }}"
                                    id="zh-tab" data-bs-toggle="tab" data-bs-target="#zh-content"
                                    type="button" role="tab">
                                🇨🇳 中文版本
                                {% if lesson.title %}
                                    <span class="badge bg-success ms-1">✓</span>
                                {% else %}
                                    <span class="badge bg-warning ms-1">!</span>
                                {% endif %}
                            </button>
                        </li>
                        <li class="nav-item" role="presentation">
                            <button class="nav-link {{ 'active' if current_lang == 'en-US' else '' }}"
                                    id="en-tab" data-bs-toggle="tab" data-bs-target="#en-content"
                                    type="button" role="tab">
                                🇺🇸 英文版本
                                {% if lesson.title_en %}
                                    <span class="badge bg-success ms-1">✓</span>
                                {% else %}
                                    <span class="badge bg-secondary ms-1">-</span>
                                {% endif %}
                            </button>
                        </li>
                    </ul>
                </div>
                <div class="card-body">
                    <div class="tab-content" id="languageTabContent">
                        <!-- 中文版本 -->
                        <div class="tab-pane fade {{ 'show active' if current_lang == 'zh-CN' else '' }}"
                             id="zh-content" role="tabpanel">
                            <form method="post">
                                <input type="hidden" name="edit_lang" value="zh-CN">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="title_zh" class="form-label">课程标题 (中文) *</label>
                                            <input type="text" class="form-control" id="title_zh" name="title"
                                                   value="{{ lesson.title or '' }}" required>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="sequence_zh" class="form-label">课程序号 *</label>
                                            <input type="number" class="form-control" id="sequence_zh" name="sequence"
                                                   value="{{ lesson.sequence }}" min="1" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="description_zh" class="form-label">课程描述 (中文) *</label>
                                    <textarea class="form-control" id="description_zh" name="description"
                                              rows="3" required>{{ lesson.description or '' }}</textarea>
                                </div>
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-primary">保存中文版本</button>
                                    <a href="/admin/lessons/{{ lesson._id }}" class="btn btn-secondary">取消</a>
                                </div>
                            </form>
                        </div>

                        <!-- 英文版本 -->
                        <div class="tab-pane fade {{ 'show active' if current_lang == 'en-US' else '' }}"
                             id="en-content" role="tabpanel">
                            <form method="post">
                                <input type="hidden" name="edit_lang" value="en-US">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="title_en" class="form-label">Course Title (English) *</label>
                                            <input type="text" class="form-control" id="title_en" name="title"
                                                   value="{{ lesson.title_en or '' }}" required>
                                            {% if lesson.title %}
                                                <div class="form-text text-muted">
                                                    <small>中文参考: {{ lesson.title }}</small>
                                                </div>
                                            {% endif %}
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label for="sequence_en" class="form-label">Course Sequence *</label>
                                            <input type="number" class="form-control" id="sequence_en" name="sequence"
                                                   value="{{ lesson.sequence }}" min="1" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="description_en" class="form-label">Course Description (English) *</label>
                                    <textarea class="form-control" id="description_en" name="description"
                                              rows="3" required>{{ lesson.description_en or '' }}</textarea>
                                    {% if lesson.description %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {{ lesson.description }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-primary">Save English Version</button>
                                    <a href="/admin/lessons/{{ lesson._id }}" class="btn btn-secondary">Cancel</a>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card mt-3">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5>{{ '课程卡片管理' if current_lang == 'zh-CN' else 'Course Cards Management' }}</h5>
                    <div class="d-flex gap-2">
                        <div class="btn-group" role="group">
                            <a href="/admin/lessons/{{ lesson._id }}/cards/create?lang=zh-CN"
                               class="btn btn-outline-primary btn-sm">
                                🇨🇳 {{ '新增中文卡片' if current_lang == 'zh-CN' else 'Add Chinese Card' }}
                            </a>
                            <a href="/admin/lessons/{{ lesson._id }}/cards/create?lang=en-US"
                               class="btn btn-outline-primary btn-sm">
                                🇺🇸 {{ '新增英文卡片' if current_lang == 'zh-CN' else 'Add English Card' }}
                            </a>
                        </div>
                        <a href="/admin/lessons/{{ lesson._id }}/cards/create" class="btn btn-success btn-sm">
                            {{ '新增卡片' if current_lang == 'zh-CN' else 'Add Card' }}
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    {% if lesson.cards %}
                        <div class="table-responsive">
                            <table class="table table-striped">
                                <thead>
                                    <tr>
                                        <th>{{ '序号' if current_lang == 'zh-CN' else 'No.' }}</th>
                                        <th>{{ '类型' if current_lang == 'zh-CN' else 'Type' }}</th>
                                        <th>{{ '内容预览' if current_lang == 'zh-CN' else 'Content Preview' }}</th>
                                        <th>{{ '翻译状态' if current_lang == 'zh-CN' else 'Translation Status' }}</th>
                                        <th>{{ '操作' if current_lang == 'zh-CN' else 'Actions' }}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for card in lesson.cards %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td>
                                            {% if card.type == 'knowledge' %}
                                                <span class="badge bg-info">{{ '知识点' if current_lang == 'zh-CN' else 'Knowledge' }}</span>
                                            {% else %}
                                                <span class="badge bg-success">{{ '练习题' if current_lang == 'zh-CN' else 'Exercise' }}</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            {% if current_lang == 'zh-CN' %}
                                                {% if card.type == 'knowledge' %}
                                                    {{ (card.get('title') or card.get('content', ''))[:50] }}
                                                {% else %}
                                                    {{ card.get('question', '')[:50] }}
                                                {% endif %}
                                                {% if card.get('title_en') or card.get('content_en') or card.get('question_en') %}
                                                    <br><small class="text-muted">
                                                        {% if card.type == 'knowledge' %}
                                                            {{ (card.get('title_en') or card.get('content_en', ''))[:50] }}
                                                        {% else %}
                                                            {{ card.get('question_en', '')[:50] }}
                                                        {% endif %}
                                                    </small>
                                                {% endif %}
                                            {% else %}
                                                {% if card.type == 'knowledge' %}
                                                    {{ (card.get('title_en') or card.get('content_en', ''))[:50] }}
                                                {% else %}
                                                    {{ card.get('question_en', '')[:50] }}
                                                {% endif %}
                                                {% if card.get('title') or card.get('content') or card.get('question') %}
                                                    <br><small class="text-muted">
                                                        {% if card.type == 'knowledge' %}
                                                            {{ (card.get('title') or card.get('content', ''))[:50] }}
                                                        {% else %}
                                                            {{ card.get('question', '')[:50] }}
                                                        {% endif %}
                                                    </small>
                                                {% endif %}
                                            {% endif %}
                                        </td>
                                        <td>
                                            <div class="d-flex align-items-center gap-1">
                                                <!-- 中文状态 -->
                                                {% if card.type == 'knowledge' %}
                                                    {% set has_chinese = card.get('title') or card.get('content') %}
                                                    {% set has_english = card.get('title_en') or card.get('content_en') %}
                                                {% else %}
                                                    {% set has_chinese = card.get('question') %}
                                                    {% set has_english = card.get('question_en') %}
                                                {% endif %}

                                                {% if has_chinese %}
                                                    <span class="badge bg-success" title="{{ '中文版本完整' if current_lang == 'zh-CN' else 'Chinese version complete' }}">🇨🇳</span>
                                                {% else %}
                                                    <span class="badge bg-danger" title="{{ '中文版本缺失' if current_lang == 'zh-CN' else 'Chinese version missing' }}">🇨🇳</span>
                                                {% endif %}

                                                <!-- 英文状态 -->
                                                {% if has_english %}
                                                    <span class="badge bg-success" title="{{ '英文版本完整' if current_lang == 'zh-CN' else 'English version complete' }}">🇺🇸</span>
                                                {% else %}
                                                    <span class="badge bg-secondary" title="{{ '英文版本缺失' if current_lang == 'zh-CN' else 'English version missing' }}">🇺🇸</span>
                                                {% endif %}
                                            </div>
                                        </td>
                                        <td>
                                            <div class="btn-group" role="group">
                                                <button type="button" class="btn btn-sm btn-warning dropdown-toggle" data-bs-toggle="dropdown">
                                                    {{ '编辑' if current_lang == 'zh-CN' else 'Edit' }}
                                                </button>
                                                <ul class="dropdown-menu">
                                                    <li><a class="dropdown-item" href="/admin/lessons/{{ lesson._id }}/cards/{{ loop.index0 }}/edit?lang=zh-CN">🇨🇳 {{ '编辑中文' if current_lang == 'zh-CN' else 'Edit Chinese' }}</a></li>
                                                    <li><a class="dropdown-item" href="/admin/lessons/{{ lesson._id }}/cards/{{ loop.index0 }}/edit?lang=en-US">🇺🇸 {{ '编辑英文' if current_lang == 'zh-CN' else 'Edit English' }}</a></li>
                                                    <li><hr class="dropdown-divider"></li>
                                                    <li><a class="dropdown-item" href="/admin/lessons/{{ lesson._id }}/cards/{{ loop.index0 }}/edit">{{ '编辑全部' if current_lang == 'zh-CN' else 'Edit All' }}</a></li>
                                                </ul>
                                            </div>
                                            <a href="/admin/lessons/{{ lesson._id }}/cards/{{ loop.index0 }}/delete"
                                               class="btn btn-sm btn-danger ms-1"
                                               onclick="return confirm('{{ '确定要删除这个卡片吗？' if current_lang == 'zh-CN' else 'Are you sure you want to delete this card?' }}')">
                                               {{ '删除' if current_lang == 'zh-CN' else 'Delete' }}
                                            </a>
                                        </td>
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p class="text-muted">
                            {{ '该课程暂无卡片，' if current_lang == 'zh-CN' else 'No cards in this course, ' }}
                            <a href="/admin/lessons/{{ lesson._id }}/cards/create">{{ '点击新增' if current_lang == 'zh-CN' else 'click to add' }}</a>
                        </p>
                    {% endif %}
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 处理标签页切换
            document.addEventListener('DOMContentLoaded', function() {
                const urlParams = new URLSearchParams(window.location.search);
                const lang = urlParams.get('lang') || 'zh-CN';

                // 激活对应的标签页
                if (lang === 'en-US') {
                    document.getElementById('en-tab').click();
                } else {
                    document.getElementById('zh-tab').click();
                }
            });
        </script>
    </body>
    </html>
    '''

    return render_template_string(edit_lesson_html, lesson=lesson, current_lang=current_lang)


@admin_bp.route('/lessons/create', methods=['GET', 'POST'])
@admin_required
def create_lesson():
    """新建课程"""
    db = get_db()

    if request.method == 'POST':
        try:
            # 获取表单数据
            title = request.form.get('title', '').strip()
            sequence = request.form.get('sequence', type=int)
            description = request.form.get('description', '').strip()

            if not title or not sequence or not description:
                flash('请填写所有必填字段', 'error')
                return redirect(url_for('admin.create_lesson'))

            # 检查序号是否已存在
            existing_lesson = db.lessons.find_one({'sequence': sequence})
            if existing_lesson:
                flash(f'序号 {sequence} 已被课程 "{existing_lesson["title"]}" 使用', 'error')
                return redirect(url_for('admin.create_lesson'))

            # 创建新课程
            new_lesson = {
                'title': title,
                'sequence': sequence,
                'description': description,
                'cards': [],
                'created_at': datetime.utcnow()
            }

            result = db.lessons.insert_one(new_lesson)

            if result.inserted_id:
                flash('课程创建成功！', 'success')
                return redirect(url_for('admin.lesson_detail', lesson_id=str(result.inserted_id)))
            else:
                flash('课程创建失败', 'error')

        except Exception as e:
            flash(f'创建课程失败：{str(e)}', 'error')

    # 获取下一个可用的序号
    last_lesson = db.lessons.find_one({}, sort=[('sequence', -1)])
    next_sequence = (last_lesson['sequence'] + 1) if last_lesson else 1

    create_lesson_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>新建课程</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/lessons">课程管理</a>
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>新建课程</h1>
                <a href="/admin/lessons" class="btn btn-secondary">返回列表</a>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show mt-3">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="card mt-3">
                <div class="card-header">
                    <h5>课程信息</h5>
                </div>
                <div class="card-body">
                    <form method="post">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="title" class="form-label">课程标题 *</label>
                                    <input type="text" class="form-control" id="title" name="title"
                                           placeholder="例如：第1课：数学环境与基础语法" required>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="sequence" class="form-label">课程序号 *</label>
                                    <input type="number" class="form-control" id="sequence" name="sequence"
                                           value="{{ next_sequence }}" min="1" required>
                                    <div class="form-text">建议使用序号：{{ next_sequence }}</div>
                                </div>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">课程描述 *</label>
                            <textarea class="form-control" id="description" name="description"
                                      rows="3" placeholder="描述课程的主要内容和学习目标" required></textarea>
                        </div>
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">创建课程</button>
                            <a href="/admin/lessons" class="btn btn-secondary">取消</a>
                        </div>
                    </form>
                </div>
            </div>

            <div class="card mt-3">
                <div class="card-header">
                    <h5>💡 提示</h5>
                </div>
                <div class="card-body">
                    <ul>
                        <li>创建课程后，您可以为课程添加知识点卡片和练习题卡片</li>
                        <li>知识点卡片用于展示理论知识和示例</li>
                        <li>练习题卡片包含问题、答案和提示，用于用户练习</li>
                        <li>建议按照学习难度递增的顺序安排课程序号</li>
                    </ul>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(create_lesson_html, next_sequence=next_sequence)


@admin_bp.route('/lessons/<lesson_id>/cards/create', methods=['GET', 'POST'])
@admin_required
def create_card(lesson_id):
    """新增卡片"""
    db = get_db()

    # 获取课程
    lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})
    if not lesson:
        flash('课程不存在', 'error')
        return redirect(url_for('admin.lessons'))

    if request.method == 'POST':
        try:
            card_type = request.form.get('card_type')

            if card_type == 'knowledge':
                # 知识点卡片
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                title_key = request.form.get('title_key', '').strip()
                content_key = request.form.get('content_key', '').strip()

                new_card = {
                    'type': 'knowledge'
                }

                if title:
                    new_card['title'] = title
                if content:
                    new_card['content'] = content
                if title_key:
                    new_card['titleKey'] = title_key
                if content_key:
                    new_card['contentKey'] = content_key

            elif card_type == 'practice':
                # 练习题卡片
                question = request.form.get('question', '').strip()
                target_formula = request.form.get('target_formula', '').strip()
                difficulty = request.form.get('difficulty', 'easy')
                hints_text = request.form.get('hints', '').strip()

                if not question or not target_formula:
                    flash('练习题的问题和答案不能为空', 'error')
                    return redirect(url_for('admin.create_card', lesson_id=lesson_id))

                # 处理提示（每行一个提示）
                hints = [hint.strip() for hint in hints_text.split('\n') if hint.strip()]

                new_card = {
                    'type': 'practice',
                    'question': question,
                    'target_formula': target_formula,
                    'difficulty': difficulty,
                    'hints': hints
                }
            else:
                flash('无效的卡片类型', 'error')
                return redirect(url_for('admin.create_card', lesson_id=lesson_id))

            # 添加卡片到课程
            result = db.lessons.update_one(
                {'_id': ObjectId(lesson_id)},
                {'$push': {'cards': new_card}}
            )

            if result.modified_count > 0:
                flash('卡片添加成功！', 'success')
                return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id))
            else:
                flash('卡片添加失败', 'error')

        except Exception as e:
            flash(f'添加卡片失败：{str(e)}', 'error')

    create_card_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>新增卡片 - {{ lesson.title }}</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/lessons">课程管理</a>
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>新增卡片</h1>
                <div>
                    <a href="/admin/lessons/{{ lesson._id }}/edit" class="btn btn-secondary">返回编辑</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show mt-3">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="card mt-3">
                <div class="card-header">
                    <h5>课程：{{ lesson.title }}</h5>
                </div>
                <div class="card-body">
                    <form method="post" id="cardForm">
                        <div class="mb-3">
                            <label class="form-label">卡片类型 *</label>
                            <div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="card_type"
                                           id="knowledge" value="knowledge" checked onchange="toggleCardType()">
                                    <label class="form-check-label" for="knowledge">
                                        知识点卡片
                                    </label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" name="card_type"
                                           id="practice" value="practice" onchange="toggleCardType()">
                                    <label class="form-check-label" for="practice">
                                        练习题卡片
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- 知识点卡片表单 -->
                        <div id="knowledgeForm">
                            <div class="mb-3">
                                <label for="title" class="form-label">标题</label>
                                <input type="text" class="form-control" id="title" name="title"
                                       placeholder="知识点标题（可选）">
                            </div>
                            <div class="mb-3">
                                <label for="content" class="form-label">内容</label>
                                <textarea class="form-control" id="content" name="content"
                                          rows="6" placeholder="知识点内容，支持Markdown格式"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="title_key" class="form-label">标题翻译键</label>
                                <input type="text" class="form-control" id="title_key" name="title_key"
                                       placeholder="用于国际化的标题键（可选）">
                            </div>
                            <div class="mb-3">
                                <label for="content_key" class="form-label">内容翻译键</label>
                                <input type="text" class="form-control" id="content_key" name="content_key"
                                       placeholder="用于国际化的内容键（可选）">
                            </div>
                        </div>

                        <!-- 练习题卡片表单 -->
                        <div id="practiceForm" style="display: none;">
                            <div class="mb-3">
                                <label for="question" class="form-label">问题 *</label>
                                <input type="text" class="form-control" id="question" name="question"
                                       placeholder="例如：请输入 LaTeX 代码来表示：x 的平方">
                            </div>
                            <div class="mb-3">
                                <label for="target_formula" class="form-label">标准答案 *</label>
                                <input type="text" class="form-control" id="target_formula" name="target_formula"
                                       placeholder="例如：$x^2$">
                            </div>
                            <div class="mb-3">
                                <label for="difficulty" class="form-label">难度</label>
                                <select class="form-select" id="difficulty" name="difficulty">
                                    <option value="easy">简单</option>
                                    <option value="medium">中等</option>
                                    <option value="hard">困难</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="hints" class="form-label">提示</label>
                                <textarea class="form-control" id="hints" name="hints"
                                          rows="4" placeholder="每行一个提示，例如：&#10;使用 ^ 符号表示上标&#10;上标内容是 2&#10;完整格式：$x^2$"></textarea>
                            </div>
                        </div>

                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">添加卡片</button>
                            <a href="/admin/lessons/{{ lesson._id }}/edit" class="btn btn-secondary">取消</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            function toggleCardType() {
                const knowledgeRadio = document.getElementById('knowledge');
                const knowledgeForm = document.getElementById('knowledgeForm');
                const practiceForm = document.getElementById('practiceForm');

                if (knowledgeRadio.checked) {
                    knowledgeForm.style.display = 'block';
                    practiceForm.style.display = 'none';
                } else {
                    knowledgeForm.style.display = 'none';
                    practiceForm.style.display = 'block';
                }
            }
        </script>
    </body>
    </html>
    '''

    return render_template_string(create_card_html, lesson=lesson)


@admin_bp.route('/lessons/<lesson_id>/cards/<int:card_index>/edit', methods=['GET', 'POST'])
@admin_required
def edit_card(lesson_id, card_index):
    """编辑卡片"""
    db = get_db()

    # 获取课程
    lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})
    if not lesson:
        flash('课程不存在', 'error')
        return redirect(url_for('admin.lessons'))

    # 检查卡片索引
    if card_index >= len(lesson.get('cards', [])):
        flash('卡片不存在', 'error')
        return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id))

    card = lesson['cards'][card_index]

    # 获取当前编辑的语言，默认为中文
    current_lang = request.args.get('lang', 'zh-CN')

    if request.method == 'POST':
        try:
            edit_lang = request.form.get('edit_lang', 'zh-CN')

            if card['type'] == 'knowledge':
                # 更新知识点卡片
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                title_key = request.form.get('title_key', '').strip()
                content_key = request.form.get('content_key', '').strip()

                # 保留现有卡片数据
                updated_card = dict(card)

                # 根据编辑语言更新对应字段
                if edit_lang == 'en-US':
                    if title:
                        updated_card['title_en'] = title
                    if content:
                        updated_card['content_en'] = content
                else:
                    if title:
                        updated_card['title'] = title
                    if content:
                        updated_card['content'] = content

                # 更新翻译键（如果提供）
                if title_key:
                    updated_card['titleKey'] = title_key
                if content_key:
                    updated_card['contentKey'] = content_key

            elif card['type'] == 'practice':
                # 更新练习题卡片
                question = request.form.get('question', '').strip()
                target_formula = request.form.get('target_formula', '').strip()
                difficulty = request.form.get('difficulty', 'easy')
                hints_text = request.form.get('hints', '').strip()

                if not question or not target_formula:
                    flash('练习题的问题和答案不能为空', 'error')
                    return redirect(url_for('admin.edit_card', lesson_id=lesson_id, card_index=card_index, lang=edit_lang))

                hints = [hint.strip() for hint in hints_text.split('\n') if hint.strip()]

                # 保留现有卡片数据
                updated_card = dict(card)

                # 根据编辑语言更新对应字段
                if edit_lang == 'en-US':
                    updated_card['question_en'] = question
                    updated_card['target_formula_en'] = target_formula
                    updated_card['hints_en'] = hints
                else:
                    updated_card['question'] = question
                    updated_card['target_formula'] = target_formula
                    updated_card['hints'] = hints

                # 难度是通用的
                updated_card['difficulty'] = difficulty

            # 更新卡片
            update_query = {f'cards.{card_index}': updated_card}
            result = db.lessons.update_one(
                {'_id': ObjectId(lesson_id)},
                {'$set': update_query}
            )

            if result.modified_count > 0:
                flash(f'卡片{"英文" if edit_lang == "en-US" else "中文"}版本更新成功！', 'success')
                return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id))
            else:
                flash('卡片数据未发生变化', 'info')

        except Exception as e:
            flash(f'更新卡片失败：{str(e)}', 'error')

    edit_card_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>编辑卡片 - {{ lesson.title }}</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/lessons">课程管理</a>
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>{{ '编辑卡片' if current_lang == 'zh-CN' else 'Edit Card' }} #{{ card_index + 1 }} - {{ '多语言版本' if current_lang == 'zh-CN' else 'Multilingual Version' }}</h1>
                <div class="d-flex gap-2">
                    <div class="btn-group" role="group">
                        <a href="/admin/lessons/{{ lesson._id }}/cards/{{ card_index }}/edit?lang=zh-CN"
                           class="btn btn-outline-primary {{ 'active' if current_lang == 'zh-CN' else '' }}">
                            🇨🇳 {{ '中文' if current_lang == 'zh-CN' else 'Chinese' }}
                        </a>
                        <a href="/admin/lessons/{{ lesson._id }}/cards/{{ card_index }}/edit?lang=en-US"
                           class="btn btn-outline-primary {{ 'active' if current_lang == 'en-US' else '' }}">
                            🇺🇸 {{ '英文' if current_lang == 'zh-CN' else 'English' }}
                        </a>
                    </div>
                    <a href="/admin/lessons/{{ lesson._id }}/edit" class="btn btn-secondary">{{ '返回编辑' if current_lang == 'zh-CN' else 'Back to Edit' }}</a>
                </div>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' if category == 'success' else 'info' }} alert-dismissible fade show mt-3">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="card mt-3">
                <div class="card-header">
                    <h5>{{ '课程' if current_lang == 'zh-CN' else 'Course' }}：{{ lesson.title if current_lang == 'zh-CN' else lesson.title_en or lesson.title }} -
                        {% if card.type == 'knowledge' %}
                            <span class="badge bg-info">{{ '知识点卡片' if current_lang == 'zh-CN' else 'Knowledge Card' }}</span>
                        {% else %}
                            <span class="badge bg-success">{{ '练习题卡片' if current_lang == 'zh-CN' else 'Exercise Card' }}</span>
                        {% endif %}
                    </h5>
                </div>
                <div class="card-body">
                    <form method="post">
                        <input type="hidden" name="edit_lang" value="{{ current_lang }}">

                        {% if card.type == 'knowledge' %}
                            <!-- 知识点卡片表单 -->
                            {% if current_lang == 'zh-CN' %}
                                <div class="mb-3">
                                    <label for="title" class="form-label">标题 (中文)</label>
                                    <input type="text" class="form-control" id="title" name="title"
                                           value="{{ card.get('title', '') }}">
                                    {% if card.get('title_en') %}
                                        <div class="form-text text-muted">
                                            <small>英文参考: {{ card.get('title_en') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="content" class="form-label">内容 (中文)</label>
                                    <textarea class="form-control" id="content" name="content"
                                              rows="6">{{ card.get('content', '') }}</textarea>
                                    {% if card.get('content_en') %}
                                        <div class="form-text text-muted">
                                            <small>英文参考: {{ card.get('content_en') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                            {% else %}
                                <div class="mb-3">
                                    <label for="title" class="form-label">Title (English)</label>
                                    <input type="text" class="form-control" id="title" name="title"
                                           value="{{ card.get('title_en', '') }}">
                                    {% if card.get('title') %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {{ card.get('title') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="content" class="form-label">Content (English)</label>
                                    <textarea class="form-control" id="content" name="content"
                                              rows="6">{{ card.get('content_en', '') }}</textarea>
                                    {% if card.get('content') %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {{ card.get('content') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                            {% endif %}

                            <div class="mb-3">
                                <label for="title_key" class="form-label">{{ '标题翻译键' if current_lang == 'zh-CN' else 'Title Translation Key' }}</label>
                                <input type="text" class="form-control" id="title_key" name="title_key"
                                       value="{{ card.get('titleKey', '') }}">
                            </div>
                            <div class="mb-3">
                                <label for="content_key" class="form-label">{{ '内容翻译键' if current_lang == 'zh-CN' else 'Content Translation Key' }}</label>
                                <input type="text" class="form-control" id="content_key" name="content_key"
                                       value="{{ card.get('contentKey', '') }}">
                            </div>
                        {% else %}
                            <!-- 练习题卡片表单 -->
                            {% if current_lang == 'zh-CN' %}
                                <div class="mb-3">
                                    <label for="question" class="form-label">问题 (中文) *</label>
                                    <input type="text" class="form-control" id="question" name="question"
                                           value="{{ card.get('question', '') }}" required>
                                    {% if card.get('question_en') %}
                                        <div class="form-text text-muted">
                                            <small>英文参考: {{ card.get('question_en') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="target_formula" class="form-label">标准答案 (中文) *</label>
                                    <input type="text" class="form-control" id="target_formula" name="target_formula"
                                           value="{{ card.get('target_formula', '') }}" required>
                                    {% if card.get('target_formula_en') %}
                                        <div class="form-text text-muted">
                                            <small>英文参考: {{ card.get('target_formula_en') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="hints" class="form-label">提示 (中文)</label>
                                    <textarea class="form-control" id="hints" name="hints"
                                              rows="4">{% for hint in card.get('hints', []) %}{{ hint }}{% if not loop.last %}
{% endif %}{% endfor %}</textarea>
                                    <div class="form-text">每行一个提示</div>
                                    {% if card.get('hints_en') %}
                                        <div class="form-text text-muted">
                                            <small>英文参考: {% for hint in card.get('hints_en', []) %}{{ hint }}{% if not loop.last %}, {% endif %}{% endfor %}</small>
                                        </div>
                                    {% endif %}
                                </div>
                            {% else %}
                                <div class="mb-3">
                                    <label for="question" class="form-label">Question (English) *</label>
                                    <input type="text" class="form-control" id="question" name="question"
                                           value="{{ card.get('question_en', '') }}" required>
                                    {% if card.get('question') %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {{ card.get('question') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="target_formula" class="form-label">Target Answer (English) *</label>
                                    <input type="text" class="form-control" id="target_formula" name="target_formula"
                                           value="{{ card.get('target_formula_en', '') }}" required>
                                    {% if card.get('target_formula') %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {{ card.get('target_formula') }}</small>
                                        </div>
                                    {% endif %}
                                </div>
                                <div class="mb-3">
                                    <label for="hints" class="form-label">Hints (English)</label>
                                    <textarea class="form-control" id="hints" name="hints"
                                              rows="4">{% for hint in card.get('hints_en', []) %}{{ hint }}{% if not loop.last %}
{% endif %}{% endfor %}</textarea>
                                    <div class="form-text">One hint per line</div>
                                    {% if card.get('hints') %}
                                        <div class="form-text text-muted">
                                            <small>中文参考: {% for hint in card.get('hints', []) %}{{ hint }}{% if not loop.last %}, {% endif %}{% endfor %}</small>
                                        </div>
                                    {% endif %}
                                </div>
                            {% endif %}

                            <div class="mb-3">
                                <label for="difficulty" class="form-label">{{ '难度' if current_lang == 'zh-CN' else 'Difficulty' }}</label>
                                <select class="form-select" id="difficulty" name="difficulty">
                                    <option value="easy" {% if card.get('difficulty') == 'easy' %}selected{% endif %}>{{ '简单' if current_lang == 'zh-CN' else 'Easy' }}</option>
                                    <option value="medium" {% if card.get('difficulty') == 'medium' %}selected{% endif %}>{{ '中等' if current_lang == 'zh-CN' else 'Medium' }}</option>
                                    <option value="hard" {% if card.get('difficulty') == 'hard' %}selected{% endif %}>{{ '困难' if current_lang == 'zh-CN' else 'Hard' }}</option>
                                </select>
                            </div>
                        {% endif %}

                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                {{ '保存' + ('中文' if current_lang == 'zh-CN' else '英文') + '版本' if current_lang == 'zh-CN' else 'Save ' + ('Chinese' if current_lang == 'zh-CN' else 'English') + ' Version' }}
                            </button>
                            <a href="/admin/lessons/{{ lesson._id }}/edit" class="btn btn-secondary">{{ '取消' if current_lang == 'zh-CN' else 'Cancel' }}</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(edit_card_html, lesson=lesson, card=card, card_index=card_index, current_lang=current_lang)


@admin_bp.route('/lessons/<lesson_id>/cards/<int:card_index>/delete')
@admin_required
def delete_card(lesson_id, card_index):
    """删除卡片"""
    db = get_db()

    try:
        # 获取课程
        lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})
        if not lesson:
            flash('课程不存在', 'error')
            return redirect(url_for('admin.lessons'))

        # 检查卡片索引
        if card_index >= len(lesson.get('cards', [])):
            flash('卡片不存在', 'error')
            return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id))

        # 删除卡片
        cards = lesson['cards']
        cards.pop(card_index)

        result = db.lessons.update_one(
            {'_id': ObjectId(lesson_id)},
            {'$set': {'cards': cards}}
        )

        if result.modified_count > 0:
            flash('卡片删除成功！', 'success')
        else:
            flash('卡片删除失败', 'error')

    except Exception as e:
        flash(f'删除卡片失败：{str(e)}', 'error')

    return redirect(url_for('admin.edit_lesson', lesson_id=lesson_id))


@admin_bp.route('/reset-users')
@admin_required
def reset_users():
    """重置用户学习数据"""
    try:
        db = get_db()
        
        # 重置所有用户的学习进度
        db.users.update_many(
            {},
            {
                '$set': {
                    'progress': {
                        'current_lesson_id': None,
                        'completed_lessons': []
                    },
                    'practice_stats': {
                        'total_attempts': 0,
                        'correct_answers': 0,
                        'accuracy_rate': 0.0
                    }
                }
            }
        )
        
        # 删除所有练习记录
        db.practice_records.delete_many({})
        
        # 删除所有复习记录
        db.reviews.delete_many({})
        
        flash('用户学习数据重置成功！', 'success')
    except Exception as e:
        flash(f'用户数据重置失败：{str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/translations/import', methods=['GET', 'POST'])
@admin_required
def import_translations():
    """导入翻译数据"""
    if request.method == 'POST':
        try:
            # 检查是否有上传的文件
            if 'translation_file' not in request.files:
                flash('请选择要上传的翻译文件', 'error')
                return redirect(url_for('admin.import_translations'))

            file = request.files['translation_file']
            if file.filename == '':
                flash('请选择要上传的翻译文件', 'error')
                return redirect(url_for('admin.import_translations'))

            if not file.filename.endswith('.json'):
                flash('请上传JSON格式的翻译文件', 'error')
                return redirect(url_for('admin.import_translations'))

            # 读取并解析JSON文件
            translation_data = json.load(file)

            # 验证数据格式
            if 'lessons' not in translation_data:
                flash('翻译文件格式错误：缺少lessons字段', 'error')
                return redirect(url_for('admin.import_translations'))

            # 导入翻译数据
            db = get_db()
            updated_count = 0
            error_count = 0

            for lesson_data in translation_data['lessons']:
                try:
                    lesson_id = lesson_data.get('id')
                    if not lesson_id:
                        error_count += 1
                        continue

                    # 查找现有课程
                    existing_lesson = db.lessons.find_one({'_id': ObjectId(lesson_id)})

                    if existing_lesson:
                        # 更新现有课程的翻译
                        update_data = {}
                        translations = lesson_data.get('translations', {})

                        for lang, trans_data in translations.items():
                            if lang == 'en-US':
                                if 'title' in trans_data:
                                    update_data['title_en'] = trans_data['title']
                                if 'description' in trans_data:
                                    update_data['description_en'] = trans_data['description']
                                if 'cards' in trans_data:
                                    update_data['cards_en'] = trans_data['cards']

                        if update_data:
                            result = db.lessons.update_one(
                                {'_id': ObjectId(lesson_id)},
                                {'$set': update_data}
                            )
                            if result.modified_count > 0:
                                updated_count += 1
                    else:
                        # 如果课程不存在，记录错误
                        error_count += 1

                except Exception as e:
                    print(f"处理课程 {lesson_data.get('id', 'unknown')} 时出错: {str(e)}")
                    error_count += 1

            # 显示导入结果
            if updated_count > 0:
                flash(f'成功更新 {updated_count} 个课程的翻译数据', 'success')
            if error_count > 0:
                flash(f'{error_count} 个课程处理失败', 'warning')

            return redirect(url_for('admin.import_translations'))

        except json.JSONDecodeError:
            flash('翻译文件格式错误：无效的JSON格式', 'error')
        except Exception as e:
            flash(f'导入翻译数据失败：{str(e)}', 'error')

        return redirect(url_for('admin.import_translations'))

    # GET请求显示导入页面
    import_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>导入翻译数据</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center">
                <h1>导入翻译数据</h1>
                <a href="/admin/dashboard" class="btn btn-secondary">返回仪表板</a>
            </div>

            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ 'danger' if category == 'error' else 'warning' if category == 'warning' else 'success' }} alert-dismissible fade show mt-3">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}

            <div class="card mt-3">
                <div class="card-header">
                    <h5>上传翻译文件</h5>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="translation_file" class="form-label">选择翻译文件 (JSON格式)</label>
                            <input type="file" class="form-control" id="translation_file" name="translation_file"
                                   accept=".json" required>
                            <div class="form-text">请上传包含课程翻译数据的JSON文件</div>
                        </div>
                        <button type="submit" class="btn btn-primary">导入翻译数据</button>
                    </form>
                </div>
            </div>

            <div class="card mt-3">
                <div class="card-header">
                    <h5>📋 翻译文件格式说明</h5>
                </div>
                <div class="card-body">
                    <p>翻译文件应为JSON格式，包含以下结构：</p>
                    <pre><code>{
  "lessons": [
    {
      "id": "课程ID",
      "translations": {
        "en-US": {
          "title": "英文标题",
          "description": "英文描述",
          "cards": [
            {
              "type": "knowledge",
              "title": "英文知识点标题",
              "content": "英文知识点内容"
            },
            {
              "type": "practice",
              "question": "英文练习题问题",
              "target_formula": "$x^2$",
              "hints": ["英文提示1", "英文提示2"],
              "difficulty": "easy"
            }
          ]
        }
      }
    }
  ]
}</code></pre>
                    <div class="mt-3">
                        <h6>导入规则：</h6>
                        <ul>
                            <li>根据课程ID匹配现有课程</li>
                            <li>存在则更新翻译数据</li>
                            <li>不存在则跳过并记录错误</li>
                            <li>支持部分字段更新</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''

    return render_template_string(import_html)


@admin_bp.route('/change-password', methods=['GET', 'POST'])
@admin_required
def change_password():
    """修改管理员密码"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        # 验证输入
        if not current_password or not new_password or not confirm_password:
            flash('请填写所有字段', 'error')
        elif new_password != confirm_password:
            flash('新密码和确认密码不匹配', 'error')
        elif len(new_password) < 6:
            flash('新密码长度至少6位', 'error')
        elif len(new_password) > 128:
            flash('新密码长度不能超过128位', 'error')
        else:
            # 获取当前管理员
            admin = get_current_admin()
            if admin:
                success, message = admin.change_password(current_password, new_password)
                if success:
                    flash(message, 'success')
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash(message, 'error')
            else:
                flash('获取管理员信息失败', 'error')

    # 显示密码修改表单
    change_password_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>修改密码 - 管理后台</title>
        <meta charset="utf-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/admin/dashboard">LaTeX训练器管理后台</a>
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="/admin/dashboard">仪表板</a>
                    <a class="nav-link" href="/admin/logout">退出登录</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="mb-0">🔑 修改管理员密码</h5>
                        </div>
                        <div class="card-body">
                            {% with messages = get_flashed_messages(with_categories=true) %}
                                {% if messages %}
                                    {% for category, message in messages %}
                                        <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }} alert-dismissible fade show">
                                            {{ message }}
                                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                        </div>
                                    {% endfor %}
                                {% endif %}
                            {% endwith %}

                            <div class="alert alert-info">
                                <strong>安全提示：</strong>
                                <ul class="mb-0">
                                    <li>密码长度至少6位，最多128位</li>
                                    <li>建议使用包含字母、数字和特殊字符的强密码</li>
                                    <li>修改密码后需要重新登录</li>
                                </ul>
                            </div>

                            <form method="post">
                                <div class="mb-3">
                                    <label for="current_password" class="form-label">当前密码 *</label>
                                    <input type="password" class="form-control" id="current_password"
                                           name="current_password" required>
                                </div>

                                <div class="mb-3">
                                    <label for="new_password" class="form-label">新密码 *</label>
                                    <input type="password" class="form-control" id="new_password"
                                           name="new_password" required minlength="6" maxlength="128">
                                </div>

                                <div class="mb-3">
                                    <label for="confirm_password" class="form-label">确认新密码 *</label>
                                    <input type="password" class="form-control" id="confirm_password"
                                           name="confirm_password" required minlength="6" maxlength="128">
                                </div>

                                <div class="d-flex gap-2">
                                    <button type="submit" class="btn btn-primary">修改密码</button>
                                    <a href="/admin/dashboard" class="btn btn-secondary">取消</a>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <script>
            // 密码确认验证
            document.getElementById('confirm_password').addEventListener('input', function() {
                const newPassword = document.getElementById('new_password').value;
                const confirmPassword = this.value;

                if (newPassword !== confirmPassword) {
                    this.setCustomValidity('密码不匹配');
                } else {
                    this.setCustomValidity('');
                }
            });
        </script>
    </body>
    </html>
    '''

    return render_template_string(change_password_html)
