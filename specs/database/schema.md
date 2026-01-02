# Database Schema Specification

## Overview

The database schema uses SQLModel for defining data models that work with Neon Serverless PostgreSQL. The schema includes user management (handled by Better Auth) and task management with proper ownership relationships.

## User Entity

**Note:** The User entity is primarily managed by Better Auth, but we define a minimal representation for our application's needs.

```sql
TABLE users (
    id UUID PRIMARY KEY,          -- Better Auth user ID
    email VARCHAR(255) UNIQUE,    -- User's email address
    name VARCHAR(255),            -- User's display name (optional)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Constraints:**
- The `id` field is the primary key and corresponds to Better Auth's user ID
- The `email` field must be unique across all users
- The `created_at` and `updated_at` fields are automatically managed

## Task Entity

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

**Constraints:**
- The `id` field is the primary key for each task
- The `user_id` field is a foreign key referencing the users table
- The `title` field is required and has a maximum length of 255 characters
- The `completed` field defaults to FALSE when a task is created
- The `created_at` and `updated_at` fields are automatically managed
- When a user is deleted, all their tasks are automatically deleted (CASCADE)

## Relationships

### User to Tasks (One-to-Many)
- One user can own many tasks
- The relationship is established through the `user_id` foreign key in the tasks table
- When a user is deleted, all their tasks are automatically deleted

## Indexes

### Tasks Table
- Index on `user_id` for efficient querying of tasks by user
- Index on `completed` for efficient filtering of completed/incomplete tasks
- Index on `created_at` for efficient sorting by creation date

### Users Table
- Index on `email` for efficient user lookup by email address

## Data Integrity Rules

### Task Ownership
- Every task must be associated with a valid user
- Users can only access, modify, or delete their own tasks
- The database enforces referential integrity through foreign key constraints

### Data Validation
- Task titles cannot be empty or null
- User emails must be unique
- Creation and update timestamps are automatically managed
- Completed status defaults to false for new tasks

## SQLModel Implementation

The SQLModel classes will be structured as follows:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
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
    
    # Relationship to user (if needed)
    user: Optional["User"] = Relationship(back_populates="tasks")

class UserBase(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True)
    name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to tasks (if needed)
    tasks: list["Task"] = Relationship(back_populates="user")
```

**Note:** The actual implementation will need to integrate with Better Auth's user management system, so the User model might be simplified or adapted to work with Better Auth's schema.