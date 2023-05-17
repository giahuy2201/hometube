import os
import json

def getAllData():
    data = []
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            file = os.path.join(dir,filename)
            video_meta = json.load(file)
            data.append(video_meta)