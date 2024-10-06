from src.models import *
from src.models.User import User


class UserStatus(Base, AsyncAttrs):
    __tablename__ = 'user_statuses'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='user_status', lazy='selectin')
