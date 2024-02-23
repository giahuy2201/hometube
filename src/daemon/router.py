from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import starlette.status as status

from core.database import engine, get_db
from daemon import models
import daemon.schemas as schemas
import daemon.service as service
import daemon.crud as tasks_crud

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return tasks_crud.get_tasks(db)


@router.get("/{id}", response_model=schemas.Task)
def get_task(id: str, db: Session = Depends(get_db)):
    task = tasks_crud.get_task_by_id(db, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to find task with id {id}",
        )
    return task


@router.post("/", response_model=schemas.Task)
def add_task(request: schemas.TaskCreate, db: Session = Depends(get_db)):
    # TODO: Implement task post: refresh, schedule
    pass


@router.delete("/{id}")
def get_task(id: str, db: Session = Depends(get_db)):
    success = tasks_crud.delete_task(db, id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete task with id {id}",
        )
    return {"status": "ok"}
