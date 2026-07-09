class ChiefAI:

    def make_decision(self, env_result, patho_result, econ_result):

        actions = []

        # 환경 분석
        if env_result["risk"] == "HIGH":
            actions.append("환기창을 개방하여 시설 내부 온도를 낮추세요.")
            actions.append("차광막을 활용하여 고온 스트레스를 줄이세요.")

        # 병해 분석
        if patho_result["confidence"] >= 70:
            actions.append("노균병 예방 방제를 실시하는 것을 권장합니다.")
            actions.append("잎의 앞·뒷면을 추가로 점검하세요.")

        # 경제 분석
        if econ_result["grade"] == "매우 우수":
            actions.append("현재 시장 상황이 좋아 출하를 고려해보세요.")
        else:
            actions.append("출하보다는 생육 관리에 집중하는 것이 좋습니다.")

        return {
            "summary": "AI 연구원들의 의견을 종합하여 최종 행동지침을 생성했습니다.",
            "actions": actions
        }
