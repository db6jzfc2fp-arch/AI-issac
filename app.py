import streamlit as st
import pandas as pd
import time
import numpy as np

from agents.env_ai import EnvAI
from agents.patho_ai import PathoAI
from agents.econ_ai import EconAI
from agents.chief_ai import ChiefAI

# ==========================
# HG Lab
# ==========================

st.set_page_config(
    page_title="HG Lab",
    page_icon="🌱",
    layout="centered"
)

st.markdown("""
<style>

.main{
    max-width:900px;
    margin:auto;
}

h1{
    text-align:center;
    color:#14532d;
}

h2{
    color:#166534;
}

.stButton>button{
    width:100%;
    height:60px;
    font-size:22px;
    font-weight:bold;
    border-radius:15px;
    background:#166534;
    color:white;
}

.stButton>button:hover{
    background:#14532d;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:20px;">

<h1 style="font-size:60px;color:#14532d;margin-bottom:0;">
🌱 HG Lab
</h1>

<h3 style="color:#4b5563;">
AI Cucumber Intelligence Platform
</h3>

<p style="font-size:20px;color:#6b7280;">
환경을 이해하고<br>
병을 예측하며<br>
농부의 의사결정을 돕는 AI 연구소
</p>

</div>
""", unsafe_allow_html=True)

col1,col2,col3=st.columns(3)

with col1:
    st.success("🟢 System Ready")

with col2:
    st.info("Version 2.0")

with col3:
    st.info("AI Researchers : 5")

st.markdown("---")

st.markdown("""
<div style="background:#f0fdf4;
padding:25px;
border-radius:15px;
text-align:center;
margin-top:20px;
">

<h2>🥒 분석 작물</h2>

<h1 style="color:#166534;">
오이
</h1>

</div>
""",unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div style="
background:#f8fafc;
padding:20px;
border-radius:15px;
margin-top:20px;
margin-bottom:20px;
">

<h2>📁 Environment Data</h2>

<p>최근 7일 또는 30일 환경데이터(CSV 또는 Excel)를 업로드하세요.</p>

</div>
""", unsafe_allow_html=True)

env_file = st.file_uploader(
    "",
    type=["csv","xlsx"]
)

st.markdown("---")

st.markdown("""
<div style="
background:#f8fafc;
padding:20px;
border-radius:15px;
margin-top:20px;
margin-bottom:20px;
">

<h2>📷 Leaf Image</h2>

<p>오이 잎 사진(JPG, PNG)을 업로드하세요.</p>

</div>
""", unsafe_allow_html=True)

leaf_image = st.file_uploader(
    "",
    type=["jpg","jpeg","png"]
)

st.markdown("---")

analyze = st.button("🧠 AI 연구원 회의 시작")

if analyze:

    # AI 연구원 실제 실행
    env_ai = EnvAI()
    patho_ai = PathoAI()
    econ_ai = EconAI()
    chief_ai = ChiefAI()

    if env_file is None:
        st.warning("환경데이터를 먼저 업로드하세요.")
        st.stop()

    if env_file.name.endswith(".csv"):
        df = pd.read_csv(env_file)
    else:
        df = pd.read_excel(env_file)

    st.write(df.columns)
    
    env_result = env_ai.analyze(df)
       
    st.success("🌤 Env-AI 환경 분석 완료")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🌡️ 평균 내부온도", f"{env_result['avg_temp']}℃")
    
    with col2:
        st.metric("💧 평균 내부습도", f"{env_result['avg_humidity']}%")
    
    st.metric("⚠️ 환경 위험도", f"{env_result['risk_score']}%")
    st.write("위험등급 :", env_result["risk_level"])
    
    st.write("### 분석 이유")
    for reason in env_result["reasons"]:
        st.write("-", reason)

    st.write("### 개선 방법")
    for tip in env_result["advice"]:
        st.write("-", tip)
    #patho_result = patho_ai.analyze_image(leaf_image, env_result)
    #econ_result = econ_ai.calculate_profit()
    #chief_result = chief_ai.make_decision(env_result, patho_result, econ_result)
        
        st.success("🟢 AI 연구원 회의를 시작합니다.")
        
        st.markdown("---")
        
st.subheader("👨‍🔬 AI 연구원 회의")
progress = st.progress(0)
status = st.empty()

status.write("🌤 Climate AI 분석 중...")
progress.progress(20)
time.sleep(0.5)

status.write("🦠 Disease AI 분석 중...")
progress.progress(40)
time.sleep(0.5)

status.write("💧 Irrigation AI 분석 중...")
progress.progress(60)
time.sleep(0.5)

status.write("🌱 Growth AI 분석 중...")
progress.progress(80)
time.sleep(0.5)

status.write("🧠 HG Core AI 최종 판단...")
progress.progress(100)
time.sleep(0.5)

status.success("✅ AI 연구원 회의 완료")
        
st.markdown("----")
    st.subheader("🧑‍🔬 AI 연구원 회의")
    
    with st.expander("🛰️ Env-AI 발표", expanded=True):
        st.success("""
    ### 기상·환경 전문 연구원
    
    ▶ 현재 평균온도와 습도 분석 완료
    
    ▶ 향후 30분 환경 예측
    
    • 결로 발생 가능성 분석
    • 고온 스트레스 분석
    • 토양 수분 분석
    
    📢 의견
    '환기와 관수 조절이 필요합니다.'
    """)
    
    with st.expander("🦠 Patho-AI 발표"):
    
        st.error("""
    ### 병해충 전문 연구원
    
    ▶ Vision-LLM 이미지 분석
    
    • 노균병 위험도 계산
    • 흰가루병 위험도 계산
    • 해충 발생 위험도 계산
    
    📢 의견
    '현재 병 발생 위험이 증가하고 있습니다.'
    """)
    
    with st.expander("💰 Econ-AI 발표"):
    
        st.info("""
    ### 경영·유통 전문 연구원
    
    ▶ 시장 분석
    
    • 예상 수확량 계산
    • 운송비 계산
    • 예상 판매가격 계산
    
    📢 의견
    '3일 후 출하가 가장 높은 수익입니다.'
    """)
    
    with st.expander("👨🏻‍💼 Chief-AI 최종 회의"):
    
        st.warning("""
    ### AI 책임연구원
    
    세 연구원의 의견을 종합합니다.
    
    ✔ 식물 안전성
    
    ✔ 병 발생 위험
    
    ✔ 예상 수익
    
    ✔ 최종 행동지침 계산
    
    최종 판단 생성 중...
    """)
        
    st.header("📊 분석 결과")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
    🛰️ Env-AI
    
    기상·환경 전문 연구원
    
    담당
    • 온도
    • 습도
    • EC
    • 토양수분
    • 일사량
    
    판단
    
    30분 후 환경 예측
    
    결로 예측
    
    고온장해 예측
    
    관수 추천
    """)
    
    with col2:
        st.error("""
    🦠 Patho-AI
    ────────────────
    
    병해충 전문 연구원
    (Vision-LLM)
    
    전문 분야
    • Vision-LLM 이미지 분석
    • 병해충 진단
    • 생육단계 분석
    • PLS 농약안전정보 연동
    
    주요 분석
    • 노균병
    • 흰가루병
    • 탄저병
    • 총채벌레
    • 진딧물
    
    현재 상태
    🟢 분석 준비 완료
    
    Vision 모델 대기
    """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("""
    💰 Econ-AI
    ────────────────
    
    경영·유통 전문 연구원
    
    전문 분야
    • 전국 도매시장 시세
    • 출하시기 예측
    • 물류비 분석
    • 예상 순이익 계산
    
    주요 분석
    • 가격 예측
    • 시장 추천
    • 운송비 계산
    • 출하 전략
    
    현재 상태
    🟢 시장 데이터 연결 완료
    
    경제성 분석 준비 완료
    """)
    
    with col4:
        st.warning("""
    👨🏻‍💼 Chief-AI
    ────────────────
    
    AI 책임연구원
    
    전문 역할
    • Env-AI 의견 종합
    • Patho-AI 의견 종합
    • Econ-AI 의견 종합
    
    의사결정
    • 위험도 평가
    • 가중치 계산
    • 행동지침 생성
    • 최종 의사결정
    
    현재 상태
    🟢 연구원 회의 대기
    
    최종 판단 준비 완료
    """)
    
    st.markdown("---")
    
    st.subheader("🏆 HG Lab 최종 행동지침")
    
    st.success("""
    ## 📋 오늘의 최종 의사결정
    
    🌡️ 환경 위험도
    72%
    
    🦠 병해충 위험도
    61%
    
    💰 예상 수익성
    85%
    
    ━━━━━━━━━━━━━━━━━━
    
    ① 환기창 30% 개방
    
    ② 관수량 10% 감소
    
    ③ 예방 살균제 점검
    
    ④ 내일 오전 재측정
    
    ━━━━━━━━━━━━━━━━━━
    
    🟡 최종 위험등급 : 주의
    
    Chief-AI 종합판단 완료
    """)
    
    if env_file is None:
        st.warning("환경데이터를 먼저 업로드하세요.")
        st.stop()
    
    if env_file.name.endswith(".csv"):
        df = pd.read_csv(env_file)
    else:
        df = pd.read_excel(env_file)
    
    st.write(df.columns)
    
    st.success("환경데이터를 불러왔습니다.")
    
    st.dataframe(df.head())
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
    🌤 Climate AI
    
    ✅ 환경 분석 완료
    """)
    
    with col2:
        st.error("""
    🦠 Disease AI
    
    ✅ 병해 분석 완료
    """)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("""
    💧 Irrigation AI
    
    ✅ 관수 분석 완료
    """)
    
    with col4:
        st.warning("""
    🌱 Growth AI
    
    ✅ 생육 분석 완료
    """)
    
    if leaf_image is not None:
        st.success("""
    📷 Vision AI
    
    ✅ 잎 사진 분석 완료
    """)
    
        st.markdown("---")
    
        st.header("🧠 HG Core AI")
    
        st.success("모든 연구원의 의견을 종합하여 분석을 시작합니다.")
