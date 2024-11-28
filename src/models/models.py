import uuid
from typing import List
from sqlalchemy import Column, String, DateTime, Boolean, UUID, ForeignKey, CheckConstraint
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __mapper_args__ = {"eager_defaults": True}


class User(Base, AsyncAttrs):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint(
            "phone ~ '^\\+7\\d{10}$'",
            name='check_phone_format'
        ),
    )
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    email: Mapped[str] = Column(String(100), nullable=True, unique=True, index=True)
    phone: Mapped[str] = Column(String(100), unique=True, nullable=False, index=True)
    password: Mapped[str] = Column(String(100), nullable=False)
    username: Mapped[str] = Column(String(100), nullable=False, unique=True, index=True)
    name: Mapped[str] = Column(String(100), nullable=False)
    surname: Mapped[str] = Column(String(100), nullable=False)
    patronymic: Mapped[str] = Column(String(100), nullable=True)
    disabled: Mapped[bool] = Column(Boolean, nullable=False, default=False)

    device_products: Mapped[List["DeviceProduct"]] = relationship(back_populates='user', lazy='selectin')
    notifications: Mapped[List["Notification"]] = relationship(back_populates='user', lazy='selectin')
    tokens: Mapped[List["Token"]] = relationship(back_populates='user', lazy='selectin')

    photo_id: Mapped[UUID] = mapped_column(ForeignKey('photos.id'), nullable=True)
    photo: Mapped["Photo"] = relationship(back_populates='user', lazy='selectin',
                                          foreign_keys='User.photo_id', remote_side='Photo.id')

    visibility_type_id: Mapped[UUID] = mapped_column(ForeignKey('visibility_types.id'))
    visibility_type: Mapped["VisibilityType"] = relationship(back_populates='users', lazy='selectin',
                                                             foreign_keys='User.visibility_type_id')

    user_status_id: Mapped[UUID] = mapped_column(ForeignKey('user_statuses.id'))
    user_status: Mapped["UserStatus"] = relationship(back_populates='users', lazy='selectin',
                                                     foreign_keys='User.user_status_id')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class UserStatus(Base, AsyncAttrs):
    __tablename__ = 'user_statuses'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='user_status', lazy='selectin')


class DeviceProduct(Base, AsyncAttrs):
    __tablename__ = 'device_products'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    mac_address: Mapped[str] = Column(String, nullable=False)
    description: Mapped[str] = Column(String, nullable=True)
    comment: Mapped[str] = Column(String, nullable=True)
    active: Mapped[bool] = Column(Boolean, nullable=False, default=True)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped["User"] = relationship(back_populates='device_products', lazy='selectin',
                                        foreign_keys='DeviceProduct.user_id')


class FavouriteList(Base, AsyncAttrs):
    __tablename__ = 'favourite_lists'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)

    owner_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    favourite_user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Notification(Base, AsyncAttrs):
    __tablename__ = 'notifications'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    title: Mapped[str] = Column(String(100), nullable=False)
    body: Mapped[str] = Column(String(255), nullable=False)

    user_id: Mapped[UUID] = Column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='notifications', lazy='selectin',
                                        foreign_keys='Notification.user_id')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)


class Photo(Base, AsyncAttrs):
    __tablename__ = 'photos'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    photo_link: Mapped[str] = Column(String(255), nullable=False)

    user_id: Mapped[UUID] = Column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='photo', lazy='selectin',
                                        foreign_keys='Photo.user_id', remote_side='User.id')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now)


class Token(Base, AsyncAttrs):
    __tablename__ = 'tokens'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    refresh_token: Mapped[str] = Column(String(511), nullable=False, unique=True)
    created_date: Mapped[datetime] = Column(DateTime, default=datetime.now)

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='tokens', lazy='selectin',
                                        foreign_keys='Token.user_id')


class VisibilityType(Base, AsyncAttrs):
    __tablename__ = 'visibility_types'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='visibility_type', lazy='selectin')
