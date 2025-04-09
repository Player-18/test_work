from app.db.session import async_session
from sqlalchemy import select
from models.tables import Message, MessageRead

class ChatRepository:
        async def get_messages_by_chat(
                self, chat_id: int, limit: int = 100, offset: int = 0
        ) -> list[MessageRead]:
            async with async_session() as session:

                result = await session.execute(
                    select(Message)
                    .where(Message.chat_id == chat_id)
                    .order_by(Message.timestamp.asc())
                    .limit(limit)
                    .offset(offset)
                )
            return result.scalars().all()
