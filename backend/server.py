from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# === CONFIGURATION ===
CHROMA_PATH = "../chroma_db"
COLLECTIONS = ["physics_textbook", "chemistry_textbook", "biology_textbook"]

# === SETUP ===
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Search across all collections
        all_results = []
        
        for collection_name in COLLECTIONS:
            try:
                # Get the collection
                collection = client.get_collection(name=collection_name, embedding_function=embedding_fn)
                
                # Search for the most similar chunk from this collection
                results = collection.query(
                    query_texts=[query],
                    n_results=1,
                    include=['documents', 'metadatas', 'distances']
                )
                
                if results['documents'] and results['documents'][0]:
                    # Add collection info to metadata
                    metadata = results['metadatas'][0][0] if results['metadatas'] else {}
                    metadata['collection'] = collection_name
                    
                    all_results.append({
                        'text': results['documents'][0][0],
                        'metadata': metadata,
                        'distance': results['distances'][0][0] if results['distances'] else None,
                        'collection': collection_name
                    })
            except Exception as e:
                print(f"Error searching collection {collection_name}: {e}")
                continue
        
        if not all_results:
            return jsonify({'error': 'No results found in any collection'}), 404
        
        # Find the single most relevant result (lowest distance = highest relevance)
        best_result = min(all_results, key=lambda x: x['distance'] if x['distance'] is not None else float('inf'))
        
        return jsonify({
            'success': True,
            'result': {
                'text': best_result['text'],
                'metadata': best_result['metadata'],
                'distance': best_result['distance']
            },
            'query': query,
            'collection': best_result['collection'],
            'searched_collections': COLLECTIONS
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections', methods=['GET'])
def get_collections():
    """Get available collections"""
    return jsonify({
        'collections': COLLECTIONS
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

if __name__ == '__main__':
    print("Starting RAG Physics Textbook Server...")
    print(f"Available collections: {COLLECTIONS}")
    print("Server will search across ALL collections and return the top result")
    print("Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 