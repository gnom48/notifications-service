from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Table, ForeignKey, Integer, BigInteger, String, Text, Float, Boolean, Enum as SqlEnum, DateTime, UniqueConstraint, func
from enum import Enum
import time


class BaseModelOrm(DeclarativeBase):
    __abstract__ = True
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    who_create: Mapped[str | None] = mapped_column(
        String(36), nullable=True, default=None)
    who_update: Mapped[str | None] = mapped_column(
        String(36), nullable=True, default=None)
    when_create: Mapped[int] = mapped_column(
        BigInteger, default=lambda: int(time.time()))
    when_update: Mapped[int] = mapped_column(BigInteger, default=lambda: int(
        time.time()), onupdate=lambda: int(time.time()))


class NotificationTypeOrm(Enum):
    """
    Тип уведомления
    """
    TG = "TG"
    PUSH = "PUSH"


class NotificationOrm(BaseModelOrm):
    """
    Уведомления
    """
    __tablename__ = "notifications"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36))
    title: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    type_id: Mapped[NotificationTypeOrm] = mapped_column(
        SqlEnum(NotificationTypeOrm))
    when_planned: Mapped[int] = mapped_column(BigInteger)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False)


class NotificationTemplateOrm(BaseModelOrm):
    __tablename__ = "notification_templates"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title_template: Mapped[str] = mapped_column(Text)
    body_template: Mapped[str] = mapped_column(Text)


class TriggerTypeOrm(Enum):
    """
    Тип триггера уведомлений
    """
    SINGLE = "SINGLE"
    INTERVAL = "INTERVAL"
    EXACT = "EXACT"


class TriggerOrm(BaseModelOrm):
    """
    Триггеры
    """
    __tablename__ = "triggers"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36))
    trigger_type: Mapped[TriggerTypeOrm] = mapped_column(
        SqlEnum(TriggerTypeOrm))
    start_time: Mapped[int] = mapped_column(BigInteger)
    times: Mapped[int] = mapped_column(Integer)
    template_id: Mapped[int] = mapped_column(ForeignKey(
        "public.notification_templates.id", ondelete="SET NULL"))


class RestrictionOrm(BaseModelOrm):
    """
    Ограничения    
    - По дням недели - битовая маска, нумерация с 0 (пн);   
    - По времени, количество минут с начала суток
    """
    __tablename__ = "restrictions"
    __table_args__ = {"schema": "public"}

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36))
    weekdays_bitmask = Column(Integer, default=0)
    time_start: Mapped[int] = mapped_column(Integer)
    time_end: Mapped[int] = mapped_column(Integer)


class RustorePushTokenOrm(BaseModelOrm):
    """
    Сервисный токен Rustore push
    """
    __tablename__ = "rustore_push_tokens"
    __table_args__ = (
        UniqueConstraint("user_id", "device_id"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    device_id: Mapped[str] = mapped_column(String(36), nullable=False)
    token: Mapped[str] = mapped_column(String(36), nullable=False)


class TgChatOrm(BaseModelOrm):
    """
    Id пользователей или чатов в TG
    """
    __tablename__ = "tg_chats"
    __table_args__ = (
        UniqueConstraint("user_id", "tg_chat"),
        {"schema": "public"},
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(36), nullable=False)
    tg_chat: Mapped[str] = mapped_column(Text, nullable=False)
