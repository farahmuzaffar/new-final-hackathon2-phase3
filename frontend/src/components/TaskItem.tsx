// frontend/src/components/TaskItem.tsx
'use client';

import React, { useState } from 'react';
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

interface TaskItemProps {
  task: Task;
  onTaskUpdated: () => void;
  onTaskDeleted: () => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdated, onTaskDeleted }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggleCompletion = async () => {
    try {
      await taskApi.toggleTask(task.id);
      onTaskUpdated(); // Refresh the task list
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error toggling task:', err);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskApi.deleteTask(task.id);
        onTaskDeleted(); // Refresh the task list
      } catch (err) {
        setError('Failed to delete task. Please try again.');
        console.error('Error deleting task:', err);
      }
    }
  };

  const handleUpdate = async () => {
    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await taskApi.updateTask(task.id, { title, description });
      setIsEditing(false);
      onTaskUpdated(); // Refresh the task list
    } catch (err) {
      setError('Failed to update task. Please try again.');
      console.error('Error updating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setTitle(task.title);
    setDescription(task.description);
  };

  return (
    <div className={`task-item ${task.completed ? 'completed' : ''}`}>
      {isEditing ? (
        <div className="edit-form">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
            required
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Task description"
          />
          {error && <div className="error-message">{error}</div>}
          <div className="button-group">
            <button onClick={handleUpdate} disabled={loading}>
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button onClick={handleCancelEdit} disabled={loading}>
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="task-content">
          <div className="task-header">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              className="completion-checkbox"
            />
            <h3 className={task.completed ? 'completed-title' : ''}>{task.title}</h3>
          </div>
          
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          
          <div className="task-actions">
            <button onClick={() => setIsEditing(true)}>Edit</button>
            <button onClick={handleDelete}>Delete</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskItem;