import asyncio
import json
from typing import Dict, Any, List
from openai import OpenAI
from src.config import settings
from jose import jwt


def verify_and_get_user_id(token: str):
    """Verify the JWT token and return the user ID."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token: no user ID")
        return user_id
    except jwt.JWTError:
        raise ValueError("Invalid token")


def execute_mcp_tool(tool_name: str, arguments: Dict[str, Any], token: str) -> Dict[str, Any]:
    """
    Execute an MCP tool by making a request to the local backend API.
    This simulates connecting the AI agent to the MCP server.
    """
    import httpx
    
    # Verify the token and get the user ID
    try:
        user_id = verify_and_get_user_id(token)
    except ValueError as e:
        return {"error": str(e)}
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Map tool names to API endpoints
    base_url = "http://localhost:8000"  # Assuming backend runs on port 8000
    
    try:
        with httpx.Client() as client:
            if tool_name == "create_task":
                response = client.post(
                    f"{base_url}/api/tasks/",
                    headers=headers,
                    json={
                        "title": arguments.get("title"),
                        "description": arguments.get("description", ""),
                        "completed": arguments.get("completed", False)
                    }
                )
                return response.json() if response.status_code == 201 else {"error": f"Failed to create task: {response.text}"}
                
            elif tool_name == "list_tasks":
                response = client.get(f"{base_url}/api/tasks/", headers=headers)
                return {"tasks": response.json()} if response.status_code == 200 else {"error": f"Failed to list tasks: {response.text}"}
                
            elif tool_name == "get_task":
                task_id = arguments.get("task_id")
                response = client.get(f"{base_url}/api/tasks/{task_id}", headers=headers)
                return response.json() if response.status_code == 200 else {"error": f"Failed to get task: {response.text}"}
                
            elif tool_name == "update_task":
                task_id = arguments.get("task_id")
                update_data = {}
                if "title" in arguments:
                    update_data["title"] = arguments["title"]
                if "description" in arguments:
                    update_data["description"] = arguments["description"]
                if "completed" in arguments:
                    update_data["completed"] = arguments["completed"]
                
                response = client.put(f"{base_url}/api/tasks/{task_id}", headers=headers, json=update_data)
                return response.json() if response.status_code == 200 else {"error": f"Failed to update task: {response.text}"}
                
            elif tool_name == "delete_task":
                task_id = arguments.get("task_id")
                response = client.delete(f"{base_url}/api/tasks/{task_id}", headers=headers)
                return {"message": "Task deleted successfully"} if response.status_code == 204 else {"error": f"Failed to delete task: {response.text}"}
                
            elif tool_name == "complete_task":
                # Get the current task to check ownership
                task_id = arguments.get("task_id")
                response = client.get(f"{base_url}/api/tasks/{task_id}", headers=headers)
                
                if response.status_code != 200:
                    return {"error": f"Failed to get task: {response.text}"}
                
                task_data = response.json()
                # Verify that the task belongs to the authenticated user
                if task_data.get("user_id") != user_id:
                    return {"error": "Unauthorized: Task does not belong to user"}
                
                # Update the task to mark as completed
                update_data = {"completed": True}
                response = client.put(f"{base_url}/api/tasks/{task_id}", headers=headers, json=update_data)
                return response.json() if response.status_code == 200 else {"error": f"Failed to complete task: {response.text}"}
                
            else:
                return {"error": f"Unknown tool: {tool_name}"}
    
    except Exception as e:
        return {"error": f"Exception during tool execution: {str(e)}"}


def create_temp_token_for_user(user_id: str):
    """
    Create a temporary token for the user to use with the API calls.
    In a real implementation, you would use the actual JWT token from the request.
    """
    from datetime import datetime, timedelta
    from jose import jwt
    from src.config import settings

    # Create a temporary token with a short expiration
    expire = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiry
    to_encode = {"sub": user_id, "exp": expire}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def run_assistant_with_tools(client: OpenAI, thread_id: str, run_id: str, user_id: str):
    """
    Handle the assistant run and execute any required tools.
    """
    # Get the run status
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

    # Handle tool calls if they exist
    if run.status == 'requires_action' and run.required_action.type == 'submit_tool_outputs':
        tool_calls = run.required_action.submit_tool_outputs.tool_calls

        # Create a temporary token for the user
        temp_token = create_temp_token_for_user(user_id)

        # Execute each tool call
        tool_outputs = []
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute the MCP tool
            result = execute_mcp_tool(function_name, arguments, temp_token)

            # Format the result for OpenAI
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(result)
            })

        # Submit the tool outputs back to the assistant
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )

    return client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)