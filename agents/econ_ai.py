import joblib
import pandas as pd
from pathlib import Path


class EconAI:
    def __init__(self):
        model_path = Path("models/econ_ai_model.pkl")

        self.model = None
        self.label_encoder = None
        self.columns = None

        if model_path.exists():
            saved = joblib.load(model_path)
            self.model = saved.get("model")
            self.label_encoder = saved.get("label_encoder")
            self.columns = saved.get("columns")

    def analyze(
        self,
        env_result=None,
        patho_result=None,
        production_kg=1000,
        market_price=2600,
        treatment_cost=50000,
        **kwargs
    ):
        env_result = env_result or {}
        patho_result = patho_result or {}

        # --------------------------
        # 1. 환경·병해 위험도 불러오기
        # --------------------------
        env_risk = float(env_result.get("risk_score", 0))

        disease_risk = float(
            patho_result.get(
                "disease_risk",
                patho_result.get(
                    "risk_score",
                    patho_result.get("confidence", 0)
                )
            )
        )

        disease_name = str(patho_result.get("disease", ""))

        safe_classes = {
            "건강한 잎",
            "개화기",
            "신선한 오이",
            "결실기 1단계",
            "결실기 2단계",
            "결실기 3단계"
        }

        # 정상 클래스의 confidence는 병해 위험도가 아님
        if disease_name in safe_classes:
            disease_risk = max(0.0, 100.0 - disease_risk)

        env_risk = max(0.0, min(100.0, env_risk))
        disease_risk = max(0.0, min(100.0, disease_risk))

        # --------------------------
        # 2. 머신러닝 출하 전략 예측
        # --------------------------
        if self.model is not None and self.columns is not None:
            input_data = pd.DataFrame([{
                "internal_temp": float(env_result.get("avg_temp", 25)),
                "humidity": float(env_result.get("avg_humidity", 70)),
                "co2": float(env_result.get("avg_co2", 400)),
                "solar": float(env_result.get("avg_solar", 0)),
                "total_solar": float(env_result.get("avg_total_solar", 0)),
                "risk_score": env_risk,
                "disease_risk": disease_risk
            }])

            input_data = input_data.reindex(
                columns=self.columns,
                fill_value=0
            )

            prediction_encoded = self.model.predict(input_data)[0]

            if self.label_encoder is not None:
                prediction_label = self.label_encoder.inverse_transform(
                    [prediction_encoded]
                )[0]
            else:
                prediction_label = str(prediction_encoded)

            if hasattr(self.model, "predict_proba"):
                confidence = (
                    max(self.model.predict_proba(input_data)[0]) * 100
                )
            else:
                confidence = 0.0

        else:
            prediction_label = "상태 관찰"
            confidence = 0.0

        # --------------------------
        # 3. 실제 경제성 계산
        # --------------------------
        production_kg = float(production_kg)
        market_price = float(market_price)
        treatment_cost = float(treatment_cost)

        gross_revenue = production_kg * market_price

        # 환경 위험과 병해 위험을 함께 반영
        combined_risk = max(
            disease_risk,
            env_risk * 0.6 + disease_risk * 0.4
        )

        # 최대 예상 손실률을 40%로 제한
        loss_rate = min(40.0, combined_risk * 0.40)

        expected_loss = gross_revenue * (loss_rate / 100)

        # 방제를 실시하면 병해 손실이 약 65% 감소한다고 가정
        treated_loss_rate = loss_rate * 0.35
        treated_loss = gross_revenue * (treated_loss_rate / 100)

        profit_without_treatment = gross_revenue - expected_loss
        profit_with_treatment = (
            gross_revenue
            - treated_loss
            - treatment_cost
        )

        benefit = (
            profit_with_treatment
            - profit_without_treatment
        )

        # --------------------------
        # 4. 최종 전략 결정
        # --------------------------
        if disease_risk >= 70 and benefit > 0:
            best_scenario = "방제 실시"
            profit_advice = (
                f"병해 위험이 {disease_risk:.1f}%로 높고, "
                f"방제 시 약 {benefit:,.0f}원의 경제적 이익이 예상됩니다."
            )

        elif benefit <= 0:
            best_scenario = "방제 미실시"
            profit_advice = (
                f"현재는 방제 비용이 예상 효과보다 "
                f"{abs(benefit):,.0f}원 더 큽니다. "
                "즉시 방제보다 상태 관찰을 권장합니다."
            )

        elif prediction_label == "즉시 출하":
            best_scenario = "즉시 출하"
            profit_advice = (
                "현재 환경과 경제 조건에서는 신속한 출하가 유리합니다."
            )

        else:
            best_scenario = str(prediction_label)
            profit_advice = (
                "현재는 급하게 출하하거나 방제하기보다 "
                "환경과 병해 상태를 계속 관찰하는 것이 적절합니다."
            )

        return {
            "econ_prediction": str(prediction_label),
            "econ_confidence": round(confidence, 1),
            "shipping_strategy": best_scenario,
            "strategy": best_scenario,
            "market_strategy": best_scenario,
            "best_scenario": best_scenario,

            "production_kg": round(production_kg, 1),
            "market_price": round(market_price, 1),
            "gross_revenue": round(gross_revenue),

            "env_risk": round(env_risk, 1),
            "disease_risk": round(disease_risk, 1),
            "loss_rate": round(loss_rate, 1),
            "treated_loss_rate": round(treated_loss_rate, 1),

            "expected_loss": round(expected_loss),
            "treatment_cost": round(treatment_cost),

            "profit_without_treatment": round(
                profit_without_treatment
            ),
            "profit_with_treatment": round(
                profit_with_treatment
            ),
            "benefit": round(benefit),

            "profit_advice": profit_advice
        }