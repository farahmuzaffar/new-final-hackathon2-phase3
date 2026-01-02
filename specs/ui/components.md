# UI Components Specification

## Overview

This specification outlines the high-level UI components for the Hackathon Todo Phase-2 application. The UI is built with Next.js using the App Router and TypeScript. The components are organized to support both authenticated and unauthenticated user experiences.

## Layout Components

### MainLayout
- Wrapper component for the entire application
- Contains header, main content area, and footer
- Handles responsive design across different screen sizes
- Conditionally renders authentication-specific elements

### AuthenticatedLayout
- Extends MainLayout for authenticated users
- Includes navigation sidebar with task management links
- Shows user profile information and logout button
- Provides consistent layout for all authenticated routes

### PublicLayout
- Extends MainLayout for public/unauthenticated routes
- Includes minimal navigation (e.g., login/signup links)
- Focuses on authentication flows and public information

## Authentication Components

### LoginForm
- Form with email and password fields
- Validation for required fields
- Error display for authentication failures
- Link to signup page
- "Forgot password" functionality (if implemented)

### SignupForm
- Form with email, password, and name fields
- Validation for required fields and password strength
- Error display for registration failures
- Link to login page

### AuthGuard
- Higher-order component that protects routes
- Redirects unauthenticated users to login
- Checks for valid authentication tokens
- Handles token refresh if needed

## Task Management Components

### TaskList
- Displays all tasks for the authenticated user
- Filters: All, Active, Completed
- Sorting options (by creation date, due date, etc.)
- Pagination for large numbers of tasks
- Empty state when no tasks exist
- Loading state during data fetch

### TaskItem
- Displays a single task with title and description
- Checkbox to toggle completion status
- Edit and delete buttons
- Visual indication of completion status
- Responsive design for different screen sizes

### TaskForm
- Form for creating or editing tasks
- Title input (required)
- Description textarea (optional)
- Submit and cancel buttons
- Validation for required fields
- Success/error feedback

### TaskActions
- Group of action buttons for a task
- Edit button
- Delete button with confirmation
- Toggle completion button

## Navigation Components

### Header
- Application logo/title
- Navigation links (conditional based on auth status)
- User profile dropdown (for authenticated users)
- Mobile menu toggle

### Sidebar
- Navigation menu for authenticated users
- Links to different sections (All Tasks, Active, Completed)
- User profile information
- Logout button

## User Profile Components

### UserProfile
- Displays user's name and email
- Account settings links
- Logout functionality
- Option to update profile (if implemented)

## Utility Components

### LoadingSpinner
- Visual indicator for loading states
- Used during API requests
- Accessible for screen readers

### ErrorMessage
- Displays error messages to the user
- Clear, actionable error messages
- Dismissible when appropriate

### ConfirmationDialog
- Modal dialog for confirming destructive actions
- Used for task deletion
- Clear action buttons (Confirm/Cancel)

## Page Components

### HomePage
- Landing page for unauthenticated users
- Overview of application features
- Call-to-action buttons (Sign up, Learn more)
- Links to login page

### DashboardPage
- Main page for authenticated users
- Shows user's task list
- Quick stats (total tasks, completed tasks, etc.)
- Call-to-action to create first task

### TaskDetailPage
- Detailed view of a single task
- Full task information
- Edit functionality
- Back to task list navigation

### AuthPages
- Login page containing LoginForm
- Signup page containing SignupForm
- Password reset page (if implemented)

## Responsive Behavior

### Mobile
- Collapsible navigation sidebar
- Stacked form elements
- Touch-friendly controls
- Optimized for thumb-based navigation

### Desktop
- Expanded sidebar navigation
- Multi-column layouts where appropriate
- Hover states for interactive elements
- Larger touch targets for precision

## Authentication State Handling

### Unauthenticated State
- Show login/signup forms
- Hide task management components
- Display public information only
- Redirect to login for protected routes

### Authenticated State
- Show task management components
- Display user-specific information
- Enable task creation and management
- Provide logout functionality

### Loading State
- Display loading indicators during auth checks
- Show skeleton screens during data loading
- Maintain layout structure during loading
- Handle transitions between states smoothly

## Component Interactions

### Task Creation Flow
1. User clicks "Add Task" button
2. TaskForm appears (either inline or in modal)
3. User fills in task details
4. Form validates input
5. Task is created and appears in TaskList

### Task Update Flow
1. User clicks edit button on TaskItem
2. TaskForm appears with existing task data
3. User modifies task details
4. Form validates input
5. Task is updated and reflects in TaskList

### Task Deletion Flow
1. User clicks delete button on TaskItem
2. ConfirmationDialog appears
3. User confirms deletion
4. Task is removed from database
5. Task disappears from TaskList

### Authentication Flow
1. User accesses application
2. AuthGuard checks authentication status
3. If unauthenticated, redirect to login
4. If authenticated, show DashboardPage
5. User can logout to return to public state