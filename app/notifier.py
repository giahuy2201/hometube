from fastapi import WebSocket
import threading
import time

class Notifier:

    # store download progress of videos as video_id: progress key-value pairs
    downloading = {}
    subscribers = []
    instance: threading.Thread

    def __init__(self):
        self.instance = threading.Thread(target=self.update_progress)
        self.instance.start()
        print("thread {} started".format(self.instance.name))

    def add_subscriber(self,socket: WebSocket):
        self.subscribers.append(socket)

    def update_progress(self):
        while(True):
            for socket in self.subscribers:
                print('update socket')
                socket.send_json(self.downloading)
            time.sleep(0.5)
            