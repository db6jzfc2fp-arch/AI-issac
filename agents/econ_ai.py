class EconAI:
    def analyze(
        self,
        production_kg=1000,
        market_price=2500,
        disease_risk=0,
        env_risk=0,
        treatment_cost=50000
    ):
        """
        production_kg: 예상 생산량(kg)
        market_price: kg당 시장 가격(원)
        disease_risk: 병해 위험도(0~100)
        env_risk: 환경 위험도(0~100)
        treatment_cost: 방제 비용(원)
        """

        # 1. 기본 매출
        gross_revenue = production_kg * market_price

        # 2. 병해/환경 위험에 따른 예상 손실률
        loss_rate = 0

        if disease_risk >= 80:
            loss_rate += 0.20
        elif disease_risk >= 60:
            loss_rate += 0.12
        elif disease_risk >= 40:
            loss_rate += 0.07
        elif disease_risk >= 20:
            loss_rate += 0.03

        if env_risk >= 80:
            loss_rate += 0.10
        elif env_risk >= 60:
            loss_rate += 0.06
        elif env_risk >= 40:
            loss_rate += 0.03

        # 최대 손실률 제한
        loss_rate = min(loss_rate, 0.45)

        # 3. 예상 손실
        expected_loss = int(gross_revenue * loss_rate)

        # 4. 방제 후 손실 감소 효과
        reduced_loss = int(expected_loss * 0.35)
        saved_loss = expected_loss - reduced_loss

        # 5. 방제했을 때 순이익 / 안 했을 때 순이익
        profit_without_treatment = gross_revenue - expected_loss
        profit_with_treatment = gross_revenue - reduced_loss - treatment_cost

        # 6. 방제 경제성
        benefit = profit_with_treatment - profit_without_treatment

        if benefit > 0:
            decision = "방제 후 출하 권장"
            strategy = "현재 병해 또는 환경 위험으로 인한 예상 손실이 방제 비용보다 크므로, 방제 후 출하하는 것이 경제적으로 유리합니다."
        else:
            decision = "관찰 후 출하 권장"
            strategy = "현재 예상 손실이 방제 비용보다 작아 즉시 방제보다는 상태를 관찰하며 출하 시기를 조정하는 것이 유리합니다."

        # 7. 가격 기준 출하 전략
        if market_price >= 3000:
            market_strategy = "현재 시장 가격이 높으므로 빠른 출하가 유리합니다."
        elif market_price >= 2200:
            market_strategy = "현재 시장 가격은 보통 수준입니다. 병해 위험이 높다면 방제 후 안정 출하를 권장합니다."
        else:
            market_strategy = "현재 시장 가격이 낮으므로 품질 관리 후 가격 회복 시 출하하는 전략이 유리합니다."

        return {
            "production_kg": production_kg,
            "market_price": market_price,
            "gross_revenue": gross_revenue,
            "disease_risk": disease_risk,
            "env_risk": env_risk,
            "loss_rate": round(loss_rate * 100, 1),
            "expected_loss": expected_loss,
            "treatment_cost": treatment_cost,
            "profit_without_treatment": int(profit_without_treatment),
            "profit_with_treatment": int(profit_with_treatment),
            "benefit": int(benefit),
            "decision": decision,
            "strategy": strategy,
            "market_strategy": market_strategy
        }

if __name__ == "__main__":
    econ = EconAI()
    result = econ.analyze(
        production_kg=1000,
        market_price=2600,
        disease_risk=85,
        env_risk=70,
        treatment_cost=50000
    )
    print(result)
