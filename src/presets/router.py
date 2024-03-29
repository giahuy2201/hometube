from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ytdlp.downloader import YTdlp
from core.database import engine, get_db
import starlette.status as status
import presets.schemas as schemas, presets.models as models
import presets.crud as crud


router = APIRouter()


@router.get("/", response_model=list[schemas.Preset])
def get_presets(db: Session = Depends(get_db), term: str = ""):
    # Retrieve all requested videos
    if term != "":
        videos = crud.search_presets(db, term)
    else:
        videos = crud.get_presets(db)
    return videos


@router.get("/{id}", response_model=schemas.Preset)
def get_preset(id: str, db: Session = Depends(get_db)):
    preset = crud.get_preset_by_id(db, id)
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find preset with id {id}",
        )
    return preset


@router.post("/", response_model=schemas.Preset)
def add_preset(request: schemas.Preset, db: Session = Depends(get_db)):
    # validate preset
    existPreset = crud.get_preset_by_id(db, request.id)
    if existPreset:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Failed to add preset with id {request.id} (existed)",
        )
    newPreset = crud.create_preset(db, request)
    return newPreset


@router.put("/{id}")
def get_preset(id: str, request: schemas.Preset, db: Session = Depends(get_db)):
    # validate
    if id != request.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update preset id {id} with id {request.id} (not allowed)",
        )
    success = crud.update_preset(db, request)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update preset with id {id}",
        )
    return {"status": "ok"}


@router.delete("/{id}")
def get_preset(id: str, db: Session = Depends(get_db)):
    success = crud.delete_preset(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete preset with id {id}",
        )
    return {"status": "ok"}
