from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from app.core.config import settings
from collections.abc import AsyncGenerator



engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    # autoflush=False, not used any more in sql2.0
    # autocommit=False,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:

    async with AsyncSessionFactory() as session:
        try:

            yield session

        except Exception:

            await session.rollback()
            raise

