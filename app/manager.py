import os
import json

dir = './metadata'
os.mkdir(dir)

def getAllData():
    data = []
    for filename in os.listdir(dir):
        if filename.endswith('.json'):
            file = os.path.join(dir,filename)
            video_meta = json.load(file)
            data.append(video_meta)
    
def saveData(meta,name):
    data = json.dumps(meta, indent=4)
    with open(dir+'/'+name+".json", "w") as outfile:
        outfile.write(data)

