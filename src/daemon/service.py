from typing import Callable
import threading
import queue
import time

from ytdlp.downloader import YTdlp
from presets.schemas import Preset
from medias.schemas import Media
from daemon.schemas import Task


stopped = False
taskQueue: queue.PriorityQueue = queue.PriorityQueue()


def add_task(task: Task):
    taskQueue.put(task)


def execute_task(task: Task):
    ytdlp = YTdlp(task.media.url)
    ytdlp.getContent(task.preset)


def stop_daemon(*args):
    global stopped
    stopped = True


def start_daemon(self):
    while not stopped:
        if not taskQueue.empty():
            task = taskQueue.get()
            task.run()
        time.sleep(1)


daemon_thread = threading.Thread(target=start_daemon)
daemon_thread.start()
print(f"Daemon thread {daemon_thread.name} started")
