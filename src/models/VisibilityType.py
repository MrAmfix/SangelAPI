from src.models import *
from src.models.User import User


class VisibilityType(Base, AsyncAttrs):
    __tablename__ = 'visibility_types'
    id: Mapped[UUID] = Column(UUID(as_uuid=True), nullable=False, primary_key=True,
                              default=uuid.uuid4)
    name: Mapped[str] = Column(String(100), nullable=False)
    users: Mapped[List["User"]] = relationship(back_populates='visibility', lazy='selectin')
