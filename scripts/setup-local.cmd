@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo [1/6] 检查便携版 MongoDB 压缩包
if not exist ".local\mongodb.zip" (
  curl -L --ssl-no-revoke -C - -o ".local\mongodb.zip" https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14.zip
) else (
  echo   已存在 .local\mongodb.zip，跳过下载
)

echo [2/6] 解压 MongoDB
if not exist ".local\mongodb-win32-x86_64-windows-7.0.14\bin\mongod.exe" (
  python -c "import zipfile;z=zipfile.ZipFile('.local/mongodb.zip');print(z.testzip());z.extractall('.local')"
) else (
  echo   已解压，跳过
)
if not exist ".local\mongodb-data" mkdir ".local\mongodb-data"

echo [3/6] 准备后端虚拟环境（Python 3.10）
if not exist "backend\.venv\Scripts\python.exe" (
  uv venv --python 3.10 backend/.venv
  uv pip install --python backend/.venv/Scripts/python.exe -r backend/requirements.txt
) else (
  echo   已存在 backend\.venv，跳过
)

echo [4/6] 生成 backend\.env
if not exist "backend\.env" (
  copy "backend\.env.example" "backend\.env" >nul
) else (
  echo   已存在 backend\.env，跳过
)

echo [5/6] 安装前端依赖
if not exist "frontend\node_modules" (
  pushd "%~dp0..\frontend"
  call npm install
  popd
) else (
  echo   已存在 frontend\node_modules，跳过
)

echo [6/6] 环境就绪，依次运行：
echo   scripts\start-mongodb.cmd
echo   scripts\start-backend.cmd
echo   scripts\seed-db.cmd
echo   scripts\start-frontend.cmd