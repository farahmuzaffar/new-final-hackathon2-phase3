// frontend/src/app/page.tsx
'use client';

import React, { useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ProtectedRoute from '../components/ProtectedRoute';
import TaskForm from '../components/TaskForm';
import TaskList, { TaskListHandle } from '../components/TaskList';
import UserProfile from '../components/UserProfile';

const HomePage: React.FC = () => {
  const { user, loading } = useAuth();
  const taskListRef = useRef<TaskListHandle>(null);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <ProtectedRoute>
      <div className="home-page">
        <h1>Todo Dashboard</h1>

        <UserProfile />

        <div className="content-section">
          <div className="task-section">
            <TaskForm onTaskCreated={() => {
              // Refresh the task list after creating a new task
              taskListRef.current?.refreshTasks();
            }} />
            <TaskList ref={taskListRef} />
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default HomePage;