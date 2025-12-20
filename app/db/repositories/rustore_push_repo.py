from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.models.sqlalchemy import RustorePushTokenOrm
from app.models.exceptions import SqlException
from app.models.pydantic import RustorePushToken, CreateUpdateRustorePushToken
from .base_repo import BaseRepository


class RustorePushRepositopry(BaseRepository[RustorePushTokenOrm]):
    model_class = RustorePushTokenOrm

    async def save_token(self, obj_in: CreateUpdateRustorePushToken) -> int:
        """
        Сохраняет или обновляет токен для устройства с указанным id для указанного пользователя

        :param obj_in: токен
        :type obj_in: CreateRustorePushToken
        :return: id токена
        :rtype: int
        """
        try:
            new_token = RustorePushTokenOrm(**obj_in.model_dump())
            self._session.add(new_token)
            await self._session.commit()
            await self._session.refresh(new_token)
            return new_token.id
        except SQLAlchemyError as e:
            self._logger.error(f"Ошибка добавления токена: {e}")
            raise SqlException(msg=f"Unable to add token ({e._message()})")

    async def get_tokens_by_user_id(self, user_id: str) -> list[RustorePushTokenOrm]:
        """
        Возвращает все токены для всех зарегистрированных устройств пользователя.

        :param user_id: id пользователя
        :type user_id: str
        :return: список токенов на устройствах пользователя
        :rtype: list[RustorePushTokenOrm]
        """
        result = await self._session.execute(
            select(RustorePushTokenOrm).where(
                RustorePushTokenOrm.user_id == user_id
            )
        )
        return result.scalars().all()
