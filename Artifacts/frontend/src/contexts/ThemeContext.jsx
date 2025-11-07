import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    try {
      // Check localStorage first, then system preference
      if (typeof window !== 'undefined') {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) return savedTheme;
        
        // Check system preference
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          return 'dark';
        }
      }
    } catch (e) {
      // If localStorage fails, default to dark
      console.warn('Theme initialization failed:', e);
    }
    return 'dark';
  });

  useEffect(() => {
    try {
      const root = document.documentElement;
      const body = document.body;
      
      if (theme === 'dark') {
        root.classList.add('dark');
        body.classList.add('dark');
        // Set CSS variables for dark theme
        root.style.setProperty('--app-bg', '#0f0f0f');
        root.style.setProperty('--nav-bg', '#1a1a1a');
        // Force dark theme on body as well
        body.style.backgroundColor = '#0f0f0f';
        body.style.color = '#e5e5e5';
      } else {
        root.classList.remove('dark');
        body.classList.remove('dark');
        // Set CSS variables for light theme
        root.style.setProperty('--app-bg', '#f9fafb');
        root.style.setProperty('--nav-bg', '#ffffff');
        // Force light theme on body
        body.style.backgroundColor = '#f9fafb';
        body.style.color = '#111827';
      }
      
      if (typeof window !== 'undefined') {
        localStorage.setItem('theme', theme);
      }
    } catch (e) {
      console.warn('Theme update failed:', e);
    }
  }, [theme]);

  const toggleTheme = React.useCallback(() => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

