import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
import logging
from typing import AsyncGenerator
from fastapi import FastAPI, status

from app.rabbitmq.consumer import RabbitMQConsumer
from app.rest.routers import router_notification
from .middleware import auth_middleware, error_middleware
from app.sender import start_tg_bot


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logger configured")

    logging.debug("Telegram bot starting")
    tg_listen_task = asyncio.create_task(start_tg_bot())

    logging.debug("RabbitMQ consumer starting")
    rabbitmq_consumer = RabbitMQConsumer()
    await rabbitmq_consumer.connect()
    rabbitmq_listen_task = asyncio.create_task(rabbitmq_consumer.listen())

    logging.debug("Server starting")

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
