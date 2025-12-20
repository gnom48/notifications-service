from fastapi import APIRouter, Depends, status
from app.models.pydantic import ResultResponseBody, CreateUpdateRustorePushToken
from app.services import RustorePushService
from app.di import di_container


router_rustore = APIRouter(prefix="/rustore_push",
                           tags=["Restore push"])


@router_rustore.post("/token", status_code=status.HTTP_201_CREATED, description="Send new ru.rustore.sdk:pushclient token")
async def post_token(
    token: CreateUpdateRustorePushToken,
):
    # FIXME: придумать как получать из di
    async with di_container.rustore_push_token_repository() as repo:
        id = await repo.save_token(token)
        return ResultResponseBody(res=id)
