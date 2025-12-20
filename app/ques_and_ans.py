from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings
from langchain_core.documents import Document

def generate_final_prompt (user_prompt: str, context : List[Document]) -> str:

    context_text = "\n\n".join(
    doc.page_content for doc in context)

    final_prompt = f"""
        You are an AI research assistant.

        Answer the question strictly using the provided context below.
        If the answer is not present in the context, say:
        "I do not have enough information to answer this."

        Context:
        {context_text}

        Question:
        {user_prompt}

        Answer:
        """.strip()
    
    return final_prompt

def ask_llm(final_prompt: str) -> str:
    llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
    response = llm.invoke(final_prompt)

    return response.content
    