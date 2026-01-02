from fastapi import FastAPI
from .api import tasks
from .database.database import engine
from .models.task import User, Task  # Import models to register them
from sqlmodel import SQLModel
from .exceptions.exceptions import task_exception_handler, TaskException


# Create the FastAPI application
app = FastAPI(
    title="Hackathon Todo API",
    description="API for the Hackathon Todo Phase-2 application",
    version="1.0.0"
)


# Create database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# Include API routes
app.include_router(tasks.router, prefix="/api", tags=["tasks"])


# Add exception handlers
app.add_exception_handler(TaskException, task_exception_handler)


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Todo API"}