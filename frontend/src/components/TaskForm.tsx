'use client';

import { useState } from 'react';
import { taskApi } from '@/lib/api';

export default function TaskForm() {
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) return;

    setLoading(true);
    setError('');

    try {
      await taskApi.createTask({
        title,
      });

      setTitle('');
      window.location.reload(); // simple refresh
    } catch (err) {
      setError('Failed to add task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow p-4 space-y-3"
    >
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Add a new task..."
        className="w-full px-4 py-3 rounded-lg border border-slate-300 
        focus:ring-2 focus:ring-indigo-500 outline-none"
      />

      {error && <p className="text-sm text-red-600">{error}</p>}

      <button
        type="submit"
        disabled={loading}
        className="w-full py-2 rounded-lg bg-indigo-600 text-white 
        hover:bg-indigo-700 transition"
      >
        {loading ? 'Adding...' : 'Add Task'}
      </button>
    </form>
  );
}
