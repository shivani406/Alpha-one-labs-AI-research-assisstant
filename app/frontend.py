import streamlit as st
import uuid
from pipeline import index_document, ask_question
import os
from pathlib import Path

# Page config
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 1rem 0;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        text-align: right;
    }
    .assistant-message {
        background-color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>📚 AI Research Assistant</h1>", unsafe_allow_html=True)
st.markdown(f"**Your Session ID:** `{st.session_state.user_id[:8]}...`")

# Sidebar
with st.sidebar:
    st.header("📁 Document Management")
    
    # File upload
    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDF files to chat with"
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            if uploaded_file.name not in st.session_state.uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Save uploaded file temporarily
                    temp_path = Path("temp") / uploaded_file.name
                    temp_path.parent.mkdir(exist_ok=True)
                    
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    try:
                        # Index the document
                        index_document(
                            pdf_path=str(temp_path),
                            user_id=st.session_state.user_id
                        )
                        st.session_state.uploaded_files.append(uploaded_file.name)
                        st.success(f"✅ {uploaded_file.name} indexed!")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                    finally:
                        # Clean up temp file
                        if temp_path.exists():
                            os.remove(temp_path)
    
    st.divider()
    
    # Display uploaded files
    if st.session_state.uploaded_files:
        st.subheader("📄 Uploaded Documents")
        for file_name in st.session_state.uploaded_files:
            st.text(f"• {file_name}")
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    # Info section
    st.info("""
    **How to use:**
    1. Upload PDF documents
    2. Wait for processing
    3. Ask questions about your documents
    4. Get AI-powered answers!
    """)

# Main chat interface
st.header("💬 Chat with Your Documents")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"""
                <div class='chat-message user-message'>
                    <strong>You:</strong> {message['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class='chat-message assistant-message'>
                    <strong>🤖 Assistant:</strong> {message['content']}
                </div>
            """, unsafe_allow_html=True)

# Question input
if not st.session_state.uploaded_files:
    st.warning("⚠️ Please upload at least one PDF document to start chatting.")
else:
    with st.form(key="question_form", clear_on_submit=True):
        question = st.text_input(
            "Ask a question about your documents:",
            placeholder="e.g., What are the main topics discussed in the document?"
        )
        submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
        
        if submit_button and question:
            # Add user message to chat
            st.session_state.chat_history.append({
                "role": "user",
                "content": question
            })
            
            # Get answer
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = ask_question(question, user_id=st.session_state.user_id)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        <small>Built with Streamlit • Powered by ChromaDB & Gemini</small>
    </div>
""", unsafe_allow_html=True)