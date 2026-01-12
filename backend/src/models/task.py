from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: UUID = Field(foreign_key="users.id")


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None


class TaskRead(SQLModel):
    id: UUID
    title: str
    description: Optional[str]
    completed: bool


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

