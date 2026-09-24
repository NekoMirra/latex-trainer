"""题库单一源头 - 从 data/latex_bank.json 展开为数据库文档"""
import json
from datetime import datetime
from pathlib import Path

from bson import ObjectId

BANK_PATH = Path(__file__).resolve().parents[3] / 'data' / 'latex_bank.json'
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@pipeak.com'
ADMIN_PASSWORD = 'admin123'
ADMIN_CREDENTIALS = f'{ADMIN_USERNAME} / {ADMIN_PASSWORD}'


def load_bank():
    """读取题库文件；缺文件或 JSON 损坏时直接抛出，不做兜底"""
    with BANK_PATH.open('r', encoding='utf-8') as handle:
        return json.load(handle)


def _cards_for_language(lesson, language):
    """把语言字典形式的卡片展开为该语言的数据库卡片"""
    cards = []
    for card in lesson['cards']:
        if card['type'] == 'knowledge':
            cards.append({'type': 'knowledge', 'content': card['content'][language]})
        else:
            cards.append({
                'type': 'practice',
                'question': card['question'][language],
                'target_formula': card['target_formula'],
                'hints': list(card['hints'][language]),
                'difficulty': card['difficulty'],
            })
    return cards


def lessons_zh(bank):
    """展开为数据库文档（中文侧，含 ObjectId）"""
    now = datetime.utcnow()
    return [{
        '_id': ObjectId(),
        'sequence': lesson['sequence'],
        'title': lesson['title']['zh-CN'],
        'description': lesson['description']['zh-CN'],
        'cards': _cards_for_language(lesson, 'zh-CN'),
        'created_at': now,
        'updated_at': now,
    } for lesson in bank['lessons']]


def lessons_en(bank):
    """展开为英文侧课程数据，按 sequence 与中文文档配对"""
    return [{
        'sequence': lesson['sequence'],
        'title': lesson['title']['en-US'],
        'description': lesson['description']['en-US'],
        'cards': _cards_for_language(lesson, 'en-US'),
    } for lesson in bank['lessons']]


def apply_translations(db, lessons_en_us):
    """按 sequence 写入 title_en/description_en/cards_en，返回更新条数"""
    updated = 0
    for lesson in lessons_en_us:
        result = db.lessons.update_one(
            {'sequence': lesson['sequence']},
            {'$set': {
                'title_en': lesson['title'],
                'description_en': lesson['description'],
                'cards_en': lesson['cards'],
                'updated_at': datetime.utcnow(),
            }}
        )
        updated += result.modified_count
    return updated


def count_practices(lessons):
    """统计课程列表中的练习题总数"""
    return sum(1 for lesson in lessons for card in lesson['cards'] if card['type'] == 'practice')


def _create_admin(db):
    """创建管理后台账号与同名登录用户（复用模型里的 bcrypt 逻辑）"""
    from app.models.admin import Admin
    from app.models.user import User

    if not Admin.find_by_username(ADMIN_USERNAME):
        Admin(username=ADMIN_USERNAME, password=ADMIN_PASSWORD).save()

    if not User.find_by_email(ADMIN_EMAIL):
        user = User(email=ADMIN_EMAIL)
        user.set_password(ADMIN_PASSWORD)
        user.save()


def seed_database(db, *, reset):
    """把题库写入数据库。

    reset=True 清空课程与用户数据后全量重建；reset=False 只补齐缺失课程与翻译。
    """
    bank = load_bank()
    zh_lessons = lessons_zh(bank)
    en_lessons = lessons_en(bank)

    if reset:
        for collection in ('lessons', 'users', 'practice_records', 'user_progress', 'admins', 'reviews'):
            db[collection].delete_many({})
        inserted = len(db.lessons.insert_many(zh_lessons).inserted_ids)
    else:
        existing = {lesson['sequence'] for lesson in db.lessons.find({}, {'sequence': 1})}
        missing = [lesson for lesson in zh_lessons if lesson['sequence'] not in existing]
        if missing:
            db.lessons.insert_many(missing)
        inserted = len(missing)

    _create_admin(db)
    translation_count = apply_translations(db, en_lessons)

    return {
        'lesson_count': db.lessons.count_documents({}),
        'inserted_lessons': inserted,
        'practice_count': count_practices(zh_lessons),
        'translation_count': translation_count,
        'admin_credentials': ADMIN_CREDENTIALS,
    }