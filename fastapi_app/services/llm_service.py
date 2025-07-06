# fastapi_app/services/llm_service.py
import httpx
import json
from fastapi import HTTPException
from ..config import settings

# --- 스트리밍 채팅을 위한 서비스 ---
async def generate_chat_response_stream(history: list):
    payload = {"model": settings.VLLM_BASE_MODEL_NAME, "messages": history, "max_tokens": 1024, "stream": True}
    try:
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", settings.VLLM_CHAT_API_URL, json=payload, timeout=60.0) as response:
                response.raise_for_status()
                async for chunk in response.aiter_text():
                    # vLLM 스트림은 'data: {...}\n\n' 형태로 옵니다.
                    if chunk.startswith("data:"):
                        data_str = chunk.lstrip("data: ").rstrip("\n\n")
                        if data_str != "[DONE]":
                            try:
                                data = json.loads(data_str)
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content")
                                if content:
                                    yield content
                            except json.JSONDecodeError:
                                continue # 가끔 빈 데이터가 올 수 있음
    except httpx.RequestError:
        yield "죄송합니다, AI 서버와 통신할 수 없습니다."

# --- 우울증 진단을 위한 서비스 ---
async def get_depression_diagnosis(history: list) -> dict:
    prompt = f"다음은 사용자와 상담사의 대화 내용입니다. 이 대화를 심리학적으로 분석하여 사용자의 우울증 가능성을 0에서 100 사이의 점수로 평가하고, 그 핵심적인 이유를 설명하시오.\n\n[대화 내용]\n{json.dumps(history, ensure_ascii=False)}\n\n[분석 결과]"
    payload = {
        "model": settings.VLLM_BASE_MODEL_NAME, "prompt": prompt, "max_tokens": 512,
        "lora_request": {"lora_name": settings.DEPRESSION_LORA_ADAPTER_NAME, "lora_weight": 0.8}
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.VLLM_COMPLETION_API_URL, json=payload, timeout=120.0)
            response.raise_for_status()
            # vLLM의 텍스트 응답을 JSON으로 파싱하는 가짜 로직
            # 실제로는 LLM이 특정 JSON 형식을 반환하도록 프롬프트를 잘 설계해야 함
            raw_text = response.json()["choices"][0]["text"]
            # 예시: "점수: 78\n이유: 부정적 단어 사용 빈도가 높음."
            score = int(raw_text.split("점수:")[1].split("\n")[0].strip())
            reason = raw_text.split("이유:")[1].strip()
            return {"depression_score": score, "reasoning": reason}
    except Exception as e:
        print(f"진단 중 오류: {e}")
        raise HTTPException(status_code=500, detail="AI 진단 중 오류가 발생했습니다.")

# --- HRV 조언 생성을 위한 서비스 ---
async def generate_hrv_advice(score: float, features: str) -> str:
    prompt = f"환자의 HRV 분석 결과 점수는 {score}점이며, 주요 특징은 '{features}'입니다. 이 결과를 바탕으로 사용자에게 친절하고 이해하기 쉬운 건강 조언을 150자 내외로 작성해주세요."
    payload = {"model": settings.VLLM_BASE_MODEL_NAME, "prompt": prompt, "max_tokens": 512}
    try:
        async with httpx.AsyncClient() as client:
            # LoRA를 사용하지 않는 일반 텍스트 생성
            response = await client.post(settings.VLLM_COMPLETION_API_URL, json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        print(f"HRV 조언 생성 중 오류: {e}")
        raise HTTPException(status_code=500, detail="AI 조언 생성 중 오류가 발생했습니다.")
