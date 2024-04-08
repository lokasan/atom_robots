from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Robot(Base):
    __tablename__ = "robots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_date: Mapped[datetime]
    pid: Mapped[int]
    duration: Mapped[Optional[int]]
    start_number: Mapped[Optional[int]]
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.datetime('now'))

    def __init__(self, start_date, start_number, pid):
        self.start_date = start_date
        self.start_number = start_number
        self.pid = pid


class SRobot(BaseModel):
    id: int
    start_date: Optional[datetime] = None
    pid: int
    duration: Optional[int] = None
    start_number: int
    updated_at: Optional[datetime] = None
