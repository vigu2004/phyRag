from flask import Flask, request, jsonify
from flask_cors import CORS
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import os

# Updated imports for lightweight seq2seq models and reranking
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from sentence_transformers import CrossEncoder

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# === CONFIGURATION ===
CHROMA_PATH = "../chroma_db"
COLLECTIONS = ["physics_textbook", "chemistry_textbook", "biology_textbook"]

# Model names (CPU-friendly)
REPHRASE_MODEL_NAME = "google/flan-t5-small"
ANSWER_PRIMARY_MODEL_NAME = "google/flan-t5-base"
ANSWER_FALLBACK_MODEL_NAME = "google/flan-t5-small"
RERANK_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# === SETUP ===
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

# Lazy-loaded globals
_t5_rephrase_tokenizer = None
_t5_rephrase_model = None
_t5_answer_tokenizer = None
_t5_answer_model = None
_reranker = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _ensure_rephrase_model_loaded():
	global _t5_rephrase_tokenizer, _t5_rephrase_model
	if _t5_rephrase_tokenizer is None or _t5_rephrase_model is None:
		_t5_rephrase_tokenizer = AutoTokenizer.from_pretrained(REPHRASE_MODEL_NAME)
		_t5_rephrase_model = AutoModelForSeq2SeqLM.from_pretrained(REPHRASE_MODEL_NAME)
		_t5_rephrase_model.to(_device)


def _ensure_answer_model_loaded():
	global _t5_answer_tokenizer, _t5_answer_model
	if _t5_answer_tokenizer is None or _t5_answer_model is None:
		try:
			_t5_answer_tokenizer = AutoTokenizer.from_pretrained(ANSWER_PRIMARY_MODEL_NAME)
			_t5_answer_model = AutoModelForSeq2SeqLM.from_pretrained(ANSWER_PRIMARY_MODEL_NAME)
		except Exception:
			_t5_answer_tokenizer = AutoTokenizer.from_pretrained(ANSWER_FALLBACK_MODEL_NAME)
			_t5_answer_model = AutoModelForSeq2SeqLM.from_pretrained(ANSWER_FALLBACK_MODEL_NAME)
		_t5_answer_model.to(_device)


def _ensure_reranker_loaded():
	global _reranker
	if _reranker is None:
		# Force CPU-safe default if CUDA not available
		_reranker = CrossEncoder(RERANK_MODEL_NAME, device=str(_device))


def _t5_generate(tokenizer, model, prompt, max_new_tokens=128):
	inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to(_device)
	with torch.no_grad():
		output_ids = model.generate(
			**inputs,
			max_new_tokens=max_new_tokens,
			temperature=0.2,
			do_sample=False
		)
	decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
	return decoded.strip()


def rephrase_query(original_query):
	"""Rephrase the query into a formal textbook-style question using FLAN-T5 small."""
	_ensure_rephrase_model_loaded()
	prompt = f"Rephrase the question to a concise, formal textbook-style question:\nQuestion: {original_query}\nRephrased:"
	rephrased = _t5_generate(_t5_rephrase_tokenizer, _t5_rephrase_model, prompt, max_new_tokens=64)
	return rephrased if rephrased else original_query


def build_answer(rephrased_query, top_docs):
	"""Generate an answer using the rephrased query and top supporting documents using FLAN-T5 (base or fallback to small)."""
	_ensure_answer_model_loaded()
	context_blocks = []
	for i, d in enumerate(top_docs, start=1):
		meta = d.get("metadata") or {}
		meta_str = " | ".join(f"{k}: {v}" for k, v in meta.items())
		context_blocks.append(
			f"[Source {i} | collection: {d.get('collection')} | page: {d.get('page')} | {meta_str}]\n{d.get('text')}"
		)
	context = "\n\n".join(context_blocks)
	prompt = (
    """
You are a domain-specific RAG assistant that only answers questions related to **Physics, Chemistry, or Biology**.
You must strictly use only the information available in the provided sources.

Rules:
1. **Domain Restriction:** Only answer questions relevant to Physics, Chemistry, or Biology. 
   - If the question is unrelated (e.g., personal, offensive, or outside these subjects), respond exactly with:
     "I can only answer questions related to Physics, Chemistry, or Biology."
2. **Source-Only Constraint:** Use only the provided sources. Do not use outside knowledge, assumptions, or speculation.
3. **Exhaustive Extraction:** If multiple relevant answers appear in the sources (e.g., a list, multiple names, or several points), include all of them.
4. **Exact Representation:** Present the answers exactly as they appear in the sources. Do not merge, paraphrase, or interpret.
5. **Formatting for Clarity:**
   - One answer → concise single line.
   - Multiple answers → bullet list or comma-separated list.
6. **Uncertainty Rule:** If the sources do not contain the answer, reply only with: "I am unsure."
7. **Safety Guard:** If the question contains inappropriate or unsafe content, respond with:
   "Please ask academic questions only."

Question: {rephrased_query}
Sources:
{context}
Answer:
"""
)

	answer = _t5_generate(_t5_answer_tokenizer, _t5_answer_model, prompt, max_new_tokens=256)
	return answer


@app.route('/api/search', methods=['POST'])
def search():
	try:
		data = request.get_json()
		query = data.get('query', '')
		
		if not query:
			return jsonify({'error': 'Query is required'}), 400
		
		# 1) Rephrase query (CPU-friendly)
		query_rephrased = rephrase_query(query)
		
		# 2) Retrieve from all collections (top-5 each)
		retrieved = []
		for collection_name in COLLECTIONS:
			try:
				collection = client.get_collection(name=collection_name, embedding_function=embedding_fn)
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
							'collection': collection_name,
							'distance': distance
						})
			except Exception as e:
				print(f"Error searching collection {collection_name}: {e}")
				continue
		
		if not retrieved:
			return jsonify({'error': 'No results found in any collection'}), 404
		
		# 3) Rerank all retrieved results against the rephrased query
		_ensure_reranker_loaded()
		pairs = [(query_rephrased, r['text']) for r in retrieved]
		scores = _reranker.predict(pairs)
		for r, s in zip(retrieved, scores):
			r['rerank_score'] = float(s)
		top_reranked = sorted(retrieved, key=lambda x: x['rerank_score'], reverse=True)[:3]
		
		# 4) Answer generation using rephrased query + top-3 documents
		answer = build_answer(query_rephrased, top_reranked)
		
		# 5) Build response
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
				}
				for r in top_reranked
			]
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
	print("Server will search across ALL collections, rerank results, and generate an answer")	
	print("Server will be available at: http://localhost:5000")
	app.run(debug=True, host='0.0.0.0', port=5000)	