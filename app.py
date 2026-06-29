import streamlit as st
import pandas as pd

# ==========================
# HG Lab
# ==========================

st.set_page_config(
    page_title="HG Lab",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 HG Lab")
st.caption("AI Cucumber Research Assistant")

st.markdown("---")

st.header("🥒 분석 작물")

st.success("오이")

st.markdown("---")

st.header("📁 환경데이터 업로드")

env_file = st.file_uploader(
    "최근 7일 또는 30일 환경데이터",
    type=["csv", "xlsx"]
)

st.markdown("---")

st.header("📷 잎 사진 업로드")

leaf_image = st.file_uploader(
    "오이 잎 사진",
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
