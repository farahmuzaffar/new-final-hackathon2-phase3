// frontend/src/components/UserProfile.tsx
'use client';

import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const UserProfile: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading profile...</div>;
  }

  if (!user) {
    return <div>Please log in to see your profile</div>;
  }

  return (
    <div className="user-profile">
      <h3>Welcome, {user.name || user.email}!</h3>
      <p>Email: {user.email}</p>
      {/* Additional profile information can be added here */}
    </div>
  );
};

export default UserProfile;