from src.models import *
from src.models.User import User


class Token(Base, AsyncAttrs):
    __tablename__ = 'tokens'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    refresh_token: Mapped[String] = Column(String(511), nullable=False)
    created_date: Mapped[datetime] = Column(DateTime, default=datetime.now())

    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship(back_populates='tokens', lazy='selectin')
