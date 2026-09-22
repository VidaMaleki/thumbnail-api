from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from database import Base

class Thumbnail(Base):
    __tablename__ = "thumbnails"
    id = Column(String, primary_key=True)
    original_filename = Column(String, nullable=False)
    preset = Column(String, nullable=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)