from fastapi import HTTPException, status
from typing import Optional


class TaskException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)


class UserNotFoundException(TaskException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class TaskNotFoundException(TaskException):
    def __init__(self, detail: str = "Task not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(TaskException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(TaskException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class ValidationError(TaskException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


# Custom exception handler
async def task_exception_handler(request, exc: TaskException):
    return {
        "error": {
            "code": type(exc).__name__,
            "message": str(exc.detail)
        }
    }