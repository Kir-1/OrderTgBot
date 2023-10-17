from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)

from asyncio import current_task

from src.core.config import settings


class Database:
    def __init__(self, url: str, echo: bool = False):
        self.engine: AsyncEngine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_scoped_session(self):
        return async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.get_scoped_session() as session:
            yield session
            await session.remove()


database = Database(url=settings.DATABASE_URL_SQLITE, echo=settings.DB_ECHO)
