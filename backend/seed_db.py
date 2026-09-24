"""题库种子入口 - 把 data/latex_bank.json 写入 MongoDB"""
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from app import create_app, get_db
from app.services.bank import seed_database


def main():
    create_app(os.environ.get('FLASK_ENV', 'development'))
    db = get_db()
    result = seed_database(db, reset='--reset' in sys.argv)

    print(f"课程数: {result['lesson_count']}（本次插入 {result['inserted_lessons']}）")
    print(f"练习题总数: {result['practice_count']}")
    print(f"英文翻译写入: {result['translation_count']}")
    print(f"管理员账号: {result['admin_credentials']}")

    incomplete = 0
    for lesson in db.lessons.find({}):
        if (not lesson.get('title_en') or not lesson.get('description_en')
                or len(lesson.get('cards_en') or []) != len(lesson['cards'])):
            incomplete += 1
            print(f"  英文缺失或不完整: 第{lesson['sequence']}课 {lesson['title']}")
    print(f"中英字段不齐全的课程: {incomplete}")


if __name__ == '__main__':
    main()