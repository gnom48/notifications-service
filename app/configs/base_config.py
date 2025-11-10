import os
import inspect
from typing import Any


# class BaseConfig:
#     def __init__(self):
#         self._topic_name = self.__class__.__name__.replace("Config", "")

#     def init(self):
#         """
#         Автоматически присваиваем значения полям класса из переменных окружения,
#         соотнося имена переменных окружения и соответствующих полей класса.
#         Производим автоконвертацию типов на основе аннотаций.
#         """
#         annotations = self.__annotations__
#         attributes = inspect.getmembers(
#             self, lambda a: not inspect.isroutine(a))
#         for attr_name, default_value in attributes:
#             env_var_name = attr_name.upper()
#             raw_value = os.getenv(env_var_name)

#             if raw_value is not None:
#                 expected_type = annotations.get(attr_name, type(default_value))

#                 try:
#                     converted_value = self.convert_to_type(
#                         raw_value, expected_type)
#                     setattr(self, attr_name, converted_value)
#                 except ValueError as e:
#                     print(
#                         f"Warning: Cannot convert {raw_value} to {expected_type}. Using default.")

#     @staticmethod
#     def convert_to_type(value: str, target_type: type) -> Any:
#         """Конвертирует строку в целевой тип."""
#         if target_type == bool:
#             return value.lower() in ('true', 'yes', 'on', '1')
#         elif target_type == int:
#             return int(value)
#         elif target_type == float:
#             return float(value)
#         else:
#             return value

#     def __repr__(self):
#         attrs = ', '.join([f"{k}={v}" for k, v in vars(self).items()])
#         return f"<AppConfig({attrs})>"

#     def __str__(self):
#         return self.__repr__()


class BaseConfig:
    def __init__(self):
        self._topic_name = self.__class__.__name__.replace("Config", "")

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
