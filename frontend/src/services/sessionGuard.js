// 会话失效处理
// token 签名仍然有效、但其中的用户已经不在数据库里（例如重置题库时重建了用户行）时，
// 后端返回 404 + code=USER_NOT_FOUND。此时必须清除本地会话并回到登录页，
// 否则页面会停在「连接服务器失败」且没有任何恢复入口。

const IDENTITY_LOST_CODE = 'USER_NOT_FOUND'

export const isIdentityLost = (error) => error?.response?.data?.code === IDENTITY_LOST_CODE

export const handleIdentityLost = async () => {
  // 动态导入 authStore：authStore 依赖 services/api，静态导入会形成循环
  const { useAuthStore } = await import('../stores/authStore')

  useAuthStore.getState().logout()

  if (window.location.pathname !== '/login') {
    window.location.href = '/login'
  }
}