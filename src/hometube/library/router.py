from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from workers.downloader import YTdlp
from library.database import engine, SessionLocal
from workers.daemon import DownloadTask, daemon
import starlette.status as status
import library.schemas as schemas, library.models as models
import library.crud as crud

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
        videos = crud.search_medias(db, term)
    else:
        videos = crud.get_medias(db)
    return videos


@router.get("/{id}", response_model=schemas.Media)
def get_media(id: str, db: Session = Depends(get_db)):
    media = crud.get_media_by_id(db, id)
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find media with id {id}",
        )
    return media


@router.post("/", response_model=schemas.Media)
def add_media(request: schemas.MediaCreate, db: Session = Depends(get_db)):
    # validate
    ytdlp = YTdlp(request.url)
    newMedia = ytdlp.getMetadata()
    if not newMedia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to add media with url {request.url}",
        )
    # check for existing record
    existMedia = crud.get_media_by_id(db, newMedia.id)
    if existMedia:
        return existMedia
    # add
    crud.create_media(db, newMedia)
    daemon.add_task(DownloadTask(request.url, request.preset))
    return newMedia
