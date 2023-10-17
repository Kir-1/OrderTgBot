from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Worker(Base):
    room_name: Mapped[str]
    room_emoji: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    status: Mapped[bool] = mapped_column(default=False)
    busy_spot: Mapped[int] = mapped_column(default=0)
    all_spot: Mapped[int] = mapped_column(default=4)
    is_available: Mapped[bool] = mapped_column(default=True)
