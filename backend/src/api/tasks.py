from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database.database import get_session
from src.models.task import Task, TaskCreate, TaskUpdate
from src.core.security import get_current_user
from src.models.user import User

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


# ================= CREATE TASK =================
@router.post("/", status_code=201)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    new_task = Task(
        title=task.title,
        description=task.description,
        completed=False,
        user_id=current_user.id,
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


# ================= GET ALL TASKS =================
@router.get("/")
def get_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id)
    ).all()

    return tasks


# ================= UPDATE TASK =================
@router.put("/{task_id}")
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)

    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


# ================= DELETE TASK =================
@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    task = session.get(Task, task_id)

    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
