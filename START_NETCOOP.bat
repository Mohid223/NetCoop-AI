@echo off
title NetCoop AI - Offline Deployment
cd /d "%~dp0"

netstat -ano | findstr "127.0.0.1:8000" | findstr "LISTENING" >nul

if %errorlevel%==0 (
    echo NetCoop AI backend is already running.
) else (
    echo Starting NetCoop AI Backend...
    start "NetCoop AI Backend" cmd /k "python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000"
    timeout /t 4 /nobreak >nul
)

start "" http://127.0.0.1:8000
exit