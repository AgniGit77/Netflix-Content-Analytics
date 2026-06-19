/**
 * App.jsx — Root Application Component
 *
 * Responsibilities:
 *  1. Wrap everything in AuthProvider so every child can access auth state.
 *  2. Conditionally render the Navbar (only when user is authenticated).
 *  3. Define all client-side routes using react-router-dom v6.
 *
 * Route map:
 *   /            → redirect to /dashboard
 *   /login       → LoginPage (public)
 *   /register    → RegisterPage (public)
 *   /dashboard   → DashboardPage (protected)
 *   /upload      → UploadPage (protected)
 *   /search      → SearchPage (protected)
 *   /documents   → DocumentsPage (protected)
 */

import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';

// Context
import { AuthProvider, useAuth } from './context/AuthContext';

// Components
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import UploadPage from './pages/UploadPage';
import SearchPage from './pages/SearchPage';
import DocumentsPage from './pages/DocumentsPage';

/**
 * Inner component that reads auth state to decide whether to show the Navbar.
 * We keep this separate so the useAuth hook lives inside <AuthProvider>.
 */
function AppContent() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  // Public routes where the Navbar should NOT appear
  const publicPaths = ['/login', '/register'];
  const showNavbar = isAuthenticated && !publicPaths.includes(location.pathname);

  return (
    <>
      {/* Render the top navigation bar on authenticated pages */}
      {showNavbar && <Navbar />}

      {/* Page content wrapper — adds top padding when Navbar is visible */}
      <main className={showNavbar ? 'main-content with-navbar' : 'main-content'}>
        <Routes>
          {/* Redirect root to dashboard */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Protected routes — wrapped in <ProtectedRoute> */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <UploadPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/search"
            element={
              <ProtectedRoute>
                <SearchPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/documents"
            element={
              <ProtectedRoute>
                <DocumentsPage />
              </ProtectedRoute>
            }
          />

          {/* Catch-all — send unknown routes to dashboard */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </>
  );
}

/**
 * App — the top-level component rendered by main.jsx.
 * Wraps the entire tree with AuthProvider for global auth state.
 */
export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
