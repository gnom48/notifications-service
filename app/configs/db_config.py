from app.configs.base_config import BaseConfig


class DbConfig(BaseConfig):
    def __init__(self):
        super().__init__()

        self.POSTGRES_HOST: str = ""
        self.POSTGRES_PORT: int = 7777
        self.POSTGRES_USER: str = ""
        self.POSTGRES_PASSWORD: str = ""
        self.POSTGRES_DB: str = ""
