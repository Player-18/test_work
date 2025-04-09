from repository.chat import ChatRepository


class ChatService:

    repo = ChatRepository()

    async def get_chat_history(self, chat_id, limit, offset):
        result = await self.repo.get_messages_by_chat(chat_id, limit, offset)
        return result