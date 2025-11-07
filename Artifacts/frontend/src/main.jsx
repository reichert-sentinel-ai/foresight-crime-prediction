import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import ErrorBoundary from './components/ErrorBoundary.jsx'
import './index.css'

// Ensure DOM is ready
const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Root element not found');
}

// Pre-enable dark theme to avoid initial flash
if (typeof document !== 'undefined') {
  const root = document.documentElement;
  root.classList.add('dark');
  document.body.classList.add('dark');
  document.body.style.backgroundColor = '#0f0f0f';
  document.body.style.color = '#e5e5e5';
}

try {
  ReactDOM.createRoot(rootElement).render(
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  );
} catch (error) {
  console.error('Failed to render app:', error);
  rootElement.innerHTML = `
    <div style="padding: 20px; font-family: sans-serif;">
      <h1>Failed to Load</h1>
      <p>Error: ${error.message}</p>
      <button onclick="window.location.reload()">Reload Page</button>
    </div>
  `;
}
