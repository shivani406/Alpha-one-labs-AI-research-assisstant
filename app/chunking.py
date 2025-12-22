from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer,  util
from nltk.tokenize import sent_tokenize


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into smaller chunks suitable for embeddings and retrieval.

    Args:
        documents (List[Document]): Documents from PDF ingestion

    Returns:
        List[Document]: Chunked documents with preserved metadata
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=150, separators=["\n\n", "\n", ". ", " "])
    chunked_document = splitter.split_documents(documents)

    return chunked_document


def compress_chunk(single_chunk: Document, query: str, top_n: int = 3) -> Document:
    """
    Docstring for compress_chunk

    :param chunks: Description
    :type chunks: Document
    :param query: Description
    :type query: str
    :param top_n: Description
    """
    st_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    text = single_chunk.page_content.strip()
    if len(text) < 300:
        return single_chunk

    # Tokenize the sentence
    sentences = sent_tokenize(text)
    sentences = [s for s in sentences if s.strip()]

    if not sentences:
        return single_chunk

    # convert query and sentences into embeddings
    sentences_embeddings = st_model.encode(sentences)
    query_embedding = st_model.encode(query)

    scores = util.cos_sim(query_embedding, sentences_embeddings)[0]
    top_indices = scores.topk(min(top_n, len(sentences))).indices.tolist()
    top_indices.sort()

    compressed_text = " ".join([sentences[i] for i in top_indices])

    return Document(page_content=compressed_text, metadata=single_chunk.metadata)
