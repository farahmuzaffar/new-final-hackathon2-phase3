from mcp.shared.exceptions import McpError
from mcp.server import Server
from mcp.types import InitOptions
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import httpx
import asyncio
from jose import jwt, JWTError
from src.config import settings

# Initialize the MCP server
server = Server("todo-mcp-server")

# JWT verification function
def verify_jwt(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise McpError("Invalid token: no user ID")
        return user_id
    except JWTError:
        raise McpError("Invalid token")


# Define input/output models for MCP tools
class CreateTaskInput(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the task")
    description: Optional[str] = Field(None, description="Optional description of the task")
    completed: Optional[bool] = Field(False, description="Whether the task is completed")


class CreateTaskOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


class ListTasksInput(BaseModel):
    page: Optional[int] = Field(1, ge=1, description="Page number for pagination")
    limit: Optional[int] = Field(10, ge=1, le=100, description="Number of tasks per page")
    status: Optional[str] = Field("all", description="Filter by completion status")


class ListTasksOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


class GetTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to retrieve")


class GetTaskOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


class UpdateTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to update")
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="New title of the task")
    description: Optional[str] = Field(None, description="New description of the task")
    completed: Optional[bool] = Field(None, description="New completion status of the task")


class UpdateTaskOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


class DeleteTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to delete")


class DeleteTaskOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, str]] = None
    error: Optional[Dict[str, str]] = None


class CompleteTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to toggle completion status")


class CompleteTaskOutput(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, str]] = None


# Helper function to make HTTP requests to the backend API
async def make_api_request(method: str, endpoint: str, token: str, data: Optional[Dict] = None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Assuming the backend is running on localhost:8000
    base_url = "http://localhost:8000"
    url = f"{base_url}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers)
            else:
                raise McpError(f"Unsupported HTTP method: {method}")
                
            return response
        except Exception as e:
            raise McpError(f"API request failed: {str(e)}")


# Tool: create_task
@server.tool("create_task")
async def create_task_tool(input: CreateTaskInput, token: str) -> CreateTaskOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)
        
        # Prepare the request data
        request_data = {
            "title": input.title,
            "description": input.description or "",
        }
        
        # Make the API request
        response = await make_api_request("POST", "/api/tasks/", token, request_data)
        
        if response.status_code == 201:
            task_data = response.json()
            # Verify that the task belongs to the authenticated user
            if task_data.get("user_id") != user_id:
                raise McpError("Unauthorized: Task does not belong to user")
            
            return CreateTaskOutput(
                success=True,
                data=task_data
            )
        else:
            return CreateTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return CreateTaskOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return CreateTaskOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Tool: list_tasks
@server.tool("list_tasks")
async def list_tasks_tool(input: ListTasksInput, token: str) -> ListTasksOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)
        
        # Construct query parameters
        params = {}
        if input.page:
            params["page"] = input.page
        if input.limit:
            params["limit"] = input.limit
            
        # Make the API request
        endpoint = f"/api/tasks/"
        if params:
            endpoint += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
            
        response = await make_api_request("GET", endpoint, token)
        
        if response.status_code == 200:
            tasks_data = response.json()
            # Verify that all tasks belong to the authenticated user
            for task in tasks_data:
                if task.get("user_id") != user_id:
                    raise McpError("Unauthorized: Retrieved tasks do not all belong to user")
                    
            return ListTasksOutput(
                success=True,
                data={
                    "tasks": tasks_data,
                    "pagination": {
                        "page": input.page or 1,
                        "limit": input.limit or 10,
                        "total": len(tasks_data),
                        "pages": 1  # Simplified pagination info
                    }
                }
            )
        else:
            return ListTasksOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return ListTasksOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return ListTasksOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Tool: get_task
@server.tool("get_task")
async def get_task_tool(input: GetTaskInput, token: str) -> GetTaskOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)
        
        # Make the API request
        response = await make_api_request("GET", f"/api/tasks/{input.task_id}", token)
        
        if response.status_code == 200:
            task_data = response.json()
            # Verify that the task belongs to the authenticated user
            if task_data.get("user_id") != user_id:
                raise McpError("Unauthorized: Task does not belong to user")
                
            return GetTaskOutput(
                success=True,
                data=task_data
            )
        else:
            return GetTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return GetTaskOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return GetTaskOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Tool: update_task
@server.tool("update_task")
async def update_task_tool(input: UpdateTaskInput, token: str) -> UpdateTaskOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)
        
        # Prepare the request data
        request_data = {}
        if input.title is not None:
            request_data["title"] = input.title
        if input.description is not None:
            request_data["description"] = input.description
        if input.completed is not None:
            request_data["completed"] = input.completed
            
        # Make the API request
        response = await make_api_request("PUT", f"/api/tasks/{input.task_id}", token, request_data)
        
        if response.status_code == 200:
            task_data = response.json()
            # Verify that the task belongs to the authenticated user
            if task_data.get("user_id") != user_id:
                raise McpError("Unauthorized: Task does not belong to user")
                
            return UpdateTaskOutput(
                success=True,
                data=task_data
            )
        else:
            return UpdateTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return UpdateTaskOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return UpdateTaskOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Tool: delete_task
@server.tool("delete_task")
async def delete_task_tool(input: DeleteTaskInput, token: str) -> DeleteTaskOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)
        
        # Make the API request
        response = await make_api_request("DELETE", f"/api/tasks/{input.task_id}", token)
        
        if response.status_code == 204:
            return DeleteTaskOutput(
                success=True,
                data={
                    "message": "Task deleted successfully"
                }
            )
        else:
            return DeleteTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return DeleteTaskOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return DeleteTaskOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Tool: complete_task
@server.tool("complete_task")
async def complete_task_tool(input: CompleteTaskInput, token: str) -> CompleteTaskOutput:
    try:
        # Verify the JWT token to get the user ID
        user_id = verify_jwt(token)

        # Since the backend doesn't have a dedicated endpoint for toggling completion,
        # we'll first get the task, then update its completion status to true
        response = await make_api_request("GET", f"/api/tasks/{input.task_id}", token)

        if response.status_code != 200:
            return CompleteTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": "Task not found"
                }
            )

        task_data = response.json()
        # Verify that the task belongs to the authenticated user
        if task_data.get("user_id") != user_id:
            raise McpError("Unauthorized: Task does not belong to user")

        # Set the completion status to true (completing the task)
        update_data = {
            "completed": True
        }

        response = await make_api_request("PUT", f"/api/tasks/{input.task_id}", token, update_data)

        if response.status_code == 200:
            updated_task = response.json()
            # Verify that the task belongs to the authenticated user
            if updated_task.get("user_id") != user_id:
                raise McpError("Unauthorized: Task does not belong to user")

            return CompleteTaskOutput(
                success=True,
                data=updated_task
            )
        else:
            return CompleteTaskOutput(
                success=False,
                error={
                    "code": str(response.status_code),
                    "message": response.text
                }
            )
    except McpError as e:
        return CompleteTaskOutput(
            success=False,
            error={
                "code": "AUTH_ERROR",
                "message": str(e)
            }
        )
    except Exception as e:
        return CompleteTaskOutput(
            success=False,
            error={
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        )


# Initialize the server
async def serve():
    options = InitOptions(
        capabilities={},
    )
    async with server.serve(options):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(serve())