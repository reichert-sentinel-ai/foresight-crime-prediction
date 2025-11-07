import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 dark:bg-[#0f0f0f] flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#1f1f1f] p-6 rounded-lg shadow-lg max-w-md">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-[#e5e5e5] mb-4">Something went wrong</h1>
            <p className="text-gray-600 dark:text-[#a0a0a0] mb-4">
              {this.state.error?.message || 'An error occurred'}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Reload Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;

