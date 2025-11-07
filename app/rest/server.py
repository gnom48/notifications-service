import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import logging
from fastapi import FastAPI, HTTPException, status

from app.rabbitmq.consumer import listen_rabbitmq
from app.rest.routers import router_notification
from middleware import auth_middleware, error_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Server started")

    listen_task = asyncio.create_task(listen_rabbitmq())
    logging.debug("RabbitMQ consumer started")

    yield
    listen_task.cancel()
    try:
        await listen_task
    except asyncio.CancelledError:
        logging.debug("RabbitMQ consumer stopped")

    logging.debug("Server stopped")


app = FastAPI(lifespan=lifespan)

app.middleware("http")(error_middleware)
app.middleware("http")(auth_middleware)


@app.get("/health_check", status_code=status.HTTP_200_OK)
async def server_config_get():
    return {"datetime": datetime.now()}


app.include_router(router_notification)
