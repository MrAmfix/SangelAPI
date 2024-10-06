from src.models import *
from src.models.User import User


class Notification(Base, AsyncAttrs):
    __tablename__ = 'notifications'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    title: Mapped[str] = Column(String(100), nullable=False)
    body: Mapped[str] = Column(String(255), nullable=False)

    user_id: Mapped[UUID] = Column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='notifications', lazy='selectin')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())
