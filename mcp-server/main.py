from mcp.server.fastmcp import FastMCP
import httpx
import os
from typing import Optional, List, Dict, Any

mcp = FastMCP("TodoManager")

# BACKEND_URL example in k8s: http://todo-backend:8000
BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
TASKS_URL = f"{BASE_URL}/api/tasks"

@mcp.tool()
async def get_tasks(session_token: str) -> List[Dict[str, Any]]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{TASKS_URL}/",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        r.raise_for_status()
        return r.json()

@mcp.tool()
async def create_task(session_token: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"title": title}
    if description is not None:
        payload["description"] = description

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{TASKS_URL}/",
            json=payload,
            headers={"Authorization": f"Bearer {session_token}"}
        )
        r.raise_for_status()
        return r.json()

@mcp.tool()
async def update_task(
    session_token: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if completed is not None:
        payload["completed"] = completed

    async with httpx.AsyncClient() as client:
        r = await client.put(
            f"{TASKS_URL}/{task_id}",
            json=payload,
            headers={"Authorization": f"Bearer {session_token}"}
        )
        r.raise_for_status()
        return r.json()

@mcp.tool()
async def delete_task(session_token: str, task_id: str) -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            f"{TASKS_URL}/{task_id}",
            headers={"Authorization": f"Bearer {session_token}"}
        )
        # backend returns 204 in your code
        if r.status_code in (200, 204):
            return {"status": "deleted", "task_id": task_id}
        r.raise_for_status()
        return {"status": "unknown", "task_id": task_id}

if __name__ == "__main__":
    mcp.run()
