from pydantic import BaseModel
from enum import Enum

from .models import NotificationType


class Msg(BaseModel):
    sender: NotificationType
    title: str
    body: str
