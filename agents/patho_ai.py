from PIL import Image
import numpy as np
import cv2


class PathoAI:

    def analyze_image(self, image, env_result):
        img = Image.open(image).convert("RGB")
        arr = np.array(img)

        # RGB → HSV 변환
        hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)

        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        # 1. 잎 영역 추출: 초록색 계열
        leaf_mask = (h >= 25) & (h <= 95) & (s >= 35) & (v >= 40)

        # 2. 흰가루병 후보: 밝고 채도가 낮은 흰/회백색 영역
        powdery_mask = (v >= 145) & (s <= 95)

        # 3. 노균병 후보: 노란 병반 영역
        downy_mask = (h >= 18) & (h <= 42) & (s >= 45) & (v >= 70)

        # 4. 갈변/괴사 후보: 갈색, 어두운 병반
        brown_mask = (h >= 5) & (h <= 25) & (s >= 45) & (v <= 170)

        leaf_area = max(leaf_mask.sum(), 1)

        powdery_ratio = (powdery_mask & leaf_mask).sum() / leaf_area * 100
        downy_ratio = (downy_mask & leaf_mask).sum() / leaf_area * 100
        brown_ratio = (brown_mask & leaf_mask).sum() / leaf_area * 100

        humidity = env_result["avg_humidity"]

        # 병해 판단
        if downy_ratio >= 6 and humidity >= 85:
            disease = "노균병 의심"
            probability = min(95, int(50 + downy_ratio * 10 + (humidity - 70) * 0.5))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "노란 병반과 높은 습도가 함께 감지됩니다. 노균병 가능성이 있으므로 환기를 강화하고 잎 표면의 물기를 줄이세요."

        elif powdery_ratio >= 3:
            disease = "흰가루병 의심"
            probability = min(95, int(45 + powdery_ratio * 12))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "잎 표면에 흰색 또는 회백색 병반이 감지됩니다. 흰가루병 가능성이 있으므로 병든 잎을 확인하고 방제 여부를 검토하세요."

        elif brown_ratio >= 2:
            disease = "갈변 또는 괴사 의심"
            probability = min(90, int(45 + brown_ratio * 10))
            risk = "중간"
            recommendation = "갈색 병반 또는 괴사 부위가 감지됩니다. 병든 잎의 확산 여부를 확인하세요."

        elif humidity >= 85:
            disease = "노균병 환경 위험"
            probability = 70
            risk = "중간"
            recommendation = "사진상 뚜렷한 병반은 적지만 습도가 높아 노균병 위험이 있습니다. 환기와 제습을 강화하세요."

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
            "powdery_ratio": round(powdery_ratio, 2),
            "downy_ratio": round(downy_ratio, 2),
            "brown_ratio": round(brown_ratio, 2),
        }
