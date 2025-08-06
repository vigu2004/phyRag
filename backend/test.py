from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer, CrossEncoder

# === Load models ===
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# === Connect to ChromaDB ===
client = PersistentClient(path="../chroma_db")

# === Subject collections ===
collection_names = ["physics_textbook", "chemistry_textbook", "biology_textbook"]

# === Input query ===
query = "Laboratory Test for Ketonic group" #"Dual Nature of Light" #"Laboratory Test for Ketonic group"
print(f"\n Embedding query: '{query}'")
query_embedding = embedding_model.encode(query).tolist()

# === Retrieve top-k per subject ===
all_candidates = []

for name in collection_names:
    print(f"Searching in collection: {name}")
    try:
        collection = client.get_collection(name=name)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5  # broader for reranking
        )

        for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
            all_candidates.append({
                "collection": name,
                "document": doc,
                "metadata": metadata
            })

    except Exception as e:
        print(f"Error in collection '{name}': {e}")

# === Apply reranking ===
if not all_candidates:
    print("No results found.")
    exit(0)

print("\n Reranking results...")
rerank_inputs = [(query, candidate["document"]) for candidate in all_candidates]
scores = reranker.predict(rerank_inputs)

# Attach scores and sort
for i in range(len(all_candidates)):
    all_candidates[i]["score"] = scores[i]

top_results = sorted(all_candidates, key=lambda x: x["score"], reverse=True)[:3]

# === Print final sorted results ===
print(f"\n Top {len(top_results)} results across subjects for: '{query}'")
for i, result in enumerate(top_results):
    print(f"\n Result {i+1} (from {result['collection']}, section: {result['metadata'].get('title', 'Unknown')}):")
    print(result["document"])
