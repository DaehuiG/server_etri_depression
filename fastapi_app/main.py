# fastapi_app/main.py

from fastapi import FastAPI, Response, status
from .routers import chat_router, diagnosis_router, hrv_router


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Exhibition AI Server",
    description="ETRI LLM & HRV depression API SERVER",
    version="1.0.0"
)


@app.get("/health", tags=["System"], status_code=status.HTTP_200_OK)
async def health_check(response: Response):
    # vLLM 서버의 헬스 엔드포인트를 확인 (vLLM은 기본적으로 /health 경로를 제공)
    try:
        async with httpx.AsyncClient() as client:
            vllm_response = await client.get("http://localhost:8001/health", timeout=5.0)
            # vLLM 서버가 200 OK를 반환하지 않으면 비정상으로 간주
            if vllm_response.status_code != 200:
                response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
                return {"status": "error", "detail": "vLLM server is not healthy"}
    except httpx.RequestError:
        # vLLM 서버에 아예 연결이 안 되면 비정상으로 간주
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "detail": "Cannot connect to vLLM server"}
    
    # 모든 것이 정상이면 최종 OK 반환
    return {"status": "ok"}

# 기능별 라우터 포함
app.include_router(hrv_router.router, prefix="/api", tags=["HRV Reports"])
app.include_router(diagnosis_router.router, prefix="/api", tags=["AI Diagnosis"])
app.include_router(chat_router.router, tags=["Real-time Chat"])
