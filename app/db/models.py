import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, String, Float, Boolean, Enum as SqlEnum, Integer, Date
from enum import Enum
import uuid
import time


class BaseModelOrm(DeclarativeBase):
    pass
