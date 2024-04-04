import asyncio
import sys
import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    AsyncConnection
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

db_file = Path(__file__).resolve().parent.parent / 'robots.db'
DATABASE_URL = f'sqlite+aiosqlite:///{db_file}'

async def create_async_engine_and_session():
    """Creates an asynchronous SQLAlchemy engine and session factory.

    This function establishes a connection to the SQLite database specified
    by the `DATABASE_URL` and
    creates an asynchronous session factory that can be used to create
    sessions for interacting with the database.

    :return: A tuple containing the created engine and session factory objects.
    """
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(bind=engine, class_=AsyncSession,
                                 expire_on_commit=False, autoflush=False)
    return engine, async_session

def connection_and_session(func):
    """Decorator for managing database connections and sessions for asynchronous functions.

    This decorator simplifies database interactions by handling
    the creation of the engine and session,
    managing transactions, and ensuring proper cleanup when the
    decorated function exits, even in case of exceptions.

    :param func: The asynchronous function to be decorated.

    :return: async function: The decorated asynchronous function with
    automatic connection and session management.
    """
    async def wrapper(*args, **kwargs):
        try:
            engine, async_session = await create_async_engine_and_session()

            async with engine.begin() as connection:
                async with async_session() as session:
                    return await func(connection, session, *args, **kwargs)

        except SQLAlchemyError as e:
            print(f'SQLAlchemy Error: {e}')

    return wrapper
