import uuid
from typing import List, Optional
from sqlalchemy import (String, DateTime, Boolean, Text, Numeric, ForeignKey, CheckConstraint,
                        UniqueConstraint, Enum as PEnum)
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from src.utils.enums import AccountType
from src.utils.moscow_datetime import datetime_now_moscow


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
    photo_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('media.id', ondelete='SET NULL'),
        nullable=True
    )
    passport_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('passports.id', ondelete='SET NULL'),
        nullable=True
    )
    card_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('cards.id', ondelete='SET NULL'),
        nullable=True
    )

    photo: Mapped["Media"] = relationship(
        'Media',
        foreign_keys=[photo_id],
        back_populates='user',
        lazy='selectin'
    )

    visibility_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('visibility_types.id'),
        nullable=False
    )
    visibility_type: Mapped["VisibilityType"] = relationship(
        'VisibilityType',
        foreign_keys=[visibility_type_id],
        back_populates='users',
        lazy='selectin'
    )

    tokens: Mapped[List["Token"]] = relationship(
        'Token',
        back_populates='user',
        lazy='selectin'
    )
    devices: Mapped[List["UserDevice"]] = relationship(
        'UserDevice',
        back_populates='user',
        lazy='selectin'
    )
    favourite_contacts: Mapped[List["FavouriteContact"]] = relationship(
        'FavouriteContact',
        foreign_keys="[FavouriteContact.owner_id]",
        back_populates='owner',
        lazy='selectin'
    )
    linked_contacts: Mapped[List["FavouriteContact"]] = relationship(
        'FavouriteContact',
        foreign_keys="[FavouriteContact.linked_user_id]",
        back_populates='linked_user',
        lazy='selectin'
    )
    notifications: Mapped[List["Notification"]] = relationship(
        'Notification',
        back_populates='user',
        lazy='selectin'
    )
    events: Mapped[List["Event"]] = relationship(
        'Event',
        back_populates='user',
        lazy='selectin'
    )
    observers: Mapped[List["Observer"]] = relationship(
        'Observer',
        back_populates='user',
        lazy='selectin'
    )

    passport: Mapped["Passport"] = relationship(
        'Passport',
        foreign_keys=[passport_id],
        back_populates='user',
        lazy='selectin'
    )
    card: Mapped["Card"] = relationship(
        'Card',
        foreign_keys=[card_id],
        back_populates='users',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow,
                                                 onupdate=datetime_now_moscow)


class RegistrationToken(Base, AsyncAttrs):
    __tablename__ = 'registration_tokens'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Media(Base, AsyncAttrs):
    # TODO: Пересмотреть надобность этой таблицы
    __tablename__ = 'media'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    media_link: Mapped[str] = mapped_column(String(255), nullable=False)
    is_photo: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped["User"] = relationship(
        'User',
        back_populates='photo',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow,
                                                 onupdate=datetime_now_moscow)


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
    account_type: Mapped[AccountType] = mapped_column(PEnum(AccountType, name='account_type_enum'),
                                                      nullable=False, default=AccountType.USER)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Token(Base, AsyncAttrs):
    __tablename__ = 'tokens'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    refresh_token: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='tokens',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class DeviceProduct(Base, AsyncAttrs):
    __tablename__ = 'device_products'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    mac_address: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    users: Mapped[List["UserDevice"]] = relationship(
        'UserDevice',
        back_populates='device',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class UserDevice(Base, AsyncAttrs):
    __tablename__ = 'user_devices'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='devices',
        lazy='selectin'
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('device_products.id'),
        nullable=False
    )
    device: Mapped["DeviceProduct"] = relationship(
        'DeviceProduct',
        foreign_keys=[device_id],
        back_populates='users',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class FavouriteContact(Base, AsyncAttrs):
    __tablename__ = 'favourite_contacts'
    __table_args__ = (
        UniqueConstraint("owner_id", "phone", name="unique_favourite_contact"),
        CheckConstraint("name ~ '^[А-Яа-я-]+$'", name="check_favourite_name_cyrillic"),
        CheckConstraint("phone ~ '^\\+7\\d{10}$' OR phone ~ '^8\\d{10}$'", name="check_favourite_phone_format"),
        CheckConstraint("owner_id != linked_user_id", name="check_different_favourite_users")
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    owner: Mapped["User"] = relationship(
        'User',
        foreign_keys=[owner_id],
        back_populates='favourite_contacts',
        lazy='selectin'
    )

    linked_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='SET NULL'),
        nullable=True
    )
    linked_user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[linked_user_id],
        back_populates='linked_contacts',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Notification(Base, AsyncAttrs):
    __tablename__ = 'notifications'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='notifications',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class VisibilityType(Base, AsyncAttrs):
    __tablename__ = 'visibility_types'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship(
        'User',
        back_populates='visibility_type',
        lazy='selectin'
    )


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
    current_latitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)
    current_longitude: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)
    current_latitude_sg: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)
    current_longitude_sg: Mapped[float] = mapped_column(Numeric(9, 6), nullable=True)
    # current - временное решение, потом перенести на IMDB 
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    organization_comment: Mapped[str] = mapped_column(Text, nullable=True)
    complete_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    called_security_group: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    called_users: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='events',
        lazy='selectin'
    )

    security_group_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('security_groups.id', ondelete='SET NULL'),
        nullable=True
    )
    security_group: Mapped["SecurityGroup"] = relationship(
        'SecurityGroup',
        back_populates='events',
        lazy='selectin'
    )

    observers: Mapped[List["Observer"]] = relationship(
        'Observer',
        back_populates='event',
        lazy='selectin',
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Observer(Base, AsyncAttrs):
    __tablename__ = 'observers'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False
    )
    user: Mapped["User"] = relationship(
        'User',
        foreign_keys=[user_id],
        back_populates='observers',
        lazy='selectin'
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('events.id'),
        nullable=False
    )
    event: Mapped["Event"] = relationship(
        'Event',
        foreign_keys=[event_id],
        back_populates='observers',
        lazy='selectin'
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Passport(Base, AsyncAttrs):
    __tablename__ = 'passports'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    surname: Mapped[str] = mapped_column(Text, nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(Text, nullable=False)
    passport_series: Mapped[str] = mapped_column(Text, nullable=False)
    passport_number: Mapped[str] = mapped_column(Text, nullable=False)
    passport_agency: Mapped[str] = mapped_column(Text, nullable=False)
    passport_code: Mapped[str] = mapped_column(Text, nullable=False)
    passport_address: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow,
                                                 onupdate=datetime_now_moscow)

    user: Mapped["User"] = relationship(
        'User',
        back_populates='passport',
        lazy='selectin'
    )


class Card(Base, AsyncAttrs):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    number: Mapped[str] = mapped_column(Text, nullable=False)
    validity_period: Mapped[str] = mapped_column(Text, nullable=False)
    cvv_number: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow,
                                                 onupdate=datetime_now_moscow)

    users: Mapped[List["User"]] = relationship(
        'User',
        back_populates='card',
        lazy='selectin'
    )


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unqiue=True, index=True)
    code_id: Mapped[str] = mapped_column(String(7), nullable=False)
    legal_address: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    logo: Mapped[str] = mapped_column(Text, nullable=True)  # Возможно переделать на FK на медиа
    license_scan: Mapped[str] = mapped_column(Text, nullable=False)  # Возможно переделать на FK на медиа

    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('employees.id'), nullable=False)
    owner: Mapped["Employee"] = relationship("Employee", back_populates='organizations_own', lazy='selectin')

    employees: List[Mapped["Employee"]] = relationship("Employee",
                                                       back_populates='works_in_organization', lazy='selectin')
    security_groups: List[Mapped["SecurityGroup"]] = relationship("SecurityGroup",
                                                                  back_populates='organization', lazy='selectin')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class Employee(Base):
    __tablename__ = "employees"

    # Табличка для сотрудников ЧОО + Капитана ГБР
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    fullname: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False, unique=True, index=True)
    photo: Mapped[str] = mapped_column(Text, nullable=True)  # Возможно переделать на FK на медиа
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    employee_role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('employee_roles.id'),
                                                        nullable=False)
    employee_role: Mapped["EmployeeRole"] = relationship("EmployeeRole", back_populates='employees', lazy='selectin')

    security_group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('security_groups.id'),
                                                         nullable=True)
    security_group: Mapped["SecurityGroup"] = relationship("SecurityGroup", back_populates='employees', lazy='selectin')

    works_in_organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                                                ForeignKey('organizations.id'), nullable=False)
    works_in_organization: Mapped["Organization"] = relationship("Organization",
                                                                 back_populates='employees', lazy='selectin')

    organizations_own: List[Mapped["Organization"]] = relationship("Organization",
                                                                   back_populates='owner', lazy='selectin')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class EmployeeRole(Base):
    __tablename__ = "employee_roles"

    # AdminOrg, StaffOrg, Captain ...
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True, index=True)

    employees: List[Mapped["Employee"]] = relationship("Employee", back_populates='employee_role', lazy='selectin')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)


class SecurityGroup(Base):
    __tablename__ = 'security_groups'

    # Табличка для инфы о ГБР (пока равносильна капитану + доп. инфа)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,
                                          default=uuid.uuid4)
    name_id: Mapped[str] = mapped_column(Text, nullable=False)  # Unique (name_id + organization_id)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    organization_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                                       ForeignKey('organizations.id'), nullable=False)
    organization: Mapped["Organization"] = relationship("Organization",
                                                        back_populates='security_groups', lazy='selectin')

    employees: List[Mapped["Employee"]] = relationship("Employee", back_populates='secutiry_group', lazy='selectin')

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime_now_moscow)
