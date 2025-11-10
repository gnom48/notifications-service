from abc import ABC, abstractmethod

from app.models.pydantic.msg import Msg


class BaseSender(ABC):
    @abstractmethod
    async def send_single(self, msg: Msg, delay: int = 0) -> bool:
        pass
