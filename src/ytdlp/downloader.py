from PIL import Image
import yt_dlp
import json

from medias.schemas import Media
from presets.schemas import Preset
from core.config import settings
import ytdlp.utils as utils

thumbnailonly = {
    "skip_download": True,
    "writethumbnail": True,
}


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

    def get_metadata(self) -> Media:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)
            metadata = ydl.sanitize_info(info)
        newMedia = Media.model_validate_json(json.dumps(metadata))
        return newMedia

    def get_thumbnail(self) -> bool:
        with yt_dlp.YoutubeDL(thumbnailonly) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def get_content(self, preset: Preset) -> bool:
        preset = utils.getParams(preset)
        with yt_dlp.YoutubeDL(preset) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True
