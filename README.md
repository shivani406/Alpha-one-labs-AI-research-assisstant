# 📚 AI Research Assistant

> An intelligent RAG (Retrieval Augmented Generation) system that allows users to upload PDF documents and chat with them using AI. Built with LangChain, ChromaDB, and Google Gemini.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Project Overview

This project was created as part of Alpha One Labs' initiative to build an AI-powered research assistant for literature review. It enables researchers and students to:

- Upload multiple PDF documents
- Ask natural language questions about the content
- Get AI-generated answers based on the uploaded documents
- Maintain conversation history within a session

**Key Feature**: Multi-user support with isolated data storage - each user can only access their own uploaded documents.

---

## 🏗️ Architecture

### System Design

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Pipeline   │─────▶│  ChromaDB   │
│ (Streamlit) │      │   (Backend)  │      │  (Vector)   │
└─────────────┘      └──────────────┘      └─────────────┘
                             │
                             ▼
                     ┌──────────────┐
                     │ Gemini LLM   │
                     │ (Google AI)  │
                     └──────────────┘
```

### How It Works

#### 1️⃣ **Document Ingestion** (One-time per PDF)
```
PDF Upload → Text Extraction → Chunking → Embeddings Generation → ChromaDB Storage
```

- **Text Extraction**: PyPDF extracts text from uploaded PDF
- **Chunking**: Text split into 1000-character chunks with 200-char overlap
- **Embeddings**: Each chunk converted to vector embeddings using Sentence Transformers
- **Storage**: Stored in ChromaDB with `user_id` metadata for isolation

#### 2️⃣ **Question Answering** (Every query)
```
Question → Embedding → Similarity Search → Context Compression → LLM → Answer
```

- **Embedding**: Question converted to vector
- **Retrieval**: Top 5 relevant chunks fetched from ChromaDB (filtered by `user_id`)
- **Compression**: Chunks compressed to reduce tokens while preserving meaning
- **Generation**: Gemini LLM generates answer using compressed context + question
- **Response**: Answer returned to user

### Component Details

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | Streamlit | User interface for uploads and chat |
| **Backend Pipeline** | LangChain | Orchestrates RAG workflow |
| **Vector DB** | ChromaDB | Stores document embeddings |
| **Embeddings** | Sentence Transformers | Converts text to vectors |
| **LLM** | Google Gemini | Generates natural language answers |
| **Text Processing** | NLTK, LangChain | Chunking and compression |

---

## 📋 Prerequisites

- **Python**: 3.11 or higher
- **Operating System**: Linux, macOS, or Windows
- **API Keys**: 
  - Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
  - ChromaDB credentials (if using cloud instance)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Alpha-one-labs-AI-research-assisstant.git
cd Alpha-one-labs-AI-research-assisstant
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This will download ~1-2GB of ML models. First-time installation takes 5-10 minutes.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# ChromaDB Configuration (if using cloud)
CHROMA_HOST=your_chroma_host
CHROMA_PORT=8000

# Optional: Customize settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RESULTS=5
```

**To get Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with Google account
3. Click "Create API Key"
4. Copy and paste into `.env`

---

## 🎮 Running the Application

### Option 1: Streamlit Frontend (Recommended)

```bash
cd app
streamlit run frontend.py
```

Access at: `http://localhost:8501`

### Option 2: Command Line Testing

```bash
cd app
python test.py
```

**Usage:**
1. Modify `test.py` with your PDF path and user_id
2. Run the script
3. Ask questions in the terminal

---

## 📁 Project Structure

```
Alpha-one-labs-AI-research-assisstant/
├── app/
│   ├── pipeline.py          # Core RAG pipeline logic
│   ├── frontend.py          # Streamlit UI
│   └── test.py              # CLI testing script
├── temp/                    # Temporary PDF storage (auto-created)
├── .env                     # Environment variables (create this)
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── LICENSE                  # MIT License
```

---

## 🎨 Frontend Features

### User Interface

- **📤 PDF Upload**: Drag-and-drop or browse to upload documents
- **💬 Chat Interface**: Chat-style Q&A with conversation history
- **🔍 Real-time Processing**: Visual feedback during indexing
- **🗑️ Clear History**: Reset conversation without losing documents
- **🆔 Session Management**: Each browser session gets unique user_id

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Getting Started

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new features
- Update README if adding features
- Test locally before submitting PR

### Areas Needing Help

- [ ] Frontend UI/UX improvements
- [ ] Unit tests for pipeline
- [ ] Docker optimization
- [ ] Documentation improvements
- [ ] Performance benchmarking
- [ ] Alternative LLM integration (OpenAI, Anthropic)

---
## 📚 Resources & References

### Documentation
- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/docs)

### Learning Materials
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)
- [Vector Databases Explained](https://www.pinecone.io/learn/vector-database/)
- [Embeddings Guide](https://www.sbert.net/)

### Related Projects
- [LangChain RAG Examples](https://github.com/langchain-ai/langchain/tree/master/templates)
- [Streamlit Gallery](https://streamlit.io/gallery)

---

**Built with:**
- 🦜 LangChain for RAG orchestration
- 🎨 Streamlit for frontend
- 🗄️ ChromaDB for vector storage
- 🤖 Google Gemini for LLM
- 🔥 Sentence Transformers for embeddings
