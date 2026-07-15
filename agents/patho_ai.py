import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


class PathoAI:
    
    DISEASE_INFO = {
    "탄저병": {
        "cause": [
            "고온다습한 환경에서 발생 위험이 커집니다.",
            "병든 잎이나 과실의 병원균이 빗물과 관수에 의해 퍼질 수 있습니다."
        ],
        "symptoms": [
            "잎이나 과실에 갈색 또는 검은색 반점이 나타납니다.",
            "병반이 커지면서 조직이 움푹 파이거나 마를 수 있습니다."
        ],
        "actions": [
            "감염 부위를 즉시 제거하고 재배지 밖으로 반출하세요.",
            "잎이 장시간 젖지 않도록 관수 시간과 환기를 조절하세요.",
            "등록된 적용 약제를 기준에 맞게 사용하세요."
        ]
    },

    "세균성 시들음병": {
        "cause": [
            "세균이 뿌리나 상처를 통해 침입해 물관을 막으면서 발생합니다.",
            "고온과 과습 조건에서 피해가 커질 수 있습니다."
        ],
        "symptoms": [
            "낮에 급격히 시들고 초기에는 밤에 일부 회복될 수 있습니다.",
            "진행되면 식물 전체가 시들고 고사합니다."
        ],
        "actions": [
            "의심 개체는 즉시 격리하거나 제거하세요.",
            "배수 상태를 점검하고 과습을 피하세요.",
            "작업 도구를 소독해 다른 개체로의 전염을 막으세요."
        ]
    },

    "배꼽썩음병": {
        "cause": [
            "과습과 통풍 불량 조건에서 과실 하부가 감염될 수 있습니다.",
            "지면이나 오염된 잔재와 접촉할 때 발생 위험이 증가합니다."
        ],
        "symptoms": [
            "과실의 꽃이 달렸던 끝부분에 물러진 갈색 병반이 나타납니다.",
            "병반이 확대되면서 과실이 썩습니다."
        ],
        "actions": [
            "감염 과실을 즉시 제거하세요.",
            "과실이 토양이나 물에 직접 닿지 않도록 관리하세요.",
            "습도를 낮추고 통풍을 강화하세요."
        ]
    },

    "노균병": {
        "cause": [
            "높은 습도와 잎의 장시간 젖음이 주요 발생 조건입니다.",
            "환기가 부족하고 밤낮 온도 차가 클 때 위험이 증가합니다."
        ],
        "symptoms": [
            "잎 앞면에 각진 황색 반점이 나타납니다.",
            "잎 뒷면에 회색 또는 자주색 곰팡이 증상이 나타날 수 있습니다."
        ],
        "actions": [
            "감염 잎을 제거하고 포장 밖으로 반출하세요.",
            "환기를 강화하고 잎 표면의 물기를 빠르게 말리세요.",
            "등록된 노균병 방제 약제를 기준에 맞게 사용하세요."
        ]
    },

    "줄기 마름병": {
        "cause": [
            "고습과 식물체 상처를 통해 병원균이 침입할 수 있습니다.",
            "병든 잔재가 남아 있으면 다음 작기로 전염될 수 있습니다."
        ],
        "symptoms": [
            "줄기에 갈색 병반과 갈라짐이 나타납니다.",
            "심하면 줄기가 마르고 식물 전체가 쇠약해집니다."
        ],
        "actions": [
            "감염 줄기와 잔재를 제거하세요.",
            "전정 도구를 소독하고 상처 발생을 줄이세요.",
            "환기와 배수 상태를 점검하세요."
        ]
    },

    "건강한 잎": {
        "cause": [
            "현재 사진에서는 뚜렷한 병징이 확인되지 않습니다."
        ],
        "symptoms": [
            "잎 색과 조직 상태가 비교적 정상적으로 보입니다."
        ],
        "actions": [
            "현재 관리 상태를 유지하세요.",
            "온도·습도와 잎 상태를 주기적으로 점검하세요."
        ]
    },

    "흰가루병": {
        "cause": [
            "통풍이 부족하고 건조와 다습이 반복될 때 발생할 수 있습니다.",
            "밀식 재배에서는 전염 속도가 빨라질 수 있습니다."
        ],
        "symptoms": [
            "잎 표면에 흰색 가루 형태의 균사가 나타납니다.",
            "심하면 잎이 누렇게 변하고 광합성이 저하됩니다."
        ],
        "actions": [
            "감염 잎을 제거하세요.",
            "밀도를 낮추고 환기를 강화하세요.",
            "등록된 흰가루병 적용 약제를 사용하세요."
        ]
    },

    "피시움 과실썩음병": {
        "cause": [
            "배수 불량과 과습한 토양에서 발생 위험이 큽니다.",
            "과실이 젖은 토양이나 오염된 물과 접촉할 때 감염될 수 있습니다."
        ],
        "symptoms": [
            "과실에 물러진 수침상 병반이 생깁니다.",
            "진행되면 흰 균사가 발생하고 빠르게 부패합니다."
        ],
        "actions": [
            "감염 과실을 제거하세요.",
            "배수를 개선하고 과도한 관수를 피하세요.",
            "과실이 지면에 닿지 않도록 유인하세요."
        ]
    },

    "부패한 오이": {
        "cause": [
            "병원균 감염이나 수확 후 관리 불량으로 부패할 수 있습니다."
        ],
        "symptoms": [
            "과실 조직이 물러지고 변색 또는 악취가 날 수 있습니다."
        ],
        "actions": [
            "부패 과실을 즉시 분리하세요.",
            "저장 온도와 습도를 점검하세요.",
            "선별 과정에서 상처 난 과실을 제거하세요."
        ]
    },

    "응애 피해(심함)": {
        "cause": [
            "고온건조한 환경에서 응애 밀도가 급증할 수 있습니다."
        ],
        "symptoms": [
            "잎에 미세한 황백색 반점이 다수 나타납니다.",
            "심하면 잎 뒷면에 거미줄이 생기고 잎이 마릅니다."
        ],
        "actions": [
            "피해가 심한 잎을 제거하세요.",
            "잎 뒷면을 중심으로 발생 밀도를 확인하세요.",
            "등록된 응애 방제 약제를 교호 살포하세요."
        ]
    },

    "가루이 피해(경미)": {
        "cause": [
            "시설 내부에 유입된 가루이가 잎 뒷면에서 흡즙하면서 발생합니다."
        ],
        "symptoms": [
            "잎 뒷면에 성충이나 약충이 소수 관찰될 수 있습니다.",
            "잎색이 옅어지거나 약한 황화가 나타날 수 있습니다."
        ],
        "actions": [
            "황색 끈끈이트랩으로 발생량을 확인하세요.",
            "초기 개체를 제거하고 유입 경로를 차단하세요."
        ]
    },

    "가루이 피해(심함)": {
        "cause": [
            "가루이 개체 수가 증가해 지속적으로 흡즙한 상태입니다."
        ],
        "symptoms": [
            "잎 황화와 생육 저하가 나타납니다.",
            "감로와 그을음병이 동반될 수 있습니다."
        ],
        "actions": [
            "피해 잎과 심한 개체를 제거하세요.",
            "황색 끈끈이트랩과 방충망을 점검하세요.",
            "등록 약제를 계통별로 교호 사용하세요."
        ]
    }
}

    def __init__(self):
        self.model_path = "models/cucumber_leaf_best_model.keras"
        self.model = load_model(self.model_path)

        self.class_names = [
            "탄저병",
            "세균성 시들음병",
            "배꼽썩음병",
            "노균병",
            "개화기",
            "신선한 오이",
            "결실기 1단계",
            "결실기 2단계",
            "결실기 3단계",
            "줄기 마름병",
            "건강한 잎",
            "흰가루병",
            "피시움 과실썩음병",
            "부패한 오이",
            "응애 피해(심함)",
            "가루이 피해(경미)",
            "가루이 피해(심함)"
            ]
        
        print("클래스 개수:", len(self.class_names))
        

    def analyze_image(self, image, env_result=None):
        img = Image.open(image).convert("RGB")
        img = img.resize((224, 224))

        arr = np.array(img)
        arr = np.expand_dims(arr, axis=0)
        arr = preprocess_input(arr)

        preds = self.model.predict(arr, verbose=0)[0]
        
        print("모델 출력 개수:", len(preds))
        print("예측값:", preds)
        print("예측 인덱스:", int(np.argmax(preds)))
                
        idx = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)

        if confidence < 70:
            disease_display = f"판단 보류 ({disease})"
            risk_level = "재촬영 필요"
            advice = (
                f"'{disease}' 가능성이 가장 높지만 "
                f"신뢰도가 {confidence:.1f}%입니다. "
                "잎 한 장이 화면 대부분을 차지하도록 다시 촬영해주세요."
            )
        else:
            disease_display = disease

        
        if 0 <= idx < len(self.class_names):
            disease = self.class_names[idx]
        else:
            disease = f"분류 오류(index={idx})"

        print("클래스 이름:", self.class_names)
        print("선택된 병명:", disease)

        info = self.DISEASE_INFO.get(
            disease,
            {
                "cause": ["현재 등록된 상세 정보가 없습니다."],
                "symptoms": ["사진과 실제 포장 상태를 함께 확인하세요."],
                "actions": ["전문가 확인과 지속적인 관찰을 권장합니다."]
            }
        )

        if confidence < 70:
            disease_display = f"판단 보류 ({disease})"
        else:
            disease_display = disease

        return {
            "disease": disease_display,
            "raw_disease": disease,
            "confidence": round(confidence, 1),
            "risk": "높음" if confidence >= 70 and disease != "건강한 잎" else "낮음",
            "cause": info["cause"],
            "symptoms": info["symptoms"],
            "actions": info["actions"],
            "advice": (
                f"딥러닝 모델이 이미지를 분석한 결과 "
                f"{disease} 가능성이 가장 높습니다. "
                f"(신뢰도 {confidence:.1f}%)"
            )
        }