#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스마트 산업안전보건 통합관제 대시보드 (Smart Safety & Health Dashboard)
외부 패키지 설치 없이 파이썬 표준 라이브러리만으로 동작하는 웹 서버입니다.
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse
from datetime import datetime

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(DIRECTORY, "safety_data.json")

# 초기 기본 데이터
DEFAULT_DATA = {
    "site_info": {
        "company_name": "스마트 스마트안전보건 관제센터",
        "current_site": "전체 사업장 (제1공장, 제2공장, 물류센터)",
        "zero_accident_days": 285,
        "target_days": 365,
        "target_multiplier": "2배 달성 도전 중",
        "last_accident_date": "2025-01-25",
        "safety_level": "우수 (Green)",
        "workers_today": 342,
        "safety_patrol_active": True
    },
    "kpis": {
        "accident_rate": {"value": "0.00%", "diff": "-0.12%", "status": "good", "label": "도수율 (재해율)"},
        "risk_action_rate": {"value": "96.4%", "diff": "+2.1%", "status": "good", "label": "위험성평가 조치율"},
        "inspection_rate": {"value": "98.2%", "diff": "+0.5%", "status": "good", "label": "정기 안전점검 이행률"},
        "training_rate": {"value": "100%", "diff": "0.0%", "status": "good", "label": "법정 안전보건교육 이수율"}
    },
    "monthly_stats": {
        "labels": ["6월", "7월", "8월", "9월", "10월", "11월"],
        "accidents": [0, 0, 0, 0, 0, 0],
        "near_misses": [4, 6, 3, 5, 2, 1],
        "safety_suggestions": [12, 15, 18, 22, 19, 14]
    },
    "risk_types": [
        {"name": "끼임/협착", "count": 14, "percentage": 28, "color": "#ef4444"},
        {"name": "추락/낙하", "count": 10, "percentage": 20, "color": "#f97316"},
        {"name": "넘어짐/전도", "count": 9, "percentage": 18, "color": "#f59e0b"},
        {"name": "화학물질/가스", "count": 7, "percentage": 14, "color": "#3b82f6"},
        {"name": "근골격계/과부하", "count": 6, "percentage": 12, "color": "#10b981"},
        {"name": "감전/화재", "count": 4, "percentage": 8, "color": "#8b5cf6"}
    ],
    "near_miss_reports": [
        {
            "id": 1,
            "date": "2026-11-05 14:20",
            "location": "제1가공동 프레스 라인 3번기",
            "type": "끼임/협착 위험",
            "urgency": "높음",
            "status": "조치완료",
            "reporter": "김안전 조장",
            "content": "방호 센서 반응 딜레이 감지되어 즉시 인터록 정밀 점검 및 부품 교체 완료",
            "action": "센서 신품 교체 및 작업 전 인터록 점검 항목 추가"
        },
        {
            "id": 2,
            "date": "2026-11-04 10:15",
            "location": "중앙 물류창고 2구역 통로",
            "type": "넘어짐/전도 위험",
            "urgency": "보통",
            "status": "조치완료",
            "reporter": "이물류 주임",
            "content": "지게차 이동 통로 바닥에 오일 누유 흔적으로 인한 미끄럼 위험 발견",
            "action": "유흡착재 배포 및 즉시 세척 작업 완료, 지게차 패킹 점검"
        },
        {
            "id": 3,
            "date": "2026-11-02 16:40",
            "location": "제2조립동 도장 스프레이실",
            "type": "화학물질/환기",
            "urgency": "높음",
            "status": "조치완료",
            "reporter": "박보건 기사",
            "content": "국소배기장치 풍량 저하로 인한 유기용제 냄새 일시 체류",
            "action": "배기 덕트 내 필터 교체 및 풍속 0.7m/s 정상화 확인"
        },
        {
            "id": 4,
            "date": "2026-10-30 09:30",
            "location": "옥외 고압변전실 외곽 펜스",
            "type": "감전/화재 위험",
            "urgency": "보통",
            "status": "조치완료",
            "reporter": "최전기 주임",
            "content": "접지선 단자 접속부 노후 부식 확인",
            "action": "접지 단자 재압착 및 방식 테이핑 조치 완료"
        }
    ],
    "emergency_contacts": [
        {"role": "안전총괄책임자 (공장장)", "name": "홍길동 상무", "tel": "010-1234-5678", "ext": "1001"},
        {"role": "안전관리자 (사내)", "name": "김안전 과장", "tel": "010-2345-6789", "ext": "1004"},
        {"role": "보건관리자 (간호사)", "name": "이보건 대리", "tel": "010-3456-7890", "ext": "1007"},
        {"role": "사내 방재센터/상황실", "name": "24시간 종합관제실", "tel": "02-123-4911", "ext": "4911"},
        {"role": "관할 소방서 / 응급구조", "name": "119 소방안전센터", "tel": "119", "ext": "119"},
        {"role": "지정 병원 응급의료센터", "name": "한국산업안전 종합병원", "tel": "02-987-6543", "ext": "응급실"}
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=2)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"데이터 로드 실패, 기본값 사용: {e}")
        return DEFAULT_DATA

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"데이터 저장 실패: {e}")
        return False

class SafetyDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/data":
            data = load_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        elif parsed.path == "/" or parsed.path == "/index.html":
            file_path = os.path.join(DIRECTORY, "index.html")
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "index.html not found")
        else:
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/report":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            try:
                new_report = json.loads(post_body.decode("utf-8"))
                data = load_data()
                new_id = max([r.get("id", 0) for r in data.get("near_miss_reports", [])] + [0]) + 1
                new_report["id"] = new_id
                if "date" not in new_report or not new_report["date"]:
                    new_report["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                if "status" not in new_report:
                    new_report["status"] = "접수완료 (조치중)"
                
                data["near_miss_reports"].insert(0, new_report)
                
                # 통계 수치 업데이트
                if "monthly_stats" in data and len(data["monthly_stats"]["near_misses"]) > 0:
                    data["monthly_stats"]["near_misses"][-1] += 1
                
                save_data(data)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "item": new_report}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
        elif parsed.path == "/api/reset":
            save_data(DEFAULT_DATA)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "초기화 완료"}).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

def run(port=PORT):
    load_data()
    # 윈도우에서 SO_REUSEADDR 지원
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), SafetyDashboardHandler) as httpd:
        print("=" * 60)
        print("🚀 [스마트 안전보건 대시보드 서버가 정상 시작되었습니다]")
        print(f"👉 로컬 접속 주소: http://localhost:{port}")
        print(f"👉 네트워크 주소: http://127.0.0.1:{port}")
        print("=" * 60)
        print("Ctrl + C 를 누르면 서버가 안전하게 종료됩니다.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n서버를 종료합니다.")
            httpd.server_close()

if __name__ == "__main__":
    port = PORT
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run(port)

