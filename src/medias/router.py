from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
import starlette.status as status
import datetime
import json

from ytdlp.downloader import YTdlp
from core.database import engine, get_db
from presets.schemas import Preset
import files.service as files_service
import daemon.service as daemon
import daemon.schemas as tasks_schemas
import medias.schemas as medias_schemas, medias.models as models
import medias.crud as medias_crud
import presets.crud as presets_crud


router = APIRouter()


@router.get("/", response_model=list[medias_schemas.Media])
def get_medias(
    db: Session = Depends(get_db),
    term: str = Query(None),
    channel_id: str = Query(None),
):
    # Retrieve all requested videos
    if term:
        return medias_crud.search_medias(db, term)
    elif channel_id:
        return medias_crud.get_medias_by_channel_id(db, channel_id)
    return medias_crud.get_medias(db)


@router.get("/{id}", response_model=medias_schemas.Media)
def get_media(id: str, db: Session = Depends(get_db)):
    media = medias_crud.get_media_by_id(db, id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find media with id {id}",
        )
    return media


@router.post("/", response_model=medias_schemas.Media)
def add_media(request: medias_schemas.MediaCreate, db: Session = Depends(get_db)):
    # validate preset
    existPreset = presets_crud.get_preset_by_id(db, request.preset_id)
    if not existPreset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to add media with preset id {request.preset_id} (not found)",
        )
    # validate url
    ytdlp = YTdlp(request.url)
    newMedia = ytdlp.get_media()
    if not newMedia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to add media with url {request.url}",
        )
    # check for existing record
    existMedia = medias_crud.get_media_by_id(db, newMedia.id)
    if not existMedia:
        existMedia = medias_crud.create_media(db, newMedia)
    # check if media version is downloaded
    existVersions = medias_crud.get_version_by_preset_id(
        db, existMedia.id, request.preset_id
    )
    if len(existVersions) > 0:
        return existMedia
    else:
        downloading_task = daemon.add_task(
            tasks_schemas.TaskCreate(
                type="download",
                status="pending",
                when=datetime.datetime.now(),
                preset_id=existPreset.id,
                media_id=existMedia.id,
            )
        )
        daemon.add_task(
            tasks_schemas.TaskCreate(
                type="import",
                status="pending",
                when=datetime.datetime.now(),
                preset_id=existPreset.id,
                media_id=existMedia.id,
                after=downloading_task.id,
            )
        )
    return existMedia


@router.delete("/{id}")
def delete_media(id: str, db: Session = Depends(get_db)):
    success = medias_crud.delete_media(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete media with id {id}",
        )
    return {"status": "ok"}


@router.delete("/{media_id}/versions/{version_id}")
def delete_version(media_id: str, version_id: str, db: Session = Depends(get_db)):
    version: medias_schemas.MediaVersion = medias_crud.get_version_by_id(db, version_id)
    success = medias_crud.delete_version(db, version_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete version with id {version_id}",
        )
    success = files_service.delete_version(version.location)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=f"Failed to delete version file at {version.location}",
        )
    return {"status": "ok"}
