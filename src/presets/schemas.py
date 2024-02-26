from typing import List
from pydantic import BaseModel


class Preset(BaseModel):
    id: str
    description: str | None = None
    download_path: str | None = None
    media_path: str | None = None
    format: str | None = None
    template: str | None = None
    addThumbnail: bool | None = None
    squareCover: bool | None = None
    addMetadata: bool | None = None
    addSubtitles: bool | None = None

    class Config:
        from_attributes = True
