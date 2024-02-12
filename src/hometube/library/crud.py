from sqlalchemy.orm import Session
from sqlalchemy import or_

import library.models as models, library.schemas as schemas


def search_medias(db: Session, term: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Media)
        .filter(
            or_(models.Media.title.contains(term), models.Media.uploader.contains(term))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_medias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Media).offset(skip).limit(limit).all()


def get_media_by_id(db: Session, id: str):
    return db.query(models.Media).get(id)


def create_media(db: Session, media: schemas.Media):
    db_media = models.Media(**media.model_dump())
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def update_media(db: Session, video_metadata: dict):
    # TODO: // Update metadata when added again
    pass
