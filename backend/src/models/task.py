from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime, timezone
from pydantic import validator


class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship to user
    user: Optional[User] = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskCreate(TaskBase):
    pass