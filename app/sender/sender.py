from enum import Enum


class SenderType(str, Enum):
    TG = "TG"


class BaseSender:
    ...
