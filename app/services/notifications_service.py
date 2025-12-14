import logging
from fastapi import HTTPException

from app.models.sqlalchemy import *
from app.models.pydantic import *
from app.db import NotificationRepository


class NotificationsService:
    def __init__(self, repo: NotificationRepository):
        self.notifications_repo = repo

    async def GetNotifications(self, filter: NotificationsFilter) -> Restriction:
        try:
            return self.notifications_repo.read_filterd(filter)
        except Exception as e:
            logging.error(
                f"Unable to read notifications with filter {filter.__str__()}:", exc_info=True)
            raise HTTPException("Unable to read notifications:", detail=e)
