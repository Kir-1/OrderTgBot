import asyncio
from pyrogram import Client
from pyrogram.types import Message
from pyrogram import filters
from src.core import settings

app = Client("report_bot", settings.REPORT_API_ID, settings.REPORT_API_HASH)


@app.on_message(
    filters.command(commands="seo")
    & filters.create(
        lambda _, __, message: message.from_user.id == int(settings.BOT_ID)
    )
)
async def report(client: Client, message: Message):
    await client.send_message(chat_id=settings.ID_REPORT_GROUP, text=message.text)


if __name__ == "__main__":
    app.run()
