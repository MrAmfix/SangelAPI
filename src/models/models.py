import uuid
from typing import List

from sqlalchemy import Column, String, DateTime, Boolean, UUID, ForeignKey, Integer, Float, \
    CheckConstraint, UniqueConstraint
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy_file import FileField


# Таблицы для ЧОП и ГБР пока не сделали
# + Потом добавить Roles


class Base(AsyncAttrs, DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}


class User(Base, AsyncAttrs):
    __tablename__ = 'users'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    email: Mapped[str] = Column(String(100), nullable=True)
    phone: Mapped[str] = Column(String(100), unique=True, nullable=False)
    password: Mapped[str] = Column(String(100), unique=True, nullable=False)
    username: Mapped[str] = Column(String(100), nullable=False)
    name: Mapped[str] = Column(String(100), nullable=False)
    surname: Mapped[str] = Column(String(100), nullable=False)
    patronymic: Mapped[str] = Column(String(100), nullable=True)
    disabled: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    device_products: Mapped[List["DeviceProduct"]] = relationship(back_populates='user', lazy='selectin')

    photo_id: Mapped[UUID] = mapped_column(ForeignKey('photos.id'))
    photo: Mapped["Photo"] = relationship(back_populates='user', lazy='selectin')

    favourite_list_id: Mapped[UUID] = mapped_column(ForeignKey('favourite_lists.id'))
    favourite_list: Mapped["FavouriteList"] = relationship(back_populates='favourite_users', lazy='selectin')

    visibility_type_id: Mapped[UUID] = mapped_column(ForeignKey('visibility_types.id'))
    visibility_type: Mapped["VisibilityType"] = relationship(back_populates='users', lazy='selectin')

    user_status_id: Mapped[UUID] = mapped_column(ForeignKey('user_statuses.id'))
    user_status: Mapped["UserStatus"] = relationship(back_populates='users', lazy='selectin')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class DeviceProduct(Base, AsyncAttrs):
    __tablename__ = 'device_products'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    mac_address: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    comment: Mapped[str] = Column(String, nullable=True)
    active: Mapped[bool] = Column(Boolean, nullable=False, default=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='device_products', lazy='selectin')


class VisibilityType(Base, AsyncAttrs):
    __tablename__ = 'visibility_types'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='visibility', lazy='selectin')


class UserStatus(Base, AsyncAttrs):
    __tablename__ = 'user_statuses'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='user_status', lazy='selectin')


class FavouriteList(Base, AsyncAttrs):
    __tablename__ = 'favourite_lists'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    favourite_users: Mapped[List["User"]] = relationship(back_populates='favourite_list', lazy='selectin')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now(), onupdate=datetime.now())


class Photo(Base, AsyncAttrs):
    __tablename__ = 'photos'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    photo_link: Mapped[str] = Column(String(255), nullable=False)

    user_id: Mapped[UUID] = Column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='photo', lazy='selectin')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())
