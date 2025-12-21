"""Converting the user's PDF into text for processing"""
from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader

def ingest_pdf(pdf_path :str, user_id )-> List[Document]:

    """
    Load a PDF file and return LangChain Document objects.

    Args:
        pdf_path (str): Path to the PDF file

    Returns:
        List[Document]: List of documents (one per page)
    """
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # add user_id to the metadata
    for doc in documents:
        doc.metadata["user_id"] = user_id

    return documents

