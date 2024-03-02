from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

import channels.models as models, channels.schemas as schemas


def get_channels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Channel).offset(skip).limit(limit).all()


def get_channel_by_id(db: Session, id: str):
    return db.query(models.Channel).get(id)


def create_channel(db: Session, channel: schemas.Channel):
    db_channel = models.Channel(**channel.model_dump(exclude_unset=True))
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel


def update_channel(db: Session, channel: schemas.Channel):
    db_channel = db.query(models.Channel).get(channel.id)
    if not db_channel:
        return False
    channel_data = channel.model_dump(exclude_unset=True)
    for key, value in channel_data.items():
        setattr(db_channel, key, value)
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return True


def delete_channel(db: Session, id: str):
    db_channel = db.query(models.Channel).get(id)
    if not db_channel:
        return False
    db.delete(db_channel)
    db.commit()
    return True
