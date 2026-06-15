import streamlit as st

# 제목
st.title("🧬 Hyogrow")
st.caption("Multi-Agent Agricultural Research Lab")

# 입력
symptom = st.text_input("증상 입력")

temp = st.number_input(
    "온도 (℃)",
    min_value=0,
    max_value=50,
    value=25
)

humidity = st.number_input(
    "습도 (%)",
    min_value=0,
    max_value=100,
    value=70
)

crop = st.selectbox(
    "작물 선택",
    ["토마토", "파프리카", "딸기", "포도"]
)

# 진단 버튼
if st.button("진단하기"):

    st.subheader("🧑‍🔬 연구원 회의")

    scores = {
        "환경 연구원": 40,
        "관수 연구원": 40,
        "양분 연구원": 40,
        "병해충 연구원": 40,
        "경영 연구원": 40
    }

    # 환경 연구원
    if temp >= 35:
        scores["환경 연구원"] += 50
        st.write("🌡️ 환경 연구원 : 고온 스트레스 가능성")

    # 병해충 연구원
    if humidity >= 85:
        scores["병해충 연구원"] += 50
        st.write("🦠 병해충 연구원 : 고습 환경 병해 위험")

    # 증상 분석
    if symptom == "노균병":
        scores["병해충 연구원"] += 40
        st.write("🍃 노균병 연구원 : 노균병 의심")

    elif symptom == "역병":
        scores["병해충 연구원"] += 40
        st.write("🍃 역병 연구원 : 역병 가능성")

    elif symptom == "흰가루병":
        scores["병해충 연구원"] += 40
        st.write("🍃 흰가루병 연구원 : 초기 방제 권장")

    elif symptom == "배꼽썩음":
        scores["양분 연구원"] += 50
        st.write("🥛 양분 연구원 : 칼슘 결핍 가능성")

    # 핵심 연구원
    best_agent = max(scores, key=scores.get)

    st.write("")
    st.write(f"🏆 핵심 연구원 : {best_agent}")

    # 점수 순위
    st.subheader("📊 연구원 점수")

    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for name, score in sorted_scores:
        st.write(f"• {name} : {score}점")

    # 농장 상태
    st.subheader("📈 농장 상태")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("건강점수", 82)

    with col2:
        st.metric("위험도", 18)

    with col3:
        st.metric("연구원 수", 5)

    st.subheader("🎯 Hyogrow 소장")

    if symptom == "":
        result = "증상을 입력해주세요."
    else:
        result = symptom

    st.success(f"최종 진단 : {result}")

    st.info(
        "Hyogrow AI가 연구원 의견을 종합하여 판단한 결과입니다."
    )
