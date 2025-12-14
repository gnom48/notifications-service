from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
from typing import Optional
import logging

from .base_repo import BaseRepository
from app.models.sqlalchemy import NotificationOrm, NotificationTypeOrm
from app.models.pydantic import Notification, NotificationCreate, NotificationUpdate, NotificationType, NotificationsFilter


class NotificationRepository(BaseRepository[NotificationOrm]):
    model_class = NotificationOrm

    async def create(self, obj_in: NotificationCreate) -> NotificationOrm:
        """Добавляет новое уведомление в базу данных."""
        try:
            new_notification = NotificationOrm(**obj_in.model_dump())
            self.__session.add(new_notification)
            await self.__session.commit()
            await self.__session.refresh(new_notification)
            return new_notification
        except SQLAlchemyError as e:
            self.__logger.error(f"Ошибка добавления уведомления: {e}")
            return None

    async def read_filterd(self, filter: NotificationsFilter) -> Optional[NotificationOrm]:
        """Получает все уведомления по фильтру"""
        stmt = select(NotificationOrm)
        if filter.user_id is not None:
            smth = smth.where(NotificationOrm.user_id >= filter.user_id)
        if filter.time_from is not None:
            smth = smth.where(NotificationOrm.when_planned >= filter.time_from)
        if filter.time_to is not None:
            smth = smth.where(NotificationOrm.when_planned <= filter.time_to)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def read_by_id(self, entity_id: int) -> Optional[NotificationOrm]:
        """Получает уведомление по идентификатору."""
        stmt = select(NotificationOrm).where(NotificationOrm.id == entity_id)
        result = await self.__session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, entity_id: int, updated_obj: dict) -> Optional[NotificationOrm]:
        """Обновляет существующее уведомление."""
        stmt = update(NotificationOrm).where(
            NotificationOrm.id == entity_id).values(updated_obj)
        await self.__session.execute(stmt)
        await self.__session.commit()
        return await self.read_by_id(entity_id)

    async def delete(self, entity_id: int) -> bool:
        """Удаляет уведомление по идентификатору."""
        stmt = delete(NotificationOrm).where(NotificationOrm.id == entity_id)
        await self.__session.execute(stmt)
        await self.__session.commit()
        return True
