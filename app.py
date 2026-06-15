import streamlit as st

# 제목
st.title("🌱 HG Lab")
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
[
"토마토",
"방울토마토",
"파프리카",
"고추",
"오이",
"딸기",
"포도",
"사과",
"배",
"복숭아",
"감귤",
"블루베리",
"수박",
"멜론",
"참외",
"상추",
"배추",
"벼",
"인삼",
"콩"
]
)

region = st.selectbox(
    "충남 시군 선택",
    [
        "천안",
        "아산",
        "공주",
        "보령",
        "논산",
        "계룡",
        "당진",
        "서산",
        "태안",
        "홍성",
        "예산",
        "청양",
        "부여",
        "서천",
        "금산"
    ]
)

if region == "천안":
    town = st.selectbox(
        "천안 읍면 선택",
        [
            "성환읍",
            "직산읍",
            "성거읍",
            "입장면",
            "목천읍",
            "병천면",
            "수신면"
        ]
    )
else:
    town = "-"

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

    # 관수 연구원
    if humidity < 50:
        scores["관수 연구원"] += 30
        st.write("💧 관수 연구원 : 수분 부족 가능성")
    
    elif humidity > 90:
        scores["관수 연구원"] += 30
        st.write("💧 관수 연구원 : 과습 위험")
    
    # 양분 연구원
    if symptom == "배꼽썩음":
        scores["양분 연구원"] += 50
        st.write("🧪 양분 연구원 : 칼슘 결핍 의심")
    
    # 경영 연구원
    if scores["병해충 연구원"] >= 80:
        scores["경영 연구원"] += 20
        st.write("🧾 경영 연구원 : 방제 비용 증가 예상")
       
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
        rank_icons = ["🥇", "🥈", "🥉", "🏅", "🏅"]
    
    sorted_scores = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    for idx, (name, score) in enumerate(sorted_scores):
        
        st.write(f"{name} : {score}점")
    
    best_agent = sorted_scores[0][0]
    
    st.subheader("🏆 핵심 연구원")
    
    st.success(f"{best_agent}의 의견이 가장 중요합니다.")
    
    st.subheader("📋 HG Lab Core AI")
    
    if scores["병해충 연구원"] >= 80:
        st.error("병해충 위험도가 높습니다. 즉시 방제를 검토하세요.")
    
    elif scores["환경 연구원"] >= 80:
        st.warning("고온 스트레스가 의심됩니다.")
    
    else:
        st.success("현재 농장 상태는 양호합니다.")
    
        # 농장 상태
        st.subheader("📈 농장 상태")
    
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.metric("건강점수", 82)
    
        with col2:
            st.metric("위험도", 18)
    
        with col3:
            st.metric("연구원 수", 5)
    
        st.subheader("🌱 HG Lab Core AI")
        if symptom == "":
            result = "증상을 입력해주세요."
        else:
            result = symptom
    
        st.success(f"최종 진단 : {result}")
    
    st.info(
        f"""
    📍 지역 : 충남 {region} {town}
    
    🌾 작물 : {crop}
    
    🌡 온도 : {temp}℃
    
    💧 습도 : {humidity}%
    
    🧠 핵심 연구원 : {best_agent}
    
    최종 판단 : {result}
    """
    )
    
    # 여기부터 추가
    
    st.subheader("📊 연구원 점수")
    
    scores = {
        "환경 연구원": 85 if temp >= 35 else 60,
        "관수 연구원": 80 if humidity < 50 else 65,
        "양분 연구원": 75 if symptom == "배꼽썩음" else 50,
        "병해 연구원": 90 if symptom == "노균병" else 55,
        "경영 연구원": 70
    }
    
    for name, score in sorted(scores.items(), key=lambda x:x[1], reverse=True):
        st.write(f"🏅 {name} : {score}점")
    
    best_agent = max(scores, key=scores.get)
    
    st.subheader("🏆 핵심 연구원")
    st.success(f"{best_agent}의 의견이 가장 중요합니다.")

    st.subheader("🌱 재배 전략")

    if symptom == "흰가루병":
        st.warning("7일 이내 방제 권장")
    elif symptom == "역병":
        st.warning("배수 개선 및 살균제 검토")
    elif symptom == "배꼽썩음":
        st.warning("칼슘 공급 필요")
    else:
        st.success("특이사항 없음")
    
    st.subheader("📊 지역 위험도")
    
    risk = 30
    
    if humidity >= 85:
        risk += 30
    
    if temp >= 35:
        risk += 20
    
    st.progress(risk)
    
    st.write(f"위험도 : {risk}%")

    st.subheader("📈 농장 상태")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("건강점수", 82)
    
    with col2:
        st.metric("위험도", 18)
    
    with col3:
        st.metric("연구원 수", 5)
