from sqlalchemy import select
from app.models.sqlalchemy import RustorePushTokenOrm
from app.models.pydantic import RustorePushToken, CreateUpdateRustorePushToken
from .base_repo import BaseRepository
from sqlalchemy.exc import SQLAlchemyError


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
            self.__session.add(new_token)
            await self.__session.commit()
            await self.__session.refresh(new_token)
            return new_token.id
        except SQLAlchemyError as e:
            self.__logger.error(f"Ошибка добавления уведомления: {e}")
            return None

    async def get_tokens_by_user_id(self, user_id: str) -> list[RustorePushTokenOrm]:
        """
        Возвращает все токены для всех зарегистрированных устройств пользователя.

        :param user_id: id пользователя
        :type user_id: str
        :return: список токенов на устройствах пользователя
        :rtype: list[RustorePushTokenOrm]
        """
        result = await self.__session.execute(
            select(RustorePushTokenOrm).where(
                RustorePushTokenOrm.user_id == user_id
            )
        )
        return result.scalars().all()
