from aiohttp import ClientResponseError, ClientSession
import logging

from app.models.pydantic import SendRequest, ErrorResponseBody
from app.db import RustorePushRepositopry
from app.configs import RustorePushConfig


class RustorePushService:
    def __init__(self, repo: RustorePushRepositopry, rustore_push_config: RustorePushConfig):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rustore_push_token_repo: RustorePushRepositopry = repo
        self.base_url = "https://vkpns.rustore.ru/v1"
        self.config = rustore_push_config

    # NOTE: как я понял, в rustore push sdk больше / еще нет метода messages:batchSend,
    # поэтому пока только единоразовая отправка
    async def send_message(self, request_body: SendRequest) -> bool:
        """
        Отправляет push-уведомление на указанный проект.
        True в случае успеха, False в случае ошибки.
        """
        headers = {
            "Authorization": f"Bearer {self.config.RUSTORE_PUSH_SERVICE_TOKEN}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/projects/{self.config.RUSTORE_PUSH_PROJECT_ID}/messages:send"

        async with ClientSession() as session:
            try:
                async with session.post(url, json=request_body.model_dump_json(), headers=headers) as resp:
                    resp.raise_for_status()
                    return True
            except ClientResponseError as err:
                error_response = await err.response.json()
                error_model = ErrorResponseBody(**error_response)
                self.logger.error(
                    f"Error sending push: {error_model.error.message}")
                return False
