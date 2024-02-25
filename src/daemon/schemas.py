from typing import List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

from medias.schemas import Media
from presets.schemas import Preset


class TaskType(str, Enum):
    Download = "download"  # to download a version with preset
    Import = "import"  # to create a version from download media
    Refresh = "refresh"  # to update media metadata
    Schedule = "schedule"  # to create automatic download for scheduled uploads
    Scan = "scan"  # to scan directory and import media and versions
    Rename = "rename"  # to update media data and versions wrt updated naming
    Retag = "retag"  # to embed media metadata into audio/video files


class TaskStatus(str, Enum):
    Pending = "pending"
    Running = "running"
    Finished = "finished"
    Scheduled = "scheduled"


class TaskCreate(BaseModel):
    type: TaskType
    status: TaskStatus = TaskStatus.Pending
    when: datetime  # when the task is executed or scheduled to be executed

    preset_id: str
    media_id: str


class Task(TaskCreate):
    id: int

    media: Media
    preset: Preset

    class Config:
        from_attributes = True
