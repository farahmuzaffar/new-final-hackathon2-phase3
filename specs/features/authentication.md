# Authentication Specification

## Signup and Login Flow using Better Auth

### Signup Process
**As a** new user
**I want to** create an account
**So that** I can use the todo application

**Flow:**
1. User navigates to the signup page
2. User enters email, password, and optional name
3. Frontend validates input fields
4. Frontend sends signup request to Better Auth
5. Better Auth creates user account and returns JWT
6. Frontend stores JWT in secure session/storage
7. User is redirected to the authenticated dashboard

### Login Process
**As a** returning user
**I want to** sign into my account
**So that** I can access my tasks

**Flow:**
1. User navigates to the login page
2. User enters email and password
3. Frontend validates input fields
4. Frontend sends login request to Better Auth
5. Better Auth validates credentials and returns JWT
6. Frontend stores JWT in secure session/storage
7. User is redirected to the authenticated dashboard

## JWT Issuance and Usage

### JWT Structure
- **Header**: Standard JWT header with algorithm information
- **Payload**: Contains user ID, email, and expiration time
- **Signature**: Signed by Better Auth with secure algorithm

### Token Storage
- JWTs are stored securely in the browser's session storage
- Tokens are included in the Authorization header for API requests
- Tokens are automatically refreshed before expiration

### Token Expiration
- JWTs have a defined expiration time (TTL)
- Frontend handles token refresh automatically
- User is redirected to login if token cannot be refreshed

## Frontend Responsibilities

### Authentication State Management
- Maintain authentication state across the application
- Redirect unauthenticated users to login page
- Display authenticated vs unauthenticated UI components
- Handle token refresh automatically

### API Request Handling
- Include JWT in Authorization header for protected endpoints
- Handle 401 responses by redirecting to login
- Manage logout when tokens become invalid

### UI Components
- Show login/signup forms to unauthenticated users
- Show task management interface to authenticated users
- Provide logout functionality
- Display user profile information

## Backend Token Verification Expectations

### Middleware Implementation
- All protected endpoints must verify JWT validity
- Extract user ID from JWT for data isolation
- Return 401 Unauthorized for invalid tokens
- Implement token refresh endpoints if needed

### Security Constraints
- JWTs must be verified using Better Auth's verification methods
- All database queries must be scoped to the authenticated user
- Sensitive operations require valid JWT
- Token expiration must be enforced strictly

## Security Constraints

### Password Requirements
- Minimum 8 characters
- At least one uppercase, one lowercase, and one number
- Secure hashing using industry-standard algorithms

### Session Management
- Secure token storage to prevent XSS attacks
- HTTP-only cookies where applicable
- Short-lived access tokens with refresh tokens
- Automatic logout after period of inactivity

### API Protection
- All endpoints require authentication unless explicitly public
- Rate limiting on authentication endpoints
- Input validation on all authentication-related fields
- Secure transmission of credentials over HTTPS only