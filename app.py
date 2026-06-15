
import streamlit as st

st.title("🍅 AI 이삭 방울토마토 연구소")

symptom = st.text_input("증상 입력")
temp = st.number_input("온도", value=25)
humidity = st.number_input("습도", value=70)

if st.button("진단하기"):

    st.subheader("👨‍🔬 연구원 회의")

    scores = {}

    env = 40

    if temp >= 35:
        env += 55
        st.write("🌡️ 환경 연구원 : 고온 스트레스 가능성")

    scores["환경 연구원"] = env

    pest = 40

    if humidity >= 85:
        pest += 50

    scores["병해 연구원"] = pest

    if symptom == "노균병":

        if humidity >= 85:
            st.write("🦠 노균병 연구원 : 고습 환경 노균병 위험")
        else:
            st.write("🦠 노균병 연구원 : 노균병 의심")

    elif symptom == "역병":
        st.write("🦠 역병 연구원 : 역병 가능성 검토")

    elif symptom == "흰가루병":
        st.write("🦠 흰가루병 연구원 : 초기 방제 권장")

    st.subheader("📊 연구원 점수")
    st.subheader("👨‍🔬 연구원 회의")

if temp >= 35:
    st.write("👨‍🔬 환경 연구원")
    st.write('"고온 스트레스 가능성이 높습니다."')

if symptom == "배꼽썩음":
    st.write("👨‍🔬 양분 연구원")
    st.write('"칼슘 결핍 가능성이 높습니다."')

if humidity >= 85:
    st.write("👨‍🔬 병해충 연구원")
    st.write('"병원균 감염 여부를 확인해야 합니다."')
    best_agent = max(scores, key=scores.get)

st.write("")
st.write(f"🏆 핵심 연구원 : {best_agent}")

    rank_icons = ["🥇", "🥈", "🥉", "4️⃣"]

for idx, (name, score) in enumerate(
    sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
):

st.subheader("📊 농장 상태")
  
icon = rank_icons[idx] if idx < len(rank_icons) else "📌"
st.write(f"{icon} {name} : {score}점")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("건강점수", 82)

with col2:
    st.metric("위험도", 18)

with col3:
    st.metric("연구원 수", 5)
    st.subheader("🎯 AI 이삭 소장")
    st.info(f"최종 판단 : {symptom}")

    st.success(f"최종 진단 : {symptom}")
    st.info(
    "AI 이삭 소장 : 연구원 의견을 종합한 결과입니다."
)
