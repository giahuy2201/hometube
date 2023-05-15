from typing import Union
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import downloader


class VideoRequest(BaseModel):
    url: str


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
def get_info(id: str):
    # send url to downloader and return immediate result
    return downloader.extract_info("https://youtu.be/{}".format(id))


@app.post("/add")
def add_request(request: VideoRequest):
    # send url to downloader and return immediate result
    return downloader.download_video(request.url)
