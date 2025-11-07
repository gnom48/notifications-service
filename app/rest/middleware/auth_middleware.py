import json
from fastapi import HTTPException, Header, Request, status
import aiohttp
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel


async def auth_middleware(request: Request, call_next):
    try:
        # TODO: проверка токена/api ключа
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"details": e.__str__()}, headers={'content-type': 'application/json'})
