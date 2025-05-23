import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Optional

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB client (persistent local DB)
client = chromadb.PersistentClient(path="./chroma", settings=Settings(allow_reset=True))

# Create or get the collection for memory
collection = client.get_or_create_collection(name="nava_memory")

def embed_text(text: str) -> List[float]:
    """Convert text into embedding vector using SentenceTransformer."""
    return embedding_model.encode(text).tolist()

def add_memory(id: str, content: str, metadata: Optional[dict] = None):
    """Store a text memory in ChromaDB with optional metadata."""
    embedding = embed_text(content)
    collection.add(
        documents=[content],
        ids=[id],
        metadatas=[metadata or {}],
        embeddings=[embedding]
    )

def query_memory(query: str, n_results: int = 3):
    """Search for top-N most similar past memories."""
    return collection.query(
        query_texts=[query],
        n_results=n_results
    )

def wipe_memory():
    """Clear all documents from the collection."""
    client.delete_collection("nava_memory")