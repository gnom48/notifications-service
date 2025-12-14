from fastapi import APIRouter, Depends, status
from app.models.pydantic import ResultResponseBody, CreateUpdateRustorePushToken
from app.services import RustorePushService
from app.di import di_container


router_rustore = APIRouter(prefix="/rustore_push",
                           tags=["Restore push"])


@router_rustore.post("/token", status_code=status.HTTP_201_OK, description="Send new ru.rustore.sdk:pushclient token")
async def post_token(
    token: CreateUpdateRustorePushToken,
    rustore_push_service: RustorePushService = Depends(
        # FIXME: мб так лучше, но если работать не будет то просто  rustore_push_service() сразу вызывать самому
        di_container.rustore_push_service)
):
    id = await rustore_push_service.rustore_push_token_repo.save_token(token)
    return ResultResponseBody(res=id)
