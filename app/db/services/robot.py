import asyncio
from typing import Dict, List
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

from sqlalchemy import Column, String, Integer, BigInteger, text, DateTime,\
    select, func, and_, desc, Text, update
from sqlalchemy.orm import declarative_base, sessionmaker, aliased
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,\
    AsyncConnection

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from .connection import connection_and_session
from models import Robot

@connection_and_session
async def set_robot(connection: AsyncConnection,
                    session: AsyncSession,
                    start_date: DateTime,
                    start_number: int,
                    pid: int):
    """Creates a new robot entry in the database.

    :param connection: The asynchronous database connection.
    :param session: The asynchronous database session.
    :param start_number: The starting number for the robot.
    :param: pid: The process id for the robot.
    :return: The ID of the newly created robot entry.
    """
    new_robot = Robot(start_date, start_number, pid)
    session.add(new_robot)
    await session.commit()

    return new_robot.id

@connection_and_session
async def update_robot(connection: AsyncConnection,
                       session: AsyncSession,
                       id: int, duration: int) -> str:
    """Records the duration of the robot's operation

    :param connection: The asynchronous database connection.
    :param session: The asynchronous database session.
    :param id: Database record ID.
    :param duration: The duration of the robot run.
    :return: A message indicating whether the update was successful or not.
    """
    try:
        robot = await session.execute(update(Robot)
                                      .where(Robot.id == id)
                                      .values(duration=duration,
                                              updated_at=func.datetime('now')))
        await session.commit()

    except SQLAlchemyError as e:
        print(f'SQLAlchemy Error: {e}')
        return False

    return robot.rowcount > 0

@connection_and_session
async def get_stats(connection: AsyncConnection,
                    session: AsyncSession,
                    offset: int, limit: int, order_by: str) -> List[Robot]:
    """Retrieves robot run statistics with pagination and sorting.

    :param connection: Asynchronous database connection.
    :param session: Asynchronous database session.
    :param offset: Offset from the beginning of the result set.
    :param limit: Maximum number of records to return.
    :param order_by: Sorting direction: 'asc' or 'desc'.
    :return: A list of dictionaries representing statistics
            for each robot run.
            Each dictionary contains the following keys:
            * 'id': Robot run ID.
            * 'start_date': Date and time of the robot run start.
            * 'pid': Process id of the robot run.
            * 'duration': Duration of the robot run.
            * 'start_number': Robot run number.
    """
    sort_field = Robot.start_date if order_by == 'asc' else desc(
        Robot.start_date)

    robot_runs = await session.execute(
        select(Robot.id, Robot.start_date, Robot.pid, Robot.duration,
               Robot.start_number)
        .order_by(sort_field).offset(offset)
        .limit(limit))

    robot_runs = robot_runs.fetchall()

    robot_stats = []

    for row in robot_runs:
        robot_stats.append(
            {
                'id': row.id,
                'start_date': row.start_date,
                'pid': row.pid,
                'duration': row.duration,
                'start_number': row.start_number
            }
        )

    return robot_stats

@connection_and_session
async def get_process(connection: AsyncConnection,
                      session: AsyncSession,
                      start_date: DateTime,
                      pid: int):
    try:
        process = await session.execute(select(Robot.id, Robot.pid, Robot.start_date)
        .where(
            and_(Robot.pid == pid, Robot.start_date == start_date,
                 Robot.duration == None)))

        process = process.fetchone()

        if process:
            return {
                'id': process.id,
                'pid': process.pid,
                'start_date': process.start_date
            }

    except SQLAlchemyError as e:
        print(f'SQLAlchemy Error: {e}')

@connection_and_session
async def get_processes(connection: AsyncConnection,
                        session: AsyncSession):
    process = await session.execute(select(Robot.id, Robot.pid, Robot.start_date)
    .where(
        and_(Robot.duration == None)))

    processes = process.fetchall()
    unfinished_processes = []

    if processes:
        for row in processes:
            unfinished_processes.append(
                {
                    'id': row.id,
                    'pid': row.pid,
                    'start_date': row.start_date
                }
            )
        return unfinished_processes
