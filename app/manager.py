import os
import json

dir = './'

def getAllData():
    data = []
    for filename in os.listdir(dir):
        if filename.endswith('.info.json'):
            file = os.path.join(dir,filename)
            video_meta = json.load(open(file))
            data.append(video_meta)
    return data