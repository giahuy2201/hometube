from PIL import Image
import yt_dlp
import manager
import main

ydl_opts = {"format": "bestvideo"}


def cropthumbnail_hook(state):
    if state["status"] == "finished":
        meta = state["info_dict"]
        crop_thumbnail("{}.webp".format(meta["id"]))
        print("\n> crop_thumbnail")


def updateprogress_hook(state: dict):
    meta: dict = state["info_dict"]
    if "downloaded_bytes" in state and "total_bytes_estimate" in state:
        progress = state["downloaded_bytes"] / state["total_bytes_estimate"] * 100
        main.progress_notifier.downloading[meta["id"]] = progress
        print("{}%".format(progress))


bestaudio_opts = {
    "format": "m4a/bestaudio/best",
    "writethumbnail": True,
    "addmetadata": True,
    "writethumbnail": True,
    "outtmpl": "%(id)s.%(ext)s",
    "progress_hooks": [updateprogress_hook, cropthumbnail_hook],
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

thumbnailonly_opts = {
    "skip_download": True,
    "writethumbnail": True,
}


def crop_thumbnail(path: str):
    img = Image.open(path)
    width, height = img.size
    side = min(width, height)
    left = (width - side) / 2
    right = left + side
    top = (height - side) / 2
    bottom = top + side
    img_square = img.crop((left, top, right, bottom))
    img_square.save(path)


def download_metadata(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        meta = ydl.sanitize_info(info)
        return meta


def download_thumbnail(url: str):
    with yt_dlp.YoutubeDL(thumbnailonly_opts) as ydl:
        error_code = ydl.download([url])
        print("download_thumbnail: {}".format(error_code))


def download_video(url: str, preset):
    if preset == "bestaudio":
        opts = bestaudio_opts
        # meta = download_metadata(url)
        # download_thumbnail(url)

    elif preset == "bestvideo":
        opts = ydl_opts
    with yt_dlp.YoutubeDL(opts) as ydl:
        error_code = ydl.download([url])
    return "failed" if error_code else "done"
