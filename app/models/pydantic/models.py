from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class NotificationType(Enum):
    TG = "TG"
    PUSH = "PUSH"


class Notification(BaseModel):
    id: int = Field(default=0)
    user_id: str = Field(max_length=255)
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1, max_length=1000)
    type_id: NotificationType
    when_planned: int = Field(
        description="Время планирования уведомления в unix")
    delivered: bool = False


class NotificationCreate(BaseModel):
    user_id: str = Field(max_length=255)
    title: str = Field(min_length=1, max_length=255)
    body: str = Field(min_length=1, max_length=1000)
    type_id: NotificationType
    when_planned: int = Field(
        description="Время планирования уведомления в unix")
    delivered: bool = False


class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    body: Optional[str] = Field(None, min_length=1, max_length=1000)
    type_id: Optional[NotificationType]
    when_planned: Optional[int] = Field(
        None, description="Время планирования уведомления в unix")
    delivered: Optional[bool]


class Template(BaseModel):
    id: int = Field(default=0)
    title_template: str = Field(min_length=1, max_length=255)
    body_template: str = Field(min_length=1, max_length=1000)


class TemplateCreate(BaseModel):
    title_template: str = Field(min_length=1, max_length=255)
    body_template: str = Field(min_length=1, max_length=1000)


class TemplateUpdate(BaseModel):
    title_template: Optional[str] = Field(None, min_length=1, max_length=255)
    body_template: Optional[str] = Field(None, min_length=1, max_length=1000)


class TriggerType(Enum):
    SINGLE = "SINGLE"
    INTERVAL = "INTERVAL"
    EXACT = "EXACT"


class Trigger(BaseModel):
    id: int = Field(default=0)
    user_id: str = Field(max_length=255)
    trigger_type: TriggerType
    start_time: int = Field(description="Время старта триггера в unix-time")
    times: int = Field(ge=1, le=10000)
    template_id: int


class TriggerCreate(BaseModel):
    user_id: str = Field(max_length=255)
    trigger_type: TriggerType
    start_time: int = Field(description="Время старта триггера в unix-time")
    times: int = Field(ge=1, le=10000)
    template_id: int


class TriggerUpdate(BaseModel):
    trigger_type: Optional[TriggerType]
    start_time: Optional[int] = Field(
        None, description="Время старта триггера в unix-time")
    times: Optional[int] = Field(None, ge=1, le=10000)
    template_id: Optional[int]


class WeekDays(int, Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 4
    THURSDAY = 8
    FRIDAY = 16
    SATURDAY = 32
    SUNDAY = 64


class Restriction(BaseModel):
    id: int = Field(default=0)
    user_id: str = Field(max_length=255)
    weekdays_bitmask: int = Field(default=0, ge=0, le=127)
    time_start: int = Field(ge=0, le=1439)
    time_end: int = Field(ge=0, le=1439)


class RestrictionCreate(BaseModel):
    user_id: str = Field(max_length=255)
    weekdays_bitmask: int = Field(default=0, ge=0, le=127)
    time_start: int = Field(ge=0, le=1439)
    time_end: int = Field(ge=0, le=1439)


class RestrictionUpdate(BaseModel):
    weekdays_bitmask: Optional[int] = Field(None, ge=0, le=127)
    time_start: Optional[int] = Field(None, ge=0, le=1439)
    time_end: Optional[int] = Field(None, ge=0, le=1439)
