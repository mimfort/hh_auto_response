from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import config
from advanced_alchemy.base import BigIntAuditBase
DATABASE_URL = config.DATABASE_URL
DATABASE_PARAMS = {}

async_engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS, echo=True, pool_pre_ping=True)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False, autoflush=False, autocommit=False)

class Base(BigIntAuditBase):
    __abstract__ = True
    pass