from sqlalchemy.orm import Session
from app.models import Task, User
from app.schemas import TaskCreate, UserCreate
from app.auth import hash_password

def create_task(db: Session, task: TaskCreate, owner_id: int):
    db_task = Task(title = task.title, description = task.description, status = task.status, owner_id = owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(db: Session, owner_id: int):
    all_tasks = db.query(Task).filter(Task.owner_id == owner_id).all()
    return all_tasks


def get_task(db: Session, task_id: int, owner_id: int):
    task_to_get = db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()
    return task_to_get


def delete_task(db: Session, task_id: int, owner_id: int):
    task_to_delete = get_task(db, task_id, owner_id)
    if task_to_delete is None:
        return None
    db.delete(task_to_delete)
    db.commit()
    return task_to_delete


def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = User(email = user.email, hashed_password = hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
    