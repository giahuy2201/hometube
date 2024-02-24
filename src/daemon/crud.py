from sqlalchemy.orm import Session
from sqlalchemy import and_

import daemon.models as models
import daemon.schemas as schemas


def get_tasks(db: Session):
    return db.query(models.Task).all()


def get_task_by_id(db: Session, id: str):
    return db.query(models.Task).get(id)


def create_task(db: Session, task: schemas.Task):
    db_task = models.Task(task.model_dump(exclude_unset=True))
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: schemas.Task):
    db_task = db.query(models.Task).get(task.id)
    if not db_task:
        return False
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return True


def delete_task(db: Session, id: str):
    db_task = db.query(models.Task).get(id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True
