# fastapi_app/services/hrv_service.py
import random

def analyze_hrv_data(raw_data: dict) -> tuple[float, str]:
    print("HRV 데이터 분석을 수행합니다...")
    score = round(random.uniform(30.0, 95.0), 2)
    features = "안정적인 심박 변이" if score > 70 else "스트레스 반응 및 심박 변이 감소"
    return score, features
