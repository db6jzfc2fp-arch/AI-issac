import streamlit as st
import pandas as pd

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

if st.button("🔍 AI 분석 시작"):

    st.header("📊 분석 결과")

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

    st.header("🌤 환경 연구원")

    st.info("환경데이터 분석 준비 완료")

    st.markdown("---")

    st.header("🦠 병해 연구원")

    st.info("병 발생 위험 분석 준비 완료")

    st.markdown("---")

    st.header("🌱 생육 연구원")

    st.info("생육 분석 준비 완료")

    st.markdown("---")

    if leaf_image is not None:

        st.header("📷 사진 연구원")

        st.image(
            leaf_image,
            caption="업로드한 오이 잎",
            use_container_width=True
        )

        st.info("사진 분석 준비 완료")

    st.markdown("---")

    st.header("🧠 HG Core AI")

    st.success("모든 연구원의 의견을 종합하여 분석을 시작합니다.")
