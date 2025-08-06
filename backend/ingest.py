import os
import fitz  # PyMuPDF
import re
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

# === CONFIGURATION ===
BOOKS = {
    "physics_textbook": "../data/phy.pdf",
    "chemistry_textbook": "../data/chem.pdf",
    "biology_textbook": "../data/bio.pdf",
}

CHROMA_PATH = "../chroma_db"
SKIP_FIRST_N_PAGES = 10
SECTION_REGEX = r"\n?(\d{1,2}(?:\.\d{1,2}){1,2})\s+([^\n]+)"  #  5.3 or 11.1.2 Title

# === SETUP ===
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

def extract_text(doc):
    full_text = ""
    for i in range(len(doc)):
        if i > SKIP_FIRST_N_PAGES:
            text = doc[i].get_text()
            full_text += f"\n--- PAGE {i} ---\n{text}"
    return full_text

def chunk_by_section(text):
    matches = list(re.finditer(SECTION_REGEX, text))
    chunks = []

    for i, match in enumerate(matches):
        section_num = match.group(1)
        title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_text = text[start:end].strip()

        if len(section_text) > 50:
            chunks.append({
                "id": f"sec_{section_num.replace('.', '_')}",
                "title": f"{section_num} {title}",
                "text": section_text
            })
    return chunks

# === MAIN INGESTION ===
for collection_name, pdf_path in BOOKS.items():
    print(f"\n Processing: {collection_name} from {pdf_path}")

    doc = fitz.open(pdf_path)
    text = extract_text(doc)
    sections = chunk_by_section(text)
    print(f" Found {len(sections)} section chunks")

    collection = client.get_or_create_collection(name=collection_name, embedding_function=embedding_fn)

    for chunk in sections:
        try:
            collection.add(
                documents=[chunk["text"]],
                ids=[chunk["id"]],
                metadatas=[{"title": chunk["title"]}]
            )
        except Exception as e:
            print(f"Failed to add chunk {chunk['id']}: {e}")

    print(f"Ingested {len(sections)} chunks into '{collection_name}'")

print("\n All books ingested into ChromaDB!")
