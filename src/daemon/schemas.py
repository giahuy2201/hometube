from typing import List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from medias.schemas import Media
from presets.schemas import Preset


class TaskType(str, Enum):
    Download = "download"
    Refresh = "refresh"
    Scheduled = "scheduled"


class TaskStatus(str, Enum):
    Running = "running"
    Finished = "finished"
    Scheduled = "scheduled"


class Task(BaseModel):
    id: str
    type: TaskType
    status: TaskStatus
    when: datetime  # when the task is executed or scheduled to be executed

    preset_id: str
    media_id: str

    media: Media
    preset: Preset

    class Config:
        from_attributes = True
