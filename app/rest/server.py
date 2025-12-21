import asyncio
from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html, get_swagger_ui_oauth2_redirect_html
from fastapi.openapi.utils import get_openapi

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
    # docs_url="/swagger"
    docs_url=None, redoc_url=None, openapi_url=None
)


@asgi_application.get("/dodocs", include_in_schema=False)
async def custom_swagger_ui_html():
    print("app.openapi_url is %s", asgi_application.openapi_url)
    return get_swagger_ui_html(
        openapi_url="/dodocs/openapi.json",
        title=asgi_application.title + " - Swagger UI",
        oauth2_redirect_url=asgi_application.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@asgi_application.get(asgi_application.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@asgi_application.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/dodocs/openapi.json",
        title=asgi_application.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


@asgi_application.get("/dodocs/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=asgi_application.title, version=asgi_application.version, routes=asgi_application.routes)


asgi_application.middleware("http")(error_middleware)
asgi_application.middleware("http")(auth_middleware)

asgi_application.include_router(router_healthcheck)
asgi_application.include_router(router_notification)
asgi_application.include_router(router_rustore)
