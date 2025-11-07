import os
import inspect


class BaseConfig:
    def __init__(self):
        self._topic_name = self.__class__.__name__.replace("Config")

    def init(self):
        """
        Автоматически присваиваем значения полям класса из переменных окружения,
        соотнося имена переменных окружения и соответствующих полей класса.
        """
        attributes = inspect.getmembers(
            self, lambda a: not inspect.isroutine(a))
        for attr_name, _ in attributes:
            value = os.getenv(attr_name.upper())  # NOTE: UPPER CASE
            if value is not None:
                setattr(self, attr_name, value)

    def __repr__(self):
        attrs = ', '.join([f"{k}={v}" for k, v in vars(self).items()])
        return f"<AppConfig({attrs})>"

    def __str__(self):
        return self.__repr__()
