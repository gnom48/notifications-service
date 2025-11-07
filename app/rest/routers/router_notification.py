from fastapi import APIRouter, Depends, HTTPException, Header, Request, Response, UploadFile, status
from fastapi.responses import RedirectResponse

from app.models.pydantic.msg import Msg

router_notification = APIRouter(prefix="/notifications",
                                tags=["Single notifications"])


@router_notification.post("/", status_code=status.HTTP_200_OK, description="Send single notification")
async def send_notification(
    msg: Msg
):
    return HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
