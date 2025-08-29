# RAG Physics Textbook System

A Retrieval-Augmented Generation (RAG) system that allows users to query physics, chemistry, and biology textbooks using natural language. The system automatically searches across all subjects and retrieves the most relevant text chunk from any of the textbooks.

## Features

- **Multi-Subject Search**: Automatically searches across Physics, Chemistry, and Biology textbooks
- **Vector Database**: Uses ChromaDB to store and search through textbook content
- **Semantic Search**: Employs sentence transformers for intelligent text retrieval
- **Web Interface**: Modern React frontend with dark/light mode
- **Smart Result Selection**: Returns the single most relevant chunk from all subjects combined
- **Real-time Search**: Get instant responses from your textbook content

## Project Structure

```
RagPhytextbook/
├── backend/                 # Python backend server
│   ├── ingest.py           # Script to ingest PDFs into ChromaDB
│   ├── server.py           # Flask server for handling queries
│   ├── test_server.py      # Test script for the server
│   └── requirements.txt    # Python dependencies
├── chroma_db/              # Vector database storage
├── data/                   # PDF textbooks
│   ├── phy.pdf            # Physics textbook
│   ├── chem.pdf           # Chemistry textbook
│   └── bio.pdf            # Biology textbook
└── react-frontend/         # React web application
    ├── src/
    │   ├── components/
    │   │   ├── ChatInterface.jsx  # Main chat interface
    │   │   └── Sidebar.jsx        # Navigation sidebar
    │   └── App.js                 # Main application
    └── package.json
```

## Setup Instructions

### 1. Backend Setup

First, set up the Python backend:

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Ingest PDFs into ChromaDB (only needed once)
python ingest.py

# Start the Flask server
python server.py
```

The server will start on `http://localhost:5000`

### 2. Frontend Setup

In a new terminal, set up the React frontend:

```bash
cd react-frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Testing the System

You can test the backend server using the provided test script:

```bash
cd backend
python test_server.py
```

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/collections` - Get available textbook collections
- `POST /api/search` - Search for relevant text chunks across all collections

### Search API Usage

```json
POST /api/search
{
    "query": "What is Newton's first law?"
}
```

**Note**: No need to specify a collection - the server automatically searches all subjects!

Response:
```json
{
    "success": true,
    "result": {
        "text": "Retrieved text chunk...",
        "metadata": {"title": "Section title"},
        "distance": 0.123
    },
    "query": "What is Newton's first law?",
    "collection": "physics_textbook",
    "searched_collections": ["physics_textbook", "chemistry_textbook", "biology_textbook"]
}
```

## How It Works

1. **Ingestion**: PDFs are processed and chunked by sections, then embedded and stored in ChromaDB
2. **Query Processing**: User queries are converted to embeddings and compared against stored chunks
3. **Multi-Collection Search**: The server searches across ALL three subject collections simultaneously
4. **Smart Selection**: The single most relevant chunk (lowest distance) from any subject is selected
5. **Display**: Results are shown in the web interface with metadata, source subject, and relevance scores

## Key Benefits

- **No Subject Selection Needed**: Users can ask questions without knowing which subject they belong to
- **Best Match Guaranteed**: Always gets the most relevant result from any subject
- **Seamless Experience**: Single search interface that covers all subjects
- **Intelligent Routing**: Automatically routes questions to the most appropriate textbook

## Customization

- **Add New Books**: Place PDFs in the `data/` folder and update `BOOKS` in `ingest.py`
- **Change Embedding Model**: Modify the model in `ingest.py` and `server.py`
- **Adjust Chunking**: Modify the `chunk_by_section` function in `ingest.py`

## Troubleshooting

- **Server Connection Error**: Ensure the Flask server is running on port 5000
- **No Results**: Check that PDFs were properly ingested using `python ingest.py`
- **CORS Issues**: The server includes CORS headers, but ensure your frontend is on the correct port

## Dependencies

### Backend
- Flask - Web framework
- ChromaDB - Vector database
- Sentence Transformers - Text embeddings
- PyMuPDF - PDF processing

### Frontend
- React - UI framework
- Tailwind CSS - Styling
- Lucide React - Icons 