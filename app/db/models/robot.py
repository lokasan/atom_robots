from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime)
    pid = Column(Integer)
    duration = Column(Integer, nullable=True)
    start_number = Column(Integer)
    updated_at = Column(DateTime, default=func.datetime('now'))

    def __init__(self, start_date, start_number, pid):
        self.start_date = start_date
        self.start_number = start_number
        self.pid = pid
