"""
PDF Loader Module
Handles loading and processing PDF files into LangChain documents.
"""

from langchain_community.document_loaders import PyPDFLoader


def load_pdf(file_path):
    """
    Load a PDF file and extract text content.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        list: List of Document objects containing page content
    """
    loader = PyPDFLoader(file_path)
    return loader.load()
