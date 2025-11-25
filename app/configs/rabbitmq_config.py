from .base_config import BaseConfig


class RabbitMQConfig(BaseConfig):
    def __init__(self):
        self.RABBITMQ_HOST: str = ""
        self.RABBITMQ_PORT: int = 7777
        self.RABBITMQ_USER: str = ""
        self.RABBITMQ_PASSWORD: str = ""
        self.RABBITMQ_QUEUE_NAME: str = ""

        super().__init__()
