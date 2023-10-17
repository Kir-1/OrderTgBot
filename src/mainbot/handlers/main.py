from aiogram import Dispatcher
from .user_commands import user_commands_router
from .user_buttons import user_buttons_router
from .user_callbacks import user_callbacks_router
from .user_payment import user_payment_router
from .user_orders import user_order_router
from .worker_callbacks import worker_callbacks_router
from .common_callbacks import common_callbacks_router
from .worker_commands import worker_commands_router
from .admin_broadcast import admin_broadcast_router
from .admin_callbacks import admin_callbacks_router
from .admin_inforamation_users import admin_information_user
from .admin_commands import admin_commands_router


def register_all_route(dp: Dispatcher) -> None:
    dp.include_routers(
        user_commands_router,
        user_buttons_router,
        user_callbacks_router,
        user_payment_router,
        user_order_router,
    )

    dp.include_routers(worker_callbacks_router, worker_commands_router)

    dp.include_routers(
        admin_broadcast_router,
        admin_callbacks_router,
        admin_information_user,
        admin_commands_router,
    )

    dp.include_routers(common_callbacks_router)
