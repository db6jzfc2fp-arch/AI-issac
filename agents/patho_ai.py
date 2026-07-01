from PIL import Image
import numpy as np
import cv2


class PathoAI:

    def analyze_image(self, image, env_result):
        img = Image.open(image).convert("RGB")
        arr = np.array(img)

        hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)

        h = hsv[:, :, 0]
        s = hsv[:, :, 1]
        v = hsv[:, :, 2]

        leaf_mask = (h >= 25) & (h <= 95) & (s >= 35) & (v >= 40)

        powdery_mask = (v >= 145) & (s <= 95)
        downy_mask = (h >= 18) & (h <= 42) & (s >= 45) & (v >= 70)
        brown_mask = (h >= 5) & (h <= 25) & (s >= 45) & (v <= 170)

        leaf_area = max(leaf_mask.sum(), 1)
        green_ratio = leaf_mask.sum() / (arr.shape[0] * arr.shape[1]) * 100

        powdery_ratio = (powdery_mask & leaf_mask).sum() / leaf_area * 100
        downy_ratio = (downy_mask & leaf_mask).sum() / leaf_area * 100
        brown_ratio = (brown_mask & leaf_mask).sum() / leaf_area * 100

        humidity = env_result["avg_humidity"]

        if green_ratio < 20:
            disease = "사진 재촬영 필요"
            probability = 40
            risk = "중간"
            recommendation = "잎 영역이 충분히 감지되지 않았습니다. 잎이 화면에 크게 나오도록 다시 촬영하세요."

        elif downy_ratio >= 1.5 and humidity >= 70:
            disease = "노균병 의심"
            probability = min(90, int(45 + downy_ratio * 8))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "노란 병반과 높은 습도가 감지됩니다. 노균병 가능성이 있으므로 환기와 제습을 강화하세요."

        elif powdery_ratio >= 6 and downy_ratio < 4:
            disease = "흰가루병 의심"
            probability = min(90, int(40 + powdery_ratio * 7))
            risk = "높음" if probability >= 70 else "중간"
            recommendation = "잎 표면에 흰색 병반이 감지됩니다. 흰가루병 가능성이 있으므로 병든 잎을 확인하세요."

        elif brown_ratio >= 3:
            disease = "갈변 또는 괴사 의심"
            probability = min(85, int(40 + brown_ratio * 8))
            risk = "중간"
            recommendation = "갈색 병반이 감지됩니다. 병든 잎의 확산 여부를 확인하세요."

        elif humidity >= 88:
            disease = "노균병 환경 위험"
            probability = 65
            risk = "중간"
            recommendation = "사진상 뚜렷한 병반은 적지만 내부 습도가 높아 노균병 위험이 있습니다. 환기와 제습을 강화하세요."

        else:
            disease = "뚜렷한 병징 없음"
            probability = 18
            risk = "낮음"
            recommendation = "현재 사진과 환경 기준으로 병해 위험은 낮습니다."

        return {
            "disease": disease,
            "probability": probability,
            "risk": risk,
            "recommendation": recommendation,
            "powdery_ratio": round(powdery_ratio, 2),
            "downy_ratio": round(downy_ratio, 2),
            "brown_ratio": round(brown_ratio, 2),
            "green_ratio": round(green_ratio, 2)
        }
