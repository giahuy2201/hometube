from PIL import Image
import yt_dlp
import json
from library.schemas import Media
from presets.schemas import Preset
from core.config import settings

bestvideo = {"format": "bestvideo"}

bestaudio = {
    "format": "bestaudio/best",
    "writethumbnail": True,
    "addmetadata": True,
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

    def getContent(self, preset: Preset) -> bool:
        pass


class YTdlp_Params:
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

    def getContent(self, preset: Preset) -> bool:
        preset = self.__getParams(preset)
        with yt_dlp.YoutubeDL(preset) as ydl:
            error_code = ydl.download([self.url])
        if error_code:
            print(f"error: {error_code}")
            return False
        return True

    def __getParams(preset: Preset):
        """
        Convert preset to yt-dlp compatible params
        """
        params = {}
        params["format"] = preset.format
        params["outtmpl"] = preset.template
        # output location
        paths = {}
        paths["home"] = preset.destination
        paths["temp"] = "./temp"
        params["paths"] = paths
        params["addmetadata"] = preset.addMetadata
        params["writethumbnail"] = preset.addThumbnail
        postprocessors = []
        # audio
        if preset.squareCover:
            params["format"] = "bestaudio"
            # Extract audio using ffmpeg
            postprocessors.append(
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                },
            )
        else:
            params["merge_output_format"] = "mkv"
        if preset.addMetadata:
            postprocessors.append(
                {
                    "key": "FFmpegMetadata",
                }
            )
        params["postprocessors"] = postprocessors
        return params
