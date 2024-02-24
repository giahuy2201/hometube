from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Callable
from contextlib import contextmanager
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
taskQueue: queue.SimpleQueue = queue.SimpleQueue()


def add_task(task: tasks_schemas.TaskCreate):
    with contextmanager(get_db)() as db:
        db_task = tasks_crud.create_task(db, task)
        task = tasks_schemas.Task.model_validate(db_task)
        taskQueue.put(task)


def __execute_task(task: tasks_schemas.Task):
    if not task:
        return
    match task.type:
        case "download":
            ytdlp = YTdlp(task.media.webpage_url)
            print(f"Download {task.media.webpage_url}")
            ytdlp.get_content(task.preset)
            with contextmanager(get_db)() as db:
                __mark_finished_task(task, db)
        case "import":
            file_location = __infer_path_from_preset(task.preset, task.media)
            version_id = f"{task.media_id}-{task.preset_id}"
            print(f"Import {file_location}")
            version = medias_schemas.MediaVersion(
                id=version_id,
                location=file_location,
                preset_id=task.preset_id,
                media_id=task.media_id,
            )
            with contextmanager(get_db)() as db:
                medias_crud.create_version(db, version)
                __mark_finished_task(task, db)


def __infer_path_from_preset(
    preset: presets_schemas.Preset, media: medias_schemas.Media
):
    file_ext = "m4a" if preset.squareCover else "mkv"
    file_name = preset.template % {
        "title": media.title,
        "id": media.id,
        "ext": file_ext,
    }
    return f"{preset.destination}/{file_name}"


def __mark_finished_task(task: tasks_schemas.Task, db: Session):
    task.when = datetime.datetime.now()
    task.status = "finished"
    tasks_crud.update_task(db, task)


def stop_daemon(*args):
    global stopped
    stopped = True


def start_daemon():
    while not stopped:
        if not taskQueue.empty():
            task = taskQueue.get()
            __execute_task(task)
        time.sleep(1)


daemon_thread = threading.Thread(target=start_daemon)
daemon_thread.start()
print(f"Daemon thread {daemon_thread.name} started")
