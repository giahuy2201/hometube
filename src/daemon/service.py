from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Callable
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor
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
import schemas as tasks_schemas


def add_task(task: tasks_schemas.TaskCreate):
    with contextmanager(get_db)() as db:
        db_task = tasks_crud.create_task(db, task)
        match task.type:
            case tasks_schemas.TaskType.Refresh:
                task = tasks_schemas.RefreshTask.model_validate(db_task)
                scheduled_tasks.put(task)
            case tasks_schemas.TaskType.Schedule:
                task = tasks_schemas.DownloadTask.model_validate(db_task)
                scheduled_tasks.put(task)
            case tasks_schemas.TaskType.Download:
                task = tasks_schemas.DownloadTask.model_validate(db_task)
                task_executor.submit(__execute_task, task)
                running_tasks[task.id] = task
            case tasks_schemas.TaskType.Import:
                task = tasks_schemas.ImportTask.model_validate(db_task)
                task_executor.submit(__execute_task, task)
                running_tasks[task.id] = task


def __execute_task(task: tasks_schemas.Task):
    if not task:
        return
    with contextmanager(get_db)() as db:
        task.run(db)
    if task.status == tasks_schemas.TaskStatus.Failed:
        print(f"Task {task} FAILED")
    else:
        del running_tasks[task.id]


def __popular_queue(tasks: list[tasks_schemas.Task]):
    for t in tasks:
        if (
            t.status == tasks_schemas.TaskStatus.Scheduled
            or t.status == tasks_schemas.TaskStatus.Pending
        ):
            match t.type:
                case tasks_schemas.TaskType.Refresh:
                    task = tasks_schemas.RefreshTask.model_validate(t)
                    scheduled_tasks.put(task)
                case tasks_schemas.TaskType.Schedule:
                    task = tasks_schemas.DownloadTask.model_validate(t)
                    scheduled_tasks.put(task)


def stop_daemon(*args):
    global stopped
    stopped = True


def start_daemon():
    # load unfinished tasks from db
    with contextmanager(get_db)() as db:
        tasks = tasks_crud.get_tasks(db)
        __popular_queue(tasks)
    while not stopped:
        if not scheduled_tasks.empty():
            task: tasks_schemas.Task = scheduled_tasks.get()
            if task.type == tasks_schemas.TaskType.Download:
                if datetime.datetime.now() > task.when:
                    task_executor.submit(__execute_task, task)
                    running_tasks[task.id] = task
                else:
                    scheduled_tasks.put(task)
            else:
                __execute_task(task)
        time.sleep(1)


stopped = False
scheduled_tasks: queue.PriorityQueue = (
    queue.PriorityQueue()
)  # time-sorted queue for scheduled refreshes and scheduled downloads
running_tasks = {}  # tasks in execution
task_executor = ThreadPoolExecutor()

daemon_thread = threading.Thread(target=start_daemon)
daemon_thread.start()
print(f"Daemon thread {daemon_thread.name} started")
