from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

import medias.models as models, medias.schemas as schemas


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
    db_media = models.Media(**media.model_dump(exclude_unset=True))
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media


def update_media(db: Session, media: schemas.Media):
    db_media = db.query(models.Media).get(media.id)
    if not db_media:
        return False
    media_data = media.model_dump(exclude_unset=True)
    for key, value in media_data.items():
        setattr(db_media, key, value)
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return True


def delete_media(db: Session, id: str):
    db_media = db.query(models.Media).get(id)
    if not db_media:
        return False
    db.delete(db_media)
    db.commit()
    return True


def get_version_by_id(db: Session, id: str):
    return db.query(models.MediaVersion).get(id)


def get_versions(db: Session, media_id: str):
    return (
        db.query(models.MediaVersion)
        .filter(
            and_(
                models.MediaVersion.media_id.is_(media_id),
            )
        )
        .all()
    )


def get_version_by_preset_id(db: Session, media_id: str, preset_id: str):
    return (
        db.query(models.MediaVersion)
        .filter(
            and_(
                models.MediaVersion.media_id.is_(media_id),
                models.MediaVersion.preset_id.is_(preset_id),
            )
        )
        .all()
    )


def create_version(db: Session, version: schemas.MediaVersion):
    db_version = models.MediaVersion(**version.model_dump(exclude_unset=True))
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return db_version


def update_version(db: Session, version: schemas.MediaVersion):
    db_version = db.query(models.MediaVersion).get(version.id)
    if not db_version:
        return False
    version_data = version.model_dump(exclude_unset=True)
    for key, value in version_data.items():
        setattr(db_version, key, value)
    db.add(db_version)
    db.commit()
    db.refresh(db_version)
    return True


def delete_version(db: Session, id: str):
    db_version = db.query(models.MediaVersion).get(id)
    if not db_version:
        return False
    db.delete(db_version)
    db.commit()
    return True
