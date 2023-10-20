import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from src.core import settings

app = Client("autoseo_bot", settings.REPORT_API_ID, settings.REPORT_API_HASH)


@app.on_message(
    filters.create(lambda _, __, message: message.from_user.id == int(settings.BOT_ID))
)
async def report(client: Client, message: Message):
    print(message.from_user)


def start_bot():
    app.run()


if __name__ == "__main__":
    app.run()
