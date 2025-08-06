import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Moon, Sun } from 'lucide-react';

const ThemeToggle = () => {
    const { isDark, toggleTheme } = useTheme();

    return (
        <button
            onClick={toggleTheme}
            className={`fixed top-4 right-4 z-50 p-3 rounded-full backdrop-blur-sm border transition-all duration-200 shadow-lg hover:shadow-xl ${isDark
                    ? 'bg-white/10 border-white/20 hover:bg-white/20'
                    : 'bg-white/80 border-gray-300 hover:bg-white/90'
                }`}
            aria-label={isDark ? 'Switch to light theme' : 'Switch to dark theme'}
        >
            {isDark ? (
                <Sun className="w-5 h-5 text-yellow-400" />
            ) : (
                <Moon className="w-5 h-5 text-gray-700" />
            )}
        </button>
    );
};

export default ThemeToggle; 