from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime, default=func.datetime('now'))
    duration = Column(Integer, nullable=True)
    start_number = Column(Integer)
    updated_at = Column(DateTime, default=func.datetime('now'))

    def __init__(self, start_number):
        self.start_number = start_number