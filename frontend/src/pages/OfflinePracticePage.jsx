import { useState, useEffect, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useDocumentTitle, PAGE_TITLES } from '../hooks/useDocumentTitle'
import MarkdownRenderer from '../components/MarkdownRenderer'
import ThemeSwitcher from '../components/ThemeSwitcher'
import LanguageSwitcher from '../components/LanguageSwitcher'
import { getPracticeQuestions, getLessonsMeta } from '../data/bank'
import { checkAdvancedAnswerEquivalence } from '../utils/answerValidation'

// 随机练习模式抽取的题量
const RANDOM_QUESTION_COUNT = 20

const OfflinePracticePage = () => {
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()

  // 设置动态页面标题
  useDocumentTitle(PAGE_TITLES.PRACTICE)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [userAnswer, setUserAnswer] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [isCorrect, setIsCorrect] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [allQuestions, setAllQuestions] = useState([])
  const [questions, setQuestions] = useState([])
  const [score, setScore] = useState(0)
  const [showResults, setShowResults] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [currentHint, setCurrentHint] = useState('')
  const [hintLevel, setHintLevel] = useState(0)
  const [answeredQuestions, setAnsweredQuestions] = useState(0)
  // 筛选条件：课程（sequence 或 'all'）、难度（easy/medium/hard 或 'all'）
  const [courseFilter, setCourseFilter] = useState('all')
  const [difficultyFilter, setDifficultyFilter] = useState('all')
  // 大于 0 表示随机题集模式，每次自增都重新抽取一批
  const [randomToken, setRandomToken] = useState(0)

  // 课程下拉选项（随当前语言变化）
  const lessonsMeta = useMemo(() => getLessonsMeta(i18n.language), [i18n.language])

  // 题库数据已本地化：语言变化时直接重建全量题集
  useEffect(() => {
    setAllQuestions(getPracticeQuestions(i18n.language))
  }, [i18n.language])

  // 题集或筛选条件变化时重建练习队列，并把进度重置到第一题
  useEffect(() => {
    let list = allQuestions
    if (courseFilter !== 'all') {
      list = list.filter((question) => question.sequence === Number(courseFilter))
    }
    if (difficultyFilter !== 'all') {
      list = list.filter((question) => question.difficulty === difficultyFilter)
    }
    if (randomToken > 0) {
      list = [...list].sort(() => Math.random() - 0.5).slice(0, RANDOM_QUESTION_COUNT)
    }

    setQuestions(list)
    setCurrentQuestionIndex(0)
    setUserAnswer('')
    setFeedback(null)
    setIsCorrect(false)
    setShowHint(false)
    setCurrentHint('')
    setHintLevel(0)
    setScore(0)
    setAnsweredQuestions(0)
    setShowResults(false)
  }, [allQuestions, courseFilter, difficultyFilter, randomToken])

  const currentQuestion = questions[currentQuestionIndex]

  const handleSubmit = async () => {
    if (!userAnswer.trim()) {
      setFeedback(t('practice.enterAnswer'))
      return
    }

    setIsSubmitting(true)
    try {
      // 离线练习模式：本地验证答案
      if (!currentQuestion.target_formula) {
        console.error('练习题缺少target_formula字段:', currentQuestion)
        setFeedback('练习题数据错误，请刷新页面重试')
        setIsSubmitting(false)
        return
      }

      // 使用增强的答案检查逻辑（包含语义比较和错误检测）
      const result = await checkAdvancedAnswerEquivalence(
        userAnswer.trim(),
        currentQuestion.target_formula.trim(),
        true // 启用语义比较
      )

      setIsCorrect(result.isCorrect)
      setAnsweredQuestions(answeredQuestions + 1)

      if (result.isCorrect) {
        setScore(score + 1)
        // 检查用户答案是否包含$，以提供友好提示
        if (!userAnswer.trim().includes('$')) {
          setFeedback(t('lesson.correct') + ' ' + t('practice.dollarSignHint'))
        } else {
          setFeedback(t('lesson.correct'))
        }
        // 答对后不自动跳转，由用户手动控制
      } else {
        // 如果有专门的错误提示，显示专门提示；否则显示通用错误信息
        if (result.errorInfo) {
          setFeedback(`❌ ${result.errorInfo.message}`)
        } else {
          setFeedback(t('lesson.incorrect'))
        }
      }
    } catch (error) {
      setFeedback(t('practice.submitError'))
      console.error('验证答案失败:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setUserAnswer('')
      setFeedback(null)
      setIsCorrect(false)
      setShowHint(false)
      setCurrentHint('')
      setHintLevel(0) // 重置提示级别
    } else {
      // 显示最终结果
      setShowResults(true)
    }
  }

  const handleGetHint = () => {
    const hints = currentQuestion?.hints
    if (hints && hints.length > 0) {
      if (hintLevel < hints.length) {
        // 渐进式提示：数据已本地化，直接取当前级别的提示
        setCurrentHint(hints[hintLevel])
        setHintLevel(hintLevel + 1)
      } else {
        // 提示已用尽：保持显示最后一条，并附上「已显示所有提示」文案
        setCurrentHint(`${hints[hints.length - 1]}\n\n💡 ${t('practice.allHintsShown')}`)
      }
      setShowHint(true)
    } else {
      setCurrentHint(t('practice.noHint'))
      setShowHint(true)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && isCorrect) {
      e.preventDefault()
      handleNextQuestion()
    } else if (e.key === 'Enter' && !isCorrect && userAnswer.trim()) {
      e.preventDefault()
      handleSubmit()
    } else if (e.key === 'F1' && !isCorrect) {
      // 使用F1键作为提示快捷键，不影响Tab导航
      e.preventDefault()
      handleGetHint()
    }
  }

  // 切换筛选条件时退出随机模式，按筛选结果的原始顺序练习
  const handleCourseFilterChange = (e) => {
    setCourseFilter(e.target.value)
    setRandomToken(0)
  }

  const handleDifficultyFilterChange = (e) => {
    setDifficultyFilter(e.target.value)
    setRandomToken(0)
  }

  // 随机抽取一批题目，重复点击则重新抽取
  const handleShuffleStart = () => {
    setRandomToken((prev) => prev + 1)
  }

  const restartPractice = () => {
    setCurrentQuestionIndex(0)
    setUserAnswer('')
    setFeedback(null)
    setIsCorrect(false)
    setScore(0)
    setAnsweredQuestions(0)
    setShowResults(false)
  }

  // 筛选控件：主视图与空状态共用
  const filterControls = (
    <div className="flex flex-wrap items-end gap-3 mb-4">
      <div className="flex flex-col">
        <label htmlFor="course-filter" className="text-xs text-gray-500 dark:text-gray-400 mb-1">
          {t('offlinePractice.filterCourse')}
        </label>
        <select
          id="course-filter"
          value={courseFilter}
          onChange={handleCourseFilterChange}
          className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none max-w-[280px]"
        >
          <option value="all">{t('offlinePractice.allOption')}</option>
          {lessonsMeta.map((lesson) => (
            <option key={lesson.sequence} value={lesson.sequence}>
              {lesson.title}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col">
        <label htmlFor="difficulty-filter" className="text-xs text-gray-500 dark:text-gray-400 mb-1">
          {t('offlinePractice.filterDifficulty')}
        </label>
        <select
          id="difficulty-filter"
          value={difficultyFilter}
          onChange={handleDifficultyFilterChange}
          className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
        >
          <option value="all">{t('offlinePractice.allOption')}</option>
          <option value="easy">{t('practice.difficulty.easy')}</option>
          <option value="medium">{t('practice.difficulty.medium')}</option>
          <option value="hard">{t('practice.difficulty.hard')}</option>
        </select>
      </div>

      <button
        type="button"
        onClick={handleShuffleStart}
        className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
          randomToken > 0
            ? 'bg-blue-600 text-white hover:bg-blue-700'
            : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600'
        }`}
      >
        {t('offlinePractice.shuffleStart')}
      </button>
    </div>
  )

  // 题库尚未加载完成
  if (allQuestions.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">{t('offlinePractice.loading')}</p>
        </div>
      </div>
    )
  }

  // 当前筛选条件下没有题目：保留筛选控件以便调整
  if (questions.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center text-sm"
          >
            {t('offlinePractice.backToHome')}
          </button>

          <div className="flex items-center space-x-2">
            <ThemeSwitcher />
            <LanguageSwitcher />
          </div>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">{t('offlinePractice.title')}</h1>

        {filterControls}

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 text-center">
          <p className="text-gray-600 dark:text-gray-400">{t('offlinePractice.empty')}</p>
        </div>
      </div>
    )
  }

  if (showResults) {
    const percentage = Math.round((score / questions.length) * 100)
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="mb-6">
            <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">🎉</span>
            </div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{t('offlinePractice.practiceComplete')}</h1>
            <p className="text-gray-600">{t('offlinePractice.congratulations')}</p>
          </div>

          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-blue-600">{score}</div>
                <div className="text-sm text-gray-600">{t('offlinePractice.correctAnswers')}</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-gray-600">{questions.length}</div>
                <div className="text-sm text-gray-600">{t('offlinePractice.totalQuestions')}</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-green-600">{percentage}%</div>
                <div className="text-sm text-gray-600">{t('offlinePractice.accuracy')}</div>
              </div>
            </div>
          </div>
          
          <div className="flex gap-4 justify-center">
            <button
              onClick={restartPractice}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              {t('offlinePractice.restartPractice')}
            </button>
            <button
              onClick={() => navigate('/')}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              {t('offlinePractice.backToHomePage')}
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* 头部 */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 flex items-center text-sm"
          >
            {t('offlinePractice.backToHome')}
          </button>

          {/* 主题和语言切换器 */}
          <div className="flex items-center space-x-2">
            <ThemeSwitcher />
            <LanguageSwitcher />
          </div>

          <div className="text-sm text-gray-600 dark:text-gray-400">
            {t('offlinePractice.questionProgress', { current: currentQuestionIndex + 1, total: questions.length })}
          </div>
        </div>
        
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-4">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>

        <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">{t('offlinePractice.title')}</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-4">{t('offlinePractice.currentAccuracy', { accuracy: answeredQuestions > 0 ? Math.round((score / answeredQuestions) * 100) : 0 })}</p>

        {/* 课程 / 难度筛选与随机题集 */}
        {filterControls}
      </div>

      {/* 练习题卡片 */}
      {currentQuestion && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <div className="mb-4">
            <div className="text-sm text-blue-600 dark:text-blue-400 mb-2">{t('offlinePractice.fromLesson', { lesson: currentQuestion.lessonTitle })}</div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">{currentQuestion.question}</h2>

            {/* 目标效果预览 */}
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-700 mb-4">
              <p className="text-sm text-blue-800 dark:text-blue-300 mb-2">{t('offlinePractice.targetEffect')}</p>
              <div className="text-center bg-white dark:bg-gray-700 p-3 rounded border dark:border-gray-600">
                <MarkdownRenderer content={currentQuestion.target_formula} />
              </div>
            </div>
          </div>

          {/* 实时预览 */}
          <div className="mb-4">
            <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">{t('offlinePractice.realTimePreview')}</p>
            <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg border border-gray-200 dark:border-gray-600 min-h-[80px] max-h-[140px] flex items-center justify-center overflow-auto">
              <div className="text-center w-full">
                {userAnswer.trim() ? (
                  <MarkdownRenderer content={userAnswer.includes('$') || userAnswer.includes('\\begin{equation}') ? userAnswer : `$${userAnswer}$`} />
                ) : (
                  <span className="text-gray-400 dark:text-gray-500 text-sm">{t('offlinePractice.previewPlaceholder')}</span>
                )}
              </div>
            </div>
          </div>

          {/* 答案输入 */}
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              {t('offlinePractice.inputPrompt')}
            </label>
            <div className="relative">
              <textarea
                value={userAnswer}
                onChange={(e) => {
                  const value = e.target.value
                  // 限制输入长度为500字符，防止界面变形
                  if (value.length <= 500) {
                    setUserAnswer(value)
                  }
                }}
                onKeyDown={handleKeyPress}
                placeholder={t('offlinePractice.inputPlaceholder')}
                maxLength={500}
                className={`w-full px-3 py-2 rounded-lg focus:ring-2 focus:ring-blue-500/20 focus:outline-none transition-all duration-200 font-mono text-sm resize-none border ${
                  isCorrect
                    ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300 border-green-300 dark:border-green-600'
                    : 'bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 focus:border-blue-500 dark:text-gray-100'
                }`}
                rows="2"
                readOnly={isCorrect}
                spellCheck={false}
                autoComplete="off"
                autoCorrect="off"
                autoCapitalize="off"
              />
              <div className="absolute bottom-2 right-2 text-xs text-gray-400 dark:text-gray-500 bg-gray-50 dark:bg-gray-600 px-1 py-0.5 rounded text-xs">
                <div>{t('practice.keyboardShortcuts')}</div>
                {!isCorrect && <div>{t('practice.hintShortcut')}</div>}
              </div>
            </div>
            {/* 字符计数器 */}
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 text-right">
              {t('practice.characterCount', { count: userAnswer.length, max: 500 })}
            </div>
          </div>

          {/* 反馈信息 */}
          {feedback && (
            <div className={`mb-4 p-3 rounded-lg border transition-all duration-300 ${
              isCorrect
                ? 'bg-green-100 dark:bg-green-900/20 border-green-300 dark:border-green-600 text-green-800 dark:text-green-300 shadow-green-100 dark:shadow-green-900/20'
                : 'bg-red-100 dark:bg-red-900/20 border-red-300 dark:border-red-600 text-red-800 dark:text-red-300 shadow-red-100 dark:shadow-red-900/20 animate-pulse'
            } shadow-lg`}>
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 mt-0.5">
                  {isCorrect ? (
                    <svg className="w-4 h-4 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4 text-red-600 dark:text-red-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
                <div className="flex-1">
                  <p className="font-medium text-sm">{feedback}</p>
                  {isCorrect && (
                    <p className="text-xs mt-1 opacity-80">
                      {t('practice.continueHint')}
                    </p>
                  )}
                  {!isCorrect && (
                    <p className="text-xs mt-1 opacity-80">
                      {t('practice.incorrectHint')}
                    </p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* 提示信息 */}
          {showHint && currentHint && (
            <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/20 border border-yellow-300 dark:border-yellow-600 rounded-lg shadow-lg transition-all duration-300">
              <div className="flex items-start space-x-2">
                <div className="flex-shrink-0 mt-0.5">
                  <svg className="w-4 h-4 text-yellow-600 dark:text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="flex-1">
                  <p className="text-yellow-800 dark:text-yellow-300 text-sm">
                    <span className="font-medium">{t('practice.hintPrefix')}</span>
                    {currentHint}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* 操作按钮 */}
          <div className="flex gap-3">
            {!isCorrect ? (
              <>
                <button
                  onClick={handleSubmit}
                  disabled={isSubmitting || !userAnswer.trim()}
                  className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
                    isSubmitting || !userAnswer.trim()
                      ? 'bg-gray-400 text-white cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  }`}
                >
                  {isSubmitting ? t('practice.submitting') : t('offlinePractice.submitAnswer')}
                </button>
                <button
                  onClick={handleGetHint}
                  disabled={isSubmitting}
                  className={`px-3 py-2 rounded-lg transition-colors text-sm ${
                    isSubmitting
                      ? 'bg-gray-400 text-white cursor-not-allowed'
                      : 'bg-yellow-500 text-white hover:bg-yellow-600'
                  }`}
                  title={t('practice.hintTooltip')}
                >
                  {t('practice.getHint')}
                </button>
              </>
            ) : (
              <button
                onClick={handleNextQuestion}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium text-sm"
              >
                {currentQuestionIndex < questions.length - 1 ? t('practice.nextQuestion') : t('practice.viewResults')}
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default OfflinePracticePage
