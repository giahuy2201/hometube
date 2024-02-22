from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, index=True)
    status = Column(String, index=True)
    when = Column(Date, index=True)

    media_id = Column(String, ForeignKey("medias.id"))
    preset_id = Column(String, ForeignKey("presets.id"))

    media = relationship("Media", uselist=False, back_populates="versions")
