from .rabbitmq_config import RabbitMQConfig
from .tg_config import TgConfig
from .server_config import ServerConfig

TG_CONFIG = TgConfig()
TG_CONFIG.init()


RABBITMQ_CONFIG = RabbitMQConfig()
RABBITMQ_CONFIG.init()

SERVER_CONFIG = ServerConfig()
SERVER_CONFIG.init()
