import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ThemeProvider } from './contexts/ThemeContext';
import ThemeToggle from './components/ThemeToggle';
import CrimeHeatmap from './components/CrimeHeatmap';
import TemporalPatterns from './components/TemporalPatterns';
import BiasAnalysisDashboard from './components/BiasAnalysisDashboard';
import PredictionExplainer from './components/PredictionExplainer';
import ThreatTimeline from './components/ThreatTimeline';

function App() {
  return (
    <ThemeProvider>
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <div className="min-h-screen bg-gray-50 dark:bg-[#0f0f0f] transition-colors" style={{ backgroundColor: 'var(--app-bg, #f9fafb)' }}>
          <nav className="bg-white dark:bg-[#1a1a1a] shadow-sm border-b border-gray-200 dark:border-[#2a2a2a]" style={{ backgroundColor: 'var(--nav-bg, #ffffff)' }}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex">
                  <div className="flex-shrink-0 flex items-center">
                    <h1 className="text-xl font-bold text-gray-900 dark:text-[#e5e5e5]">
                      🗺️ Foresight
                    </h1>
                  </div>
                  <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                    <Link
                      to="/crime-map"
                      className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                    >
                      Crime Heatmap
                    </Link>
                    <Link
                      to="/temporal-patterns"
                      className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                    >
                      Temporal Patterns
                    </Link>
                    <Link
                      to="/bias-analysis"
                      className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                    >
                      Bias Analysis
                    </Link>
                    <Link
                      to="/explainability"
                      className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                    >
                      Explainability
                    </Link>
                    <Link
                      to="/threat-timeline"
                      className="border-transparent text-gray-500 dark:text-[#a0a0a0] hover:border-gray-300 dark:hover:border-[#2a2a2a] hover:text-gray-700 dark:hover:text-[#e5e5e5] inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors"
                    >
                      Threat Timeline
                    </Link>
                  </div>
                </div>
                <div className="flex items-center">
                  <ThemeToggle />
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8 bg-transparent text-gray-900 dark:text-[#e5e5e5]">
            <Routes>
              <Route path="/" element={
                <div className="px-4 py-8">
                  <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-[#e5e5e5]">Welcome to Foresight</h2>
                  <p className="text-gray-600 dark:text-[#a0a0a0] mb-4">
                    Predictive crime intelligence platform with geospatial analytics.
                  </p>
                  <Link
                    to="/crime-map"
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 transition-colors"
                  >
                    View Crime Heatmap
                  </Link>
                </div>
              } />
              <Route path="/crime-map" element={<CrimeHeatmap />} />
              <Route path="/temporal-patterns" element={<TemporalPatterns />} />
              <Route path="/bias-analysis" element={<BiasAnalysisDashboard />} />
              <Route path="/explainability" element={<PredictionExplainer />} />
              <Route path="/threat-timeline" element={<ThreatTimeline />} />
            </Routes>
          </main>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
