# OAuth 配置指南

本文档说明如何为 LaTeX 速成训练器配置 GitHub OAuth 登录。

## 🔧 配置步骤

### 1. 创建 GitHub OAuth App

1. 访问 [GitHub Developer Settings](https://github.com/settings/developers)
2. 点击 "New OAuth App"
3. 填写应用信息：
   - Application name：`LaTeX Speed Trainer`
   - Homepage URL：`http://localhost:5173`（开发环境）
   - Authorization callback URL：`http://localhost:5173/auth/callback`
4. 保存 Client ID 与 Client Secret

### 2. 配置环境变量

只需要配后端一处，前端会通过 `GET /api/auth/oauth/config` 读取 Client ID：

```bash
# backend/.env
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

授权时前端申请的 scope 为 `read:user user:email`，用于读取账号 ID、昵称、头像与主邮箱。

### 3. 生成加密密钥

如需加密存储 OAuth 访问令牌，先生成密钥：

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

```bash
# backend/.env
TOKEN_ENCRYPTION_KEY=your-generated-encryption-key
```

## 🚀 部署配置

1. **更新 OAuth App 设置**：把 Homepage URL 与 Authorization callback URL 换成生产域名
2. **环境变量**：
   ```bash
   OAUTH_REDIRECT_URI=https://yourdomain.com/auth/callback
   ```
3. **HTTPS**：生产环境必须使用 HTTPS，OAuth 提供商不接受明文回调

## 🔒 安全注意事项

1. **密钥保护**：不要在代码里硬编码 Client Secret，只放环境变量，并定期轮换
2. **回调地址校验**：只在 OAuth App 里登记可信回调地址，且必须与浏览器实际访问的源完全一致
3. **令牌管理**：JWT 访问令牌 24 小时过期，刷新令牌 30 天过期

## 🧪 测试

### 本地测试
1. 后端运行在 `http://localhost:5000`，前端运行在 `http://localhost:5173`
2. 访问 `http://localhost:5173/login`，点击「使用 GitHub 继续」
3. 未配置 Client ID 时按钮为禁用态，并在下方提示尚未配置

### 测试用例
- [ ] GitHub 登录成功
- [ ] 新用户自动注册
- [ ] 邮箱相同的既有账号完成绑定
- [ ] 错误处理（取消授权、网络错误、账号无可读邮箱）
- [ ] 登录表单中按回车提交邮箱密码登录，而不是触发 GitHub 跳转

## 🐛 常见问题

### 1. redirect_uri_mismatch
- 检查 OAuth App 中登记的回调地址与浏览器地址栏的协议、域名、端口是否完全一致
- 用 `127.0.0.1:5173` 访问时，回调地址也必须登记 `http://127.0.0.1:5173/auth/callback`

### 2. invalid_client
- 检查 `GITHUB_CLIENT_ID` 与 `GITHUB_CLIENT_SECRET` 是否填对
- 通过 `GET /api/auth/oauth/config` 确认 `github_configured` 为 `true`

### 3. GitHub 账号没有可读邮箱
- 授权时勾选邮箱权限，或在 GitHub 账号设置里公开一个邮箱
- 后端会返回 `GitHub account has no readable email`

### 4. CORS 错误
- 检查后端 `CORS_ORIGINS` 是否包含前端实际访问的源

## 📚 相关文档

- [GitHub OAuth 文档](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [Flask-JWT-Extended 文档](https://flask-jwt-extended.readthedocs.io/)