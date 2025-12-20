from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""
    Split documents into smaller chunks suitable for embeddings and retrieval.

    Args:
        documents (List[Document]): Documents from PDF ingestion

    Returns:
        List[Document]: Chunked documents with preserved metadata
"""


def chunk_documents(documents : List[Document ]) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 150,
        separators= ["\n\n", "\n", ". ", " "]
    )
    chunked_document = splitter.split_documents(documents)

    return chunked_document  


