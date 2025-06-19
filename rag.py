import chromadb
from chromadb.utils import embedding_functions
import os

# For demo: In-memory Chroma (use persistent for prod)
chroma_client = chromadb.Client()
# Use Groq-supported open models for embedding (e.g., "nomic-embed-text-v1")
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = chroma_client.create_collection(name="pm_context", embedding_function=embedding_func)

def add_context(texts: list[str]):
    for t in texts:
        collection.add(
            documents=[t], ids=[str(hash(t))]
        )

def retrieve_context(query_items: list[str]) -> str:
    results = []
    for item in query_items:
        res = collection.query(query_texts=[item], n_results=2)
        for doc in res["documents"][0]:
            results.append(doc)
    return "\n".join(results)