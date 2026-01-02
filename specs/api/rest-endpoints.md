# REST API Endpoints Specification

## Authentication Endpoints

### POST /api/auth/signup
**Description:** Create a new user account
**Authentication:** Not required
**Request Body:**
```json
{
  "email": "string (required)",
  "password": "string (required, min 8 chars)",
  "name": "string (optional)"
}
```
**Response:**
- 200: User created successfully, returns JWT
- 400: Invalid input data
- 409: User with email already exists

### POST /api/auth/login
**Description:** Authenticate user and return JWT
**Authentication:** Not required
**Request Body:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```
**Response:**
- 200: Authentication successful, returns JWT
- 400: Invalid input data
- 401: Invalid credentials

### POST /api/auth/logout
**Description:** Logout user and invalidate session
**Authentication:** Required (valid JWT)
**Request Body:** None
**Response:**
- 200: Logout successful
- 401: Invalid or expired token

## Task Management Endpoints

### GET /api/tasks
**Description:** Retrieve all tasks for the authenticated user
**Authentication:** Required (valid JWT)
**Query Parameters:**
- `page` (optional): Page number for pagination
- `limit` (optional): Number of tasks per page
- `status` (optional): Filter by task status (all, active, completed)
**Response:**
- 200: List of tasks for the user
- 401: Invalid or expired token

### POST /api/tasks
**Description:** Create a new task for the authenticated user
**Authentication:** Required (valid JWT)
**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (optional, default: false)"
}
```
**Response:**
- 201: Task created successfully
- 400: Invalid input data
- 401: Invalid or expired token

### GET /api/tasks/{task_id}
**Description:** Retrieve a specific task by ID
**Authentication:** Required (valid JWT)
**Path Parameters:**
- `task_id`: ID of the task to retrieve
**Response:**
- 200: Task details
- 401: Invalid or expired token
- 403: User does not own this task
- 404: Task not found

### PUT /api/tasks/{task_id}
**Description:** Update an existing task
**Authentication:** Required (valid JWT)
**Path Parameters:**
- `task_id`: ID of the task to update
**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```
**Response:**
- 200: Task updated successfully
- 400: Invalid input data
- 401: Invalid or expired token
- 403: User does not own this task
- 404: Task not found

### PATCH /api/tasks/{task_id}/toggle
**Description:** Toggle the completion status of a task
**Authentication:** Required (valid JWT)
**Path Parameters:**
- `task_id`: ID of the task to toggle
**Response:**
- 200: Task status updated successfully
- 401: Invalid or expired token
- 403: User does not own this task
- 404: Task not found

### DELETE /api/tasks/{task_id}
**Description:** Delete a specific task
**Authentication:** Required (valid JWT)
**Path Parameters:**
- `task_id`: ID of the task to delete
**Response:**
- 200: Task deleted successfully
- 401: Invalid or expired token
- 403: User does not own this task
- 404: Task not found

## User Profile Endpoints

### GET /api/user/profile
**Description:** Retrieve the authenticated user's profile
**Authentication:** Required (valid JWT)
**Response:**
- 200: User profile information
- 401: Invalid or expired token

## Error Response Format

All error responses follow the same structure:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

## Authentication Requirements Summary

- **Public endpoints:** No authentication required (signup, login)
- **Protected endpoints:** Valid JWT required in Authorization header
- **User-specific endpoints:** Valid JWT + user must own the resource
- **Authorization header format:** `Bearer {jwt_token}`

## Common Error Cases

- **401 Unauthorized:** Invalid, expired, or missing JWT
- **403 Forbidden:** User does not have permission to access the resource
- **404 Not Found:** Requested resource does not exist
- **400 Bad Request:** Invalid request format or validation errors
- **500 Internal Server Error:** Unexpected server error