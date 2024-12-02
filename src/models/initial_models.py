import uuid
from typing import Optional
from sqlalchemy import String, DateTime, Boolean, Text, Numeric, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    __mapper_args__ = {'eager_defaults': True}


class User(Base, AsyncAttrs):
    __tablename__ = 'users'
    __table_args__ = (
        CheckConstraint("name ~ '^[А-Яа-я-]+$'", name="check_users_name_cyrillic"),
        CheckConstraint("surname ~ '^[А-Яа-я-]+$'", name="check_users_surname_cyrillic"),
        CheckConstraint("patronymic ~ '^[А-Яа-я-]+$'", name="check_users_patronymic_cyrillic"),
        CheckConstraint("phone ~ '^\\+7\\d{10}$' OR phone ~ '^8\\d{10}$'", name="check_users_phone_format"),
        CheckConstraint("email ~ '^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'", name="check_users_email_format")
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class Media(Base, AsyncAttrs):
    __tablename__ = 'media'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    media_link: Mapped[str] = mapped_column(String(255), nullable=False)
    is_photo: Mapped[bool] = mapped_column(Boolean, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class VerificationCode(Base, AsyncAttrs):
    __tablename__ = 'verification_codes'
    __table_args__ = (
        CheckConstraint("code ~ '^\\d{6}$'", name="check_verif_code_format"),
        CheckConstraint("phone ~ '^\\+7\\d{10}$' OR phone ~ '^8\\d{10}$'", name="check_verif_code_phone_format")
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(6), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Token(Base, AsyncAttrs):
    __tablename__ = 'tokens'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class DeviceProduct(Base, AsyncAttrs):
    __tablename__ = 'device_products'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    mac_address: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class UserDevice(Base, AsyncAttrs):
    __tablename__ = 'user_devices'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class FavouriteContact(Base, AsyncAttrs):
    __tablename__ = 'favourite_contacts'
    __table_args__ = (
        CheckConstraint("name ~ '^[А-Яа-я-]+$'", name="check_favourite_name_cyrillic"),
        CheckConstraint("phone ~ '^\\+7\\d{10}$' OR phone ~ '^8\\d{10}$'", name="check_favourite_phone_format"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Notification(Base, AsyncAttrs):
    __tablename__ = 'notifications'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class VisibilityType(Base, AsyncAttrs):
    __tablename__ = 'visibility_types'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class Event(Base, AsyncAttrs):
    __tablename__ = 'events'
    __table_args__ = (
        CheckConstraint("-90 <= start_latitude AND start_latitude <= 90", name="check_latitude_range"),
        CheckConstraint("-180 <= start_longitude AND start_longitude <= 180", name="check_longitude_range"),
        CheckConstraint("complete_date > created_at", name="check_complete_after_created"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    start_latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    start_longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    complete_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Observer(Base, AsyncAttrs):
    __tablename__ = 'observers'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
