from pydantic import BaseModel

from app.sender import SenderType


class Msg(BaseModel):
    sender: SenderType
    title: str
    body: str
