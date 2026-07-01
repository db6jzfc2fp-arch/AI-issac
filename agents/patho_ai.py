from PIL import Image
import numpy as np


class PathoAI:

    def analyze_image(self, image, env_result):
        img = Image.open(image).convert("RGB")
        arr = np.array(img)

        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        # 흰가루병 후보: 밝고 흰색에 가까운 픽셀
        white_mask = (r > 180) & (g > 180) & (b > 180)

        # 잎/초록 영역 후보
        green_mask = (g > r) & (g > b) & (g > 80)

        white_ratio = white_mask.mean() * 100
        green_ratio = green_mask.mean() * 100
        humidity = env_result["avg_humidity"]

        if white_ratio >= 8:
            disease = "흰가루병 의심"
            probability = min(95, int(white_ratio * 8))
            risk = "높음"
            recommendation = "잎 표면에 흰색 병징이 감지됩니다. 흰가루병 가능성이 있으므로 병든 잎을 확인하고 방제 여부를 검토하세요."

        elif humidity >= 85:
            disease = "노균병 의심"
            probability = 82
            risk = "높음"
            recommendation = "습도가 높아 노균병 위험이 있습니다. 환기를 강화하고 잎 표면의 물기를 줄이세요."

        elif green_ratio < 15:
            disease = "잎 상태 확인 필요"
            probability = 55
            risk = "중간"
            recommendation = "초록 잎 영역이 적게 감지됩니다. 사진 품질이나 잎 상태를 다시 확인하세요."

        else:
            disease = "뚜렷한 병징 없음"
            probability = 18
            risk = "낮음"
            recommendation = "현재 병해 위험은 낮습니다. 잎 상태를 주기적으로 관찰하세요."

        return {
            "disease": disease,
            "probability": probability,
            "risk": risk,
            "recommendation": recommendation,
            "white_ratio": round(white_ratio, 2),
            "green_ratio": round(green_ratio, 2)
        }
