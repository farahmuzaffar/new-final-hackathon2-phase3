// frontend/src/components/TaskList.tsx
'use client';

import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import TaskItem from './TaskItem';
import { taskApi } from '../lib/api';

interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface TaskListHandle {
  refreshTasks: () => void;
}

const TaskList = forwardRef<TaskListHandle>((_, ref) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch tasks when component mounts
  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskApi.getTasks();
      setTasks(response.data.tasks || []);
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Expose the refreshTasks function to parent components
  useImperativeHandle(ref, () => ({
    refreshTasks: fetchTasks
  }));

  if (loading) {
    return <div>Loading tasks...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="task-list">
      <h2>Your Tasks</h2>
      {tasks.length === 0 ? (
        <p>No tasks yet. Create your first task!</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              <TaskItem
                task={task}
                onTaskUpdated={fetchTasks}
                onTaskDeleted={fetchTasks}
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
});

TaskList.displayName = 'TaskList';

export default TaskList;