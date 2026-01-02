# API Contract: Task Management

## Overview

This document defines the API contract for task management endpoints in the Hackathon Todo Phase-2 application.

## Base URL

All API endpoints are relative to: `https://api.hackathontodo.com/v1` (or `http://localhost:8000` for development)

## Authentication

All endpoints except authentication endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

## Common Response Format

Successful responses follow this structure:
```json
{
  "data": { ... } // Response payload varies by endpoint
}
```

Error responses follow this structure:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": { ... } // Optional
  }
}
```

## Endpoints

### Create Task

**POST** `/api/tasks`

Creates a new task for the authenticated user.

#### Request

**Headers:**
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Body:**
```json
{
  "title": "string (required, 1-255 characters)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}
```

#### Response

**201 Created**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

**400 Bad Request** - Invalid input
**401 Unauthorized** - Invalid or expired token

### Get User Tasks

**GET** `/api/tasks`

Retrieves all tasks for the authenticated user.

#### Query Parameters

- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Number of tasks per page (default: 10, max: 100)
- `status` (optional): Filter by completion status ("all", "active", "completed"; default: "all")

#### Response

**200 OK**
```json
{
  "data": {
    "tasks": [
      {
        "id": "uuid",
        "user_id": "uuid",
        "title": "string",
        "description": "string",
        "completed": "boolean",
        "created_at": "timestamp",
        "updated_at": "timestamp"
      }
    ],
    "pagination": {
      "page": "number",
      "limit": "number",
      "total": "number",
      "pages": "number"
    }
  }
}
```

**401 Unauthorized** - Invalid or expired token

### Get Task by ID

**GET** `/api/tasks/{task_id}`

Retrieves a specific task by ID.

#### Path Parameters

- `task_id`: UUID of the task to retrieve

#### Response

**200 OK**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

**401 Unauthorized** - Invalid or expired token
**403 Forbidden** - User does not own this task
**404 Not Found** - Task does not exist

### Update Task

**PUT** `/api/tasks/{task_id}`

Updates an existing task.

#### Path Parameters

- `task_id`: UUID of the task to update

#### Request

**Headers:**
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Body:**
```json
{
  "title": "string (optional, 1-255 characters)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

#### Response

**200 OK**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

**400 Bad Request** - Invalid input
**401 Unauthorized** - Invalid or expired token
**403 Forbidden** - User does not own this task
**404 Not Found** - Task does not exist

### Toggle Task Completion

**PATCH** `/api/tasks/{task_id}/toggle`

Toggles the completion status of a task.

#### Path Parameters

- `task_id`: UUID of the task to toggle

#### Response

**200 OK**
```json
{
  "data": {
    "id": "uuid",
    "user_id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
}
```

**401 Unauthorized** - Invalid or expired token
**403 Forbidden** - User does not own this task
**404 Not Found** - Task does not exist

### Delete Task

**DELETE** `/api/tasks/{task_id}`

Deletes a specific task.

#### Path Parameters

- `task_id`: UUID of the task to delete

#### Response

**200 OK**
```json
{
  "data": {
    "message": "Task deleted successfully"
  }
}
```

**401 Unauthorized** - Invalid or expired token
**403 Forbidden** - User does not own this task
**404 Not Found** - Task does not exist