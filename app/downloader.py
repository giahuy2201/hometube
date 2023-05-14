import json
import yt_dlp
import manager

ydl_opts = {"format": "bestvideo"}


def extract_info(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    meta = ydl.sanitize_info(info)
    manager.saveData(info,info['id'])
    return info


def download_video(url: str):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])
    return "failed" if error_code else "done"
