import json
import uuid
from datetime import datetime, timezone
from typing import Optional

import httpx
from pydantic import ValidationError

from api.conf import Config, Credentials
from api.enums import ApiChatModels
from api.models.doc import ApiChatMessage, ApiConversationHistoryDocument, ApiChatMessageMetadata, \
    ApiChatMessageTextContent
from api.schemas.openai_schemas import OpenAIChatResponse
from utils.common import singleton_with_lock
from utils.logger import get_logger

logger = get_logger(__name__)

config = Config()
credentials = Credentials()

MAX_CONTEXT_MESSAGE_COUNT = 1000


class OpenAIChatException(Exception):
    def __init__(self, source: str, message: str, code: int = None):
        self.source = source
        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.source} {self.code} error: {self.message}"


async def _check_response(response: httpx.Response) -> None:
    # 改成自带的错误处理
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as ex:
        await response.aread()
        error = OpenAIChatException(
            source="OpenAI",
            message=response.text,
            code=response.status_code,
        )
        raise error from ex


@singleton_with_lock
class OpenAIChatManager:
    """
    OpenAI API Manager
    """

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=None)  # TODO: support proxies

    async def ask(self, content: str, conversation_id: uuid.UUID = None,
                  parent_id: uuid.UUID = None, model: ApiChatModels = None,
                  timeout: int = None, context_message_count: int = -1, extra_args: Optional[dict] = None):

        now_time = datetime.now().astimezone(tz=timezone.utc)
        message_id = uuid.uuid4()
        new_message = ApiChatMessage(
            type="api",
            id=message_id,
            role="user",
            create_time=now_time,
            parent=parent_id,
            children=[],
            content=ApiChatMessageTextContent(content_type="text", text=content),
            metadata=ApiChatMessageMetadata(
                type="api",
            )
        )

        messages = []

        if not conversation_id:
            assert parent_id is None, "parent_id must be None when conversation_id is None"
            messages = [new_message]
        else:
            conv_history = await ApiConversationHistoryDocument.get(conversation_id)
            if not conv_history:
                raise ValueError("conversation_id not found")
            if conv_history.type != "api":
                raise ValueError(f"{conversation_id} is not api conversation")
            if not conv_history.mapping.get(str(parent_id)):
                raise ValueError(f"{parent_id} is not a valid parent of {conversation_id}")

            # 从 current_node 开始往前找 context_message_count 个 message
            if not conv_history.current_node:
                raise ValueError(f"{conversation_id} current_node is None")

            msg = conv_history.mapping.get(str(conv_history.current_node))
            assert msg, f"{conv_history.id} current_node({conv_history.current_node}) not found in mapping"

            count = 0
            iter_count = 0

            while msg:
                count += 1
                messages.append(msg)
                if context_message_count != -1 and count >= context_message_count:
                    break
                iter_count += 1
                if iter_count > MAX_CONTEXT_MESSAGE_COUNT:
                    raise ValueError(f"too many messages to iterate, conversation_id={conversation_id}")
                msg = conv_history.mapping.get(str(msg.parent))

            messages.reverse()
            messages.append(new_message)

        # TODO: credits 判断

        base_url = config.api.openai_base_url
        data = {
            "model": model.code(),
            "messages": [{"role": msg.role, "content": msg.content.text} for msg in messages],
            "stream": True,
            **(extra_args or {})
        }

        reply_message = None
        text_content = ""

        async with self.client.stream(
                method="POST",
                url=f"{base_url}chat/completions",
                json=data,
                headers={"Authorization": f"Bearer {credentials.openai_api_key}"},
                timeout=timeout
        ) as response:
            await _check_response(response)
            async for line in response.aiter_lines():
                if not line or line is None:
                    continue
                if "data: " in line:
                    line = line[6:]
                if "[DONE]" in line:
                    break

                try:
                    line = json.loads(line)
                    resp = OpenAIChatResponse(**line)

                    if resp.choices[0].message is not None:
                        text_content = resp.choices[0].message.get("content")
                    if resp.choices[0].delta is not None:
                        text_content += resp.choices[0].delta.get("content", "")
                    if reply_message is None:
                        reply_message = ApiChatMessage(
                            type="api",
                            id=uuid.uuid4(),
                            role="assistant",
                            model=model,
                            create_time=datetime.now().astimezone(tz=timezone.utc),
                            parent=message_id,
                            children=[],
                            content=ApiChatMessageTextContent(content_type="text", text=text_content),
                            metadata=ApiChatMessageMetadata(
                                type="api",
                                finish_reason=resp.choices[0].finish_reason,
                            )
                        )
                    else:
                        reply_message.content = ApiChatMessageTextContent(content_type="text", text=text_content)

                    if resp.usage:
                        reply_message.metadata.usage = resp.usage

                    yield reply_message

                except json.decoder.JSONDecodeError:
                    logger.warning(f"OpenAIChatResponse parse json error")
                except ValidationError as e:
                    logger.warning(f"OpenAIChatResponse validate error: {e}")
