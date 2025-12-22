from typing import List,Dict
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from config import settings


def generate_embeddings(chunks : List[Document]) -> List[dict]:
    """
    Generate embeddings for document chunks.

    Returns a list of dicts with:
    - id
    - embedding
    - metadata
    - text
    """

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    #Extract raw text from each chunk
    texts: List[str] = []
    for chunk in chunks:
        texts.append(chunk.page_content)

    # Generate embeddings
    vectors = embedding_model.embed_documents(texts)

    #Combine these embeddings again with metadata
    embedded_records: List[Dict] = []
    for index in range(len(chunks)):
        chunk = chunks[index]
        vector = vectors[index]
        user_id = chunk.metadata["user_id"]
        source = chunk.metadata["source"]
        page = chunk.metadata["page"]

        #generate each record
        record = {
            "id": f"{user_id}_{source}_page{page}_chunk{index}",
            "embedding": vector,
            "metadata": chunk.metadata,            
            "document": chunk.page_content
        }

        embedded_records.append(record)
    return embedded_records


def store_embeddings(embedded_records: List[Dict]):
    """
    Stores embeddings into Chroma Cloud.
    """

    client = chromadb.CloudClient(
        api_key=settings.CHROMA_API_KEY,
        tenant=settings.CHROMA_TENANT,
        database=settings.CHROMA_DATABASE
    )

    collection = client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION
    )

    ids = []
    embeddings = []
    metadatas = []
    documents = []

    for record in embedded_records:
        ids.append(record["id"])
        embeddings.append(record["embedding"])
        metadatas.append(record["metadata"])
        documents.append(record["document"])
    collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas,
        documents=documents
    )

    return collection