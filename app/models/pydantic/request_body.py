from typing import Optional
from pydantic import BaseModel


class MessageNotification(BaseModel):
    title: str
    body: str
    image: Optional[str] = None


class AndroidNotification(MessageNotification):
    # NOTE: включает все поля MessageNotification
    icon: Optional[str] = None
    color: Optional[str] = None
    channel_id: Optional[str] = None
    click_action: Optional[str] = None
    click_action_type: int = 0


class AndroidMessage(BaseModel):
    # NOTE: в документации сказано что это строка от double + s, например "3.5s"
    ttl: str = "5.0s"
    notification: Optional[AndroidNotification] = None


class MessageRequestBody(BaseModel):
    token: str
    data: Optional[dict] = None
    notification: Optional[MessageNotification] = None
    android: Optional[AndroidMessage] = None


class SendRequest(BaseModel):
    message: MessageRequestBody


# errors

class ErrorDetails(BaseModel):
    code: int
    message: str
    status: str


class ErrorResponseBody(BaseModel):
    error: ErrorDetails
