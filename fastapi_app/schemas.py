# fastapi_app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional

# --- HRV 리포트 관련 ---
class HrvReportResponse(BaseModel):
    hrv_score: float = Field(..., example=85.2)
    ai_advice: str = Field(..., example="안정적인 상태를 잘 유지하고 계십니다.")
    graph_data_url: str = Field(..., example="data:image/png;base64,...")

# --- 우울증 진단 관련 ---
class DiagnosisRequest(BaseModel):
    # 대화 기록은 'role'과 'content'를 키로 갖는 딕셔너리의 리스트 형태
    conversation_history: List[dict] = Field(..., example=[
        {"role": "assistant", "content": "안녕하세요."},
        {"role": "user", "content": "기분이 좋지 않아요."}
    ])

class DiagnosisResponse(BaseModel):
    depression_score: int = Field(..., example=78, description="0-100 사이의 우울증 가능성 점수")
    reasoning: str = Field(..., example="대화 전반에 걸쳐 부정적인 단어 사용 빈도가 높고, 미래에 대한 비관적 표현이 나타났습니다.")
