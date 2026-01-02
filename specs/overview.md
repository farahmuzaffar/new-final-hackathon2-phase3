# Hackathon Todo – Phase 2: Full-Stack Web Application

## Project Purpose

The Hackathon Todo project aims to transform a simple in-memory todo application into a fully-featured, multi-user, full-stack web application with persistent storage and authentication. This Phase-2 implementation will provide users with the ability to manage their personal tasks securely with proper data isolation between users.

## Phase-2 Description

Phase-2 involves building a complete full-stack web application with:
- A Next.js frontend with TypeScript
- A FastAPI backend with Python 3.13+
- SQLModel for database modeling
- Neon Serverless PostgreSQL for persistent storage
- Better Auth for JWT-based authentication
- REST API for communication between frontend and backend

## High-Level Architecture

The application follows a standard full-stack architecture:

```
┌─────────────────┐    REST API     ┌──────────────────┐
│   Next.js       │◄────────────────►   FastAPI        │
│   Frontend      │                 │   Backend        │
│ (TypeScript)    │                 │ (Python 3.13+)   │
└─────────────────┘                 └──────────────────┘
                                              │
                                              │ Database
                                              ▼
                                    ┌──────────────────┐
                                    │   Neon PostgreSQL│
                                    │   (Serverless)   │
                                    └──────────────────┘
```

The frontend handles user interface and authentication state management, while the backend manages business logic, authentication verification, and database operations. The database stores user information and their associated tasks.

## Explicit In-Scope Items

- Multi-user support with proper data isolation
- JWT-based authentication using Better Auth
- Task CRUD operations (Create, Read, Update, Delete)
- User session management
- REST API endpoints for all required functionality
- SQLModel-based data models
- Neon Serverless PostgreSQL database schema
- Next.js frontend with App Router
- Responsive UI components for task management
- Error handling and validation
- Secure authentication flows (signup, login, logout)

## Explicit Out-Of-Scope Items

- AI chatbot functionality
- MCP / Agents SDK integration
- Kubernetes, Docker, or Helm deployment
- Kafka or Dapr for messaging
- Advanced analytics or reporting
- Email notifications
- File attachments to tasks
- Task sharing between users
- Real-time collaborative features
- Offline-first capabilities