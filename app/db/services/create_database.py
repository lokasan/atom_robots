import asyncio
import logging
import sys
import os
from pathlib import Path

if __package__ is None or __package__ == "":
    from connection import create_async_engine_and_session
else:
    from .connection import create_async_engine_and_session

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from models import Base

db_file = Path(__file__).resolve().parent.parent / 'robots.db'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def create_database():
    """Creates the database schema if the database file doesn't exist.

    This function checks if the database file exists and, if not, creates
    the database schema using the SQLAlchemy models defined in the `models`
    module.

    Logs an informational message upon successful database creation and
    logs any errors encountered during the process.
    """
    if not db_file.exists():
        engine, _ = await create_async_engine_and_session()

        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
                logger.info('Database created successfully.')
        except Exception as e:
            logger.error(f'Error creating database: {e}')


if __name__ == '__main__':
    asyncio.run(create_database())
