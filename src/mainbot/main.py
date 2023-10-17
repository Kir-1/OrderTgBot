# import os
#
# from aiogram import Bot, Dispatcher
# from src.core.config import settings
# from .handlers import register_all_route
#
#
# bot = Bot(settings.BOT_TOKEN, parse_mode="HTML")
# dp = Dispatcher()
#
#
# async def start_bot() -> None:
#     await bot.delete_webhook(drop_pending_updates=True)
#     await register_all_route(dp)
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     start_bot()


"""
This example shows how to use webhook with SSL certificate.
"""
import asyncio
import logging
import ssl
import sys
from os import getenv

from aiohttp import web

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from src.core import settings
from .handlers import register_all_route

# Bot token can be obtained via https://t.me/BotFather


# Webserver settings
# bind localhost only to prevent any external access
WEB_SERVER_HOST = "127.0.0.1"
# Port for incoming request from reverse proxy. Should be any available port
WEB_SERVER_PORT = settings.BOT_PORT

# Path to webhook route, on which Telegram will send requests
WEBHOOK_PATH = settings.WEBHOOK_PATH
# Secret key to validate requests from Telegram (optional)
WEBHOOK_SECRET = settings.BOT_WEBHOOK_SECRET
# Base URL for webhook will be used to generate webhook URL for Telegram,
# in this example it is used public address with TLS support
BASE_WEBHOOK_URL = settings.BASE_WEBHOOK_URL

# Path to SSL certificate and private key for self-signed certificate.
# WEBHOOK_SSL_CERT = "/path/to/cert.pem"
# WEBHOOK_SSL_PRIV = "/path/to/private.key"


# All handlers should be attached to the Router (or Dispatcher)
router = Router()


async def on_startup(bot: Bot) -> None:
    # In case when you have a self-signed SSL certificate, you need to send the certificate
    # itself to Telegram servers for validation purposes
    # (see https://core.telegram.org/bots/self-signed)
    # But if you have a valid SSL certificate, you SHOULD NOT send it to Telegram servers.
    await bot.delete_webhook(drop_pending_updates=True)

    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
    )


def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    register_all_route(dp)

    # Register startup hook to initialize webhook
    dp.startup.register(on_startup)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(settings.BOT_TOKEN, parse_mode=ParseMode.HTML)

    # Create aiohttp.web.Application instance
    app = web.Application()

    # Create an instance of request handler,
    # aiogram has few implementations for different cases of usage
    # In this example we use SimpleRequestHandler which is designed to handle simple cases
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)

    # Generate SSL context
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

    # And finally start webserver
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


def start_bot() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
