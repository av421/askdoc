# 📄 AskDoc

An end-to-end Retrieval-Augmented Generation (RAG) system that lets you upload PDF documents and ask natural language questions against them.

Built with FastAPI, ChromaDB, Sentence Transformers, and OpenAI.

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 🧠 How It Works

AskDoc uses a RAG pipeline to answer questions grounded in your documents:

1. **Ingest** — PDFs are parsed and split into overlapping text chunks
2. **Embed** — Each chunk is converted into a vector using `sentence-transformers`
3. **Store** — Vectors are stored in a local ChromaDB vector database
4. **Retrieve** — At query time, the most semantically similar chunks are retrieved
5. **Generate** — Retrieved chunks are passed as context to GPT-4o-mini to generate a grounded answer

---

## 🗂️ Project Structure

askdoc/
├── src/
│   ├── ingestor.py       # PDF parsing and text chunking
│   ├── embedder.py       # Sentence-transformer embeddings
│   ├── retriever.py      # ChromaDB vector storage and retrieval
│   ├── generator.py      # OpenAI answer generation
│   └── api.py            # FastAPI endpoints
├── app.py                # Streamlit frontend
├── config.py             # Configuration
├── data/
│   └── sample_docs/      # Sample PDFs for testing
├── tests/                # Unit tests
├── .env.example          # Environment variable template
└── requirements.txt      # Dependencies

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOURUSERNAME/askdoc.git
cd askdoc
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 5. Run the API
```bash
uvicorn src.api:app --reload
```

### 6. Run the Streamlit UI (in a new terminal tab)
```bash
streamlit run app.py
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/upload` | Upload and ingest a PDF |
| `POST` | `/query` | Ask a question |
| `DELETE` | `/collection/{name}` | Delete a collection |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| PDF Parsing | PyMuPDF |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector Store | ChromaDB |
| LLM | OpenAI GPT-4o-mini |
| API | FastAPI |
| Frontend | Streamlit |

---

## 💡 Design Decisions

- **Chunk overlap** — Chunks overlap by 50 characters to preserve context at boundaries
- **Cosine similarity** — Used for vector search as it performs well on semantic similarity tasks
- **GPT-4o-mini** — Chosen for its balance of quality and low cost
- **Local vector store** — ChromaDB runs fully locally, no external services needed

---

## 📄 License

MIT