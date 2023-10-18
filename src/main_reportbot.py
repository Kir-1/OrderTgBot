import asyncio
from core.models import Base, User
from core import Database, database
from reportbot import start_bot


if __name__ == "__main__":
    start_bot()
