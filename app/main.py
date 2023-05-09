from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

import os
import downloader


class VideoRequest(BaseModel):
    url: str


app = FastAPI()


@app.get("/")
def get_videos():
    # scan directory
    return os.listdir(".")


@app.get("/info")
def get_info(id: str):
    # send url to downloader and return immediate result
    return downloader.extract_info("https://youtu.be/{}".format(id))


@app.post("/add")
def add_request(request: VideoRequest):
    # send url to downloader and return immediate result
    return downloader.download_video(request.url)
