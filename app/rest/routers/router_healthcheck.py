from datetime import datetime
from fastapi import APIRouter, status

router_healthcheck = APIRouter(prefix="",
                               tags=["Healthcheck"])


@router_healthcheck.get("/health_check", status_code=status.HTTP_200_OK, description="Health check inside service")
async def server_config_get():
    return {"datetime": datetime.now()}
