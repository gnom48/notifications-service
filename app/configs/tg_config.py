from app.configs.base_config import BaseConfig


class TgConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.TG_BOT_TOKEN: str = "NO_TOKEN"
        self.TG_DEFAULT_CHAT_ID: str = "NO_CHAT_ID"
