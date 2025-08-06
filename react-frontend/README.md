# Physics, Chemistry & Biology RAG Interface

A modern, responsive chat interface built with React that provides a RAG (Retrieval-Augmented Generation) system for 12th grade Physics, Chemistry, and Biology textbooks.

## Features

- **Subject-Specific RAG**: Specialized for Physics, Chemistry, and Biology content
- **Clean, Modern UI**: Inspired by ChatGPT's design with a clean and intuitive interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Mode Support**: Built-in dark mode with smooth transitions
- **Real-time Chat**: Interactive chat interface with message history
- **Sidebar Navigation**: Collapsible sidebar with conversation management
- **Smooth Animations**: Loading states and smooth transitions throughout
- **Keyboard Shortcuts**: Enter to send messages, Shift+Enter for new lines

## Tech Stack

- **React 19**: Latest React with hooks and modern patterns
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Lucide React**: Beautiful, customizable icons
- **RAG System**: Retrieval-Augmented Generation for textbook content

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Project Structure

```
src/
├── components/
│   ├── ChatInterface.jsx    # Main chat area with messages and input
│   └── Sidebar.jsx         # Collapsible sidebar with conversations
├── App.js                  # Main app component
├── App.css                 # Global styles and animations
└── index.css              # Tailwind setup and base styles
```

## Features

### Chat Interface
- Message bubbles with different styles for user and assistant
- Auto-scrolling to latest messages
- Loading animations during AI responses
- Responsive textarea with auto-resize
- Send button with proper disabled states
- Subject-specific placeholder text

### Sidebar
- New study session button
- Conversation history with active states
- Delete conversation functionality
- Collapsible design for mobile
- User account and settings buttons

### Subject Coverage
- **Physics**: Mechanics, thermodynamics, electromagnetism, optics, modern physics
- **Chemistry**: Physical chemistry, organic chemistry, inorganic chemistry, analytical chemistry
- **Biology**: Cell biology, genetics, evolution, ecology, human physiology

### Responsive Design
- Mobile-first approach
- Collapsible sidebar on smaller screens
- Touch-friendly interface
- Proper spacing and typography

## Customization

The interface is built with Tailwind CSS, making it easy to customize colors, spacing, and other design elements. The main color scheme can be modified in the component classes.

## Future Enhancements

- Real RAG integration with textbook databases
- Subject-specific conversation filtering
- File upload support for study materials
- Voice input/output for accessibility
- Code syntax highlighting for formulas
- Markdown rendering for scientific notation
- Integration with learning management systems
