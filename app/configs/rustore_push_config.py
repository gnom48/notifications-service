from .base_config import BaseConfig


class RustorePushConfig(BaseConfig):
    def __init__(self):
        self.RUSTORE_PUSH_PROJECT_ID: str = ""
        self.RUSTORE_PUSH_SERVICE_TOKEN: str = ""

        super().__init__()
