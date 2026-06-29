def analyze_environment(crop, temp, humidity):
    risk_score = 0
    reasons = []
    advice = []

    # 온도 분석
    if temp >= 35:
        risk_score += 35
        reasons.append("고온 스트레스 위험이 큽니다.")
        advice.append("차광, 환기, 관수량 증가를 고려하세요.")
    elif temp >= 30:
        risk_score += 20
        reasons.append("온도가 다소 높습니다.")
        advice.append("환기와 수분 관리를 강화하세요.")
    elif temp <= 10:
        risk_score += 30
        reasons.append("저온 스트레스 위험이 있습니다.")
        advice.append("보온 관리가 필요합니다.")
    elif temp <= 15:
        risk_score += 15
        reasons.append("온도가 다소 낮습니다.")
        advice.append("야간 온도 저하를 주의하세요.")
    else:
        reasons.append("온도는 비교적 적정 범위입니다.")

    # 습도 분석
    if humidity >= 90:
        risk_score += 35
        reasons.append("습도가 매우 높아 병 발생 위험이 큽니다.")
        advice.append("환기와 제습을 강화하세요.")
    elif humidity >= 80:
        risk_score += 20
        reasons.append("습도가 높아 곰팡이성 병 위험이 있습니다.")
        advice.append("잎 표면의 물기와 과습을 줄이세요.")
    elif humidity <= 40:
        risk_score += 20
        reasons.append("습도가 낮아 건조 스트레스 위험이 있습니다.")
        advice.append("관수 간격과 토양 수분을 확인하세요.")
    else:
        reasons.append("습도는 비교적 안정적입니다.")

    # 작물별 보정
    if crop == "방울토마토":
        if temp >= 30 and humidity >= 80:
            risk_score += 15
            reasons.append("방울토마토는 고온다습 조건에서 잿빛곰팡이병 위험이 증가합니다.")
            advice.append("밀식 상태를 피하고 하엽 제거와 환기를 관리하세요.")

        if temp >= 32:
            risk_score += 10
            reasons.append("고온 조건에서는 착과불량과 열과 위험이 증가할 수 있습니다.")
            advice.append("급격한 수분 변화가 생기지 않도록 관수를 일정하게 유지하세요.")

    elif crop == "파프리카":
        if temp >= 30:
            risk_score += 10
            reasons.append("파프리카는 고온에서 착과 불량 위험이 커질 수 있습니다.")
            advice.append("온실 내부 온도와 차광 관리를 확인하세요.")

    # 점수 제한
    risk_score = min(risk_score, 100)

    # 위험 등급
    if risk_score >= 70:
        risk_level = "높음"
    elif risk_score >= 40:
        risk_level = "주의"
    else:
        risk_level = "낮음"

    return {
        "agent": "Env-AI",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": reasons,
        "advice": advice
    }
