from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, default="pending", nullable=False)
    total_rows = Column(Integer, default=0)
    processed = Column(Integer, default=0)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class RawContact(Base):
    __tablename__ = "raw_contacts"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False, index=True)
    data = Column(JSON, nullable=False)

class CleanedContact(Base):
    __tablename__ = "cleaned_contacts"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, nullable=False, index=True)
    data = Column(JSON, nullable=False)
