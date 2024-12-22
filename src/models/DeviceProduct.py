from src.models import *
from src.models.User import User


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
