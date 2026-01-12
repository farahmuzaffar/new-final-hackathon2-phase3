'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email.trim(),
          password: password.trim(),
        }),
      });

      if (!res.ok) {
        throw new Error('Invalid email or password');
      }

      const data = await res.json();

      // ✅ CORRECT WAY (fetch → data)
      localStorage.setItem('access_token', data.access_token);

      // ✅ dashboard route (change if needed)
      router.push('/');
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid grid-cols-1 md:grid-cols-2">

      {/* LEFT SIDE */}
      <div className="hidden md:flex flex-col justify-center px-16 
        bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 text-white">
        <h1 className="text-4xl font-bold mb-4">
          Task Manager ✨
        </h1>
        <p className="text-lg text-white/80 leading-relaxed">
          Organize your work.<br />
          Stay productive.<br />
          Manage tasks beautifully.
        </p>
      </div>

      {/* RIGHT SIDE */}
      <div className="flex items-center justify-center bg-slate-50 px-6">
        <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">

          <h2 className="text-2xl font-semibold text-slate-800">
            Welcome back
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            Login to your account
          </p>

          {error && (
            <div className="mt-4 bg-red-50 border border-red-200 
              text-red-600 text-sm p-2 rounded-lg">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-6 space-y-4">

            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-lg border border-slate-300 
                focus:ring-2 focus:ring-indigo-500 outline-none"
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 rounded-lg border border-slate-300 
                focus:ring-2 focus:ring-indigo-500 outline-none"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg bg-indigo-600 text-white 
                font-medium hover:bg-indigo-700 transition"
            >
              {loading ? 'Signing in...' : 'Login'}
            </button>
          </form>

          <p className="text-sm text-slate-500 text-center mt-6">
            Don’t have an account?{' '}
            <a
              href="/signup"
              className="text-indigo-600 font-medium hover:underline"
            >
              Sign up
            </a>
          </p>

        </div>
      </div>
    </div>
  );
}
