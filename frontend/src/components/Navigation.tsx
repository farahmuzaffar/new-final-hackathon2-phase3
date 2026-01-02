// frontend/src/components/Navigation.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../contexts/AuthContext';
import LogoutButton from './LogoutButton';

const Navigation: React.FC = () => {
  const { user, loading } = useAuth();

  return (
    <nav className="navigation">
      <div className="nav-brand">
        <Link href="/">Todo App</Link>
      </div>
      
      <div className="nav-links">
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <>
            <Link href="/">Home</Link>
            <LogoutButton />
          </>
        ) : (
          <>
            <Link href="/login">Login</Link>
            <Link href="/signup">Sign Up</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navigation;