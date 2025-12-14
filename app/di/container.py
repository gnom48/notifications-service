from dependency_injector.containers import DeclarativeContainer, providers
from dependency_injector import providers
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.db import NotificationRepository, RustorePushRepositopry
from app.db import configure_db
from app.rabbitmq.consumer import RabbitMQConsumer
from app.sender import TgSender
from app.sender.tg import start_tg_bot
from app.services import NotificationsService, RustorePushService
from app.configs import TgConfig, RabbitMQConfig, ServerConfig, DbConfig
from app.sender import translation


class Container(DeclarativeContainer):
    configuration = providers.Configuration()

    tg_config = providers.Singleton(TgConfig)
    rabbitmq_config = providers.Singleton(RabbitMQConfig)
    server_config = providers.Singleton(ServerConfig)
    db_config = providers.Singleton(DbConfig)

    __db_url = providers.Resource(
        URL.create,
        drivername="postgresql+asyncpg",
        username=db_config.provided.POSTGRES_USER,
        password=db_config.provided.POSTGRES_PASSWORD,
        host=db_config.provided.POSTGRES_HOST,
        port=db_config.provided.POSTGRES_PORT,
        database=db_config.provided.POSTGRES_DB
    )

    __async_engine = providers.Resource(
        create_async_engine,
        url=__db_url,
        echo=False,
        pool_size=5,
        max_overflow=3
    )

    __session_factory = providers.Factory(
        async_sessionmaker,
        bind=__async_engine,
        expire_on_commit=False
    )

    notification_repository = providers.Factory(
        NotificationRepository,
        session_factory=__session_factory
    )

    rustore_push_token_repository = providers.Factory(
        RustorePushRepositopry,
        session_factory=__session_factory
    )

    rabbitmq_consumer = providers.Singleton(
        RabbitMQConsumer,
        config=rabbitmq_config
    )

    db_configurer = providers.Callable(
        configure_db,
        session_factory=__session_factory,
        need_create_tables=db_config.provided.CREATE_TABLES,
        need_drop_tables=db_config.provided.DROP_TABLES
    )

    tg_bot = providers.Singleton(
        Bot,
        token=tg_config.provided.TG_BOT_TOKEN
    )

    tg_dispatcher = providers.Singleton(
        Dispatcher,
        storage=MemoryStorage()
    )

    tg_bot_starter = providers.Callable(
        start_tg_bot,
        tg_dispatcher=tg_dispatcher,
        tg_bot=tg_bot
    )

    translator = providers.Callable(translation)

    notification_service = providers.Factory(
        NotificationsService,
        repo=notification_repository
    )

    rustore_push_service = providers.Factory(
        RustorePushService,
        repo=rustore_push_token_repository
    )

    tg_sender = providers.Factory(
        TgSender,
        config=tg_config
    )
