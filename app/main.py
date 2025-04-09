from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import async_session
from app.schemas.message import MessageCreate, MessageRead
from services.message import MessageService
from app.websocket.manager import ConnectionManager
import json
from datetime import datetime
from views import router as chat_router

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manager = ConnectionManager()

app.include_router(chat_router, prefix="/api/v1", tags=["chat"])


@app.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, user_id: int):
    await manager.connect(websocket, chat_id, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            message = await MessageService().create_message(
                MessageCreate(
                    chat_id=chat_id,
                    sender_id=user_id,
                    text=message_data["text"],
                    timestamp=datetime.now(),
                    is_read=False
                )
            )

            # Отправляем сообщение всем участникам чата
            await manager.broadcast(
                MessageRead.from_orm(message).json(),
                chat_id,
                exclude_user=user_id
            )

    except Exception as exc:
        manager.disconnect(websocket, chat_id, user_id)
        await manager.broadcast(
            json.dumps({"user_id": user_id, "status": "disconnected"}),
            chat_id
        )