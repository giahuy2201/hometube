from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from workers.downloader import YTdlp
from core.database import engine, SessionLocal
from workers.daemon import DownloadTask, daemon
import starlette.status as status
import library.schemas as schemas, library.models as models
import library.crud as medias_crud
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
    if existMedia:
        return existMedia
    # add
    medias_crud.create_media(db, newMedia)
    daemon.add_task(DownloadTask(request.url, request.preset_id))
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
