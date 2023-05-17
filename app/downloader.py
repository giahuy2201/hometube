import json
import yt_dlp
import manager

ydl_opts = {"format": "bestvideo"}

bestaudio_opts = {
    "format": "m4a/bestaudio/best",
    "writethumbnail": True,
    "addmetadata": True,
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
            "already_have_thumbnail": True,
        },
    ],
}


def extract_info(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    meta = ydl.sanitize_info(info)
    manager.saveData(info, info["id"])
    return info


def download_video(url: str, preset):
    if preset == "bestaudio":
        opts = bestaudio_opts
    elif preset == "bestvideo":
        opts = ydl_opts
    with yt_dlp.YoutubeDL(opts) as ydl:
        error_code = ydl.download([url])
    return "failed" if error_code else "done"
