# Quickstart Guide: Hackathon Todo Phase-2

## Project Setup

This guide will help you set up the development environment for the Hackathon Todo Phase-2 project.

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.13 or higher)
- PostgreSQL (or access to Neon PostgreSQL)
- Git

### Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hackathon-todo-phase2
   ```

2. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

### Environment Variables

Create `.env` files in both frontend and backend directories:

**Backend (.env):**
```
DATABASE_URL=postgresql://username:password@localhost:5432/hackathon_todo
NEON_DATABASE_URL=your_neon_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_SECRET=your_auth_secret
```

### Running the Application

1. Start the backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload --port 8000
   ```

2. In a separate terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. The application will be available at `http://localhost:3000`

### Database Setup

1. Run database migrations:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Initial migration"
   alembic upgrade head
   ```

### Running Tests

1. Backend tests:
   ```bash
   cd backend
   pytest
   ```

2. Frontend tests:
   ```bash
   cd frontend
   npm test
   ```

## Development Workflow

### Adding New Features

1. Update specifications in the `specs/` directory
2. Update the plan in `specs/hackathon-todo-phase2/plan.md` if needed
3. Generate tasks using `/sp.tasks`
4. Implement features following the generated tasks
5. Test the implementation against specifications

### API Endpoints

The backend provides the following REST API endpoints:

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/auth/logout` - User logout
- `GET /api/tasks` - Get user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a task
- `PATCH /api/tasks/{task_id}/toggle` - Toggle task completion
- `DELETE /api/tasks/{task_id}` - Delete a task
- `GET /api/user/profile` - Get user profile

### Authentication

The application uses JWT-based authentication with Better Auth:

1. Users register or login through the frontend
2. Better Auth manages user sessions and JWT tokens
3. Frontend includes JWT in Authorization header for API requests
4. Backend verifies JWT and extracts user ID for data isolation

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Verify your PostgreSQL connection string in the environment variables
2. **Authentication Issues**: Ensure Better Auth is properly configured with correct secrets
3. **API Communication Errors**: Check that the backend is running and the API URL is correctly configured in the frontend

### Getting Help

- Check the specifications in the `specs/` directory for detailed requirements
- Review the architecture plan in `specs/hackathon-todo-phase2/plan.md`
- Look at the data models in `specs/hackathon-todo-phase2/data-model.md`