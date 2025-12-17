import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document

def load_document(file_path: str) -> List[Document]:
    """Loads a document from a file path (PDF or TXT)."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif ext == ".txt":
        loader = TextLoader(file_path)
        return loader.load()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def split_documents(documents: List[Document]) -> List[Document]:
    """Splits documents into smaller chunks for embedding."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def process_file(file_path: str):
    """Full processing pipeline: Load -> Split."""
    docs = load_document(file_path)
    chunks = split_documents(docs)
    return chunks
