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

### 5. Download NLTK Data (First Run Only)

```bash
python -c "import nltk; nltk.download('punkt')"
```

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
│   ├── backend_api.py       # FastAPI endpoints (optional)
│   └── test.py              # CLI testing script
├── chroma_db/               # Local ChromaDB storage (auto-created)
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

### Screenshots

*(Add screenshots here after deployment)*

---

## 🔧 Configuration Options

### Chunking Parameters (`pipeline.py`)

```python
CHUNK_SIZE = 1000        # Characters per chunk
CHUNK_OVERLAP = 200      # Overlap between chunks
```

**Tuning Guide:**
- **Smaller chunks** (500-800): Better for precise answers, more chunks to search
- **Larger chunks** (1200-1500): More context per chunk, fewer chunks
- **Overlap**: 10-20% of chunk size recommended

### Retrieval Parameters

```python
TOP_K = 5  # Number of chunks to retrieve
```

**Tuning Guide:**
- **More chunks** (7-10): More comprehensive answers, higher token cost
- **Fewer chunks** (3-4): Faster, cheaper, but might miss context

### Compression Settings

Adjust in `pipeline.py` → `ContextualCompressionRetriever`:
- Currently uses Gemini's flash model for speed
- Can switch to more powerful models for better compression

---

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t ai-research-assistant .
```

### Run Container

```bash
docker run -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/chroma_db:/app/chroma_db \
  ai-research-assistant
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./chroma_db:/app/chroma_db
```

---

## 🌐 Deployment Options

### 1. Streamlit Cloud (Easiest - Free Tier)

1. Push code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io/)
3. Connect repository
4. Add secrets (Gemini API key)
5. Deploy!

**Limitations**: 1GB RAM, CPU-only

### 2. Hugging Face Spaces (Recommended - Free GPU)

```bash
# Create new Space
# Select "Streamlit" SDK
# Upload files
# Add secrets in Settings
```

**Advantages**: Free GPU, 16GB RAM, 50GB storage

### 3. Railway (Paid - $5-10/month)

```bash
railway login
railway init
railway up
```

**Advantages**: Simple deployment, persistent storage, custom domains

### 4. AWS / GCP / Azure (Enterprise)

See deployment guides in `/docs/deployment/` (coming soon)

---

## 🚨 Known Issues

### Issue 1: Large File Downloads During Install

**Problem**: `pip install` downloads 1-2GB of ML models

**Solutions:**
- Use fast internet connection
- Pre-download models and cache in Docker layer
- Consider using lighter embedding models

### Issue 2: ChromaDB Persistence

**Problem**: Data lost between restarts with default settings

**Solution**: ChromaDB automatically persists to `./chroma_db/` directory. Ensure this folder is:
- Not in `.gitignore` for local dev (but add to `.gitignore` for production)
- Mounted as volume in Docker
- Backed up in production

### Issue 3: User ID Management

**Problem**: User IDs stored only in session state (lost on browser close)

**Future Enhancement**: Implement proper authentication with persistent user accounts

### Issue 4: Memory Usage

**Problem**: Large PDFs or many documents can cause memory issues

**Solutions:**
- Limit PDF size (e.g., 50MB max)
- Implement pagination for chunk storage
- Use cloud ChromaDB for large datasets

---

## 🔐 Security Considerations

### Current State

⚠️ **This is an MVP - NOT production-ready for sensitive data**

- No authentication system
- API keys in environment variables only
- User isolation based on UUID only
- No rate limiting
- No input sanitization

### Before Production Deployment

1. **Add Authentication**: 
   - OAuth 2.0 (Google/GitHub)
   - JWT tokens
   - User database (PostgreSQL/MongoDB)

2. **Secure API Keys**:
   - Use secret management (AWS Secrets Manager, Azure Key Vault)
   - Rotate keys regularly

3. **Implement Rate Limiting**:
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

4. **Data Encryption**:
   - Encrypt PDFs at rest
   - Use HTTPS only
   - Encrypt ChromaDB storage

5. **Input Validation**:
   - Validate PDF file types
   - Scan for malicious content
   - Limit file sizes

---

## 🔮 Future Enhancements

### Phase 1: Core Improvements (Short-term)

- [ ] **User Authentication**: OAuth with Google/GitHub
- [ ] **Data Deletion**: API to delete user data from ChromaDB
- [ ] **Citation Display**: Show which document chunks were used
- [ ] **Export Conversations**: Download chat history as PDF/JSON
- [ ] **Multi-format Support**: Word docs, PowerPoint, plain text
- [ ] **Progress Indicators**: Better feedback during long operations

### Phase 2: Advanced Features (Medium-term)

- [ ] **Semantic Search**: Search across all documents
- [ ] **Document Summarization**: Auto-generate summaries
- [ ] **Comparative Analysis**: Compare multiple documents
- [ ] **Collaborative Features**: Share documents with team
- [ ] **Version Control**: Track document updates
- [ ] **API Rate Limiting**: Prevent abuse

### Phase 3: Architecture Redesign (Long-term)

#### Microservices Architecture

```
┌────────────────┐
│  React Frontend │ (Vercel - Free)
└───────┬────────┘
        │ REST API
┌───────▼────────┐
│  FastAPI Backend│ (Railway - $5/mo)
└───────┬────────┘
        │
   ┌────┴─────┬──────────┬──────────┐
   ▼          ▼          ▼          ▼
ChromaDB   Gemini    PostgreSQL  Redis
(Cloud)    (API)     (Users)     (Cache)
```

**Benefits:**
- **Scalability**: Scale components independently
- **Performance**: Frontend CDN, backend auto-scaling
- **Cost**: Frontend free, backend only when needed
- **Maintenance**: Easier updates and debugging

#### Separation Implementation

**Backend API** (`backend_api.py`):
```python
# FastAPI endpoints
POST /api/upload     # Upload PDF
POST /api/ask        # Ask question
DELETE /api/user     # Delete user data
GET /api/documents   # List user's documents
```

**Frontend** (React/Next.js):
```javascript
// API calls instead of direct imports
fetch('/api/upload', { method: 'POST', body: formData })
fetch('/api/ask', { method: 'POST', body: { question } })
```

**Deployment:**
- Frontend: Vercel/Netlify (Static hosting)
- Backend: Railway/Render (Container hosting)
- Database: Supabase (PostgreSQL) + ChromaDB Cloud

**Migration Steps:**
1. Create FastAPI backend with current pipeline
2. Deploy backend to Railway
3. Build React frontend consuming API
4. Deploy frontend to Vercel
5. Add authentication layer (Auth0/Clerk)

### Phase 4: Advanced ML Features

- [ ] **Multi-modal Search**: Search images in PDFs
- [ ] **Custom Fine-tuning**: Domain-specific models
- [ ] **Automated Fact-checking**: Verify claims with sources
- [ ] **Research Graph**: Visualize connections between papers
- [ ] **Citation Network**: Auto-generate bibliographies

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

## 📊 Performance Benchmarks

*(To be added - contributors welcome!)*

| Metric | Current | Target |
|--------|---------|--------|
| PDF Upload (10MB) | ~15s | <5s |
| Question Response | ~3-5s | <2s |
| Memory Usage | ~2GB | <1GB |
| Concurrent Users | 1 | 10+ |

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Error: "Gemini API key not found"
```bash
# Check .env file exists
cat .env

# Verify key is set
echo $GEMINI_API_KEY

# Restart application after adding key
```

### Error: "ChromaDB connection failed"
```bash
# Check ChromaDB directory
ls -la chroma_db/

# Remove and recreate
rm -rf chroma_db/
# Restart app - will recreate automatically
```

### Error: "Out of memory"
```bash
# Reduce chunk size in pipeline.py
CHUNK_SIZE = 500  # Down from 1000

# Or reduce top_k results
TOP_K = 3  # Down from 5
```

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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team & Acknowledgments

**Project Lead**: Alpha One Labs  
**Contributors**: [List contributors here]

**Built with:**
- 🦜 LangChain for RAG orchestration
- 🎨 Streamlit for frontend
- 🗄️ ChromaDB for vector storage
- 🤖 Google Gemini for LLM
- 🔥 Sentence Transformers for embeddings

**Special Thanks:**
- Alpha One Labs for the opportunity
- Open source community for amazing tools
- All contributors and testers

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/Alpha-one-labs-AI-research-assisstant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Alpha-one-labs-AI-research-assisstant/discussions)
- **Email**: support@alphaonelabs.com (replace with actual)

---

## 🌟 Star History

If you find this project helpful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/Alpha-one-labs-AI-research-assisstant&type=Date)](https://star-history.com/#yourusername/Alpha-one-labs-AI-research-assisstant&Date)

---

**Made with ❤️ by the Alpha One Labs Community**