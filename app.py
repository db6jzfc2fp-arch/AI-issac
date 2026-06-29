import streamlit as st
import pandas as pd
import time

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

병해충 전문 연구원

담당

• Vision AI

• 노균병

• 흰가루병

• 탄저병

• 해충

판단

병 발생 확률

농약 추천

희석배수 계산

살포시기 추천
""")

col3, col4 = st.columns(2)

with col3:

    st.info("""
💰 Econ-AI

경영·유통 전문 연구원

담당

• 전국 도매시장

• 운송비

• 생산량

• 예상순이익

판단

출하시기

시장 추천

가격 예측

최대 수익 계산
""")

with col4:

    st.warning("""
👨🏻‍💼 Chief-AI

AI 책임연구원

담당

세 연구원의 의견 수집

가중치 계산

위험도 분석

최종 행동지침 생성

역할

식물 안전성

경제성

병해 위험

환경 위험

종합 판단
""")



if env_file is None:
    st.warning("환경데이터를 먼저 업로드하세요.")
    st.stop()

if env_file.name.endswith(".csv"):
    df = pd.read_csv(env_file)
else:
    df = pd.read_excel(env_file)

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
