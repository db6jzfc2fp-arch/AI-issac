import joblib
import pandas as pd
from pathlib import Path


class EconAI:
    def __init__(self):
        model_path = Path("models/econ_ai_model.pkl")

        if not model_path.exists():
            self.model = None
            self.label_encoder = None
            self.columns = None
        else:
            saved = joblib.load(model_path)
            self.model = saved["model"]
            self.label_encoder = saved["label_encoder"]
            self.columns = saved["columns"]

    def analyze(self, env_result=None, patho_result=None, **kwargs):
        if env_result is None:
            env_result = {}

        if self.model is None:
            return {
                "econ_prediction": "모델 파일 없음",
                "econ_confidence": 0,
                "shipping_strategy": "models/econ_ai_model.pkl 파일을 확인하세요.",
                "profit_advice": "Econ-AI 모델이 연결되지 않았습니다."
            }

        input_data = pd.DataFrame([{
            "internal_temp": env_result.get("avg_temp", 25),
            "humidity": env_result.get("avg_humidity", 70),
            "co2": env_result.get("avg_co2", 400),
            "solar": env_result.get("avg_solar", 0),
            "total_solar": env_result.get("avg_total_solar", 0),
        }])

        input_data = input_data.reindex(columns=self.columns, fill_value=0)

        prediction_encoded = self.model.predict(input_data)[0]
        prediction_label = self.label_encoder.inverse_transform([prediction_encoded])[0]

        if hasattr(self.model, "predict_proba"):
            confidence = max(self.model.predict_proba(input_data)[0]) * 100
        else:
            confidence = 0

        if prediction_label == "즉시 출하":
            advice = "현재 조건에서는 출하 전략이 가장 유리합니다."
        elif prediction_label == "즉시 방제":
            advice = "현재 조건에서는 병해 및 품질 저하 위험이 있어 방제를 우선하는 것이 좋습니다."
        else:
            advice = "현재 조건에서는 급하게 출하하거나 방제하기보다 상태를 관찰하는 것이 좋습니다."

        return {
            "econ_prediction": prediction_label,
            "econ_confidence": round(confidence, 1),
            "shipping_strategy": prediction_label,
            "profit_advice": advice
        }