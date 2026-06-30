class EnvAI:

    def analyze(self, df):
        return {
            "avg_temp": 0,
            "avg_humidity": 0,            
            "risk_score": 50,
            "risk_level": "주의",
            "reasons": [
                "환경데이터 업로드가 확인되었습니다.",
                "오이 재배 환경 분석을 시작했습니다."
            ],
            "advice": [
                "온도, 습도, EC, 토양수분 데이터를 기준으로 추가 분석이 필요합니다."
            ]
        }
