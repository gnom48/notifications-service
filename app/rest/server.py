import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI

from app.rest.routers import router_notification, router_healthcheck, router_rustore
from .middleware import auth_middleware, error_middleware
from app.di import di_container


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None, None]:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.debug("Logger configured")

    await di_container.db_configurer()
    logging.debug("Db postgres connected")

    logging.debug("Telegram bot starting")
    tg_listen_task = asyncio.create_task(di_container.tg_bot_starter())

    logging.debug("RabbitMQ consumer starting")
    rabbitmq_consumer = di_container.rabbitmq_consumer()
    await rabbitmq_consumer.connect()
    rabbitmq_listen_task = asyncio.create_task(rabbitmq_consumer.listen())

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


asgi_application = FastAPI(
    lifespan=lifespan,
    description="Notifications service",
    docs_url="/swagger"
)

asgi_application.middleware("http")(error_middleware)
asgi_application.middleware("http")(auth_middleware)

asgi_application.include_router(router_healthcheck)
asgi_application.include_router(router_notification)
asgi_application.include_router(router_rustore)
