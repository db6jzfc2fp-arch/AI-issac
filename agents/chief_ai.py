class ChiefAI:

    def make_decision(self, env_result, patho_result, econ_result):
        env_result = env_result or {}
        patho_result = patho_result or {}
        econ_result = econ_result or {}

        actions = []

        env_risk_score = float(env_result.get("risk_score", 0))
        env_risk_level = str(env_result.get("risk_level", "안정"))

        disease = str(patho_result.get("disease", "진단 정보 없음"))
        confidence = float(patho_result.get("confidence", 0))
        disease_risk = float(
            patho_result.get("disease_risk", patho_result.get("risk_score", confidence))
        )

        best_scenario = str(
            econ_result.get(
                "best_scenario",
                econ_result.get("shipping_strategy", "상태 관찰")
            )
        )

        benefit = float(econ_result.get("benefit", 0))
        loss_rate = float(econ_result.get("loss_rate", 0))

        safe_classes = {
            "건강한 잎",
            "개화기",
            "신선한 오이",
            "결실기 1단계",
            "결실기 2단계",
            "결실기 3단계"
        }

        # 정상 클래스는 confidence가 높을수록 실제 병해 위험은 낮음
        if disease in safe_classes:
            disease_risk = max(0.0, 100.0 - confidence)

        # 환경 분석
        if env_risk_score >= 70:
            actions.append("시설 내부 온도와 습도를 즉시 확인하세요.")
            actions.append("환기창과 순환팬을 가동하여 환경 위험을 낮추세요.")

        elif env_risk_score >= 40:
            actions.append("온도·습도·풍속과 근권부 EC·pH를 주기적으로 점검하세요.")

        else:
            actions.append("현재 환경은 안정적이므로 기존 관리 상태를 유지하세요.")

        # 병해 분석
        if disease in safe_classes:
            actions.append(
                f"Patho-AI는 '{disease}' 상태를 {confidence:.1f}% 확률로 예측했습니다."
            )
            actions.append("현재 추가적인 병해 방제는 필요하지 않습니다.")
            actions.append("잎과 생육 상태를 정기적으로 재확인하세요.")

        elif disease_risk >= 70:
            actions.append(
                f"'{disease}' 가능성이 높으므로 피해 부위를 현장에서 확인하세요."
            )
            actions.append("피해 잎이나 과실을 제거하고 적절한 초기 방제를 검토하세요.")
            actions.append("환기와 습도 관리를 강화하세요.")

        elif disease_risk >= 40:
            actions.append(
                f"'{disease}' 가능성이 있으므로 병징 변화를 지속적으로 관찰하세요."
            )
            actions.append("즉시 방제보다 재촬영과 현장 확인을 우선하세요.")

        else:
            actions.append("현재 뚜렷한 병해 위험은 낮습니다.")

        # 경제 분석
        if best_scenario == "방제 실시" and benefit > 0:
            actions.append(
                f"방제를 실시하면 약 {benefit:,.0f}원의 추가 경제효과가 예상됩니다."
            )

        elif best_scenario == "방제 미실시" or benefit < 0:
            actions.append(
                f"현재는 즉시 방제보다 상태 관찰이 경제적으로 유리합니다."
            )

        elif best_scenario == "즉시 출하":
            actions.append("현재 경제 조건에서는 신속한 출하를 검토하세요.")

        else:
            actions.append(
                econ_result.get(
                    "profit_advice",
                    "현재는 생육 상태와 시장 상황을 계속 관찰하세요."
                )
            )

        # 최종 위험도
        final_risk_score = max(env_risk_score, disease_risk)

        if final_risk_score >= 70:
            final_risk_level = "높음"
        elif final_risk_score >= 40:
            final_risk_level = "주의"
        else:
            final_risk_level = "안정"

        # 최종 요약
        if disease in safe_classes and final_risk_level == "안정":
            summary = (
                f"환경과 병해 상태가 안정적입니다. "
                f"현재는 방제보다 기존 관리 상태를 유지하는 것이 적절합니다."
            )

        elif final_risk_level == "높음":
            summary = (
                "환경 또는 병해 위험이 높게 나타났습니다. "
                "현장 확인 후 즉각적인 대응이 필요합니다."
            )

        else:
            summary = (
                "현재 종합 위험도는 주의 수준입니다. "
                "즉각적인 조치보다 지속적인 관찰과 예방 관리가 적절합니다."
            )

        return {
            "summary": summary,
            "actions": actions,
            "final_risk_score": round(final_risk_score, 1),
            "final_risk_level": final_risk_level,
            "environment_risk": round(env_risk_score, 1),
            "disease_risk": round(disease_risk, 1),
            "disease": disease,
            "best_scenario": best_scenario,
            "loss_rate": round(loss_rate, 1),
            "benefit": round(benefit)
        }