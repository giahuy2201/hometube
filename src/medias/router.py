from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import starlette.status as status

from src.yt_dlp.downloader import YTdlp
from core.database import engine, SessionLocal
from src.daemon.daemon import DownloadTask, daemon
from presets.schemas import Preset
import medias.schemas as schemas, medias.models as models
import medias.crud as medias_crud
import presets.crud as presets_crud

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Media])
def get_medias(db: Session = Depends(get_db), term: str = ""):
    # Retrieve all requested videos
    if term != "":
        videos = medias_crud.search_medias(db, term)
    else:
        videos = medias_crud.get_medias(db)
    return videos


@router.get("/{id}", response_model=schemas.Media)
def get_media(id: str, db: Session = Depends(get_db)):
    media = medias_crud.get_media_by_id(db, id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find media with id {id}",
        )
    return media


@router.post("/", response_model=schemas.Media)
def add_media(request: schemas.MediaCreate, db: Session = Depends(get_db)):
    # validate preset
    existPreset = presets_crud.get_preset_by_id(db, request.preset_id)
    if not existPreset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to add media with preset id {request.preset_id} (not found)",
        )
    # validate url
    ytdlp = YTdlp(request.url)
    newMedia = ytdlp.getMetadata()
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
    existVersions = medias_crud.get_version(db, existMedia.id, request.preset_id)
    if len(existVersions) > 0:
        return existMedia
    else:
        daemon.add_task(DownloadTask(request.url, existMedia, existPreset, add_version))
    return newMedia


@router.delete("/{id}")
def get_media(id: str, db: Session = Depends(get_db)):
    success = medias_crud.delete_media(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete media with id {id}",
        )
    return {"status": "ok"}


def add_version(media_id: str, preset: Preset, db: Session = Depends(get_db)):
    """
    Save a MediaVersion record to db when finish downloading
    """
    location = f"{preset.destination}/"
    version = schemas.MediaVersion(location="", media_id=media_id, preset_id=preset_id)
    newVersion = medias_crud.create_version(db, version)
