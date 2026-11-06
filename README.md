# ⛑️ 스마트 산업안전보건 통합관제 대시보드 (Smart EHS Portal)

> 산업안전보건법 및 중대재해처벌법 대응을 위한 실시간 산업안전보건 관리 및 통계 시각화 웹 대시보드입니다.

---

## 📌 주요 특징 및 기능

1. **무재해 목표 달성 운동 전광판**
   - 연속 무재해 일수 카운터 (목표 일수 대비 달성률 시각화)
   - 사업장 안전등급(Green Level) 및 금일 현장 작업자 현황 실시간 표기
2. **핵심 안전보건 KPI 4종 모니터링**
   - 도수율(재해율 0.00%)
   - 위험성평가 개선 조치율 (96.4%)
   - 법정 정기 안전점검 이행률 (98.2%)
   - 법정 안전보건교육 이수율 (100%)
3. **인터랙티브 통계 분석**
   - 최근 6개월 안전사고 및 아차사고(Near-Miss) 추이 차트
   - 6대 중점 위험유형 (끼임/협착, 추락, 전도, 화학물질, 근골격계, 감전/화재) 도넛 분석
4. **아차사고 & 위험요인 신속 제보 시스템 (양방향 REST API)**
   - 작업자가 현장에서 스마트폰/PC로 위험요인을 등록하면 실시간 대시보드에 즉시 반영
5. **위험성평가(Risk Assessment) 5×5 매트릭스**
   - 빈도(가능성 1~5) × 강도(중대성 1~5) 등급별 건수 및 관리 상태 시각화
6. **일일 10대 핵심 현장 안전수칙 체크리스트**
   - 작업 개시 전 자율 점검 및 점수(100점 만점)/등급(A~C) 즉시 산출 및 저장
7. **비상대응 절차 & 24시간 비상연락망**
   - 4대 골든타임 행동요령 및 사내외 비상연락처(119, 의무실, 상황실) 원클릭 확인

---

## 🚀 빠른 시작 (접속 방법)

본 대시보드는 **외부 패키지 설치가 전혀 필요 없는 순수 파이썬(Zero-Dependency)** 모드와 **Streamlit** 모드 둘 다 지원합니다.

### 방법 1: 가장 빠른 실행 (추천 / 외부 설치 불필요)

1. 터미널을 열고 프로젝트 폴더로 이동합니다:
   ```bash
   cd safety_dashboard
   python server.py
   ```
   *(윈도우 사용자는 `run.bat` 파일을 더블클릭해도 즉시 실행됩니다.)*

2. 웹 브라우저(크롬, 엣지 등)를 열고 다음 주소로 접속합니다:
   👉 **접속 주소: [http://localhost:8080](http://localhost:8080)**  
   👉 **네트워크 주소: [http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

### 방법 2: Streamlit 버전 실행

Streamlit 환경을 선호하시는 경우 아래 명령어로 실행할 수 있습니다:

```bash
pip install -r requirements.txt
streamlit run app_streamlit.py
```
👉 브라우저 자동 실행 및 접속 주소: **`http://localhost:8501`**

---

## 📂 프로젝트 구조

```text
safety_dashboard/
├── server.py             # 파이썬 내장 HTTP & REST API 서버 (포트 8080)
├── index.html            # 반응형 대시보드 UI (Chart.js, 인터랙티브 폼/체크리스트)
├── safety_data.json      # 안전보건 데이터 저장소 (사고 제보, KPI 등)
├── app_streamlit.py      # Streamlit 전용 대시보드 소스코드
├── requirements.txt      # Streamlit 의존성 목록
├── run.bat               # 윈도우 원클릭 자동 실행 스크립트
├── .gitignore            # Git 제외 설정
└── README.md             # 프로젝트 설명서
```

---

## 🌐 GitHub에 업로드하는 방법

GitHub에 본 프로젝트를 올려서 팀원들과 공유하거나 버전 관리를 하려면:

1. [GitHub](https://github.com)에서 새 리포지토리(Repository)를 생성합니다 (예: `safety-dashboard`).
2. 로컬 터미널에서 아래 명령어를 순서대로 입력합니다:

```bash
cd safety_dashboard

# 1. git 저장소 초기화
git init

# 2. 파일 추가 및 첫 커밋
git add .
git commit -m "feat: 산업안전보건 통합관제 대시보드 초기 구축"

# 3. 브랜치명 main 설정 및 원격 저장소 연결
git branch -M main
git remote add origin https://github.com/<본인_아이디>/safety-dashboard.git

# 4. GitHub에 푸시
git push -u origin main
```

---

## 📄 라이선스
MIT License

