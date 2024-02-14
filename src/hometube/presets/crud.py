from sqlalchemy.orm import Session
from sqlalchemy import or_

import presets.models as models, presets.schemas as schemas


def search_presets(db: Session, term: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Preset)
        .filter(
            or_(
                models.Preset.id.contains(term),
                models.Preset.description.contains(term),
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_presets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Preset).offset(skip).limit(limit).all()


def get_preset_by_id(db: Session, id: str):
    return db.query(models.Preset).get(id)


def create_preset(db: Session, preset: schemas.Preset):
    db_preset = models.Preset(**preset.model_dump())
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset


def update_preset(db: Session, preset: schemas.Preset):
    db_preset = db.query(models.Preset).get(preset.id)
    if not db_preset:
        return False
    preset_data = preset.model_dump(exclude_unset=True)
    for key, value in preset_data.items():
        setattr(db_preset, key, value)
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return True


def delete_preset(db: Session, id: str):
    db_preset = db.query(models.Preset).get(id)
    if not db_preset:
        return False
    db.delete(db_preset)
    db.commit()
    return True
