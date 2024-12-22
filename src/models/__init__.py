import uuid
from typing import List
from sqlalchemy import Column, String, DateTime, Boolean, UUID, ForeignKey
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


# Таблицы для ЧОП и ГБР пока не сделали
# + Потом добавить Roles


class Base(AsyncAttrs, DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}
