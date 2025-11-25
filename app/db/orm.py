from dependency_injector.providers import Factory
from sqlalchemy import text

from app.models.sqlalchemy.models import *


async def configure_db(
    session_factory: Factory,
    need_create_tables: bool = False,
    need_drop_tables: bool = False
):
    async with session_factory() as session:
        check = await session.execute(text("SELECT 1"))
        if (list(check)[0][0] != 1):
            raise Exception("Database is unavailable")

        if (need_create_tables):
            await session.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
            await session.run_sync(BaseModelOrm.metadata.create_all)

        if (need_drop_tables):
            await session.run_sync(BaseModelOrm.metadata.drop_all)
