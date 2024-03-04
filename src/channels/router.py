from fastapi import APIRouter, HTTPException, Depends
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
import channels.schemas as channels_schemas, channels.models as models
import channels.crud as channels_crud
import presets.crud as presets_crud


router = APIRouter()


@router.get("/", response_model=list[channels_schemas.Channel])
def get_channels(db: Session = Depends(get_db)):
    return channels_crud.get_channels(db)


@router.get("/{id}", response_model=channels_schemas.Channel)
def get_channel(id: str, db: Session = Depends(get_db)):
    channel = channels_crud.get_channel_by_id(db, id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find channel with id {id}",
        )
    return channel


@router.post("/", response_model=channels_schemas.Channel)
def add_channel(request: channels_schemas.ChannelCreate, db: Session = Depends(get_db)):
    # validate url
    ytdlp = YTdlp(request.url)
    newChannel = channels_schemas.Channel.model_validate_json(
        json.dumps(ytdlp.get_metadata())
    )
    if not newChannel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to add channel with url {request.url}",
        )
    # check for existing record
    existChannel = channels_crud.get_channel_by_id(db, newChannel.id)
    if not existChannel:
        existChannel = channels_crud.create_channel(db, newChannel)
    return existChannel


@router.delete("/{id}")
def delete_channel(id: str, db: Session = Depends(get_db)):
    success = channels_crud.delete_channel(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete channel with id {id}",
        )
    return {"status": "ok"}
