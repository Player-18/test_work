from fastapi import Depends, APIRouter

from services.chat import ChatService

router = APIRouter()


@router.get("/history/{chat_id}")
async def get_history(chat_id: int, limit: int = 100, offset: int = 0, service: ChatService = Depends(ChatService)):
    result = await service.get_chat_history(chat_id, limit, offset)

    return result