from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = 'todo'


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
