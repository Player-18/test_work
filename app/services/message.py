from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.message import MessageCreate, MessageRead
from models.tables import Message, MessageRead, ChatParticipant
from repository.message import MessageRepository


class MessageService:
    repo = MessageRepository()


    async def create_message(self, message: MessageCreate) -> Message:
        db_message = Message(**message.dict())
        raw = await self.repo.add_row(db_message)
        return raw

    async def mark_as_read(self, message_id: int, user_id: int):
        read = MessageRead(
            message_id=message_id,
            user_id=user_id,
            read_at=func.now()
        )
        await self.repo.add_row(read)

        # Обновляем статус is_read в сообщении, если все участники прочитали

        await self.repo.mark_message(message_id)
