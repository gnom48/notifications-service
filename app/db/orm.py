from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncConnection
from sqlalchemy import text
from sqlalchemy.engine.url import URL
from .models import *
from app.configs import DB_CONFIG, DbConfig


url = URL.create(
    drivername="postgresql+asyncpg",
    username=DB_CONFIG.POSTGRES_USER,
    password=DB_CONFIG.POSTGRES_PASSWORD,
    host=DB_CONFIG.POSTGRES_HOST,
    port=int(DB_CONFIG.POSTGRES_PORT),
    database=DB_CONFIG.POSTGRES_DB
)

async_engine = create_async_engine(
    url,
    echo=False,
    pool_size=5,
    max_overflow=3
)

new_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def configure_db(need_create_tables=False, need_drop_tables=False) -> bool:
    async with async_engine.connect() as conn:
        check = await conn.execute("SELECT 1")
        if (list(check)[0][0] != 1):
            return False

        if (need_create_tables):
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
            await conn.run_sync(BaseModelOrm.metadata.create_all)

        if (need_drop_tables):
            await conn.run_sync(BaseModelOrm.metadata.drop_all)

        return True
