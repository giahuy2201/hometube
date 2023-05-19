from starlette.responses import FileResponse
import os
import json

dir = "./"


def getAllData():
    data = []
    for filename in os.listdir(dir):
        if filename.endswith(".info.json"):
            file = os.path.join(dir, filename)
            video_meta = json.load(open(file))
            data.append(video_meta)
    return data


def getFile(id: str):
    file = ""
    for filename in os.listdir(dir):
        if filename.startswith(id) and not filename.endswith(".json"):
            file = filename
    print(file)
    if file != "":
        return FileResponse(file, media_type="application/octet-stream", filename=file)
