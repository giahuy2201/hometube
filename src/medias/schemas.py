from typing import List
from pydantic import BaseModel
from presets.schemas import Preset


class MediaVersion(BaseModel):
    id: str
    location: str

    preset_id: str
    media_id: str

    media: "Media"
    preset: Preset

    class Config:
        from_attributes = True


class MediaBase(BaseModel):
    id: str


class MediaCreate(BaseModel):
    url: str
    preset_id: str


class Media(MediaBase):
    title: str | None = None
    description: str | None = None
    uploader: str | None = None
    uploader_id: str | None = None
    duration: int | None = None
    view_count: int | None = None
    was_live: bool | None = None
    upload_date: str | None = None
    filesize: int | None = None
    ext: str | None = None
    url: str | None = None

    versions: List[MediaVersion] | None = []

    class Config:
        from_attributes = True
