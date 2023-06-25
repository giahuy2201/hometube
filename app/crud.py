from sqlalchemy.orm import Session
from app.schemas import VideoBase
from sqlalchemy import or_

import models, schemas

def search_videos(db: Session, term: str, skip: int = 0, limit: int = 100):
    return db.query(models.Video).filter(or_(models.Video.title.contains(term),models.Video.uploader.contains(term))).offset(skip).limit(limit).all()

def get_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()


def create_video(db: Session, video_metadata: dict):
    dummy = schemas.Video(id='')
    # filter out extra keys
    filtered_metadata = {k:v for k,v in video_metadata.items() if k in dummy.dict()}
    db_video = models.Video(**filtered_metadata)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
