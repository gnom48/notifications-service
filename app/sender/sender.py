from abc import ABC, abstractmethod

from app.models.pydantic.msg import Msg


class BaseSender(ABC):
    """
    Абстракция над сендером
    """
    @abstractmethod
    async def send_single(self, msg: Msg, delay: int = 0) -> bool:
        """
        Docstring for send_single

        :param msg: объект сообщения
        :type msg: Msg
        :param delay: задержка в секундах (в пределах разумного!)
        :type delay: int
        :return: 
        :rtype: bool
        """
        pass
