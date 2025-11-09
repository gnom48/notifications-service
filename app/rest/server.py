import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import logging
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, status

from app.rabbitmq.consumer import listen_rabbitmq
from app.rest.routers import router_notification
from .middleware import auth_middleware, error_middleware
from app.sender import tg_dispatcher, tg_bot


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s')  # ,
    # datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logger configured")

    logging.debug("Server started")

    tg_listen_task = asyncio.create_task(
        tg_dispatcher.start_polling(dispatcher=tg_dispatcher)
    )
    logging.debug("Telegram bot started")

    rabbitmq_listen_task = asyncio.create_task(listen_rabbitmq())
    logging.debug("RabbitMQ consumer started")

    try:
        yield
    except Exception as e:
        logging.error("Error in hosted service: ", exc_info=e)
    finally:
        tg_listen_task.cancel()
        rabbitmq_listen_task.cancel()

        await asyncio.gather(tg_listen_task, rabbitmq_listen_task, return_exceptions=True)

        logging.debug("Hosted services stopped")
        logging.debug("Server stopped")


app = FastAPI(lifespan=lifespan)

app.middleware("http")(error_middleware)
app.middleware("http")(auth_middleware)


@app.get("/health_check", status_code=status.HTTP_200_OK)
async def server_config_get():
    return {"datetime": datetime.now()}


app.include_router(router_notification)
