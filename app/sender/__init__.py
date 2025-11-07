from sender import SenderType, BaseSender
from tg_sender import TgSender


def create_sender(sender_type: SenderType) -> BaseSender:
    if sender_type == SenderType.TG:
        return TgSender()
    else:
        raise Exception(f"Unknown or unimplemented sender type: {sender_type}")
