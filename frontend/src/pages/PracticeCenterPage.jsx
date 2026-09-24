import { useState, useEffect, useMemo, useCallback } from 'react'
import { useTranslation } from 'react-i18next'
import { practiceAPI } from '../services/api'
import PracticeCard from '../components/PracticeCard'
import LoadingSpinner from '../components/LoadingSpinner'

// 难度筛选项（与后端 difficulty 取值一致）
const DIFFICULTY_OPTIONS = ['easy', 'medium', 'hard']
// 「随机开始」生成的队列长度
const RANDOM_QUEUE_SIZE = 10

// 难度徽章样式（与复习页保持同款配色）
const difficultyBadgeClass = (difficulty) => {
  if (difficulty === 'easy') {
    return 'bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200'
  }
  if (difficulty === 'medium') {
    return 'bg-yellow-100 dark:bg-yellow-800 text-yellow-800 dark:text-yellow-200'
  }
  return 'bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-200'
}

const PracticeCenterPage = () => {
  const { t, i18n } = useTranslation()

  // 全量练习数据与统计
  const [practices, setPractices] = useState([])
  const [total, setTotal] = useState(0)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // 筛选条件
  const [courseFilter, setCourseFilter] = useState('all')
  const [difficultyFilter, setDifficultyFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')
  const [keyword, setKeyword] = useState('')

  // 练习队列（null 表示处于列表视图）
  const [queue, setQueue] = useState(null)
  const [currentIndex, setCurrentIndex] = useState(0)

  // 拉取练习列表与统计
  const loadData = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const [listData, statsData] = await Promise.all([
        practiceAPI.getPractices(),
        practiceAPI.getStats()
      ])
      setPractices(listData?.practices || [])
      setTotal(listData?.total || 0)
      setStats(statsData)
    } catch (err) {
      console.error('加载练习数据失败:', err)
      setError(err?.message || String(err))
    } finally {
      setLoading(false)
    }
  }, [i18n.language])

  // 切换语言时后端返回的题干与课程名会换语言，需要重新拉取
  useEffect(() => {
    loadData()
  }, [loadData])

  // 按 lesson_id 去重枚举课程，供课程下拉使用
  const courses = useMemo(() => {
    const seen = new Map()
    for (const item of practices) {
      if (!seen.has(item.lesson_id)) {
        seen.set(item.lesson_id, item.lesson_title)
      }
    }
    return Array.from(seen, ([id, title]) => ({ id, title }))
  }, [practices])

  // 前端过滤：课程 / 难度 / 完成状态 / 关键词（匹配题干与课程名）
  const filtered = useMemo(() => {
    const kw = keyword.trim().toLowerCase()
    return practices.filter((item) => {
      if (courseFilter !== 'all' && item.lesson_id !== courseFilter) return false
      if (difficultyFilter !== 'all' && item.difficulty !== difficultyFilter) return false
      if (statusFilter === 'completed' && !item.completed) return false
      if (statusFilter === 'incomplete' && item.completed) return false
      if (kw) {
        const haystack = `${item.question || ''} ${item.lesson_title || ''}`.toLowerCase()
        if (!haystack.includes(kw)) return false
      }
      return true
    })
  }, [practices, courseFilter, difficultyFilter, statusFilter, keyword])

  // 返回列表并刷新完成状态与统计
  const backToList = useCallback(() => {
    setQueue(null)
    setCurrentIndex(0)
    loadData()
  }, [loadData])

  // 推进到队列下一项；队列末尾则返回列表
  const goNext = useCallback(() => {
    if (!queue) return
    if (currentIndex < queue.length - 1) {
      setCurrentIndex(currentIndex + 1)
    } else {
      backToList()
    }
  }, [queue, currentIndex, backToList])

  // 从列表点开某题：队列 = 当前筛选结果，从该题开始
  const startFromItem = (item) => {
    if (filtered.length === 0) return
    const index = filtered.findIndex((p) => p.id === item.id)
    setQueue(filtered)
    setCurrentIndex(index >= 0 ? index : 0)
  }

  // 随机开始：从当前筛选结果中乱序抽取至多 RANDOM_QUEUE_SIZE 题
  const startRandom = () => {
    if (filtered.length === 0) return
    const shuffled = [...filtered]
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
    }
    setQueue(shuffled.slice(0, RANDOM_QUEUE_SIZE))
    setCurrentIndex(0)
  }

  // ============ 练习视图 ============
  if (queue) {
    const currentItem = queue[currentIndex]

    if (!currentItem) {
      return (
        <div className="max-w-4xl mx-auto">
          <button
            onClick={backToList}
            className="mb-6 text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            {t('practiceCenter.backToList')}
          </button>
          <div className="card">
            <div className="card-body text-center text-gray-600 dark:text-gray-400">
              {t('practiceCenter.empty')}
            </div>
          </div>
        </div>
      )
    }

    return (
      <div className="max-w-4xl mx-auto">
        {/* 顶部：返回列表 + 进度 */}
        <div className="mb-6 flex items-center justify-between">
          <button
            onClick={backToList}
            className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
          >
            {t('practiceCenter.backToList')}
          </button>
          <div className="text-right">
            <div className="text-base text-gray-500 dark:text-gray-400">
              {t('practiceCenter.progressLabel', { current: currentIndex + 1, total: queue.length })}
            </div>
          </div>
        </div>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2 mb-6">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / queue.length) * 100}%` }}
          ></div>
        </div>

        {/* 题目信息 */}
        <div className="mb-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
              {currentItem.lesson_title}
            </span>
            <span className={`text-sm px-2 py-1 rounded ${difficultyBadgeClass(currentItem.difficulty)}`}>
              {t(`practice.difficulty.${currentItem.difficulty}`)}
            </span>
            {currentItem.completed && (
              <span className="text-sm bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 px-2 py-1 rounded">
                {t('learning.completed')}
              </span>
            )}
          </div>
        </div>

        {/* 练习卡片（非复习模式，走既有后端记录路径） */}
        <PracticeCard
          key={`${currentItem.id}-${currentIndex}`}
          exercise={{
            question: currentItem.question,
            target_formula: currentItem.target_formula,
            hints: currentItem.hints || [],
            difficulty: currentItem.difficulty
          }}
          lessonId={currentItem.lesson_id}
          cardIndex={currentItem.card_index}
          practiceIndex={currentIndex + 1}
          onComplete={() => goNext()}
        />

        {/* 下一题按钮 */}
        <div className="mt-6 flex justify-end">
          <button onClick={goNext} className="btn btn-primary">
            {t('practiceCenter.nextQuestion')}
          </button>
        </div>
      </div>
    )
  }

  // ============ 列表视图 ============
  return (
    <div className="max-w-6xl mx-auto">
      {/* 页面标题 */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
          {t('practiceCenter.title')}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">{t('practiceCenter.subtitle')}</p>
      </div>

      {/* 顶部统计 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 mb-6 md:mb-8">
        <div className="card">
          <div className="card-body text-center">
            <div className="text-2xl md:text-3xl font-bold text-blue-600 mb-2">{total}</div>
            <div className="text-sm md:text-base text-gray-600 dark:text-gray-300 font-medium">
              {t('practiceCenter.statsTotal')}
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-2xl md:text-3xl font-bold text-green-600 mb-2">
              {stats?.correct_count || 0}
            </div>
            <div className="text-sm md:text-base text-gray-600 dark:text-gray-300 font-medium">
              {t('practiceCenter.statsCompleted')}
            </div>
          </div>
        </div>
        <div className="card">
          <div className="card-body text-center">
            <div className="text-2xl md:text-3xl font-bold text-orange-600 mb-2">
              {Number(stats?.accuracy_rate || 0).toFixed(1)}%
            </div>
            <div className="text-sm md:text-base text-gray-600 dark:text-gray-300 font-medium">
              {t('practiceCenter.statsAccuracy')}
            </div>
          </div>
        </div>
      </div>

      {/* 筛选区 */}
      <div className="card mb-6">
        <div className="card-body">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('practiceCenter.filterCourse')}
              </label>
              <select
                value={courseFilter}
                onChange={(e) => setCourseFilter(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
              >
                <option value="all">{t('practiceCenter.allOption')}</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>
                    {course.title}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('practiceCenter.filterDifficulty')}
              </label>
              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
              >
                <option value="all">{t('practiceCenter.allOption')}</option>
                {DIFFICULTY_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {t(`practice.difficulty.${option}`)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('practiceCenter.filterStatus')}
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
              >
                <option value="all">{t('practiceCenter.allOption')}</option>
                <option value="completed">{t('learning.completed')}</option>
                <option value="incomplete">{t('learning.notStarted')}</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                {t('common.search')}
              </label>
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder={t('practiceCenter.searchPlaceholder')}
                className="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
              />
            </div>
          </div>

          <div className="mt-4 flex items-center justify-between">
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {t('practiceCenter.progressLabel', { current: filtered.length, total })}
            </span>
            <button
              onClick={startRandom}
              disabled={filtered.length === 0}
              className="btn btn-primary"
            >
              {t('practiceCenter.randomStart')}
            </button>
          </div>
        </div>
      </div>

      {/* 加载态 */}
      {loading && (
        <div className="card">
          <div className="card-body flex flex-col items-center justify-center py-12 gap-3">
            <LoadingSpinner size="lg" className="text-blue-600" />
            <span className="text-gray-600 dark:text-gray-400">{t('practiceCenter.loading')}</span>
          </div>
        </div>
      )}

      {/* 错误态 */}
      {!loading && error && (
        <div className="card">
          <div className="card-body text-center py-12">
            <p className="text-red-600 dark:text-red-400 mb-4">{t('common.error')}: {error}</p>
            <button onClick={loadData} className="btn btn-secondary">
              {t('lesson.tryAgain')}
            </button>
          </div>
        </div>
      )}

      {/* 空状态 */}
      {!loading && !error && filtered.length === 0 && (
        <div className="card">
          <div className="card-body text-center py-12 text-gray-600 dark:text-gray-400">
            {t('practiceCenter.empty')}
          </div>
        </div>
      )}

      {/* 练习列表 */}
      {!loading && !error && filtered.length > 0 && (
        <div className="card">
          <div className="divide-y divide-gray-200 dark:divide-gray-700">
            {filtered.map((item) => (
              <button
                key={item.id}
                onClick={() => startFromItem(item)}
                className="w-full text-left px-4 md:px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex-1 min-w-0">
                    <p className="text-base text-gray-900 dark:text-gray-100 truncate">
                      {item.question}
                    </p>
                    <div className="mt-2 flex flex-wrap items-center gap-2 text-xs">
                      <span className="bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded">
                        {item.lesson_title}
                      </span>
                      <span className={`px-2 py-0.5 rounded ${difficultyBadgeClass(item.difficulty)}`}>
                        {t(`practice.difficulty.${item.difficulty}`)}
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        {t('practiceCenter.attempts', { count: item.attempts || 0 })}
                      </span>
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    {item.completed ? (
                      <span className="text-sm bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 px-2 py-1 rounded">
                        {t('learning.completed')}
                      </span>
                    ) : (
                      <span className="text-sm bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-2 py-1 rounded">
                        {t('learning.notStarted')}
                      </span>
                    )}
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default PracticeCenterPage
