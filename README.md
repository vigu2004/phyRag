# 📘 Physics Knowledge Base

A local, intelligent question-answering system built from 12th-grade Physics, Chemistry, and Biology textbooks. This application uses vector embeddings to store and retrieve semantically relevant content from multiple textbooks, allowing users to ask natural language questions and get precise, contextually matched textbook passages in return.

## 🚀 Features

- **Multi-Subject Search**: Query across Physics, Chemistry, and Biology textbooks simultaneously
- **Semantic Search**: Ask questions in natural language and get relevant textbook excerpts
- **Advanced Reranking**: Uses cross-encoder models for improved result relevance
- **Session Management**: Organize your research with multiple search sessions
- **Modern UI**: Beautiful, responsive interface with dark theme and gradient backgrounds
- **Real-time Search**: Instant results with loading states and smooth animations
- **Contextual Results**: Get precise textbook passages with source citations

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19 with modern hooks
- **Styling**: Tailwind CSS with custom components
- **UI Components**: Radix UI primitives with custom styling
- **Icons**: Lucide React for consistent iconography
- **Build Tool**: Create React App

### Backend
- **Vector Database**: ChromaDB for local vector storage
- **Embedding Model**: SentenceTransformers (all-MiniLM-L6-v2)
- **Reranking Model**: Cross-encoder/ms-marco-MiniLM-L-6-v2
- **PDF Processing**: PyMuPDF for text extraction
- **Python**: 3.8+ with virtual environment

## 📋 Prerequisites

- Node.js (version 16 or higher)
- Python 3.8 or higher
- npm or yarn package manager
- pip (Python package manager)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd RagPhytextbook
```

### 2. Setup Backend

```bash
# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
cd backend
pip install -r requirements.txt
```

### 3. Data Ingestion

```bash
# Make sure you're in the backend directory
python ingest.py
```

This will:
- Process PDF textbooks from the `data/` directory
- Extract text content and chunk by sections
- Generate embeddings using SentenceTransformers
- Store everything in ChromaDB vector database

### 4. Test the Vector Store

```bash
# Test the search functionality
python test.py
```

You can modify the query in `test.py` to test different questions.

### 5. Setup Frontend

```bash
cd ../react-frontend
npm install
```

### 6. Start the Development Server

```bash
npm start
```

The application will open in your browser at `http://localhost:3000`.

## 🎯 Usage

### Testing Vector Search
1. Navigate to the `backend/` directory
2. Edit the `query` variable in `test.py`
3. Run `python test.py` to see search results

### Frontend Interface
1. Type your question in the search bar
2. Press Enter or click the Search button
3. View relevant textbook excerpts with source citations

### Example Queries
- "What is Ohm's Law?"
- "Explain Newton's three laws"
- "What is wave-particle duality?"
- "Laboratory Test for Ketonic group"
- "How do electric and magnetic fields interact?"

### Session Management
- Use the sidebar to organize different research sessions
- Create new sessions for different topics
- Switch between sessions to maintain context

## 📁 Project Structure

```
RagPhytextbook/
├── backend/
│   ├── ingest.py           # Data ingestion script
│   ├── test.py             # Vector search test script
│   └── requirements.txt    # Python dependencies
├── data/
│   ├── phy.pdf            # Physics textbook
│   ├── chem.pdf           # Chemistry textbook
│   └── bio.pdf            # Biology textbook
├── chroma_db/             # Vector database storage
├── react-frontend/
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── ui/       # Reusable UI components
│   │   │   ├── PhysicsKnowledgeBase.jsx
│   │   │   └── SessionsSidebar.jsx
│   │   ├── lib/          # Utility functions
│   │   └── App.js        # Main application component
│   ├── package.json      # Dependencies and scripts
│   └── tailwind.config.js # Tailwind CSS configuration
└── README.md             # This file
```

## 🔧 Backend Implementation

### Data Processing Pipeline
1. **PDF Extraction**: Uses PyMuPDF to extract text from PDF textbooks
2. **Text Chunking**: Splits content by section numbers (e.g., 5.3, 11.1.2)
3. **Embedding Generation**: Creates vector embeddings using SentenceTransformers
4. **Vector Storage**: Stores embeddings and metadata in ChromaDB

### Search Architecture
1. **Query Embedding**: Converts user query to vector representation
2. **Semantic Search**: Retrieves top-k candidates from each subject collection
3. **Cross-Encoder Reranking**: Uses advanced reranking model for better relevance
4. **Result Ranking**: Combines and sorts results across all subjects

### Vector Database Schema
- **Collections**: Separate collections for physics, chemistry, and biology
- **Documents**: Textbook sections with full text content
- **Metadata**: Section titles and identifiers
- **Embeddings**: 384-dimensional vectors from all-MiniLM-L6-v2

## 🎨 UI Components

The application uses a modern, accessible design system:

- **Cards**: Display search results with proper hierarchy
- **Input Fields**: Styled search inputs with focus states
- **Buttons**: Consistent button styling with hover effects
- **Sidebar**: Collapsible session management panel
- **Dark Theme**: Purple gradient background with proper contrast

## 🔧 Development

### Backend Scripts

- `python ingest.py` - Process PDFs and populate vector database
- `python test.py` - Test vector search functionality

### Frontend Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run test suite
- `npm eject` - Eject from Create React App

### Code Style

The project follows modern patterns:
- **Backend**: Clean Python with proper error handling
- **Frontend**: Functional components with hooks
- **UI**: Custom components with Radix primitives
- **Styling**: Tailwind CSS for responsive design

## ✅ Current Status

The project is now fully functional with:

### Backend (✅ Complete)
- ✅ PDF text extraction and processing
- ✅ Multi-subject data ingestion (Physics, Chemistry, Biology)
- ✅ Vector database setup with ChromaDB
- ✅ Semantic search with SentenceTransformers
- ✅ Advanced reranking with Cross-Encoder
- ✅ Test script for querying the vector store

### Frontend (✅ Complete)
- ✅ Modern React application structure
- ✅ Responsive design with Tailwind CSS
- ✅ Session management interface
- ✅ Beautiful gradient UI design
- ✅ Mock search functionality

### Data (✅ Complete)
- ✅ Physics textbook processed and stored
- ✅ Chemistry textbook processed and stored
- ✅ Biology textbook processed and stored
- ✅ Vector embeddings generated and indexed

## 🔄 Next Steps

To complete the full system integration:

1. **API Integration**: Connect frontend to backend search API
2. **Real-time Search**: Implement live search functionality
3. **Result Display**: Show actual search results in the UI
4. **Error Handling**: Add proper error handling for search failures
5. **Performance Optimization**: Optimize search speed and result quality

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
- Vector search powered by SentenceTransformers and ChromaDB
- UI components inspired by modern design systems
- Multi-subject content based on 12th-grade curriculum standards

---

**Note**: The backend vector search system is fully functional and can be tested using the `test.py` script. The frontend is ready for integration with the backend API to create a complete intelligent question-answering system. 