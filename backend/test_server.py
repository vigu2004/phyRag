import requests
import json

def test_server():
    base_url = "http://localhost:5000"
    
    # Test health check
    print("Testing health check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test collections endpoint
    print("\nTesting collections endpoint...")
    try:
        response = requests.get(f"{base_url}/api/collections")
        print(f"Collections: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Collections failed: {e}")
        return
    
    # Test search endpoint with a sample query
    print("\nTesting search endpoint (RAG flow with rephrasing, reranking, answer gen)...")
    test_query = "Explain Laboratory Test for Aldehydes."
    print(f"\nQuery: {test_query}")
    try:
        response = requests.post(
            f"{base_url}/api/search",
            json={"query": test_query}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            # Print key fields from new response shape
            print("query_original:", data.get("query_original"))
            print("query_rephrased:", data.get("query_rephrased"))
            print("answer (first 300 chars):", (data.get("answer") or "")[:300] + ("..." if data.get("answer") and len(data.get("answer")) > 300 else ""))
            
            sources = data.get("sources") or []
            print(f"sources (top {len(sources)}):")
            for i, s in enumerate(sources, start=1):
                print(f"  [{i}] collection={s.get('collection')} page={s.get('page')} rerank_score={s.get('rerank_score')} distance={s.get('distance')}")
                text = s.get('text') or ""
                snippet = text[:200].replace("\n", " ") + ("..." if len(text) > 200 else "")
                print(f"      snippet: {snippet}")
        else:
            # Print error payload
            try:
                print(f"Error: {response.json()}")
            except Exception:
                print(f"Error body: {response.text}")
    except Exception as e:
        print(f"Search failed: {e}")

if __name__ == "__main__":
    test_server() 