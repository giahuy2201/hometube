from typing import List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ytdlp.downloader import YTdlp
import medias.schemas as medias_schemas
import presets.schemas as presets_schemas
import medias.crud as medias_crud
import daemon.crud as tasks_crud
import presets.utils as presets_utils


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
    Failed = "failed"


class TaskCreate(BaseModel):
    type: TaskType
    status: TaskStatus = TaskStatus.Pending
    when: datetime  # when the task is executed or scheduled to be executed
    after: int = -1  # run only after some task has finished

    preset_id: str
    media_id: str


class Task(TaskCreate):
    id: int
    priority: int = 99  # for tasks initiated by the daemon

    media: medias_schemas.Media
    preset: presets_schemas.Preset

    class Config:
        from_attributes = True

    def __mark_finished(self, db: Session):
        self.when = datetime.now()
        self.status = "finished"
        tasks_crud.update_task(db, self)

    def run(self, db: Session):
        pass

    def __lt__(self, other: "Task"):
        return self.priority < other.priority


class RefreshTask(Task):
    priority: int = 1

    def run(self, db: Session):
        ytdlp = YTdlp(self.media.webpage_url)
        print(f"Refresh {self.media.webpage_url}")
        updated_media = ytdlp.get_metadata()
        medias_crud.update_media(db, updated_media)
        self.__mark_finished(db)


class DownloadTask(Task):
    priority: int = 2

    def run(self, db: Session):
        ytdlp = YTdlp(self.media.webpage_url)
        print(f"Download {self.media.webpage_url}")
        ytdlp.get_content(self.preset)
        self.__mark_finished(db)


class ImportTask(Task):
    def run(self, db: Session):
        file_location = presets_utils.__infer_path(self.preset, self.media)
        version_id = f"{self.media_id}-{self.preset_id}"
        print(f"Import {file_location}")
        version = medias_schemas.MediaVersion(
            id=version_id,
            location=file_location,
            preset_id=self.preset_id,
            media_id=self.media_id,
        )
        medias_crud.create_version(db, version)
        self.__mark_finished(db)
