@echo off
chcp 65001 >nul
cd /d "%~dp0.."
rem diagnosticDataCollectionEnabled=false: the FTDC thread rotates files by renaming them
rem under diagnostic.data, and a denied rename on Windows kills mongod outright
rem (observed: FileRenameFailed -> unhandled exception -> exit 14). Diagnostics only.
".local\mongodb-win32-x86_64-windows-7.0.14\bin\mongod.exe" --dbpath "%CD%\.local\mongodb-data" --port 27017 --bind_ip 127.0.0.1 --setParameter diagnosticDataCollectionEnabled=false