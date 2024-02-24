from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Callable
import threading
import queue
import time
import datetime

from core.database import get_db
from ytdlp.downloader import YTdlp
import presets.schemas as presets_schemas
import daemon.schemas as tasks_schemas
import medias.schemas as medias_schemas
import daemon.crud as tasks_crud
import medias.crud as medias_crud

stopped = False
taskQueue: queue.PriorityQueue = queue.PriorityQueue()


def add_task(task: tasks_schemas.Task, db: Session = Depends(get_db)):
    taskQueue.put(task)
    tasks_crud.create_task(db, task)


def execute_task(task: tasks_schemas.Task, db: Session = Depends(get_db)):
    if not task:
        return
    match task.type:
        case "download":
            ytdlp = YTdlp(task.media.url)
            ytdlp.getContent(task.preset)
            __mark_finished_task(task, db)
        case "import":
            file_location = __infer_path_from_preset(task.preset, task.media)
            print(f"import {file_location}")
            version = medias_schemas.MediaVersion(
                location=file_location, preset_id=task.preset_id, media_id=task.media_id
            )
            medias_crud.create_version(db, version)
            __mark_finished_task(task, db)


def __infer_path_from_preset(
    preset: presets_schemas.Preset, media: medias_schemas.Media
):
    file_ext = "m4a" if preset.squareCover else "mkv"
    file_name = preset.template.format(title=media.title, id=media.id, ext=file_ext)
    return f"{preset.destination}/{file_name}"


def __mark_finished_task(task: tasks_schemas.Task, db: Session):
    task.when = datetime.datetime()
    task.status = "finished"
    tasks_crud.update_task(db, task)


def stop_daemon(*args):
    global stopped
    stopped = True


def start_daemon():
    while not stopped:
        if not taskQueue.empty():
            task = taskQueue.get()
            task.run()
        time.sleep(1)


daemon_thread = threading.Thread(target=start_daemon)
daemon_thread.start()
print(f"Daemon thread {daemon_thread.name} started")
