"""Converting the user's PDF into text for processing"""
from langchain_community.document_loaders import PyPDFLoader
from typing import List

"""
    Load a PDF file and return LangChain Document objects.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        List[Document]: List of documents (one per page)
"""

from langchain_community.document_loaders import PyPDFLoader

def ingest_pdf(pdf_path :str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents
