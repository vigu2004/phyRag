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
    
    # Test search endpoint - now searches all collections automatically
    print("\nTesting search endpoint (searches all collections)...")
    test_queries = [
        "What is Newton's first law?",
        "What is the chemical formula for water?",
        "What is photosynthesis?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = requests.post(
                f"{base_url}/api/search",
                json={"query": query}
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Result from: {data['collection']}")
                print(f"Text length: {len(data['result']['text'])}")
                print(f"Metadata: {data['result']['metadata']}")
                print(f"Distance: {data['result']['distance']}")
                print(f"Searched collections: {data['searched_collections']}")
            else:
                print(f"Error: {response.json()}")
        except Exception as e:
            print(f"Search failed: {e}")

if __name__ == "__main__":
    test_server() 