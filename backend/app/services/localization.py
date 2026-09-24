"""按语言从课程文档中取标题与卡片内容"""
DEFAULT_LANGUAGE = 'zh-CN'


def localized_title(lesson, language):
    """课程标题：英文界面优先取 title_en，缺失时回退中文标题"""
    if language == 'en-US' and lesson.get('title_en'):
        return lesson['title_en']
    return lesson['title']


def localized_card(lesson, card_index, language):
    """课程卡片：英文界面优先取 cards_en 同下标的翻译卡片，缺字段逐项回退中文卡片"""
    card = lesson['cards'][card_index]
    if language != 'en-US':
        return card

    cards_en = lesson.get('cards_en')
    if not cards_en or card_index >= len(cards_en):
        return card

    card_en = cards_en[card_index]
    return {
        'question': card_en.get('question', card.get('question', '')),
        'target_formula': card_en.get('target_formula', card.get('target_formula', '')),
        'difficulty': card_en.get('difficulty', card.get('difficulty', 'medium')),
        'hints': card_en.get('hints', card.get('hints', [])),
    }