class EconAI:
    def analyze(
        self,
        production_kg=1000,
        market_price=2500,
        disease_risk=0,
        env_risk=0,
        treatment_cost=50000
    ):
        gross_revenue = production_kg * market_price

        base_loss_rate = min(
            disease_risk * 0.22 + env_risk * 0.08,
            45
        )

        scenarios = []

        plans = [
            ("즉시 방제", 0.35, treatment_cost, "추천"),
            ("2일 관찰 후 방제", 0.55, int(treatment_cost * 0.9), "조건부"),
            ("방제하지 않음", 1.0, 0, "비추천")
        ]

        for name, loss_multiplier, cost, label in plans:
            loss_rate = base_loss_rate * loss_multiplier
            expected_loss = int(gross_revenue * loss_rate / 100)
            profit = gross_revenue - expected_loss - cost

            scenarios.append({
                "name": name,
                "loss_rate": round(loss_rate, 1),
                "expected_loss": expected_loss,
                "treatment_cost": cost,
                "profit": int(profit),
                "label": label
            })

        best = max(scenarios, key=lambda x: x["profit"])

        profit_without_treatment = scenarios[2]["profit"]
        profit_with_treatment = scenarios[0]["profit"]
        benefit = profit_with_treatment - profit_without_treatment

        if best["name"] == "즉시 방제":
            decision = "즉시 방제 권장"
            strategy = "세 가지 선택지 중 즉시 방제 시 예상 순이익이 가장 높습니다."
        elif best["name"] == "2일 관찰 후 방제":
            decision = "2일 관찰 후 방제 권장"
            strategy = "현재는 즉시 방제보다 짧은 관찰 후 방제가 더 유리합니다."
        else:
            decision = "방제 없이 관찰 권장"
            strategy = "현재 위험도에서는 방제 비용이 예상 손실보다 커서 관찰이 유리합니다."

        if market_price >= 3000:
            market_strategy = "현재 시장 가격이 높으므로 빠른 출하가 유리합니다."
        elif market_price >= 2200:
            market_strategy = "현재 시장 가격은 보통 수준입니다. 품질을 유지하며 안정 출하를 권장합니다."
        else:
            market_strategy = "현재 시장 가격이 낮으므로 품질 관리 후 가격 회복 시 출하하는 전략이 유리합니다."

        return {
            "production_kg": production_kg,
            "market_price": market_price,
            "gross_revenue": gross_revenue,
            "disease_risk": disease_risk,
            "env_risk": env_risk,
            "loss_rate": scenarios[0]["loss_rate"],
            "expected_loss": scenarios[0]["expected_loss"],
            "treatment_cost": treatment_cost,
            "profit_without_treatment": int(profit_without_treatment),
            "profit_with_treatment": int(profit_with_treatment),
            "benefit": int(benefit),
            "decision": decision,
            "strategy": strategy,
            "market_strategy": market_strategy,
            "scenarios": scenarios,
            "best_scenario": best["name"]
        }
