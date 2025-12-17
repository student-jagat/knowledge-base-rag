import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List

# Persist directory for FAISS
PERSIST_DIRECTORY = "./data/faiss_index"

def get_vector_store():
    """Initializes or loads the FAISS vector store."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(PERSIST_DIRECTORY):
        vector_store = FAISS.load_local(PERSIST_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
    else:
        # Create a dummy empty store if not exists (FAISS requires at least one text to init, handled by add_documents)
        # For simplicity, we return None and handle creation in add_documents, 
        # OR we just init with a dummy text and then add.
        # Better: just return the class or handle it.
        # Actually, FAISS.from_documents is the standard way.
        pass
    return None # We will load dynamically or create new

def add_documents_to_store(chunks: List[Document]):
    """Adds processed document chunks to the vector store."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.exists(PERSIST_DIRECTORY):
        vector_store = FAISS.load_local(PERSIST_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
    
    vector_store.save_local(PERSIST_DIRECTORY)

def query_vector_store(query: str, k: int = 4) -> List[Document]:
    """Retrieves top-k relevant documents for a query."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if not os.path.exists(PERSIST_DIRECTORY):
        return []
        
    vector_store = FAISS.load_local(PERSIST_DIRECTORY, embeddings, allow_dangerous_deserialization=True)
    results = vector_store.similarity_search(query, k=k)
    return results
