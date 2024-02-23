from typing import List
from pydantic import BaseModel

from medias.schemas import MediaVersion


class Preset(BaseModel):
    id: str
    description: str | None = None
    destination: str | None = None
    format: str | None = None
    template: str | None = None
    addThumbnail: bool | None = None
    squareCover: bool | None = None
    addMetadata: bool | None = None
    addSubtitles: bool | None = None

    medias: List[MediaVersion] = None

    class Config:
        from_attributes = True
