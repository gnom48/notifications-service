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
                    if resp.status >= 400:
                        error_data = await resp.json()
                        error_message = error_data.get("message")
                        self.logger.error(
                            f"Error sending push: {error_message}")
                        return False
                    return True
            except ClientResponseError as err:
                self.logger.error(
                    f"Connection error while sending push: {err}", exc_info=True)
                return False
            except Exception as exc:
                self.logger.exception(
                    f"Unexpected error occurred during push sending: {exc}", exc_info=True)
                return False
