# fastapi_app/routers/hrv_router.py
from fastapi import APIRouter, Body
from ..services import hrv_service, graph_service, llm_service
from ..schemas import HrvReportResponse

router = APIRouter()

@router.post("/generate_hrv_report", response_model=HrvReportResponse)
async def generate_hrv_report_endpoint(raw_data: dict = Body(..., example={"ppg_signal": [1,2,3]})):
    score, features = hrv_service.analyze_hrv_data(raw_data)
    advice = await llm_service.generate_hrv_advice(score, features)
    graph_url = graph_service.create_hrv_graph(score)
    return HrvReportResponse(hrv_score=score, ai_advice=advice, graph_data_url=graph_url)
