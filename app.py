import streamlit as st
import pandas as pd

disease_db = {
    "흰가루병": {
        "temp": (20, 28),
        "humidity": (60, 85),
        "advice": [
            "환기 강화",
            "하엽 제거",
            "7일 이내 방제"
        ]
    },

    "노균병": {
        "temp": (15, 25),
        "humidity": (80, 100),
        "advice": [
            "과습 방지",
            "배수 관리",
            "예방 살균제 검토"
        ]
    },

    "역병": {
        "temp": (18, 30),
        "humidity": (85, 100),
        "advice": [
            "배수 개선",
            "관수량 조절",
            "방제 실시"
        ]
    },

    "배꼽썩음": {
        "temp": (20, 35),
        "humidity": (40, 80),
        "advice": [
            "칼슘 공급",
            "급격한 수분 변화 방지",
            "관수 균일화"
        ]
    }
}
def calculate_risk(symptom, temp, humidity):

    if symptom not in disease_db:
        return 30

    disease = disease_db[symptom]

    risk = 40

    temp_min, temp_max = disease["temp"]
    humidity_min, humidity_max = disease["humidity"]

    if temp_min <= temp <= temp_max:
        risk += 25

    if humidity_min <= humidity <= humidity_max:
        risk += 25

    return min(risk, 100)
# 제목
st.title("🌱 HG Lab")
st.caption("Multi-Agent Agricultural Research Lab")

st.subheader("🥒 분석 작물")

st.success("오이")

st.markdown("---")

st.subheader("📂 환경데이터 업로드")

uploaded_file = st.file_uploader(
    "최근 7일 또는 30일 환경데이터(CSV 또는 Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ 환경데이터를 성공적으로 불러왔습니다.")

    st.subheader("📋 업로드 데이터")

    st.dataframe(df.head())

st.caption("💡 농장에서 내려받은 환경데이터를 업로드하면 AI가 자동으로 분석합니다.")

# 진단 버튼
if st.button("🌱 환경데이터 분석 시작"):

    st.subheader("🧑‍🔬 연구원 회의")

    scores = {
    "기후 연구원": 40,
    "생육 연구원": 40,
    "수확 연구원": 40,
    "시장 연구원": 40,
    "AI 연구원": 40,
    "관수 연구원": 0,
    "양분 연구원": 0,
    "환경 연구원": 0,
    "병해충 연구원": 0,
    "경영 연구원": 0
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
        risk = calculate_risk(symptom, temp, humidity)
        if symptom in disease_db:

            disease = disease_db[symptom]
        
            temp_min, temp_max = disease["temp"]
            humidity_min, humidity_max = disease["humidity"]
        
            st.subheader("🔍 분석 근거")
            if symptom in disease_db:

                st.subheader("📋 권장 조치")
                st.subheader("🧑‍🔬 연구원 회의")
                st.subheader("🤖 HyoGrow AI 소장 보고서")

                if risk >= 80:
                    final_level = "고위험"
                elif risk >= 60:
                    final_level = "주의"
                else:
                    final_level = "양호"
                
                st.success(
                    f"""
                📍 지역 : {region} {town}
                
                🌱 작물 : {crop}
                
                🔎 진단 대상 : {symptom}
                
                📊 위험도 : {risk}%
                
                🚨 종합 평가 : {final_level}
                
                📋 HyoGrow 최종 의견
                
                현재 {symptom} 발생 가능성이 {final_level} 수준으로 판단됩니다.
                
                환경 조건과 입력 정보를 종합했을 때 지속적인 모니터링이 필요하며 권장 조치를 우선 수행하는 것을 추천합니다.
                """
                )

                # 병해충 연구원
                st.write("🦠 병해충 연구원")
                
                if risk >= 80:
                    st.write(f"{symptom} 발생 가능성이 높습니다.")
                elif risk >= 60:
                    st.write(f"{symptom} 발생 주의가 필요합니다.")
                else:
                    st.write(f"{symptom} 위험도는 낮습니다.")
                
                # 기후 연구원
                st.write("🌡️ 기후 연구원")
                
                if temp >= 35:
                    st.write("고온 스트레스 위험이 있습니다.")
                elif temp <= 10:
                    st.write("저온 피해 가능성이 있습니다.")
                else:
                    st.write("현재 온도는 비교적 양호합니다.")
                
                # 관수 연구원
                st.write("💧 관수 연구원")
                
                if humidity >= 85:
                    st.write("과습 위험이 있습니다.")
                elif humidity <= 50:
                    st.write("수분 부족 가능성이 있습니다.")
                else:
                    st.write("관수 상태는 양호합니다.")
                
                # 양분 연구원
                st.write("🧪 양분 연구원")
                
                if symptom == "배꼽썩음":
                    st.write("칼슘 공급을 검토하세요.")
                else:
                    st.write("특이한 양분 결핍 징후는 없습니다.")
                            
                for advice in disease_db[symptom]["advice"]:
                    st.write(f"✅ {advice}")
                    
            if temp_min <= temp <= temp_max:
                st.write(f"✅ 온도 {temp}℃ : 발생 적합 구간")
        
            else:
                st.write(f"❌ 온도 {temp}℃ : 발생 적합 구간 아님")
        
            if humidity_min <= humidity <= humidity_max:
                st.write(f"✅ 습도 {humidity}% : 발생 적합 구간")
        
            else:
                st.write(f"❌ 습도 {humidity}% : 발생 적합 구간 아님")

        st.write(f"📊 병 발생 위험도 : {risk}%")
        
        if risk >= 80:
            st.error("🔴 고위험")
        
        elif risk >= 60:
            st.warning("🟠 주의 필요")
        
        else:
            st.success("🟢 낮은 위험")
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
    st.subheader("🧠 HG Lab Core AI")

    st.success(
        f"""
    📍 지역 : {region} {town}
    
    🌱 작물 : {crop}
    
    🏆 핵심 연구원 : {best_agent}
    
    📋 최종 권장사항 :
    {symptom} 관련 정밀 점검 필요
    """
    )
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
    st.subheader("📍 지역 맞춤 분석")

    if region == "천안":
        st.info("천안은 배·포도·시설채소 재배가 활발한 지역입니다.")
    
    elif region == "아산":
        st.info("아산은 시설원예와 수도작 비중이 높은 지역입니다.")
    
    elif region == "논산":
        st.info("논산은 딸기와 엽채류 재배 중심지입니다.")
    
    elif region == "당진":
        st.info("당진은 벼와 시설채소 재배가 활발합니다.")
    
    elif region == "예산":
        st.info("예산은 사과 재배 비중이 높은 지역입니다.")
        st.subheader("📈 농장 상태")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("건강점수", 82)
    
    with col2:
        st.metric("위험도", 18)
    
    with col3:
        st.metric("연구원 수", 5)
