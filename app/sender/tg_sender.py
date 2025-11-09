from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters.command import CommandStart

from .sender import BaseSender
from app.models.pydantic.msg import Msg
from app.configs import TG_CONFIG, TgConfig


tg_bot = Bot(token=TG_CONFIG.TG_BOT_TOKEN)
tg_storage = MemoryStorage()
tg_dispatcher = Dispatcher(storage=tg_storage)


@tg_dispatcher.message(CommandStart())
async def cmd_start(message: Message):
    await tg_bot.send_message(chat_id=message.chat.id, text="gnom48.ru")


class TgSender(BaseSender):
    def __init__(self, config: TgConfig = TG_CONFIG):
        super().__init__()
        self.__config = config

    def send_single(self, msg: Msg, delay: int = 0):
        tg_bot.send_message(
            chat_id=self.__config.TG_DEFAULT_CHAT_ID,
            text=TgSender.build_msg(msg))

    @staticmethod
    def build_msg(msg: Msg) -> str:
        return f"{msg.title}\n\n📌{msg.body}"
