@echo off
chcp 65001 > nul
echo ========================================================
echo   스마트 산업안전보건 통합관제 대시보드 실행기
echo ========================================================
echo.
echo 1. 웹 대시보드 서버를 시작합니다...
echo 2. 접속 주소: http://localhost:8080
echo.

start "" "http://localhost:8080"
python server.py 8080
pause

