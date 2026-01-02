# Data Model: Hackathon Todo Phase-2

## Overview

This document defines the data models for the Hackathon Todo Phase-2 application. The models will be implemented using SQLModel and will map to tables in the Neon PostgreSQL database.

## User Model

The User model represents the application users. Since authentication is handled by Better Auth, this model will primarily serve to link application data to authenticated users.

```sql
TABLE users (
    id UUID PRIMARY KEY,          -- Better Auth user ID
    email VARCHAR(255) UNIQUE,    -- User's email address
    name VARCHAR(255),            -- User's display name (optional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Task Model

The Task model represents the todo items that users can create, update, and delete.

```sql
TABLE tasks (
    id UUID PRIMARY KEY,          -- Unique task identifier
    user_id UUID NOT NULL,        -- Foreign key to users table
    title VARCHAR(255) NOT NULL,  -- Task title
    description TEXT,             -- Optional task description
    completed BOOLEAN DEFAULT FALSE, -- Completion status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

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