from .sender import BaseSender
from .tg import TgSender, start_tg_bot
from app.models.pydantic.msg import SenderType


def create_sender(sender_type: SenderType) -> BaseSender:
    if sender_type == SenderType.TG:
        return TgSender()
    else:
        raise Exception(f"Unknown or unimplemented sender type: {sender_type}")
