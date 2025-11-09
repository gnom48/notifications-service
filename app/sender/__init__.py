from .sender import BaseSender
from .tg_sender import TgSender
from app.models.pydantic.msg import SenderType
from .tg_sender import tg_dispatcher, tg_bot


def create_sender(sender_type: SenderType) -> BaseSender:
    if sender_type == SenderType.TG:
        return TgSender()
    else:
        raise Exception(f"Unknown or unimplemented sender type: {sender_type}")
