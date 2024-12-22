from src.models import *
from src.models.User import User


class FavouriteList(Base, AsyncAttrs):
    __tablename__ = 'favourite_lists'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    favourite_users: Mapped[List["User"]] = relationship(back_populates='favourite_list', lazy='selectin')

    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
