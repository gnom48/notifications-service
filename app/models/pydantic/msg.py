from pydantic import BaseModel
from enum import Enum


class SenderType(str, Enum):
    TG = "TG"


class Msg(BaseModel):
    sender: SenderType
    title: str
    body: str
