import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


class PathoAI:
    def __init__(self):
        self.model_path = "models/cucumber_leaf_best_model.keras"
        self.model = load_model(self.model_path)

        self.class_names = [
            "Anthracnose",
            "Bacterial Wilt",
            "Belly Rot",
            "Downy Mildew",
            "Flowering",
            "Fresh Cucumber",
            "Healthy Leaves",
            "Powdery Mildew",
        ]

    def analyze_image(self, image, env_result=None):
        img = Image.open(image).convert("RGB")
        img = img.resize((224, 224))

        arr = np.array(img)
        arr = np.expand_dims(arr, axis=0)
        arr = preprocess_input(arr)

        preds = self.model.predict(arr, verbose=0)[0]
        idx = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)

        if idx >= len(self.class_names):
            disease = "Unknown"
        else:
            disease = self.class_names[idx]
            
        return {
            "disease": disease,
            "confidence": round(confidence, 1),
            "risk": "높음" if confidence >= 70 and disease != "Healthy Leaves" else "낮음",
            "advice": f"딥러닝 모델이 이미지를 분석한 결과 {disease} 가능성이 가장 높습니다."
        }