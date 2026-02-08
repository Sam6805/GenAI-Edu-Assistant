"""
Vector Store Module
Manages FAISS vector store for document embeddings.
"""

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_vector_store(docs):
    """
    Create a FAISS vector store from documents.
    
    Args:
        docs (list): List of Document objects
        
    Returns:
        FAISS: Vector store instance
    """
    # Split documents into chunks for better retrieval
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)
    
    # Create embeddings using HuggingFace (free, no API key needed)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)


def search_vector_store(vector_store, query, k=4):
    """
    Search the vector store for relevant documents.
    
    Args:
        vector_store (FAISS): Vector store instance
        query (str): Search query
        k (int): Number of results to return
        
    Returns:
        list: List of relevant documents
    """
    return vector_store.similarity_search(query, k=k)
