from tensorflow.keras.models import load_model
import numpy as np
import cv2
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

MODEL_PATH = "models/cucumber_leaf_best_model.keras"

@st.cache_resource
def load_patho_model():
    return load_model(MODEL_PATH)

patho_model = load_patho_model()

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

root_file = st.file_uploader(
    "🌱 근권부(EC, pH) 데이터 업로드",
    type=["csv","xlsx"],
    key="root_file"
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
    "confidence": 0,
    "risk_score": 0,
    "risk_level": "낮음",
    "advice": "잎 사진 업로드 후 분석을 실행하세요."
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

    if root_file is not None:
        if root_file.name.endswith(".csv"):
            root_df = pd.read_csv(root_file)
        else:
            root_df = pd.read_excel(root_file)
    else:
        root_df = None

    env_result = env_ai.analyze(df, root_df)
    patho_result = patho_ai.analyze_image(leaf_image, env_result)

    # 병해가 아닌 정상·생육 단계 클래스
    safe_classes = {
        "건강한 잎",
        "개화기",
        "신선한 오이",
        "결실기 1단계",
        "결실기 2단계",
        "결실기 3단계"
    }

    predicted_class = patho_result.get(
        "raw_disease",
        patho_result.get("disease", "")
    )
    patho_confidence = float(patho_result.get("confidence", 0))

    # 정상 또는 생육 단계라면 확신도가 높을수록 병해 위험은 낮아짐
    if predicted_class in safe_classes:
        disease_risk_score = max(0, 100 - patho_confidence)
    else:
        disease_risk_score = patho_confidence

    # 환경 위험과 실제 병해 위험 중 높은 값을 최종 위험도로 사용
    final_risk_score = max(
        float(env_result.get("risk_score", 0)),
        disease_risk_score
    )

    if final_risk_score >= 70:
        final_risk_level = "높음"
    elif final_risk_score >= 40:
        final_risk_level = "주의"
    else:
        final_risk_level = "안정"

    if predicted_class not in safe_classes and disease_risk_score >= 70:
        chief_comment = (
            f"병해 진단 결과 '{predicted_class}' 가능성이 "
            f"{patho_confidence:.1f}%로 높게 나타났습니다. "
            "해당 병해에 맞는 현장 확인과 초기 대응이 필요합니다."
        )

    elif env_result.get("risk_score", 0) >= 70:
        chief_comment = (
            "환경 위험도가 높게 나타났습니다. "
            "온도·습도·환기와 근권부 EC·pH 상태를 우선 점검해야 합니다."
     )

    elif predicted_class in safe_classes:
        chief_comment = (
            f"Patho-AI는 '{predicted_class}' 상태를 "
            f"{patho_confidence:.1f}% 확률로 예측했습니다. "
            "현재 뚜렷한 병해 위험은 낮으므로 기존 관리 상태를 유지하고 "
            "정기적으로 잎과 환경 상태를 점검하는 것이 적절합니다."
        )

    else:
        chief_comment = (
            "현재 종합 위험도는 낮거나 주의 수준입니다. "
            "즉각적인 방제보다는 지속적인 관찰과 예방 관리가 적절합니다."
        )
    
    #econ_comment = (
    #f"Econ-AI는 '{econ_result.get('best_scenario', '분석중')}' 전략이 가장 유리하다고 판단했습니다. "
    #f"경제적 효과는 {econ_result['benefit']:,}원입니다."
    #)
    
    try:
        econ_result = econ_ai.analyze(
        env_result=env_result,
        patho_result={
            **patho_result,
            "disease_risk": disease_risk_score
        },
        production_kg=1000,
        market_price=2600,
        treatment_cost=50000
       )

    except Exception as e:
        st.error(f"Econ-AI 분석 오류: {e}")
        st.stop()

    chief_result = chief_ai.make_decision(
        env_result=env_result,
        patho_result={
            **patho_result,
            "disease_risk": disease_risk_score
        },
        econ_result=econ_result
    )    

    economic_effect = float(econ_result.get("benefit", 0))
    best_scenario = econ_result.get("best_scenario", "상태 관찰")

    if economic_effect > 0:
        econ_comment = (
            f"Econ-AI는 '{best_scenario}' 전략을 권장했습니다. "
            f"예상 경제적 효과는 약 {economic_effect:,.0f}원입니다."
        )
    elif economic_effect < 0:
        econ_comment = (
            f"Econ-AI는 '{best_scenario}' 전략을 권장했습니다. "
            f"현재 방제를 실시하면 약 "
            f"{abs(economic_effect):,.0f}원의 추가 비용이 발생합니다."
        )
    else:
        econ_comment = (
            f"Econ-AI는 '{best_scenario}' 전략을 권장했습니다. "
            "두 시나리오의 경제적 차이는 크지 않습니다."
        )

        #econ_result.setdefault("production_kg", 1000)
        #econ_result.setdefault("market_price", 2600)
        #econ_result.setdefault("gross_revenue", 2600000)
        #econ_result.setdefault("loss_rate", 0)
        #econ_result.setdefault("expected_loss", 0)
        #econ_result.setdefault("treatment_cost", 50000)
        #econ_result.setdefault("profit_without_treatment", 2600000)
        #econ_result.setdefault("profit_with_treatment", 2550000)
        #con_result.setdefault("benefit", 50000)
        #econ_result.setdefault("strategy", "경제성 분석 완료")
        #econ_result.setdefault("market_strategy", "분석 완료")
        #econ_result.setdefault("best_scenario", "분석 완료")

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
▶ 발생 확률 : {patho_result['confidence']}%  
▶ 위험도 : {patho_result.get("risk_level", "낮음")}

📢 의견  
{patho_result['advice']}
""")

    with st.expander("💰 Econ-AI 발표"):
        st.success(f"📦 출하 전략: {econ_result.get('shipping_strategy', '분석중')}")
        st.write(f"예측 신뢰도: {econ_result.get('econ_confidence', 0)}%")
        st.write(econ_result.get("profit_advice", "경제성 분석 결과를 확인 중입니다."))

    st.write("### 📊 Econ-AI 의사결정 시뮬레이션")

    production_kg = float(econ_result.get("production_kg", 1000))
    market_price = float(econ_result.get("market_price", 2600))
    treatment_cost = float(econ_result.get("treatment_cost", 50000))

    # 현재 병해 위험도
    current_loss_rate = float(econ_result.get("loss_rate", disease_risk_score))

    # 방제 실시 시 손실률 감소를 가정
    treated_loss_rate = max(0.0, current_loss_rate * 0.35)

    gross_revenue = production_kg * market_price

    profit_without_treatment = gross_revenue * (1 - current_loss_rate / 100)

    profit_with_treatment = (
        gross_revenue * (1 - treated_loss_rate / 100)
        - treatment_cost
    )

    economic_difference = profit_with_treatment - profit_without_treatment

    col_sim1, col_sim2 = st.columns(2)

    with col_sim1:
        st.info(f"""
    ### 방제 미실시
    - 예상 손실률: {current_loss_rate:.1f}%
    - 예상 매출: {gross_revenue:,.0f}원
    - 예상 순이익: {profit_without_treatment:,.0f}원
    """)

    with col_sim2:
        st.success(f"""
    ### 방제 실시
    - 예상 손실률: {treated_loss_rate:.1f}%
    - 방제 비용: {treatment_cost:,.0f}원
    - 예상 순이익: {profit_with_treatment:,.0f}원
    """)

    if economic_difference > 0:
        st.success(
            f"AI 추천: 방제를 실시하면 약 {economic_difference:,.0f}원의 "
            "추가 경제효과가 예상됩니다."
        )
    else:
        st.warning(
            f"AI 추천: 현재는 방제 비용이 예상 효과보다 "
            f"{abs(economic_difference):,.0f}원 더 커서 즉시 방제를 권장하지 않습니다."
        )

    with st.expander("👨🏻‍💼 Chief-AI 최종 회의"):
        st.warning(f"""
    ### AI 책임연구원

    Env-AI, Patho-AI, Econ-AI 결과를 종합했습니다.

    ✔ 환경 위험도: {chief_result.get('environment_risk', 0)}%  
    ✔ 병해 위험도: {chief_result.get('disease_risk', 0)}%  
    ✔ Econ-AI 전략: {chief_result.get('best_scenario', '상태 관찰')}  
    ✔ 예상 손실률: {chief_result.get('loss_rate', 0)}%  
    ✔ 경제적 효과: {chief_result.get('benefit', 0):,}원  

    ---

    ### 최종 판단

    {chief_result.get('summary', '최종 판단을 생성했습니다.')}

    ### 최종 위험등급

    {chief_result.get('final_risk_level', '안정')}

    최종 판단 생성 완료
    """)

        st.write("### 연구원 종합 행동지침")

        for action in chief_result.get("actions", []):
            st.write(f"• {action}")

### AI 책임연구원

#Env-AI, Patho-AI, Econ-AI 결과를 종합했습니다.

#✔ 환경 위험도: {env_result['risk_score']}%  
#✔ 병해 위험도: {disease_risk_score:.1f}% 
#✔ 예상 손실액: {econ_result.get('expected_loss', 0):,}원 
#✔ 방제 비용: {econ_result.get('treatment_cost', 0):,}원  
#✔ 경제적 효과: {econ_result.get('benefit', 0):,}원  

#---

### 최종 판단

#{chief_comment}

#{econ_comment}

### 최종 위험등급

#{final_risk_level}

#최종 판단 생성 완료
#""")

    
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

    if predicted_class in safe_classes:
        st.write("• 현재 추가적인 병해 방제는 필요하지 않습니다.")
        st.write("• 기존 관리 상태를 유지하세요.")
        st.write("• 잎과 환경 상태를 정기적으로 재확인하세요.")

    elif disease_risk_score >= 70:
        st.write(f"• '{predicted_class}' 의심 부위를 현장에서 확인하세요.")
        st.write("• 피해 잎이나 과실을 제거하세요.")
        st.write("• 환기와 습도 관리를 강화하세요.")

    elif disease_risk_score >= 40:
        st.write("• 즉시 방제보다 병징 변화를 지속적으로 관찰하세요.")
        st.write("• 다른 각도에서 잎 사진을 다시 촬영해 분석하세요.")

    else:
        st.write("• 현재 뚜렷한 병해 위험은 낮습니다.")
        st.write("• 예방 관리와 정기 점검을 유지하세요.")

    st.markdown("---")

else:
    st.info("환경데이터를 업로드한 뒤 AI 연구원 회의를 시작하세요.")
