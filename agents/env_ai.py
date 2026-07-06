import pandas as pd

class EnvAI:

    def analyze(self, df):

        # 숫자 변환
        internal_temp = pd.to_numeric(df["온도_내부"], errors="coerce")
        outside_temp = pd.to_numeric(df["온도_외부"], errors="coerce")
        humidity = pd.to_numeric(df["상대습도_내부"], errors="coerce")
        wind_speed = pd.to_numeric(df["풍속_외부"], errors="coerce")
        solar = pd.to_numeric(df["일사량_외부"], errors="coerce")
        total_solar = pd.to_numeric(df["누적일사량_외부"], errors="coerce")
        co2 = pd.to_numeric(df["잔존CO2"], errors="coerce")
        soil_temp = pd.to_numeric(df["토양온도"], errors="coerce")

        # 평균 계산
        avg_temp = round(internal_temp.mean(), 1)
        avg_outside_temp = round(outside_temp.mean(), 1)
        avg_humidity = round(humidity.mean(), 1)
        avg_wind_speed = round(wind_speed.mean(), 1)
        avg_solar = round(solar.mean(), 1)
        avg_total_solar = round(total_solar.mean(), 1)
        avg_co2 = round(co2.mean(), 1)
        avg_soil_temp = round(soil_temp.mean(), 1)

        risk_score = 0
        reasons = []
        advice = []

        # 온도 분석
        if avg_temp >= 30:
            risk_score += 30
            reasons.append("내부 온도가 높아 오이 고온 스트레스 위험이 있습니다.")
            advice.append("환기와 차광을 강화하세요.")
        elif avg_temp <= 15:
            risk_score += 25
            reasons.append("내부 온도가 낮아 오이 생육 저하 위험이 있습니다.")
            advice.append("보온 관리가 필요합니다.")
        else:
            reasons.append("내부 온도는 비교적 안정적입니다.")

        # 습도 분석
        if avg_humidity >= 85:
            risk_score += 35
            reasons.append("내부 습도가 높아 결로와 병 발생 위험이 증가합니다.")
            advice.append("오전 환기와 과습 관리를 강화하세요.")
        elif avg_humidity <= 45:
            risk_score += 20
            reasons.append("내부 습도가 낮아 건조 스트레스 가능성이 있습니다.")
            advice.append("관수 상태를 확인하세요.")
        else:
            reasons.append("내부 습도는 비교적 안정적입니다.")

        # CO2 분석
        if avg_co2 < 400:
            risk_score += 10
            reasons.append("잔존 CO2가 낮아 광합성 효율이 떨어질 수 있습니다.")
            advice.append("CO2 공급 또는 환기 상태를 확인하세요.")

        # 일사량 분석
        if avg_solar > 700:
            risk_score += 10
            reasons.append("일사량이 높아 내부 온도 상승 가능성이 있습니다.")
            advice.append("차광막 사용을 검토하세요.")

        # 풍속 분석
        if avg_wind_speed >= 5:
            reasons.append("외부 풍속이 있어 자연환기 효과를 기대할 수 있습니다.")
        else:
            reasons.append("외부 풍속이 낮아 자연환기 효과가 제한적일 수 있습니다.")

        risk_score = min(risk_score, 100)

        if risk_score >= 70:
            risk_level = "위험"
        elif risk_score >= 40:
            risk_level = "주의"
        else:
            risk_level = "안정"

        if not advice:
            advice.append("현재 환경은 전반적으로 안정적입니다. 현재 관리 상태를 유지하세요.")
            advice.append("주기적으로 온도·습도·병해 상태를 확인하세요.")
            advice.append("외부 풍속이 낮을 경우 환기 타이밍을 점검하세요.")
        
        return {
            "avg_temp": avg_temp,
            "avg_outside_temp": avg_outside_temp,
            "avg_humidity": avg_humidity,
            "avg_wind_speed": avg_wind_speed,
            "avg_solar": avg_solar,
            "avg_total_solar": avg_total_solar,
            "avg_co2": avg_co2,
            "avg_soil_temp": avg_soil_temp,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons,
            "advice": advice
        }
