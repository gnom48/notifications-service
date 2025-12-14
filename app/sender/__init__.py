from .sender import BaseSender
from .tg import TgSender
from .rustore_push_sender import RustorePushSender
from app.models.pydantic.models import NotificationType
from .locales import translation


def create_sender(sender_type: NotificationType) -> BaseSender:
    if sender_type == NotificationType.TG:
        return TgSender()
    elif sender_type == NotificationType.PUSH:
        return RustorePushSender()
    else:
        raise Exception(f"Unknown or unimplemented sender type: {sender_type}")
