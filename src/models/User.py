from src.models import *
from src.models.DeviceProduct import DeviceProduct
from src.models.FavouriteList import FavouriteList
from src.models.Notification import Notification
from src.models.Photo import Photo
from src.models.UserStatus import UserStatus
from src.models.VisibilityType import VisibilityType


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
    notifications: Mapped[List["Notification"]] = relationship(back_populates='user', lazy='selectin')

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
