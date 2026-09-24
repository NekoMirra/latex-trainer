import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'

// 后端配置探查地址：client_id 属于公开信息，OAuth 配置只放在后端 .env 一处
const getApiBaseUrl = () => import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

const GitHubLoginButton = ({ className = '' }) => {
  const { t } = useTranslation()
  const [clientId, setClientId] = useState('')
  const [isConfigured, setIsConfigured] = useState(false)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    fetch(`${getApiBaseUrl()}/auth/oauth/config`)
      .then((response) => (response.ok ? response.json() : null))
      .then((config) => {
        if (cancelled) return
        setClientId(config?.github_client_id || '')
        // 缺少 client secret 时授权码无法兑换，直接置为不可用，避免跳到 GitHub 再失败
        setIsConfigured(Boolean(config?.github_configured))
      })
      .catch(() => {
        if (cancelled) return
        setClientId('')
        setIsConfigured(false)
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [])

  const handleGitHubLogin = () => {
    if (!clientId || !isConfigured) return

    const authUrl = new URL('https://github.com/login/oauth/authorize')
    authUrl.searchParams.set('client_id', clientId)
    authUrl.searchParams.set('redirect_uri', `${window.location.origin}/auth/callback`)
    authUrl.searchParams.set('scope', 'read:user user:email')
    authUrl.searchParams.set('state', 'github')

    // 登录成功后回到当前页面
    sessionStorage.setItem('oauth_redirect', window.location.pathname)
    window.location.href = authUrl.toString()
  }

  const isDisabled = isLoading || !isConfigured

  return (
    <div className="space-y-1">
      <button
        // 必须是 button：表单里的默认提交按钮会被输入框的回车触发，导致回车误跳 OAuth
        type="button"
        onClick={handleGitHubLogin}
        disabled={isDisabled}
        className={`flex w-full items-center justify-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin mr-2"></div>
        ) : (
          <svg className="w-5 h-5 mr-2" viewBox="0 0 16 16" aria-hidden="true">
            <path
              fill="currentColor"
              d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"
            />
          </svg>
        )}
        {isLoading ? t('common.loading') : t('auth.continueWithGitHub')}
      </button>

      {!isLoading && !isConfigured && (
        <p className="text-xs text-gray-500 dark:text-gray-400">{t('auth.githubNotConfigured')}</p>
      )}
    </div>
  )
}

export default GitHubLoginButton