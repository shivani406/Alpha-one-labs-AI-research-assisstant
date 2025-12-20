import chromadb
from typing import List
from langchain_core.documents import Document
from config import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def retrive_context(user_prompt: str, user_id, top_k: int = 5  ) -> List[Document]:

    #convert user's prompt into embeddings
    embeddings_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    user_prompt_embeddings = embeddings_model.embed_query(user_prompt)

    #connect to the chroma client

    client = chromadb.CloudClient(api_key = settings.CHROMA_API_KEY , tenant=settings.CHROMA_TENANT, database=settings.CHROMA_DATABASE)
    collection = client.get_collection(settings.CHROMA_COLLECTION)

    # Adding the filtering query which will fetch only the user's data
    if user_id:
        filter = {"user_id": user_id}
    else:
        filter = None

    # Fetch data from chromadb 
    top_k_results = collection.query (query_embeddings=[user_prompt_embeddings], n_results= top_k, where = filter )

    # Reconstruct the langchain document with the top_k_results
    retrived_documents = List[Document] = []

    documents = top_k_results.get("documents" , [[]])[0]
    metadata = top_k_results.get("metadatas", [[]])[0]

    for text , metadata in zip(documents , metadata):
        if text:
            retrived_documents.append(Document(page_content= text, metadata = metadata))
    return retrived_documents