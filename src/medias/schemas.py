from typing import List, Optional
from pydantic import BaseModel

from channels.schemas import Channel


class MediaVersion(BaseModel):
    id: str | None = None
    location: str | None = None

    preset_id: str | None = None
    media_id: str | None = None

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
    thumbnail: str | None = None  # link to yt thumbnail
    duration: int | None = None
    view_count: int | None = None
    was_live: bool | None = None
    upload_date: str | None = None
    filesize: int | None = None
    ext: str | None = None
    webpage_url: str | None = None

    channel_id: str | None = None
    uploader: str | None = None
    uploader_id: str | None = None

    channel: Channel | None = None
    versions: List[MediaVersion] | None = []

    class Config:
        from_attributes = True
