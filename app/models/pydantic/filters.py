from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class BaseFilter(BaseModel):
    pass


class PageFilter(BaseModel):
    page_index: int = 0
    count_on_page: int = 50

    def __str__(self):
        return f"<{self.model_dump()}>"


class NotificationsFilter(PageFilter):
    user_id: str = None
    time_from: int = None
    time_to: int = None

    def __str__(self):
        return f"<{self.model_dump()}>"
