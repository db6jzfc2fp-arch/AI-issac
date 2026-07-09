import joblib
import pandas as pd
from pathlib import Path


class EconAI:
    def __init__(self):
        model_path = Path("models/econ_ai_model.pkl")

        if not model_path.exists():
            self.model = None
        else:
            self.model = joblib.load(model_path)

    def analyze(self, env_result=None, patho_result=None):
        if self.model is None:
            return {
                "econ_prediction": "모델 파일 없음",
                "econ_confidence": 0,
                "shipping_strategy": "models/econ_ai_model.pkl 파일을 확인하세요.",
                "profit_advice": "Econ-AI 모델이 연결되지 않았습니다."
            }

        input_data = pd.DataFrame([{
            "internal_temp": env_result.get("avg_temp", 25),
            "internal_humidity": env_result.get("avg_humidity", 70),
            "risk_score": env_result.get("risk_score", 50),
            "disease_risk": patho_result.get("confidence", 0) if patho_result else 0
        }])

        prediction = self.model.predict(input_data)[0]

        if hasattr(self.model, "predict_proba"):
            confidence = max(self.model.predict_proba(input_data)[0]) * 100
        else:
            confidence = 0

        if prediction == 1:
            strategy = "출하 권장"
            advice = "현재 환경과 병해 위험을 고려했을 때 출하 전략이 유리합니다."
        else:
            strategy = "출하 보류"
            advice = "현재 조건에서는 품질 저하나 수익성 감소 가능성이 있어 출하를 보류하는 것이 좋습니다."

        return {
            "econ_prediction": int(prediction),
            "econ_confidence": round(confidence, 1),
            "shipping_strategy": strategy,
            "profit_advice": advice
        }
