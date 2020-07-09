from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index

Base = declarative_base()


class Tick(Base):
    __tablename__ = 'ticks'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)
