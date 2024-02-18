from typing import Callable
import threading
import queue
import time

from workers.downloader import YTdlp
from presets.schemas import Preset
from library.schemas import Media


class Task:
    priority: int = 3

    def __lt__(self, other):
        return self.priority < other.priority


class DownloadTask(Task):
    url: str
    preset: Preset
    callback: Callable
    media: Media

    def __init__(self, url: str, media: Media, preset: Preset, callback: Callable):
        self.priority = 2
        self.url = url
        self.media = media
        self.preset = preset
        self.callback = callback

    def run(self):
        ytdlp = YTdlp(self.url)
        ytdlp.getContent(self.preset)
        self.callback(self.media.id, self.preset.id)


class Daemon:
    taskQueue: queue.PriorityQueue
    stopped = False

    def __init__(self):
        self.taskQueue = queue.PriorityQueue()

    def add_task(self, task: Task):
        self.taskQueue.put(task)

    def stop(*args):
        Daemon.stopped = True

    def start(self):
        while not Daemon.stopped:
            if not self.taskQueue.empty():
                task = self.taskQueue.get()
                task.run()
            time.sleep(1)


daemon = Daemon()
daemon_thread = threading.Thread(target=daemon.start)
daemon_thread.start()
print(f"Daemon thread {daemon_thread.name} started")
