"""
Database session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create async engine
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug_mode,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync engine for migrations
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.debug_mode,
)

SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncSession:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_sync_session():
    """Get sync database session (for migrations)"""
    with SyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()