from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.config import Settings
from advanced_alchemy.base import BigIntAuditBase

settings = Settings()

# if settings.MODE == "TEST":
#     DATABASE_URL = settings.TEST_DATABASE_URL
#     DATABASE_PARAMS = {"poolclass":NullPool}

# else:
#   TODO: #remove this when not needed
DATABASE_URL = settings.database_url
DATABASE_PARAMS = {}

async_engine = create_async_engine(
    DATABASE_URL, **DATABASE_PARAMS, echo=True, pool_pre_ping=True
)
async_session_maker = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False, autocommit=False
)


class Base(BigIntAuditBase):
    __abstract__ = True
    pass
