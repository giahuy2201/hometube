from pydantic import BaseModel


class VideoBase(BaseModel):
    title: str
    thumbnail: str
    description: str
    uploader: str
    uploader_id: str
    duration: int
    view_count: int
    was_live: bool
    upload_date: str
    filesize: int
    ext: str


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int

    class Config:
        orm_mode = True
