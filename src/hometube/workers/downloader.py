from PIL import Image
import yt_dlp
import json
from library.schemas import Media

bestvideo = {"format": "bestvideo"}

bestaudio = {
    "format": "m4a/bestaudio/best",
    "writethumbnail": True,
    "addmetadata": True,
    "writethumbnail": True,
    "outtmpl": "%(id)s.%(ext)s",
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        },
        {
            "key": "FFmpegMetadata",
        },
        {
            "key": "EmbedThumbnail",
            # "already_have_thumbnail": True,
        },
    ],
}

thumbnailonly = {
    "skip_download": True,
    "writethumbnail": True,
}


class Downloader:
    url: str

    def __init__(self, url: str) -> None:
        self.url = url

    def getMetadata(self) -> Media:
        pass

    def getThumbnail(self) -> bool:
        pass

    def getSubtitles(self) -> bool:
        pass

    def getContent(self, preset: str) -> bool:
        pass

    def getAudio(self, preset: str) -> bool:
        pass


class YTdlp(Downloader):
    def getMetadata(self) -> Media:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(self.url, download=False)
            metadata = ydl.sanitize_info(info)
        newMedia = Media.model_validate_json(json.dumps(metadata))
        return newMedia

    def getThumbnail(self) -> bool:
        with yt_dlp.YoutubeDL(thumbnailonly) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def getContent(self, preset: str = bestvideo) -> bool:
        with yt_dlp.YoutubeDL(preset) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def getAudio(self, preset: str = bestaudio) -> bool:
        with yt_dlp.YoutubeDL(preset) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True
