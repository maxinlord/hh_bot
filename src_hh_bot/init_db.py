import config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

_engine = create_async_engine(config.DATABASE_URL)
_engine_for_func = create_async_engine(config.DATABASE_URL)
_sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
_sessionmaker_for_func = async_sessionmaker(_engine_for_func, expire_on_commit=False)
