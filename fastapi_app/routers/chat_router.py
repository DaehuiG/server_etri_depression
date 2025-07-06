# fastapi_app/routers/chat_router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services import llm_service

router = APIRouter()

@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            conversation_history = await websocket.receive_json()
            async for token in llm_service.generate_chat_response_stream(conversation_history):
                await websocket.send_text(token)
            await websocket.send_text("[END_OF_STREAM]")
    except WebSocketDisconnect:
        print("채팅 클라이언트 연결 끊김.")
