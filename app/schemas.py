from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str | None = None
    thumbnail: str | None = None
    description: str | None = None
    uploader: str | None = None
    uploader_id: str | None = None
    duration: int | None = None
    view_count: int | None = None
    was_live: bool | None = None
    upload_date: str | None = None
    filesize: int | None = None
    ext: str | None = None


class VideoCreate(BaseModel):
    url: str
    preset: str


class Video(VideoBase):
    id: str

    class Config:
        orm_mode = True
