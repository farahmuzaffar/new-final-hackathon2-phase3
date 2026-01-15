# MCP Tools Specification: Todo API Integration

## Overview

This document specifies the MCP (Model Context Protocol) tools that expose existing Todo REST API endpoints to AI agents. These tools allow AI agents to perform task management operations on behalf of authenticated users.

## Authentication

All tools require a valid JWT token to be provided in the tool configuration or with each request. The token must be associated with an authenticated user account.

## Tools

### 1. create_task

**Description:** Creates a new task for the authenticated user.

**Endpoint:** `POST /api/tasks`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Title of the task (required, 1-255 characters)",
      "minLength": 1,
      "maxLength": 255
    },
    "description": {
      "type": "string",
      "description": "Optional description of the task"
    },
    "completed": {
      "type": "boolean",
      "description": "Whether the task is completed (default: false)",
      "default": false
    }
  },
  "required": ["title"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the created task"
        },
        "user_id": {
          "type": "string",
          "description": "UUID of the user who owns the task"
        },
        "title": {
          "type": "string",
          "description": "Title of the task"
        },
        "description": {
          "type": "string",
          "description": "Description of the task"
        },
        "completed": {
          "type": "boolean",
          "description": "Whether the task is completed"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was created"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was last updated"
        }
      },
      "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

### 2. list_tasks

**Description:** Retrieves all tasks for the authenticated user with optional filtering.

**Endpoint:** `GET /api/tasks`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "page": {
      "type": "integer",
      "minimum": 1,
      "description": "Page number for pagination (default: 1)",
      "default": 1
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100,
      "description": "Number of tasks per page (default: 10, max: 100)",
      "default": 10
    },
    "status": {
      "type": "string",
      "enum": ["all", "active", "completed"],
      "description": "Filter by completion status (default: 'all')",
      "default": "all"
    }
  }
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "tasks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "description": "UUID of the task"
              },
              "user_id": {
                "type": "string",
                "description": "UUID of the user who owns the task"
              },
              "title": {
                "type": "string",
                "description": "Title of the task"
              },
              "description": {
                "type": "string",
                "description": "Description of the task"
              },
              "completed": {
                "type": "boolean",
                "description": "Whether the task is completed"
              },
              "created_at": {
                "type": "string",
                "format": "date-time",
                "description": "Timestamp when the task was created"
              },
              "updated_at": {
                "type": "string",
                "format": "date-time",
                "description": "Timestamp when the task was last updated"
              }
            },
            "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
          }
        },
        "pagination": {
          "type": "object",
          "properties": {
            "page": {
              "type": "number",
              "description": "Current page number"
            },
            "limit": {
              "type": "number",
              "description": "Number of tasks per page"
            },
            "total": {
              "type": "number",
              "description": "Total number of tasks"
            },
            "pages": {
              "type": "number",
              "description": "Total number of pages"
            }
          },
          "required": ["page", "limit", "total", "pages"]
        }
      },
      "required": ["tasks", "pagination"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

### 3. get_task

**Description:** Retrieves a specific task by its ID.

**Endpoint:** `GET /api/tasks/{task_id}`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "UUID of the task to retrieve"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the task"
        },
        "user_id": {
          "type": "string",
          "description": "UUID of the user who owns the task"
        },
        "title": {
          "type": "string",
          "description": "Title of the task"
        },
        "description": {
          "type": "string",
          "description": "Description of the task"
        },
        "completed": {
          "type": "boolean",
          "description": "Whether the task is completed"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was created"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was last updated"
        }
      },
      "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

### 4. update_task

**Description:** Updates an existing task.

**Endpoint:** `PUT /api/tasks/{task_id}`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "UUID of the task to update"
    },
    "title": {
      "type": "string",
      "description": "New title of the task (optional, 1-255 characters)",
      "minLength": 1,
      "maxLength": 255
    },
    "description": {
      "type": "string",
      "description": "New description of the task (optional)"
    },
    "completed": {
      "type": "boolean",
      "description": "New completion status of the task (optional)"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the task"
        },
        "user_id": {
          "type": "string",
          "description": "UUID of the user who owns the task"
        },
        "title": {
          "type": "string",
          "description": "Updated title of the task"
        },
        "description": {
          "type": "string",
          "description": "Updated description of the task"
        },
        "completed": {
          "type": "boolean",
          "description": "Updated completion status of the task"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was created"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was last updated"
        }
      },
      "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

### 5. delete_task

**Description:** Deletes a specific task.

**Endpoint:** `DELETE /api/tasks/{task_id}`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "UUID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "message": {
          "type": "string",
          "description": "Confirmation message that the task was deleted"
        }
      },
      "required": ["message"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

### 6. complete_task

**Description:** Toggles the completion status of a task.

**Endpoint:** `PATCH /api/tasks/{task_id}/toggle`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "description": "UUID of the task to toggle completion status"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether the operation was successful"
    },
    "data": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "UUID of the task"
        },
        "user_id": {
          "type": "string",
          "description": "UUID of the user who owns the task"
        },
        "title": {
          "type": "string",
          "description": "Title of the task"
        },
        "description": {
          "type": "string",
          "description": "Description of the task"
        },
        "completed": {
          "type": "boolean",
          "description": "Updated completion status of the task"
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was created"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "description": "Timestamp when the task was last updated"
        }
      },
      "required": ["id", "user_id", "title", "completed", "created_at", "updated_at"]
    },
    "error": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "Error code if operation failed"
        },
        "message": {
          "type": "string",
          "description": "Error message if operation failed"
        }
      },
      "required": ["code", "message"]
    }
  },
  "required": ["success"]
}
```

## Error Handling

All tools follow the same error response format:
- 401 Unauthorized: Invalid or expired authentication token
- 403 Forbidden: User does not have permission to access the resource
- 404 Not Found: The requested resource does not exist
- 400 Bad Request: Invalid input parameters

## Security Considerations

- All tools require valid authentication tokens
- Tools enforce user ownership of tasks
- Input validation is performed according to API contract specifications
- Sensitive data is handled according to existing security policies