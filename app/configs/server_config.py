from .base_config import BaseConfig


class ServerConfig(BaseConfig):
    def __init__(self):
        self.SERVER_PORT: int = 30010

        super().__init__()
