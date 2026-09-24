/**
 * 题库前端唯一读入口
 * 数据源头：仓库根目录 data/latex_bank.json（经 vite alias '@bank' 引入）
 * 所有文本字段均已按语言本地化，调用方传入当前语言即可直接渲染。
 */
import bank from '@bank'

// 支持的语言与默认回退语言
const SUPPORTED_LANGUAGES = ['zh-CN', 'en-US']
const DEFAULT_LANGUAGE = 'zh-CN'

/**
 * 归一化语言代码，不支持的语言回退到默认语言
 * @param {string} language - 语言代码（zh-CN / en-US）
 * @returns {string} 题库实际使用的语言代码
 */
function resolveLanguage(language) {
  return SUPPORTED_LANGUAGES.includes(language) ? language : DEFAULT_LANGUAGE
}

/**
 * 从语言字典中取文本，缺失时回退默认语言，仍缺失则返回空字符串
 * @param {Object} dict - 形如 {'zh-CN': '…', 'en-US': '…'} 的语言字典
 * @param {string} language - 已归一化的语言代码
 * @returns {string} 对应语言的文本
 */
function localized(dict, language) {
  if (!dict || typeof dict !== 'object') return ''
  const value = dict[language]
  if (typeof value === 'string') return value
  const fallback = dict[DEFAULT_LANGUAGE]
  return typeof fallback === 'string' ? fallback : ''
}

/**
 * 获取课程元信息列表（不含卡片内容）
 * @param {string} language - 语言代码（zh-CN / en-US）
 * @returns {Array<{sequence: number, title: string, description: string}>}
 */
export function getLessonsMeta(language) {
  const lang = resolveLanguage(language)
  return (bank.lessons || []).map((lesson) => ({
    sequence: lesson.sequence,
    title: localized(lesson.title, lang),
    description: localized(lesson.description, lang),
  }))
}

/**
 * 获取扁平化的练习题列表（只含 practice 卡，保持卡片原始顺序）
 * @param {string} language - 语言代码（zh-CN / en-US）
 * @returns {Array<{id: string, sequence: number, lessonTitle: string, question: string, target_formula: string, hints: string[], difficulty: string}>}
 */
export function getPracticeQuestions(language) {
  const lang = resolveLanguage(language)
  const questions = []
  for (const lesson of bank.lessons || []) {
    const lessonTitle = localized(lesson.title, lang)
    const cards = lesson.cards || []
    cards.forEach((card, cardIndex) => {
      if (card.type !== 'practice') return
      questions.push({
        id: `${lesson.sequence}-${cardIndex}`,
        sequence: lesson.sequence,
        lessonTitle,
        question: localized(card.question, lang),
        target_formula: card.target_formula,
        hints: card.hints?.[lang] || card.hints?.[DEFAULT_LANGUAGE] || [],
        difficulty: card.difficulty,
      })
    })
  }
  return questions
}
