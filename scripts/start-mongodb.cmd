@echo off
chcp 65001 >nul
cd /d "%~dp0.."
".local\mongodb-win32-x86_64-windows-7.0.14\bin\mongod.exe" --dbpath "%CD%\.local\mongodb-data" --port 27017 --bind_ip 127.0.0.1