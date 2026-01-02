// frontend/src/app/layout.tsx
import './globals.css';
import { AuthProvider } from '../contexts/AuthContext';
import Navigation from '../components/Navigation';

export const metadata = {
  title: 'Hackathon Todo App',
  description: 'A todo application for Hackathon Phase-2',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <Navigation />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}