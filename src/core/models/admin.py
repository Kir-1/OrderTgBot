from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Admin(Base):
    is_available: Mapped[bool] = mapped_column(default=True)
