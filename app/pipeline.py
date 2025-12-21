from ingest import ingest_pdf
from chunking import chunk_documents
from embed import generate_embeddings , store_embeddings
from retrieve import retrieve_context
from ques_and_ans import generate_final_prompt, ask_llm

def index_document (pdf_path: str , user_id):
    """
    Runs once per PDF upload.
    Stores embeddings in Chroma.

    """
    # Load PDF
    documents = ingest_pdf(pdf_path , user_id)

    # Chunk documents
    chunks = chunk_documents(documents)

    # Generate embeddings
    embedded_records = generate_embeddings(chunks)

    #Store embeddings in chroma
    store_embeddings(embedded_records)

def ask_question (user_prompt: str, user_id, top_k: int = 5 ) -> str:
    """
    Runs per user query.
    Retrieves context and generates answer.

    """
    # Retreive relevant compressed chunks
    context_docs = retrieve_context(user_prompt = user_prompt, user_id = user_id, top_k = top_k)

    if not context_docs:
        return "I do not have enough information on this"
    
    # Send the final prompt
    final_prompt = generate_final_prompt (user_prompt = user_prompt, context= context_docs)
     
    # Ask LLM
    answer = ask_llm(final_prompt)

    return answer

