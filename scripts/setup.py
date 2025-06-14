import chromadb
from chromadb.utils import embedding_functions
import os

def initialize_vector_db():
    # Initialize with Gemini embeddings
    gemini_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key="your_api_key_here",  # Replace with your actual API key
        model_name="models/embedding-001"
    )
    
    client = chromadb.Client()
    collection = client.create_collection(
        name="altibbe_docs",
        embedding_function=gemini_ef
    )
    
    
    doc_path = os.path.join("data", "sample-documents", "altibbe_faqs.txt")
    with open(doc_path, "r", encoding="utf-8") as f:
        documents = [line.strip() for line in f if line.strip()]
    
    collection.add(
        documents=documents,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )
    
    print(f"Initialized DB with {len(documents)} documents")
    return collection

if __name__ == "__main__":
    initialize_vector_db()