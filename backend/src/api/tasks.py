from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from ..database.database import get_session
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate, User
from ..auth.jwt_bearer import JWTBearer
from ..exceptions.exceptions import TaskNotFoundException, ForbiddenException, ValidationError


router = APIRouter()


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Create the task with the authenticated user's ID
    db_task = Task(**task.model_dump(), user_id=UUID(user_id))
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks", response_model=List[TaskRead])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    # Query tasks for the authenticated user only
    tasks = session.exec(
        select(Task).where(Task.user_id == uuid.UUID(user_id)).offset(skip).limit(limit)
    ).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskRead)
def read_task(
    task_id: UUID,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Get the task
    task = session.get(Task, task_id)
    if not task:
        raise TaskNotFoundException()

    # Verify that the task belongs to the authenticated user
    if str(task.user_id) != user_id:
        raise ForbiddenException("You don't have permission to access this task")

    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Get the task
    db_task = session.get(Task, task_id)
    if not db_task:
        raise TaskNotFoundException()

    # Verify that the task belongs to the authenticated user
    if str(db_task.user_id) != user_id:
        raise ForbiddenException("You don't have permission to update this task")

    # Update the task
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/tasks/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion(
    task_id: UUID,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Get the task
    db_task = session.get(Task, task_id)
    if not db_task:
        raise TaskNotFoundException()

    # Verify that the task belongs to the authenticated user
    if str(db_task.user_id) != user_id:
        raise ForbiddenException("You don't have permission to update this task")

    # Toggle completion status
    db_task.completed = not db_task.completed
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: UUID,
    session: Session = Depends(get_session),
    token: str = Depends(JWTBearer())
):
    # Get user ID from token (set by JWTBearer middleware)
    user_id = getattr(token, 'user_id', None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Get the task
    db_task = session.get(Task, task_id)
    if not db_task:
        raise TaskNotFoundException()

    # Verify that the task belongs to the authenticated user
    if str(db_task.user_id) != user_id:
        raise ForbiddenException("You don't have permission to delete this task")

    # Delete the task
    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}