class EnvAI:

    def analyze(self, df):
        columns = list(df.columns)

        result = {
            "columns": columns,
            "risk_score": 0,
            "risk_level": "안전",
            "reasons": [],
            "advice": []
        }

        # 컬럼 자동 찾기
        def find_col(names):
            for name in names:
                if name in df.columns:
                    return name
            return None

        inside_temp_col = find_col(["내부온도", "내부 온도", "기온", "온도"])
        outside_temp_col = find_col(["외부온도", "외부 온도"])
        humidity_col = find_col(["내부습도", "내부상대습도", "상대습도", "습도"])
        co2_col = find_col(["잔존CO2", "잔존 CO2", "CO2"])
        soil_temp_col = find_col(["토양온도", "토양 온도", "지온"])
        solar_col = find_col(["외부일사량", "일사량"])
        rain_col = find_col(["강우감지", "강우 감지"])

        # 평균값 계산
        result["avg_temp"] = round(df[inside_temp_col].mean(), 1) if inside_temp_col else 0
        result["avg_humidity"] = round(df[humidity_col].mean(), 1) if humidity_col else 0

        # 내부온도 분석
        if inside_temp_col:
            avg_temp = result["avg_temp"]

            if avg_temp >= 32:
                result["risk_score"] += 25
                result["reasons"].append("내부 평균온도가 높아 오이 고온 스트레스 위험이 있습니다.")
                result["advice"].append("차광, 환기, 관수 조절이 필요합니다.")
            elif avg_temp <= 15:
                result["risk_score"] += 20
                result["reasons"].append("내부 평균온도가 낮아 생육 저하 위험이 있습니다.")
                result["advice"].append("야간 보온 관리가 필요합니다.")
            else:
                result["reasons"].append("내부온도는 비교적 안정적입니다.")

        # 습도 분석
        if humidity_col:
            avg_humidity = result["avg_humidity"]

            if avg_humidity >= 90:
                result["risk_score"] += 30
                result["reasons"].append("내부습도가 매우 높아 결로와 병 발생 위험이 큽니다.")
                result["advice"].append("오전 환기와 과습 방지가 필요합니다.")
            elif avg_humidity >= 80:
                result["risk_score"] += 20
                result["reasons"].append("내부습도가 높아 노균병 등 병 발생 위험이 증가합니다.")
                result["advice"].append("환기 시간을 늘리고 잎 표면 물기를 줄이세요.")
            else:
                result["reasons"].append("내부습도는 비교적 안정적입니다.")

        # 토양온도 분석
        if soil_temp_col:
            avg_soil_temp = round(df[soil_temp_col].mean(), 1)
            result["avg_soil_temp"] = avg_soil_temp

            if avg_soil_temp <= 15:
                result["risk_score"] += 15
                result["reasons"].append("토양온도가 낮아 뿌리 활력이 떨어질 수 있습니다.")
                result["advice"].append("지온 확보와 보온 관리를 확인하세요.")
            elif avg_soil_temp >= 28:
                result["risk_score"] += 15
                result["reasons"].append("토양온도가 높아 뿌리 스트레스 가능성이 있습니다.")
                result["advice"].append("관수 시간과 지온 상승을 점검하세요.")

        # CO2 분석
        if co2_col:
            avg_co2 = round(df[co2_col].mean(), 1)
            result["avg_co2"] = avg_co2

            if avg_co2 < 350:
                result["risk_score"] += 10
                result["reasons"].append("CO₂ 농도가 낮아 광합성 효율이 떨어질 수 있습니다.")
                result["advice"].append("환기와 CO₂ 공급 상태를 확인하세요.")

        # 강우 감지
        if rain_col:
            rain_count = df[rain_col].sum()
            result["rain_count"] = int(rain_count)

            if rain_count > 0:
                result["risk_score"] += 10
                result["reasons"].append("강우 감지가 있어 외부 습도 상승과 병 발생 위험이 증가할 수 있습니다.")
                result["advice"].append("강우 후 온실 내부 습도와 결로를 확인하세요.")

        # 위험도 제한
        result["risk_score"] = min(result["risk_score"], 100)

        if result["risk_score"] >= 70:
            result["risk_level"] = "위험"
        elif result["risk_score"] >= 40:
            result["risk_level"] = "주의"
        else:
            result["risk_level"] = "안전"

        if not result["advice"]:
            result["advice"].append("현재 환경은 비교적 안정적입니다. 정기적인 모니터링을 유지하세요.")

        return result
