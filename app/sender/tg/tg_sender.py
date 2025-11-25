from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio

from ..sender import BaseSender
from .router_support import router_support
from .router_notifications import router_notifications
from app.models.pydantic.msg import Msg
from app.configs import TgConfig


async def start_tg_bot(tg_dispatcher: Dispatcher, tg_bot: Bot):
    tg_dispatcher.include_router(router_notifications)
    tg_dispatcher.include_router(router_support)

    await tg_bot.delete_webhook(drop_pending_updates=True)
    await tg_dispatcher.start_polling(tg_bot)


class TgSender(BaseSender):
    def __init__(self, config: TgConfig, bot: Bot, dp: Dispatcher):
        super().__init__()
        logging.debug(config.__str__())
        self.__config = config
        self.tg_dispatcher = dp
        self.tg_bot = bot

    async def send_single(self, msg: Msg, delay: int = 0) -> bool:
        try:
            await asyncio.sleep(delay)
            await self.tg_bot.send_message(
                chat_id=self.__config.TG_DEFAULT_CHAT_ID,
                text=TgSender.__build_msg(msg))
            return True
        except Exception as e:
            logging.error(
                f"Unable to send msg for user _ in Telegram: ", exc_info=e)
            return False

    @staticmethod
    def __build_msg(msg: Msg) -> str:
        return f"{msg.title}\n\n📌{msg.body}"
