from workers.downloader import YTdlp
import threading
import queue
import time


class Task:
    priority: int = 3

    def __lt__(self, other):
        return self.priority < other.priority


class DownloadTask(Task):
    url: str
    preset: str

    def __init__(self, url: str, preset: str):
        self.priority = 2
        self.url = url
        self.preset = preset

    def run(self):
        ytdlp = YTdlp(self.url)
        ytdlp.getContent()


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
