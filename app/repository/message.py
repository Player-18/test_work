from app.db.session import async_session
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.message import MessageCreate, MessageRead
from models.tables import Message, MessageRead, ChatParticipant


class MessageRepository:

    async def add_row(self, db_message: dict) -> Message:
        async with async_session() as session:
            session.add(db_message)
            await session.commit()
            await session.refresh(db_message)
        return db_message

    async def mark_message(self, message_id: int):
        async with async_session() as session:
            message = await session.get(Message, message_id)

            chat_participants = await session.execute(
                select(ChatParticipant.user_id)
                .where(ChatParticipant.chat_id == message.chat_id)
            )
            participant_ids = [p.user_id for p in chat_participants.scalars().all()]

            read_users = await session.execute(
                select(MessageRead.user_id)
                .where(MessageRead.message_id == message_id)
            )
            read_user_ids = [r.user_id for r in read_users.scalars().all()]

            if all(uid in read_user_ids for uid in participant_ids if uid != message.sender_id):
                message.is_read = True
                await session.add(message)

            await session.commit()