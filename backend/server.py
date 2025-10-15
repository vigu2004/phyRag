# ==============================
# RAG Flask Server using Fine-Tuned FLAN5
# ==============================

from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import CrossEncoder
import torch
import os

# ==============================
# CONFIGURATION
# ==============================
CHROMA_PATH = "../chroma_db"
FINETUNED_MODEL_PATH = "../finetuned_model/flan5-sft-full"

COLLECTIONS = ["physics_textbook", "chemistry_textbook", "biology_textbook"]

REPHRASE_MODEL_NAME = "google/flan-t5-small"  # CPU-friendly
RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ==============================
# DEVICE SETUP
# ==============================
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==============================
# Chroma client & embedding
# ==============================
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

# ==============================
# Lazy-loaded globals
# ==============================
_t5_rephrase_tokenizer = None
_t5_rephrase_model = None
_t5_answer_tokenizer = None
_t5_answer_model = None
_reranker = None

# ==============================
# MODEL LOADING FUNCTIONS
# ==============================
def _ensure_rephrase_model_loaded():
    global _t5_rephrase_tokenizer, _t5_rephrase_model
    if _t5_rephrase_tokenizer is None or _t5_rephrase_model is None:
        _t5_rephrase_tokenizer = AutoTokenizer.from_pretrained(REPHRASE_MODEL_NAME)
        _t5_rephrase_model = AutoModelForSeq2SeqLM.from_pretrained(REPHRASE_MODEL_NAME)
        _t5_rephrase_model.to(_device)

def _ensure_answer_model_loaded():
    global _t5_answer_tokenizer, _t5_answer_model
    if _t5_answer_tokenizer is None or _t5_answer_model is None:
        _t5_answer_tokenizer = AutoTokenizer.from_pretrained(FINETUNED_MODEL_PATH)
        _t5_answer_model = AutoModelForSeq2SeqLM.from_pretrained(FINETUNED_MODEL_PATH)
        _t5_answer_model.to(_device)

def _ensure_reranker_loaded():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANK_MODEL_NAME, device=str(_device))

# ==============================
# HELPER FUNCTIONS
# ==============================
def _t5_generate(tokenizer, model, prompt, max_new_tokens=2048):
    """
    Generate text using a FLAN-T5 model with sampling for richer answers.
    """
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(_device)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,        # sampling
            do_sample=True,         # enables multi-sentence output
            top_p=0.95,             # nucleus sampling
            repetition_penalty=1.2, # discourage repeating phrases
            num_beams=1
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()


def truncate_text(text, tokenizer, max_tokens=500):
    """
    Truncate a source to fit into the prompt without losing too much info.
    """
    ids = tokenizer.encode(text, truncation=True, max_length=max_tokens)
    return tokenizer.decode(ids, skip_special_tokens=True)


def rephrase_query(original_query):
    """
    Rephrase the query into a concise, formal textbook-style question.
    """
    _ensure_rephrase_model_loaded()
    prompt = f"Rephrase the question into a concise, formal textbook-style question:\nQuestion: {original_query}\nRephrased:"
    return _t5_generate(_t5_rephrase_tokenizer, _t5_rephrase_model, prompt, max_new_tokens=64) or original_query


def build_answer(rephrased_query, top_docs):
    """
    Generate a detailed answer using fine-tuned FLAN5 based on top documents.
    Automatically truncates long sources and labels them.
    """
    _ensure_answer_model_loaded()

    context_blocks = []
    for i, d in enumerate(top_docs, start=1):
        meta = d.get("metadata") or {}
        meta_str = " | ".join(f"{k}: {v}" for k, v in meta.items())
        truncated_text = truncate_text(d.get("text", ""), _t5_answer_tokenizer, max_tokens=500)
        block = f"Source {i} | Collection: {d.get('collection')} | Page: {d.get('page')} | {meta_str}\n{truncated_text}"
        context_blocks.append(block)

    context = "\n\n".join(context_blocks)

    prompt = f"""
		You are a domain-specific RAG assistant for Physics, Chemistry, or Biology.

		Rules:
		1. Only answer from the sources provided.
		2. List each unique test, method, or point only once.
		3. Do not repeat information.
		4. Use bullet points for multiple items.
		5. If unsure, reply: "I am unsure."

		Question: {rephrased_query}
		Sources:
		{context}
		Answer:
		"""


    return _t5_generate(_t5_answer_tokenizer, _t5_answer_model, prompt)

# ==============================
# FLASK APP
# ==============================
app = Flask(__name__)
CORS(app)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # 1️⃣ Rephrase
        query_rephrased = rephrase_query(query)

        # 2️⃣ Retrieve
        retrieved = []
        for coll_name in COLLECTIONS:
            try:
                collection = client.get_collection(name=coll_name, embedding_function=embedding_fn)
                results = collection.query(
                    query_texts=[query_rephrased],
                    n_results=5,
                    include=['documents', 'metadatas', 'distances']
                )
                if results and results.get('documents') and results['documents'][0]:
                    for idx, text in enumerate(results['documents'][0]):
                        metadata = (results.get('metadatas') or [[{}]])[0][idx] or {}
                        page = metadata.get('page') if isinstance(metadata, dict) else None
                        distance = (results.get('distances') or [[None]])[0][idx]
                        retrieved.append({
                            'text': text,
                            'metadata': metadata,
                            'page': page,
                            'collection': coll_name,
                            'distance': distance
                        })
            except Exception as e:
                print(f"Error searching collection {coll_name}: {e}")
                continue

        if not retrieved:
            return jsonify({'error': 'No results found in any collection'}), 404

        # 3️⃣ Rerank
        _ensure_reranker_loaded()
        pairs = [(query_rephrased, r['text']) for r in retrieved]
        scores = _reranker.predict(pairs)
        for r, s in zip(retrieved, scores):
            r['rerank_score'] = float(s)
        top_reranked = sorted(retrieved, key=lambda x: x['rerank_score'], reverse=True)[:3]

        # 4️⃣ Generate answer
        answer = build_answer(query_rephrased, top_reranked)

        return jsonify({
            'success': True,
            'query_original': query,
            'query_rephrased': query_rephrased,
            'answer': answer,
            'sources': [
                {
                    'text': r['text'],
                    'metadata': r.get('metadata'),
                    'page': r.get('page'),
                    'collection': r.get('collection'),
                    'distance': r.get('distance'),
                    'rerank_score': r.get('rerank_score')
                } for r in top_reranked
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/collections', methods=['GET'])
def get_collections():
    return jsonify({'collections': COLLECTIONS})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

# ==============================
# START SERVER
# ==============================
if __name__ == '__main__':
    print("Starting RAG Physics Textbook Server...")
    print(f"Collections: {COLLECTIONS}")
    print(f"Using fine-tuned model from: {FINETUNED_MODEL_PATH}")
    print(f"Device: {_device}")
    app.run(debug=True, host='0.0.0.0', port=5000)
