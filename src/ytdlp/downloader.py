from PIL import Image
import yt_dlp
import json

from channels.schemas import Channel
from medias.schemas import Media
from presets.schemas import Preset
from core.config import settings
import ytdlp.utils as utils

thumbnailonly = {
    "skip_download": True,
    "writethumbnail": True,
}

channelonly = {"playlist_items": "0"}


class Downloader:
    url: str

    def __init__(self, url: str) -> None:
        self.url = url

    def get_metadata(self) -> Media:
        pass

    def get_thumbnail(self) -> bool:
        pass

    def get_subtitles(self) -> bool:
        pass

    def get_content(self, preset: Preset) -> bool:
        pass


class YTdlp(Downloader):
    printed = False

    def get_metadata(self, params=None):
        with yt_dlp.YoutubeDL(params) as ydl:
            info = ydl.extract_info(self.url, download=False)
            return ydl.sanitize_info(info)

    def get_media(self) -> Media:
        metadata = self.get_metadata()
        # remove some attributes from ytdlp metadata that could cause conflicts with our schemas
        metadata.pop("channel")
        media: Media = Media.model_validate_json(json.dumps(metadata))
        return media

    def get_channel(self) -> Channel:
        metadata = self.get_metadata(params=channelonly)
        channel: Channel = Channel.model_validate_json(json.dumps(metadata))
        # add in extra attributes missing from ytdlp metadata
        channel.thumbnail = self.__extract_avatar(metadata)
        return channel

    def get_thumbnail(self) -> bool:
        with yt_dlp.YoutubeDL(thumbnailonly) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def get_content(self, preset: Preset) -> bool:
        params = utils.getParams(preset)
        with yt_dlp.YoutubeDL(params) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def __extract_avatar(self, metadata):
        thumbnails = [
            t for t in metadata["thumbnails"] if t.get("id") == "avatar_uncropped"
        ]
        if len(thumbnails) > 0:
            return thumbnails[0]["url"]
        return None
