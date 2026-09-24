import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import MarkdownRenderer from '../components/MarkdownRenderer'
import { reviewAPI } from '../services/api'
import PracticeCard from '../components/PracticeCard'

const ReviewPage = () => {
  const { t, i18n } = useTranslation()
  const [reviews, setReviews] = useState([])
  const [stats, setStats] = useState(null)
  const [currentReviewIndex, setCurrentReviewIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [showStats, setShowStats] = useState(false)
  const [nextReviewDate, setNextReviewDate] = useState(null)
  const navigate = useNavigate()

  // PracticeCard引用，用于自动聚焦
  const practiceCardRef = useRef(null)

  // 数据适配器：将复习数据转换为PracticeCard期望的格式
  const adaptReviewDataToPracticeCard = (reviewData) => {
    const adaptedData = {
      question: reviewData.question,
      answer: reviewData.target_formula,
      target_formula: reviewData.target_formula,
      difficulty: reviewData.difficulty,
      hints: reviewData.hints || [], // 添加提示数组
      // 添加复习特有的字段
      review_id: reviewData.review_id,
      lesson_title: reviewData.lesson_title,
      repetitions: reviewData.repetitions,
      memory_strength: reviewData.easiness_factor
    }

    return adaptedData
  }

  // 处理复习完成
  const handleReviewComplete = async (reviewData, userAnswer, isCorrect) => {
    try {
      const submitData = {
        review_id: reviewData.review_id,
        user_answer: userAnswer,
        is_correct: isCorrect,
        quality: isCorrect ? 4 : 1
      }

      const response = await reviewAPI.submitReview(submitData)

      // 记录 SM-2 排出的下次复习时间，供界面显示
      if (response?.next_review_date) {
        setNextReviewDate(response.next_review_date)
      }

      // 移除自动跳转，让用户手动控制复习进度
      // 用户可以通过"下一题"按钮或Enter键手动切换到下一题

      return response
    } catch (error) {
      console.error('提交复习失败:', error)
      throw error
    }
  }

  // 手动切换到下一题
  const handleNextReview = () => {
    setNextReviewDate(null)
    if (currentReviewIndex < reviews.length - 1) {
      setCurrentReviewIndex(currentReviewIndex + 1)
      // 延迟聚焦，确保组件状态已重置
      setTimeout(() => {
        if (practiceCardRef.current) {
          practiceCardRef.current.focus()
        }
      }, 100)
    } else {
      // 所有复习任务完成，重新加载数据显示统计
      loadTodayReviews()
    }
  }

  // 加载今日复习任务
  useEffect(() => {
    loadTodayReviews()
  }, [])

  const loadTodayReviews = async () => {
    try {
      setLoading(true)
      const response = await reviewAPI.getTodayReviews()

      setReviews(response.reviews)
      setStats(response.stats)

      // 判断是否有待复习任务：优先使用stats.due_today，fallback到reviews.length
      const hasDueReviews = (response.stats?.due_today > 0) || (response.reviews.length > 0)

      if (!hasDueReviews) {
        // 没有复习任务，加载详细统计
        const statsResponse = await reviewAPI.getStats()
        setStats(statsResponse.stats)
        setShowStats(true)
      } else {
        // 有待复习任务，应该显示复习界面
        setReviews(response.reviews)
        setStats(response.stats)
      }
    } catch (error) {
      console.error('加载复习任务失败:', error)
    } finally {
      setLoading(false)
    }
  }



  if (loading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">{t('reviewPage.loadingReviews')}</p>
          </div>
        </div>
      </div>
    )
  }

  // 处理有待复习任务但无法加载具体内容的情况
  if (!showStats && reviews.length === 0 && stats?.due_today > 0) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">复习中心</h1>
          <p className="text-gray-600 dark:text-gray-400">基于SM-2算法的智能复习系统</p>
        </div>

        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6 mb-6">
          <div className="text-center">
            <div className="text-yellow-600 dark:text-yellow-400 text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-yellow-900 dark:text-yellow-100 mb-2">
              复习任务加载异常
            </h2>
            <p className="text-yellow-700 dark:text-yellow-300 mb-4">
              检测到有 {stats.due_today} 个待复习任务，但无法加载具体内容。
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-yellow-600 dark:bg-yellow-500 text-white px-4 py-2 rounded-lg hover:bg-yellow-700 dark:hover:bg-yellow-600 transition-colors"
            >
              刷新页面重试
            </button>
          </div>
        </div>
      </div>
    )
  }

  // 显示统计页面
  if (showStats) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            {t('reviewPage.reviewStats')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('reviewPage.sm2Description')}
          </p>
        </div>

        {reviews.length === 0 ? (
          <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 mb-6">
            <div className="text-center">
              <div className="text-green-600 dark:text-green-400 text-4xl mb-4">🎉</div>
              <h2 className="text-xl font-semibold text-green-900 dark:text-green-100 mb-2">
                {t('reviewPage.todayCompleted')}
              </h2>
              <p className="text-green-700 dark:text-green-300">
                {t('reviewPage.congratulations')}
              </p>
            </div>
          </div>
        ) : null}

        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
              <div className="text-blue-600 dark:text-blue-400 text-2xl mb-2">📚</div>
              <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">{stats.total_reviews}</div>
              <div className="text-base text-blue-700 dark:text-blue-300">{t('reviewPage.totalReviews')}</div>
            </div>

            <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6">
              <div className="text-orange-600 dark:text-orange-400 text-2xl mb-2">⏰</div>
              <div className="text-2xl font-bold text-orange-900 dark:text-orange-100">{stats.due_today}</div>
              <div className="text-base text-orange-700 dark:text-orange-300">{t('reviewPage.dueToday')}</div>
            </div>

            <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-6">
              <div className="text-purple-600 dark:text-purple-400 text-2xl mb-2">📈</div>
              <div className="text-2xl font-bold text-purple-900 dark:text-purple-100">{stats.accuracy_rate || 0}%</div>
              <div className="text-base text-purple-700 dark:text-purple-300">{t('reviewPage.accuracyRate')}</div>
            </div>

            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6">
              <div className="text-green-600 dark:text-green-400 text-2xl mb-2">🔥</div>
              <div className="text-2xl font-bold text-green-900 dark:text-green-100">{stats.week_completed || 0}</div>
              <div className="text-base text-green-700 dark:text-green-300">{t('reviewPage.weekCompleted')}</div>
            </div>
          </div>
        )}

        <div className="text-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {t('reviewPage.backToDashboard')}
          </button>
        </div>
      </div>
    )
  }

  // 显示复习练习
  const currentReview = reviews[currentReviewIndex]

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
              {t('reviewPage.todayReview')}
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              {t('reviewPage.forgettingCurveDescription')}
            </p>
          </div>
          <div className="text-right">
            <div className="text-base text-gray-500 dark:text-gray-400">{t('reviewPage.progress')}</div>
            <div className="text-lg font-semibold text-gray-900 dark:text-gray-100">
              {currentReviewIndex + 1} / {reviews.length}
            </div>
          </div>
        </div>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mt-4">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentReviewIndex + 1) / reviews.length) * 100}%` }}
          ></div>
        </div>
      </div>

      {/* 复习信息卡片 */}
      {currentReview && (
        <div className="mb-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div className="flex items-center gap-3">
            <div className="text-blue-600 dark:text-blue-400 text-xl">🔄</div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100">
                {t('reviewPage.reviewQuestion', { number: currentReviewIndex + 1 })}
              </h3>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-sm bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                  {currentReview.lesson_title}
                </span>
                <span className={`text-sm px-2 py-1 rounded ${
                  currentReview.difficulty === 'easy'
                    ? 'bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200'
                    : currentReview.difficulty === 'medium'
                    ? 'bg-yellow-100 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-200'
                    : 'bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-200'
                }`}>
                  {currentReview.difficulty === 'easy' ? t('practice.difficulty.easy') :
                   currentReview.difficulty === 'medium' ? t('practice.difficulty.medium') : t('practice.difficulty.hard')}
                </span>
              </div>
            </div>
            <div className="text-right text-sm text-gray-600 dark:text-gray-400">
              <p>📊 {t('reviewPage.repeated', { count: currentReview.repetitions || 1 })}</p>
              <p>🧠 {t('reviewPage.memoryStrength', { strength: currentReview.easiness_factor || 2.5 })}</p>
            </div>
          </div>
        </div>
      )}

      {/* 上一题提交后 SM-2 排出的下次复习时间 */}
      {nextReviewDate && (
        <div className="mb-6 rounded-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 px-4 py-3 text-sm text-green-800 dark:text-green-200">
          ⏰ {t('reviewPage.nextReview')}: {new Date(nextReviewDate).toLocaleDateString(i18n.language)}
        </div>
      )}

      {/* 使用PracticeCard组件进行复习练习 */}
      {currentReview && (
        <PracticeCard
          key={`review-${currentReview.review_id}-${currentReviewIndex}`}
          ref={practiceCardRef}
          exercise={adaptReviewDataToPracticeCard(currentReview)}
          lessonId="review"
          knowledgePointId="review"
          cardIndex={currentReviewIndex + 1}
          practiceIndex={currentReviewIndex + 1}
          isReviewMode={true}
          onComplete={(exerciseData, userAnswer, isCorrect) => {
            // 先提交答案
            handleReviewComplete(currentReview, userAnswer, isCorrect)
            // 然后切换到下一题
            handleNextReview()
          }}
        />
      )}

    </div>
  )
}

export default ReviewPage
