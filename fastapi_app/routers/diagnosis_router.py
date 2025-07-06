# fastapi_app/routers/diagnosis_router.py
from fastapi import APIRouter
from ..services import llm_service
from ..schemas import DiagnosisRequest, DiagnosisResponse

router = APIRouter()

@router.post("/diagnose_depression", response_model=DiagnosisResponse)
async def diagnose_depression_endpoint(request: DiagnosisRequest):
    result = await llm_service.get_depression_diagnosis(request.conversation_history)
    return DiagnosisResponse(**result)
