class PathoAI:

    def analyze_image(self, image, env_result):

        if env_result["humidity"] >= 85:
            disease = "노균병 의심"
            probability = 82
            risk = "높음"
            recommendation = "습도가 높아 노균병 위험이 있습니다. 환기 강화와 예방 방제를 검토하세요."
        else:
            disease = "뚜렷한 병징 없음"
            probability = 18
            risk = "낮음"
            recommendation = "현재 병해 위험은 낮습니다. 잎 상태를 주기적으로 관찰하세요."

        return {
            "disease": disease,
            "probability": probability,
            "risk": risk,
            "recommendation": recommendation
        }
