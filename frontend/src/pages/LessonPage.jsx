import { useEffect, useState, useRef } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useDocumentTitle, PAGE_TITLES } from '../hooks/useDocumentTitle'
import useFrontendLessonStore from '../stores/frontendLessonStore'
import { useAuthStore } from '../stores/authStore'
import LoadingSpinner from '../components/LoadingSpinner'
import MarkdownRenderer from '../components/MarkdownRenderer'
import PracticeCard from '../components/PracticeCard'
import { useToast } from '../components/Toast'
import LessonCompleteModal from '../components/LessonCompleteModal'
import LessonSkeleton from '../components/LessonSkeleton'
import ResponsiveNavigation, { useDeviceType } from '../components/ResponsiveNavigation'
import { learningAPI } from '../services/api'

const LessonPage = () => {
  const { lessonId } = useParams()
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()
  const [currentCardIndex, setCurrentCardIndex] = useState(0)
  const [isTransitioning, setIsTransitioning] = useState(false)
  const [showLessonCompleteModal, setShowLessonCompleteModal] = useState(false)

  // 检查是否是复习模式（通过URL查询参数）
  const urlParams = new URLSearchParams(window.location.search)
  const isReviewMode = urlParams.get('mode') === 'review'

  // Toast系统
  const { showSuccess, showError, showWarning, ToastContainer } = useToast()

  // PracticeCard引用，用于自动聚焦
  const practiceCardRef = useRef(null)

  // 设备类型检测
  const deviceType = useDeviceType()

  // 认证状态
  const { user } = useAuthStore()
  const isLoggedIn = !!user

  const {
    lessons,
    currentLesson,
    currentKnowledgePointIndex,
    fetchLessons,
    setCurrentLesson,
    setCurrentKnowledgePointIndex,
    completeKnowledgePoint,
    completeLesson,
    isLessonCompleted,
    isKnowledgePointCompleted,
    getLessonProgress,
    isLoading,
    error
  } = useFrontendLessonStore()

  // 设置动态页面标题
  useDocumentTitle(PAGE_TITLES.LESSON, {
    lessonTitle: currentLesson?.title || t('common.loading')
  })

  // 初始化课程数据
  useEffect(() => {
    fetchLessons()
  }, []) // 移除fetchLessons依赖，避免重复执行

  // 监听语言变化并更新课程内容
  useEffect(() => {
    const { setLanguage } = useFrontendLessonStore.getState()
    setLanguage(i18n.language)
  }, [i18n.language])

  // 设置当前课程 - 确保课程数据加载完成后再查找
  useEffect(() => {
    if (lessonId && lessons && lessons.length > 0) {
      // 检查是否是同一个课程的数据刷新（如语言切换）
      const isSameLessonRefresh = currentLesson && currentLesson.id === lessonId
      setCurrentLesson(lessonId, isSameLessonRefresh) // 如果是同一课程刷新，保持知识点索引
    }
  }, [lessonId, lessons, setCurrentLesson, currentLesson])

  // 键盘导航支持
  useEffect(() => {
    const handleNextKnowledgePoint = () => {
      if (currentLesson && currentKnowledgePointIndex < currentLesson.knowledgePoints.length - 1 && !isTransitioning) {
        setIsTransitioning(true)
        setTimeout(() => {
          setCurrentKnowledgePointIndex(currentKnowledgePointIndex + 1)
          setIsTransitioning(false)
        }, 150)
      }
    }

    const handlePrevKnowledgePoint = () => {
      if (currentKnowledgePointIndex > 0 && !isTransitioning) {
        setIsTransitioning(true)
        setTimeout(() => {
          setCurrentKnowledgePointIndex(currentKnowledgePointIndex - 1)
          setIsTransitioning(false)
        }, 150)
      }
    }

    const handleKeyPress = (event) => {
      if (!currentLesson) return

      // 检查是否在输入框中，如果是则不处理导航键
      const activeElement = document.activeElement
      const isInInput = activeElement && (
        activeElement.tagName === 'INPUT' ||
        activeElement.tagName === 'TEXTAREA' ||
        activeElement.contentEditable === 'true'
      )

      // 检查输入框是否为只读状态（练习题已完成）
      const isReadOnly = activeElement && activeElement.readOnly

      // 按钮与链接的回车由控件自身触发点击，避免与下面的导航重复推进
      const isOnControl = activeElement && (activeElement.tagName === 'BUTTON' || activeElement.tagName === 'A')

      // 如果用户正在输入（非只读状态），只处理 Escape 键
      if (isInInput && !isReadOnly && event.key !== 'Escape') {
        return
      }

      switch (event.key) {
        case 'ArrowLeft':
          event.preventDefault()
          handlePrevKnowledgePoint()
          break
        case 'ArrowRight':
          event.preventDefault()
          handleNextKnowledgePoint()
          break
        case 'Enter':
          // 知识点卡片上没有输入控件，回车直接进入下一个知识点
          if (isInInput || isOnControl) {
            return
          }
          event.preventDefault()
          handleNextKnowledgePoint()
          break
        case 'Escape':
          event.preventDefault()
          // 如果在输入框中，先失焦，否则返回课程列表
          if (isInInput) {
            activeElement.blur()
          } else {
            navigate('/dashboard')
          }
          break
      }
    }

    window.addEventListener('keydown', handleKeyPress)
    return () => window.removeEventListener('keydown', handleKeyPress)
  }, [currentLesson, currentKnowledgePointIndex, isTransitioning, setCurrentKnowledgePointIndex, navigate])

  const handleNextKnowledgePoint = () => {
    if (currentLesson && currentKnowledgePointIndex < currentLesson.knowledgePoints.length - 1 && !isTransitioning) {
      setIsTransitioning(true)
      setTimeout(() => {
        setCurrentKnowledgePointIndex(currentKnowledgePointIndex + 1)
        setIsTransitioning(false)
      }, 150)
    }
  }

  const handlePrevKnowledgePoint = () => {
    if (currentKnowledgePointIndex > 0 && !isTransitioning) {
      setIsTransitioning(true)
      setTimeout(() => {
        setCurrentKnowledgePointIndex(currentKnowledgePointIndex - 1)
        setIsTransitioning(false)
      }, 150)
    }
  }

  const handleKnowledgePointClick = (index) => {
    if (index !== currentKnowledgePointIndex && !isTransitioning) {
      setIsTransitioning(true)
      setTimeout(() => {
        setCurrentKnowledgePointIndex(index)
        setIsTransitioning(false)
      }, 150)
    }
  }

  const handlePracticeComplete = (isCorrect, immediate = false) => {
    // 复习模式下不更新进度，不检查课程完成
    if (isReviewMode) {
      if (immediate) {
        // 复习模式下仍然支持Enter键切换到下一题
        handleNextKnowledgePoint()
      }
      return
    }

    // 学习模式下的正常逻辑
    if (isCorrect && currentLesson) {
      const currentKnowledgePoint = currentLesson.knowledgePoints[currentKnowledgePointIndex]
      if (currentKnowledgePoint) {
        // 标记知识点为已完成
        completeKnowledgePoint(currentLesson.id, currentKnowledgePoint.id)
        // 删除"知识点完成！"提示，避免频繁打断用户学习体验

        // 检查是否应该完成整个课程
        setTimeout(async () => {
          await checkAndCompleteLesson()
        }, 500) // 稍微延迟以确保状态更新完成
      }

      if (immediate) {
        // 立即进入下一个知识点（用户按Enter键触发）
        handleNextKnowledgePoint()
      }
      // 移除自动跳转逻辑，让用户主动控制学习进度
    }
  }

  // 检查并自动完成课程
  const checkAndCompleteLesson = async () => {
    if (!currentLesson) return

    // 统计课程中的所有练习题（仅登录用户）
    let totalPractices = 0
    let completedPractices = 0

    try {
      const response = await learningAPI.getCompletionStatus(currentLesson.id)
      const completionStatus = response.data

      // 使用后端返回的统计数据
      totalPractices = completionStatus.total_practices || 0
      completedPractices = completionStatus.completed_practices || 0
    } catch (error) {
      console.error('获取课程完成状态失败:', error)
      showError('获取课程完成状态失败')
      return
    }

    if (completedPractices === totalPractices && totalPractices > 0) {
      // 所有练习题都已完成，自动完成课程
      completeLesson(currentLesson.id)
      showSuccess(t('lessonPage.lessonCompleted'))
      setShowLessonCompleteModal(true)

      // 尝试同步到后端（失败也不影响前端流程）
      try {
        import('../services/api').then(({ learningAPI }) => {
          learningAPI.completeLesson(currentLesson.id).catch((error) => {
            console.error('同步课程完成状态到后端失败:', error)
          })
        })
      } catch (error) {
        console.error('导入API模块失败:', error)
      }
    }
  }

  // 处理课程完成 - 基于后端状态检查所有练习题是否完成
  const handleCompleteLesson = async () => {
    if (!currentLesson) return

    // 复习模式下不允许完成课程
    if (isReviewMode) {
      navigate('/app/dashboard')
      return
    }

    // 统计课程中的所有练习题（仅登录用户）
    let totalPractices = 0
    let completedPractices = 0

    try {
      const response = await learningAPI.getCompletionStatus(currentLesson.id)
      const completionStatus = response.data

      // 使用后端返回的统计数据
      totalPractices = completionStatus.total_practices || 0
      completedPractices = completionStatus.completed_practices || 0
    } catch (error) {
      console.error('获取课程完成状态失败:', error)
      showError('获取课程完成状态失败')
      return
    }

    if (completedPractices === totalPractices) {
      // 所有练习题都已完成，可以完成课程
      completeLesson(currentLesson.id)
      showSuccess(t('lessonPage.lessonCompleted'))
      setShowLessonCompleteModal(true)

      // 尝试同步到后端（失败也不影响前端流程）
      try {
        const { learningAPI } = await import('../services/api')
        await learningAPI.completeLesson(currentLesson.id)
      } catch (error) {
        console.error('同步课程完成状态到后端失败:', error)
        // 不显示错误，因为前端流程已经完成
      }
    } else {
      // 还有练习题未完成
      showWarning(`请先完成所有练习题！已完成 ${completedPractices}/${totalPractices} 题`)
    }
  }



  // 处理课程完成模态框
  const handleLessonCompleteClose = () => {
    setShowLessonCompleteModal(false)
  }

  const handleLessonCompleteContinue = () => {
    setShowLessonCompleteModal(false)
    navigate('/app/dashboard')
  }

  if (!currentLesson) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">{t('common.courseNotFound')}</p>
          <Link to="/app/dashboard" className="btn btn-primary mt-4">
            {t('lessonPage.backToDashboard')}
          </Link>
        </div>
      </div>
    )
  }

  const currentKnowledgePoint = currentLesson.knowledgePoints[currentKnowledgePointIndex]
  const isLastKnowledgePoint = currentKnowledgePointIndex === currentLesson.knowledgePoints.length - 1

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* 课程头部 */}
      <div className="mb-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3 space-y-2 sm:space-y-0">
          <Link
            to="/app/dashboard"
            className="text-blue-600 hover:text-blue-700 flex items-center text-sm"
          >
            {t('lessonPage.backToDashboard')}
          </Link>
          {isLessonCompleted(currentLesson.id) && (
            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
              {t('dashboard.mastered')}
            </span>
          )}
        </div>

        <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {currentLesson.title}
        </h1>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
          {currentLesson.description}
        </p>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5">
          <div
            className="bg-blue-600 h-1.5 rounded-full transition-all duration-300"
            style={{
              width: `${((currentKnowledgePointIndex + 1) / currentLesson.knowledgePoints.length) * 100}%`
            }}
          ></div>
        </div>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          {t('lessonPage.progress', { current: currentKnowledgePointIndex + 1, total: currentLesson.knowledgePoints.length })}
        </p>
      </div>

      {/* 知识点内容卡片 */}
      {currentKnowledgePoint && (
        <div className={`card mb-4 transition-all duration-300 ${isTransitioning ? 'opacity-50 scale-95' : 'opacity-100 scale-100'}`}>
          <div className="card-body">
            {/* 只对非练习题类型显示蓝色知识点区域 */}
            {!(currentKnowledgePoint.exercises && currentKnowledgePoint.exercises.length > 0) && (
              <div className="prose max-w-none">
                <div className="bg-blue-50 dark:bg-blue-900/20 border-l-4 border-blue-400 dark:border-blue-600 p-6 rounded-r-lg">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <div className="w-8 h-8 bg-blue-100 dark:bg-blue-800 rounded-full flex items-center justify-center">
                        <span className="text-blue-600 dark:text-blue-400 font-semibold text-sm">💡</span>
                      </div>
                    </div>
                    <div className="ml-4 flex-1 min-w-0">
                      <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-6">
                        {currentKnowledgePoint.titleKey ? t(currentKnowledgePoint.titleKey) : currentKnowledgePoint.title}
                      </h3>
                      <div className="text-blue-800 dark:text-blue-200 text-base leading-relaxed overflow-visible">
                        <MarkdownRenderer content={currentKnowledgePoint.contentKey ? t(currentKnowledgePoint.contentKey) : currentKnowledgePoint.content} theme="default" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 练习题部分 - 直接显示练习内容，无蓝色卡片包装 */}
            {currentKnowledgePoint.exercises && currentKnowledgePoint.exercises.length > 0 && (
              <div className="space-y-4">
                {currentKnowledgePoint.exercises.map((exercise, index) => {
                  // 计算当前练习题在整个课程中的序号（用于显示）- 与导航按钮逻辑保持一致
                  let practiceIndex = 0;
                  for (let i = 0; i < currentKnowledgePointIndex; i++) {
                    if (currentLesson.knowledgePoints[i].exercises && currentLesson.knowledgePoints[i].exercises.length > 0) {
                      practiceIndex++;
                    }
                  }
                  practiceIndex++; // 当前练习题的编号

                  // 计算当前练习题在后端课程卡片数组中的实际索引
                  // 前端knowledgePoints索引 = 后端cards索引（因为转换时保持了顺序）
                  let cardIndex = currentKnowledgePointIndex;

                  return (
                    <PracticeCard
                      key={`${index}-${isReviewMode ? 'review' : 'normal'}`}
                      ref={practiceCardRef}
                      exercise={exercise}
                      lessonId={currentLesson.id}
                      knowledgePointId={currentKnowledgePoint.id}
                      cardIndex={cardIndex}
                      practiceIndex={practiceIndex}
                      isReviewMode={isReviewMode}
                      onComplete={handlePracticeComplete}
                    />
                  );
                })}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 响应式导航 */}
      <div className="mb-6">
        <ResponsiveNavigation
          items={currentLesson.knowledgePoints.map((kp, index) => {
            // 判断是否为练习题类型
            const isPractice = kp.exercises && kp.exercises.length > 0

            let title
            if (isPractice) {
              // 计算这是第几个练习题（相对编号）
              let practiceIndex = 0
              for (let i = 0; i <= index; i++) {
                if (currentLesson.knowledgePoints[i].exercises && currentLesson.knowledgePoints[i].exercises.length > 0) {
                  practiceIndex++
                }
              }
              title = t('lessonPage.practiceExercise', { index: practiceIndex })
            } else {
              // 计算这是第几个知识点（相对编号）
              let knowledgeIndex = 0
              for (let i = 0; i <= index; i++) {
                if (!(currentLesson.knowledgePoints[i].exercises && currentLesson.knowledgePoints[i].exercises.length > 0)) {
                  knowledgeIndex++
                }
              }
              title = t('lessonPage.knowledgePoint', { index: knowledgeIndex })
            }

            return {
              title,
              subtitle: kp.title
            }
          })}
          currentIndex={currentKnowledgePointIndex}
          onChange={handleKnowledgePointClick}
        />
      </div>

      {/* 导航按钮 */}
      <div className="flex items-center justify-between">
        <button
          onClick={handlePrevKnowledgePoint}
          disabled={currentKnowledgePointIndex === 0 || isTransitioning}
          className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {t('lessonPage.prevKnowledgePoint')}
        </button>

        {isLastKnowledgePoint ? (
          isReviewMode ? (
            <button
              onClick={() => navigate('/app/dashboard')}
              disabled={isTransitioning}
              className="btn btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              结束复习 ✓
            </button>
          ) : (
            <button
              onClick={handleCompleteLesson}
              disabled={isTransitioning}
              className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {t('lessonPage.lessonCompleted')} ✓
            </button>
          )
        ) : (
          <button
            onClick={handleNextKnowledgePoint}
            disabled={currentKnowledgePointIndex === currentLesson.knowledgePoints.length - 1 || isTransitioning}
            className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {t('lessonPage.nextKnowledgePoint')}
          </button>
        )}
      </div>

      {/* 设备感知的交互提示 */}
      <div className="mt-6 text-center text-base text-gray-500 dark:text-gray-400">
        {deviceType === 'mobile' ? (
          <p>{t('lessonPage.swipeHint')}</p>
        ) : (
          <p>{t('lessonPage.keyboardShortcuts')}</p>
        )}
      </div>




      {/* 课程完成模态框 */}
      <LessonCompleteModal
        isOpen={showLessonCompleteModal}
        onClose={handleLessonCompleteClose}
        lessonTitle={currentLesson?.title}
        onContinue={handleLessonCompleteContinue}
      />

      {/* Toast容器 */}
      <ToastContainer />
    </div>
  )
}

export default LessonPage
