import asyncio
import os

from fastapi.encoders import jsonable_encoder
from utils.common import get_conversation_model

import api.globals as g
from api.enums import ChatModels
# from revChatGPT.V1 import AsyncChatbot
# from revChatGPT.V3 import Chatbot as ChatbotV3
from api.v3.v3 import Chatbot as ChatbotV3


class ChatGPTManager:
    def __init__(self):
        self.chatbot = ChatbotV3(api_key=g.config.get("api_key"))
        # self.chatbot = AsyncChatbot({
        #     "access_token": g.config.get("chatgpt_access_token"),
        #     "paid": g.config.get("chatgpt_paid"),
        #     "model": "text-davinci-002-render-sha", # default model
        # },base_url=g.config.get("chatgpt_base_url", None))
        self.semaphore = asyncio.Semaphore(1)

    def is_busy(self):
        return self.semaphore.locked()

    async def get_conversations(self):
        conversations = await self.chatbot.get_conversations(limit=80)
        return conversations

    async def get_conversation_messages(self, conversation_id: str):
        # 需要二次处理 将原来的
        # TODO: 使用 redis 缓存
        messages = await self.chatbot.get_msg_history(conversation_id)
        # messages = jsonable_encoder(messages)
        # model_name = get_conversation_model(messages)
        # messages["model_name"] = model_name or ChatModels.unknown.value
        return messages

    async def clear_conversations(self):
        return self.chatbot.reset()
        # await self.chatbot.clear_conversations()


    def ask(self, message, conversation_id: str = None, parent_id: str = None,
            timeout=360, model_name: ChatModels = None):
        model = None
        if model_name is not None and model_name != ChatModels.unknown:
            model = model_name.value
        return self.chatbot.ask_async(prompt=message, convo_id=conversation_id, model=model,
                                timeout=timeout)

    async def delete_conversation(self, conversation_id: str):
        await self.chatbot.delete_conversation(conversation_id)

    async def set_conversation_title(self, conversation_id: str, title: str):
        """Hack change_title to set title in utf-8"""
        await self.chatbot.change_title(conversation_id, title)

    async def generate_conversation_title(self, conversation_id: str, message_id: str):
        """Hack gen_title to get title"""
        await self.chatbot.gen_title(conversation_id, message_id)

    def reset_chat(self):
        self.chatbot.reset_chat()


chatgpt_manager = ChatGPTManager()
