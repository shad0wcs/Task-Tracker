from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import TaskCreate, TaskResponse
from app import crud
from app.models import User
from app.auth import get_current_user


router = APIRouter()


@router.post('/tasks', response_model=TaskResponse)
def create_new_task(task: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_task(db, task, current_user.id)


@router.get('/tasks', response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.get_tasks(db, current_user.id)


@router.get('/tasks/{task_id}', response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task


@router.delete('/tasks/{task_id}', response_model=TaskResponse)
def remove_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = crud.delete_task(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return task