from pydantic import BaseModel


class ChannelBase(BaseModel):
    id: str


class ChannelCreate(BaseModel):
    pass


class Channel(ChannelBase):
    channel: str | None = None  # channel name
    channel_id: str | None = None  # uuid
    channel_url: str | None = None
    thumbnail: str | None = None  # link to yt thumbnail
    description: str | None = None
    uploader: str | None = None
    uploader_id: str | None = None
    uploader_url: str | None = None
    channel_follower_count: int | None = None

    class Config:
        from_attributes = True
