/**
 * main.jsx — Application Entry Point
 *
 * Wraps the entire app with:
 *  - BrowserRouter   → enables client-side routing
 *  - ToastContainer  → renders toast notifications anywhere in the tree
 *
 * We import App.css here so every component inherits the global styles.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import App from './App';
import './App.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      {/* Main application component */}
      <App />

      {/* Global toast notification container — dark-themed to match the UI */}
      <ToastContainer
        position="top-right"
        autoClose={4000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="dark"
        toastStyle={{
          backgroundColor: 'rgba(15, 15, 35, 0.95)',
          backdropFilter: 'blur(12px)',
          border: '1px solid rgba(255,255,255,0.08)',
          borderRadius: '12px',
          fontFamily: "'Inter', sans-serif",
        }}
      />
    </BrowserRouter>
  </React.StrictMode>
);
