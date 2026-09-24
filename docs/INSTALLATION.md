# 📦 详细安装指南

本文档提供LaTeX速成训练器的详细安装和配置指南。

## 🔧 系统要求

### 最低要求
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **内存**: 4GB RAM
- **存储**: 2GB 可用空间
- **网络**: 用于下载依赖包

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **内存**: 8GB+ RAM
- **存储**: 5GB+ 可用空间
- **处理器**: 多核处理器

## 🛠️ 环境准备

### 1. Python 环境

#### Windows
```bash
# 下载并安装Python 3.8+
# 访问 https://python.org/downloads/
# 确保勾选 "Add Python to PATH"

# 验证安装
python --version
pip --version
```

#### macOS
```bash
# 使用Homebrew安装
brew install python

# 或下载官方安装包
# https://python.org/downloads/macos/

# 验证安装
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# 更新包列表
sudo apt update

# 安装Python和pip
sudo apt install python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

### 2. Node.js 环境

#### Windows
```bash
# 下载并安装Node.js 16+
# 访问 https://nodejs.org/

# 验证安装
node --version
npm --version
```

#### macOS
```bash
# 使用Homebrew安装
brew install node

# 验证安装
node --version
npm --version
```

#### Linux
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

### 3. MongoDB 数据库

#### Windows
```bash
# 下载MongoDB Community Server
# 访问 https://www.mongodb.com/try/download/community

# 安装后启动MongoDB服务
# 在服务管理器中启动MongoDB服务
```

#### macOS
```bash
# 使用Homebrew安装
brew tap mongodb/brew
brew install mongodb-community

# 启动MongoDB服务
brew services start mongodb-community
```

#### Linux
```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# 启动MongoDB服务
sudo systemctl start mongod
sudo systemctl enable mongod
```

## 📥 项目安装

### 1. 克隆项目
```bash
git clone https://github.com/prehisle/pipeak.git
cd pipeak
```

### 2. 后端安装

```bash
cd backend

# 创建虚拟环境 (推荐)
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量 (可选)
cp .env.example .env
# 编辑 .env 文件设置数据库连接等配置
```

### 3. 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 或使用yarn (如果已安装)
yarn install
```

## ⚙️ 配置说明

### 后端配置

创建 `backend/.env` 文件：

```env
# 数据库配置
MONGODB_URI=mongodb://localhost:27017/latex_trainer
MONGODB_DB=latex_trainer

# JWT配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
```

### 前端配置

创建 `frontend/.env` 文件：

```env
# API配置
VITE_API_BASE_URL=http://localhost:5000/api

# 开发配置
VITE_DEV_MODE=true
```

## ⚡ Windows 本地一键部署（便携 MongoDB，无需装服务）

仓库自带 `scripts/` 下的批处理脚本，会在 `.local/`（已 git 忽略）里放便携版 MongoDB 7.0.14 与数据目录，不动系统服务。

```bat
:: 1. 准备环境：下载解压 MongoDB、建 Python 3.10 虚拟环境装后端依赖、生成 backend\.env、装前端依赖
scripts\setup-local.cmd

:: 2. 启动数据库（保持窗口不关）
scripts\start-mongodb.cmd

:: 3. 启动后端（另开一个窗口）
scripts\start-backend.cmd

:: 4. 把 data\latex_bank.json 的题库写进数据库（另开一个窗口，只需在题库变化后重跑）
scripts\seed-db.cmd

:: 5. 启动前端（另开一个窗口）
scripts\start-frontend.cmd
```

`backend\.venv` 固定用 Python 3.10：`pymongo==4.1.1` 只有到 cp310 的 Windows wheel。

## 🚀 启动应用

### 开发模式

#### 1. 启动后端 (终端1)
```bash
cd backend
# 激活虚拟环境 (如果使用)
source venv/bin/activate  # macOS/Linux
# 或 venv\Scripts\activate  # Windows

python run.py
```

#### 2. 初始化题库 (终端2)
```bash
cd backend
python seed_db.py --reset
```
`seed_db.py` 从 `data/latex_bank.json`（题库唯一源头）读取 18 课的全部卡片与中英翻译，写进 MongoDB；`--reset` 会清空并重建课程、用户与练习记录。同一条逻辑也通过 `/api/reset-db`（仅开发环境）与 `/api/init-db`（生产首次部署，需 `INIT_DB_SECRET`）暴露。

#### 3. 启动前端 (终端3)
```bash
cd frontend
npm run dev
```

#### 4. 访问应用
- 前端: http://localhost:5173
- 后端API: http://localhost:5000

### 生产模式

#### 1. 构建前端
```bash
cd frontend
npm run build
```

#### 2. 配置生产环境
```bash
# 设置环境变量
export FLASK_ENV=production
export MONGODB_URI=mongodb://your-production-db

# 启动后端
cd backend
python run.py
```

## 🔍 故障排除

### 常见问题

#### 1. MongoDB连接失败
```bash
# 检查MongoDB服务状态
# Windows: 在服务管理器中查看
# macOS: brew services list | grep mongodb
# Linux: sudo systemctl status mongod

# 重启MongoDB服务
# Windows: 在服务管理器中重启
# macOS: brew services restart mongodb-community
# Linux: sudo systemctl restart mongod
```

#### 2. 端口占用
```bash
# 检查端口占用
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000

# 终止占用进程
# Windows: taskkill /PID <PID> /F
# macOS/Linux: kill -9 <PID>
```

#### 3. 依赖安装失败
```bash
# 清理npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install

# Python依赖问题
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📊 验证安装

### 1. 后端健康检查
```bash
curl http://localhost:5000/api/health
# 应返回: {"status": "healthy"}
```

### 2. 前端访问测试
访问 http://localhost:5173，应该看到登录页面

### 3. 数据库连接测试
```bash
# 在MongoDB shell中
mongo
> use latex_trainer
> db.stats()
```

## 🎯 下一步

安装完成后，您可以：

1. 注册新用户账户
2. 开始第一个LaTeX课程
3. 体验练习中心功能
4. 查看学习统计数据

如有问题，请查看 [故障排除指南](TROUBLESHOOTING.md) 或提交 [Issue](https://github.com/prehisle/pipeak/issues)。
