from agents.econ_ai import EconAI
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

env_result = {
    "avg_temp": 25.0,
    "avg_humidity": 69.0,
    "risk_score": 0,
    "risk_level": "안정",
    "reasons": ["AI 연구원 회의 전 기본 환경 분석값입니다."],
    "advice": ["환경데이터 업로드 후 분석을 실행하세요."]
}

patho_result = {
    "disease": "뚜렷한 병징 없음",
    "probability": 0,
    "risk_score": 0,
    "risk_level": "낮음",
    "recommendation": "잎 사진 업로드 후 분석을 실행하세요."
}

econ_result = {
    "production_kg": 1000,
    "market_price": 2600,
    "gross_revenue": 2600000,
    "loss_rate": 0,
    "expected_loss": 0,
    "treatment_cost": 50000,
    "profit_without_treatment": 2600000,
    "profit_with_treatment": 2550000,
    "benefit": -50000,
    "strategy": "시장 분석 대기",
    "market_strategy": "시장 분석 대기"
}

final_risk_score = 0
final_risk_level = "안정"

env_ai = EnvAI()
patho_ai = PathoAI()
econ_ai = EconAI()
chief_ai = ChiefAI()

if analyze:
    if env_file is None:
        st.warning("환경데이터를 먼저 업로드하세요.")
        st.stop()

    if leaf_image is None:
        st.warning("잎 사진을 먼저 업로드하세요.")
        st.stop()

    if env_file.name.endswith(".csv"):
        df = pd.read_csv(env_file)
    else:
        df = pd.read_excel(env_file)

    env_result = env_ai.analyze(df)
    patho_result = patho_ai.analyze_image(leaf_image, env_result)

    final_risk_score = max(
        env_result["risk_score"],
        patho_result.get("probability", 0)
    )

    if final_risk_score >= 70:
        final_risk_level = "높음"
    elif final_risk_score >= 40:
        final_risk_level = "주의"
    else:
        final_risk_level = "안정"

    try:
        econ_result = econ_ai.analyze(
            production_kg=1000,
            market_price=2600,
            disease_risk=patho_result.get("risk_score", patho_result.get("probability", 0)),
            env_risk=env_result.get("risk_score", 0),
            treatment_cost=50000
        )
    except Exception as e:
        st.error(f"Econ-AI 분석 오류: {e}")

    st.success("🌤 Env-AI 환경 분석 완료")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("🌡️ 평균 내부온도", f"{env_result['avg_temp']}℃")
        st.metric("⚠️ 환경 위험도", f"{env_result['risk_score']}%")

    with col2:
        st.metric("💧 평균 내부습도", f"{env_result['avg_humidity']}%")

    st.write("위험등급 :", env_result["risk_level"])

    st.write("### 분석 이유")
    for reason in env_result["reasons"]:
        st.write("-", reason)

    st.write("### 개선 방법")
    for tip in env_result["advice"]:
        st.write("-", tip)

    st.markdown("---")
    st.success("🟢 AI 연구원 회의를 시작합니다.")

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

    st.markdown("---")
    st.subheader("🧑‍🔬 AI 연구원 회의")

    with st.expander("🌿 Env-AI 발표", expanded=True):
        st.success(f"""
### 기상·환경 전문 연구원

▶ 평균 내부온도: {env_result['avg_temp']}℃  
▶ 평균 내부습도: {env_result['avg_humidity']}%  
▶ 환경 위험도: {env_result['risk_score']}%  
▶ 위험등급: {env_result['risk_level']}

📢 의견  
{env_result['reasons'][0]}
""")

    with st.expander("🦠 Patho-AI 발표"):
        st.error(f"""
### 🦠 병해충 전문 연구원

▶ 진단 결과 : {patho_result['disease']}  
▶ 발생 확률 : {patho_result['probability']}%  
▶ 위험도 : {patho_result.get("risk_level", "낮음")}

📢 의견  
{patho_result['recommendation']}
""")

    with st.expander("💰 Econ-AI 발표"):
        st.info(f"""
### 경영·유통 전문 연구원

▶ 예상 생산량: {econ_result['production_kg']:,}kg  
▶ 기준 시장가격: {econ_result['market_price']:,}원/kg  
▶ 예상 총매출: {econ_result['gross_revenue']:,}원  
▶ 예상 손실률: {econ_result['loss_rate']}%  
▶ 예상 손실액: {econ_result['expected_loss']:,}원  
▶ 방제 비용: {econ_result['treatment_cost']:,}원  
▶ 방제 전 순이익: {econ_result['profit_without_treatment']:,}원  
▶ 방제 후 순이익: {econ_result['profit_with_treatment']:,}원  
▶ 경제적 효과: {econ_result['benefit']:,}원  

📢 의견  
{econ_result['strategy']}

📦 출하 전략  
{econ_result['market_strategy']}
""")

with st.expander("👨🏻‍💼 Chief-AI 최종 회의"):
    st.warning(f"""
### AI 책임연구원

Env-AI, Patho-AI, Econ-AI 결과를 종합했습니다.

✔ 환경 위험도: {env_result['risk_score']}%  
✔ 병해 위험도: {patho_result['probability']}%  
✔ 예상 손실률: {econ_result['loss_rate']}%  
✔ 예상 손실액: {econ_result['expected_loss']:,}원  
✔ 방제 비용: {econ_result['treatment_cost']:,}원  
✔ 경제적 효과: {econ_result['benefit']:,}원  

---

### 최종 판단

현재 병해 위험도가 가장 크게 작용했습니다.  
환경은 안정적이지만, 잎 이미지 분석에서 병해 가능성이 높게 나타났으므로  
즉시 병든 잎 제거와 환기 강화가 필요합니다.

### 최종 위험등급

{final_risk_level}

최종 판단 생성 완료
""")

    st.header("📊 분석 결과")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"""
🛰️ Env-AI

기상·환경 전문 연구원

담당  
• 내부온도  
• 내부습도  
• 외부온도  
• 풍속  
• 일사량  
• CO2

판단  
환경 위험도: {env_result['risk_score']}%  
위험등급: {env_result['risk_level']}
""")

    with col2:
        st.error(f"""
🦠 Patho-AI

병해충 전문 연구원

진단 결과  
{patho_result['disease']}

발생 확률  
{patho_result['probability']}%

위험도  
{patho_result.get("risk_level", "낮음")}

현재 상태  
🟢 Vision 분석 완료
""")

    col3, col4 = st.columns(2)

    with col3:
        st.info(f"""
💰 Econ-AI

경영·유통 전문 연구원

예상 생산량  
{econ_result['production_kg']:,}kg

예상 매출  
{econ_result['gross_revenue']:,}원

경제적 효과  
{econ_result['benefit']:,}원
""")

    with col4:
        st.warning(f"""
👨🏻‍💼 Chief-AI

AI 책임연구원

현재 판단  
Env-AI, Patho-AI, Econ-AI 결과를 종합했습니다.

환경 위험도: {env_result['risk_score']}%  
병해 위험도: {patho_result['probability']}%  
최종 위험등급: {final_risk_level}
""")

    st.markdown("---")
    st.subheader("🏆 HG Lab 최종 행동지침")

    st.success(f"""
## 📋 오늘의 최종 의사결정

🎯 종합 위험도  
{final_risk_score}%

━━━━━━━━━━━━━━━━━━

🟡 최종 위험등급  
{final_risk_level}

━━━━━━━━━━━━━━━━━━

Chief-AI 종합판단 완료
""")

    st.write("### ✅ 권장 조치")

    for tip in env_result["advice"]:
        st.write(f"• {tip}")

    if patho_result["probability"] >= 70:
        st.write("• 병든 잎을 제거하세요.")
        st.write("• 환기를 강화하세요.")
    else:
        st.write("• 현재 추가적인 병해 조치는 필요하지 않습니다.")

    st.markdown("---")

else:
    st.info("환경데이터를 업로드한 뒤 AI 연구원 회의를 시작하세요.")
