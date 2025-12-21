import logging
import asyncio

from app.models.pydantic import Msg, SendRequest, MessageNotification, AndroidMessage, AndroidNotification, MessageRequestBody
from .sender import BaseSender
from app.services import RustorePushService


class RustorePushSender(BaseSender):
    def __init__(self, rustore_push_service: RustorePushService):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.service = rustore_push_service

    async def send_single(self, msg: Msg) -> bool:
        try:

            async with self.service.rustore_push_token_repo as repo:
                tokens = await repo.get_tokens_by_user_id(user_id=msg.user_id)
                for token in tokens:
                    req = SendRequest(
                        message=MessageRequestBody(
                            android=AndroidMessage(
                                notification=AndroidNotification(
                                    title=msg.title,
                                    body=msg.body
                                )
                            ),
                            data={},
                            notification=MessageNotification(
                                title=msg.title,
                                body=msg.body,
                            ),
                            token=token.token
                        )
                    )
                    await self.service.send_message(request_body=req)
            return True
        except Exception as e:
            self.logger.error(
                f"Unable to send msg for user {msg.user_id} in Rustore Push: ", exc_info=e)
            return False
