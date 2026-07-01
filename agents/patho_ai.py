from PIL import Image
import numpy as np


class PathoAI:

    def analyze_image(self, image, env_result):
        img = Image.open(image).convert("RGB")
        arr = np.array(img)

        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        # 기본 색상 분석
        white_mask = (r > 160) & (g > 160) & (b > 160) & (abs(r - g) < 35) & (abs(g - b) < 35)
        yellow_mask = (r > 120) & (g > 100) & (b < 100) & (r >= g * 0.8)
        brown_mask = (r > 80) & (g > 40) & (b < 80) & (r > g)
        green_mask = (g > r * 1.05) & (g > b * 1.05) & (g > 60)

        white_ratio = white_mask.mean() * 100
        yellow_ratio = yellow_mask.mean() * 100
        brown_ratio = brown_mask.mean() * 100
        green_ratio = green_mask.mean() * 100

        humidity = env_result["avg_humidity"]

        # 1. 흰가루병: 잎 표면의 흰/회백색 반점
        if white_ratio >= 3:
            disease = "흰가루병 의심"
            probability = min(95, int(45 + white_ratio * 8))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "잎 표면에 흰색 또는 회백색 병징이 감지됩니다. 흰가루병 가능성이 있으므로 병든 잎을 확인하고 방제 여부를 검토하세요."

        # 2. 노균병: 고습도 + 노란 병반
        elif humidity >= 80 and yellow_ratio >= 2:
            disease = "노균병 의심"
            probability = min(92, int(50 + yellow_ratio * 8))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "습도가 높고 노란 병반이 감지됩니다. 노균병 가능성이 있으므로 환기를 강화하고 잎 표면의 물기를 줄이세요."

        # 3. 갈변/괴사 의심
        elif brown_ratio >= 4:
            disease = "갈변 또는 괴사 의심"
            probability = min(85, int(40 + brown_ratio * 7))
            risk = "중간"
            recommendation = "갈색 병반 또는 괴사 부위가 감지됩니다. 병든 잎을 관찰하고 확산 여부를 확인하세요."

        # 4. 환경성 노균병 위험
        elif humidity >= 85:
            disease = "노균병 환경 위험"
            probability = 70
            risk = "중간"
            recommendation = "사진상 뚜렷한 병반은 적지만 습도가 높아 노균병 위험이 있습니다. 환기와 제습을 강화하세요."

        # 5. 사진/잎 상태 확인
        elif green_ratio < 10:
            disease = "잎 상태 확인 필요"
            probability = 50
            risk = "중간"
            recommendation = "초록 잎 영역이 적게 감지됩니다. 잎이 화면에 크게 나오도록 다시 촬영하거나 사진 품질을 확인하세요."

        else:
            disease = "뚜렷한 병징 없음"
            probability = 18
            risk = "낮음"
            recommendation = "현재 사진과 환경 기준으로 병해 위험은 낮습니다. 잎 상태를 주기적으로 관찰하세요."

        return {
            "disease": disease,
            "probability": probability,
            "risk": risk,
            "recommendation": recommendation,
            "white_ratio": round(white_ratio, 2),
            "yellow_ratio": round(yellow_ratio, 2),
            "brown_ratio": round(brown_ratio, 2),
            "green_ratio": round(green_ratio, 2)
        }
