from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.database import Base


class MediaVersion(Base):
    __tablename__ = "mediaversions"

    id = Column(String, primary_key=True)
    location = Column(String, index=True)

    media_id = Column(String, ForeignKey("medias.id"))
    preset_id = Column(String, ForeignKey("presets.id"))


class Media(Base):
    __tablename__ = "medias"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    uploader = Column(String, index=True)
    uploader_id = Column(String, index=True)
    duration = Column(Integer, index=True)
    view_count = Column(Integer, index=True)
    was_live = Column(Boolean, index=True)
    upload_date = Column(String, index=True)
    filesize = Column(Integer, index=True)
    ext = Column(String, index=True)
    webpage_url = Column(String, index=True)

    versions = relationship("MediaVersion")
