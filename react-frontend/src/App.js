import React, { useState } from 'react';
import './App.css';
import ChatInterface from './components/ChatInterface';
import Sidebar from './components/Sidebar';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  return (
    <div className={`flex h-screen ${isDarkMode ? 'bg-[#18191A]' : 'bg-gray-50'}`}>
      <Sidebar isOpen={sidebarOpen} onToggle={toggleSidebar} isDarkMode={isDarkMode} />
      <div className="flex-1 flex flex-col">
        <ChatInterface sidebarOpen={sidebarOpen} onToggleSidebar={toggleSidebar} isDarkMode={isDarkMode} onToggleDarkMode={toggleDarkMode} />
      </div>
    </div>
  );
}

export default App;
