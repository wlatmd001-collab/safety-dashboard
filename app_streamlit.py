import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="스마트 산업안전보건 통합관제 대시보드",
    page_icon="⛑️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #065f46;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .zero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 1.75rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .zero-number {
        font-size: 3.5rem;
        font-weight: 900;
        color: #34d399;
        line-height: 1;
    }
    .metric-card {
        background: white;
        padding: 1.25rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-top: 4px solid #059669;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 파일 로드
DATA_FILE = os.path.join(os.path.dirname(__file__), "safety_data.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

data = load_data()

# 사이드바
st.sidebar.image("https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=300", caption="Safety First (안전제일)")
st.sidebar.title("⛑️ 안전보건 관제 메뉴")
selected_site = st.sidebar.selectbox(
    "사업장 선택",
    ["전체 사업장 (통합)", "제1공장 (가공/프레스)", "제2공장 (조립/도장)", "스마트 물류센터"]
)
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚨 긴급 연락망")
st.sidebar.error("🔥 사내 상황실: **02-123-4911**")
st.sidebar.warning("🚑 119 소방안전센터: **119**")
st.sidebar.info("👨‍⚕️ 사내 의무실: **내선 1007**")

# 메인 타이틀
st.markdown('<div class="main-header">⛑️ 스마트 산업안전보건 통합관제 대시보드</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">중대재해 예방 및 안전보건관리체계 (KOSHA-MS) 실시간 모니터링 시스템</div>', unsafe_allow_html=True)

# 무재해 전광판
zero_days = data.get("site_info", {}).get("zero_accident_days", 285)
target_days = data.get("site_info", {}).get("target_days", 365)
pct = int((zero_days / target_days) * 100)

st.markdown(f"""
<div class="zero-card">
    <div style="font-size: 1.1rem; color: #a7f3d0; font-weight: 600;">🏆 무재해 목표 달성 운동 추진 현황</div>
    <div style="display: flex; align-items: baseline; gap: 1rem; margin: 0.5rem 0;">
        <span class="zero-number">{zero_days}</span>
        <span style="font-size: 1.4rem; color: #f1f5f9; font-weight: 700;">일 연속 무재해 기록 진행 중</span>
    </div>
    <div style="color: #cbd5e1; font-size: 0.9rem;">목표 일수: {target_days}일 (달성률 {pct}%) | 사업장 안전수준: 🟢 최우수 안전등급</div>
</div>
""", unsafe_allow_html=True)

# 4대 KPI 지표
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="도수율 (재해 발생률)", value="0.00%", delta="-0.12% (감소)", delta_color="normal")
with col2:
    st.metric(label="위험성평가 조치율", value="96.4%", delta="+2.1% (상승)", delta_color="normal")
with col3:
    st.metric(label="정기 안전점검 이행률", value="98.2%", delta="목표 100% 근접", delta_color="normal")
with col4:
    st.metric(label="법정 안전보건교육 이수율", value="100%", delta="전 임직원 완료", delta_color="normal")

st.markdown("---")

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["📊 사고·위험 통계 분석", "📢 아차사고 신속 제보", "⚖️ 위험성평가 현황", "✅ 일일 자율 안전점검"])

with tab1:
    col_chart1, col_chart2 = st.columns([3, 2])
    
    with col_chart1:
        st.subheader("📈 최근 6개월 안전사고 & 아차사고 추이")
        chart_data = pd.DataFrame({
            "월": ["6월", "7월", "8월", "9월", "10월", "11월"],
            "인명사고": [0, 0, 0, 0, 0, 0],
            "아차사고 발굴": [4, 6, 3, 5, 2, 1],
            "안전제안 건수": [12, 15, 18, 22, 19, 14]
        }).set_index("월")
        st.line_chart(chart_data)

    with col_chart2:
        st.subheader("🍩 주요 위험 요인 분석")
        risk_df = pd.DataFrame({
            "유형": ["끼임/협착", "추락/낙하", "넘어짐/전도", "화학물질", "근골격계", "감전/화재"],
            "건수": [14, 10, 9, 7, 6, 4]
        }).set_index("유형")
        st.bar_chart(risk_df)

    st.subheader("🔔 최근 발굴된 잠재 위험 및 개선 조치 내역")
    reports = data.get("near_miss_reports", [])
    if reports:
        df_rep = pd.DataFrame(reports)[["date", "location", "type", "urgency", "content", "action", "status"]]
        df_rep.columns = ["발생일시", "작업위치", "위험유형", "긴급도", "상세내용", "개선조치", "상태"]
        st.dataframe(df_rep, use_container_width=True)

with tab2:
    st.subheader("✍️ 현장 아차사고(Near-Miss) & 위험요인 신속 제보")
    with st.form("quick_report_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            rep_name = st.text_input("제보자 성명 / 직급")
            rep_loc = st.text_input("위험 발견 장소 (예: 제1공장 2호기)")
        with col_f2:
            rep_type = st.selectbox("위험 유형", ["끼임/협착", "추락/낙하", "넘어짐/전도", "화학물질/가스", "감전/화재", "기타"])
            rep_urg = st.selectbox("긴급도", ["보통", "높음", "긴급 (즉시조치)"])
        
        rep_desc = st.text_area("발견된 위험 상황 상세 내용")
        rep_action = st.text_input("권장 개선안 (선택)")
        
        submitted = st.form_submit_button("📨 위험요인 등록")
        if submitted:
            if rep_name and rep_loc and rep_desc:
                st.success("✅ 제보가 성공적으로 접수되었습니다. 즉시 안전관리자에게 통보됩니다.")
            else:
                st.warning("⚠️ 필수 입력 항목(이름, 위치, 내용)을 확인해주세요.")

with tab3:
    st.subheader("⚖️ 산업안전보건 위험성평가 매트릭스 현황")
    st.info("중대재해 감축 로드맵에 따른 위험성평가 중심 자기규율 예방체계 가동 중")
    c1, c2, c3 = st.columns(3)
    c1.metric("저위험 (관리 유지)", "144 건", "일상 관리")
    c2.metric("중위험 (개선 조치)", "22 건 (20건 조치완료)", "90.9% 완료")
    c3.metric("고위험 (즉시 개선)", "2 건 (전담반 편성)", "개선 진행 중")

with tab4:
    st.subheader("✅ 작업 전 10대 핵심 안전수칙 일일 체크리스트")
    c_item1 = st.checkbox("1. 개인보호구(안전모, 안전화 등) 올바른 착용", value=True)
    c_item2 = st.checkbox("2. 기계 회전부 방호덮개 및 인터록 센서 정상 작동", value=True)
    c_item3 = st.checkbox("3. 작업 통로 내 적치물 제거 및 바닥 미끄럼 방지", value=True)
    c_item4 = st.checkbox("4. 소화기 비치 상태 및 비상유도등 점등 확인", value=True)
    c_item5 = st.checkbox("5. 작업 전 TBM(안전 10분 회의) 완료 및 작업자 건강상태 확인", value=True)

    if st.button("💾 점검 결과 제출"):
        st.balloons()
        st.success("🎉 일일 안전점검 완료! 오늘의 안전 등급: A등급 (양호)")

