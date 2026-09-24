@echo off
chcp 65001 >nul
cd /d "%~dp0..\backend"
".venv\Scripts\python.exe" seed_db.py --reset