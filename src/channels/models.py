from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String, index=True)
    channel_url = Column(String, index=True)
    uploader = Column(String, index=True)
    uploader_id = Column(String, index=True)
    uploader_url = Column(String, index=True)
    thumbnail = Column(String, index=True)
    description = Column(String, index=True)
    channel_follower_count = Column(Integer, index=True)
