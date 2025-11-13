from .sender import BaseSender
from .tg import TgSender, start_tg_bot
from app.models.pydantic.models import NotificationType


def create_sender(sender_type: NotificationType) -> BaseSender:
    if sender_type == NotificationType.TG:
        return TgSender()
    else:
        raise Exception(f"Unknown or unimplemented sender type: {sender_type}")
