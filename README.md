# 📘 Physics Knowledge Base

A local, intelligent question-answering system built from a 12th-grade Physics textbook. This application uses vector embeddings to store and retrieve semantically relevant content from the textbook, allowing users to ask natural language questions and get precise, contextually matched textbook passages in return.

## 🚀 Features

- **Semantic Search**: Ask questions in natural language and get relevant textbook excerpts
- **Session Management**: Organize your research with multiple search sessions
- **Modern UI**: Beautiful, responsive interface with dark theme and gradient backgrounds
- **Real-time Search**: Instant results with loading states and smooth animations
- **Contextual Results**: Get precise textbook passages with source citations

## 🛠️ Technology Stack

- **Frontend**: React 19 with modern hooks
- **Styling**: Tailwind CSS with custom components
- **UI Components**: Radix UI primitives with custom styling
- **Icons**: Lucide React for consistent iconography
- **Build Tool**: Create React App

## 📋 Prerequisites

- Node.js (version 16 or higher)
- npm or yarn package manager

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RagPhytextbook
```

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Start the Development Server

```bash
npm start
```

The application will open in your browser at `http://localhost:3000`.

## 🎯 Usage

### Basic Search
1. Type your physics question in the search bar
2. Press Enter or click the Search button
3. View relevant textbook excerpts with source citations

### Example Queries
- "What is Ohm's Law?"
- "Explain Newton's three laws"
- "What is wave-particle duality?"
- "How do electric and magnetic fields interact?"

### Session Management
- Use the sidebar to organize different research sessions
- Create new sessions for different topics
- Switch between sessions to maintain context

## 📁 Project Structure

```
RagPhytextbook/
├── frontend/
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ui/            # Reusable UI components
│   │   │   ├── PhysicsKnowledgeBase.jsx
│   │   │   └── SessionsSidebar.jsx
│   │   ├── lib/               # Utility functions
│   │   └── App.js             # Main application component
│   ├── package.json           # Dependencies and scripts
│   └── tailwind.config.js     # Tailwind CSS configuration
└── README.md                  # This file
```

## 🎨 UI Components

The application uses a modern, accessible design system:

- **Cards**: Display search results with proper hierarchy
- **Input Fields**: Styled search inputs with focus states
- **Buttons**: Consistent button styling with hover effects
- **Sidebar**: Collapsible session management panel
- **Dark Theme**: Purple gradient background with proper contrast

## 🔧 Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run test suite
- `npm eject` - Eject from Create React App

### Code Style

The project follows modern React patterns:
- Functional components with hooks
- Custom UI components with Radix primitives
- Tailwind CSS for styling
- Proper TypeScript-like prop handling

## 🚧 Current Status

This is a frontend prototype demonstrating the UI and user experience. The current implementation includes:

- ✅ Modern React application structure
- ✅ Responsive design with Tailwind CSS
- ✅ Session management interface
- ✅ Mock search functionality
- ✅ Beautiful gradient UI design

### Next Steps

To complete the full system, you'll need to implement:

1. **Backend API**: Vector database integration
2. **Text Processing**: Textbook content parsing and embedding
3. **Search Engine**: Semantic search implementation
4. **Data Storage**: Vector database setup (e.g., Pinecone, Weaviate, or local ChromaDB)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with React and modern web technologies
- UI components inspired by modern design systems
- Physics content based on 12th-grade curriculum standards

---

**Note**: This is a prototype demonstrating the frontend interface. The vector embedding and semantic search functionality will need to be implemented to create a fully functional intelligent question-answering system. 