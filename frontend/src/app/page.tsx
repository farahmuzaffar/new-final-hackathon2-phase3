'use client';

import LogoutButton from '@/components/LogoutButton';
import TaskForm from '@/components/TaskForm';
import TaskList from '@/components/TaskList';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-100 p-6">
      <div className="max-w-4xl mx-auto space-y-6">

        {/* Header */}
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-semibold text-slate-800">
            My Tasks
          </h1>
          <LogoutButton />
        </div>

        {/* Add / Update Task */}
        <TaskForm />

        {/* Task List */}
        <TaskList />
      </div>
    </div>
  );
}
