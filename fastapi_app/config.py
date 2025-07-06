# fastapi_app/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # vLLM 서버의 주소들
    VLLM_CHAT_API_URL: str = "http://localhost:8001/v1/chat/completions"
    VLLM_COMPLETION_API_URL: str = "http://localhost:8001/v1/completions" # LoRA는 보통 이 엔드포인트 사용

    # 모델 및 어댑터 이름
    VLLM_BASE_MODEL_NAME: str = "your-base-model-name" # 예: "meta-llama/Llama-2-7b-chat-hf"
    DEPRESSION_LORA_ADAPTER_NAME: str = "depression-adapter" # vLLM 시작 시 어댑터에 부여한 이름

# 어디서든 이 settings 객체를 임포트하여 설정값을 사용할 수 있습니다.
settings = Settings()
