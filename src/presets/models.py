from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class Preset(Base):
    __tablename__ = "presets"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, index=True)
    download_path = Column(String, index=True)  # where to store downloaded files
    media_path = Column(String, index=True)  # where imported media is moved to
    format = Column(String, index=True)  # format
    template = Column(String, index=True)  # outtmpl
    addThumbnail = Column(Boolean, index=True)
    squareCover = Column(Boolean, index=True)  # also imply audio only
    addMetadata = Column(Boolean, index=True)
    addSubtitles = Column(Boolean, index=True)

    medias = relationship("MediaVersion")
