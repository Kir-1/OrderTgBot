from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    balance: Mapped[int] = mapped_column(default=0)
    accept_info: Mapped[bool] = mapped_column(default=False)
    count_orders: Mapped[int] = mapped_column(default=0)
    count_fail_orders: Mapped[int] = mapped_column(default=0)
    max_count_fail_orders: Mapped[int] = mapped_column(default=0)
    notification: Mapped[bool] = mapped_column(default=False)
    is_available: Mapped[bool] = mapped_column(default=True)
