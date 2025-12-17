# 🧠 Knowledge-Base RAG & Search Engine

A powerful **Retrieval-Augmented Generation (RAG)** system that allows users to chat with their documents (PDFs, Text). Built with **FastAPI**, **Streamlit**, **LangChain**, and **Google Gemini Models**.

## ✨ Features

- **Document Ingestion**: Seamlessly upload and process PDF and TXT files.
- **RAG Architecture**: Uses FAISS vector store for efficient similarity search.
- **Advanced LLM**: Powered by **Google Gemini 2.0 Flash / Flash-Latest** for high-speed, accurate responses.
- **Modern UI**: A sleek, animated **Streamlit** frontend with glassmorphism design and "Quantum Spinner" animations.
- **Source Citation**: Provides exact source documents for every answer.
- **Robust Backend**: Scalable **FastAPI** server handling ingestion and query logic.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) (with Custom CSS/Animations)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **LLM Orchestration**: [LangChain](https://www.langchain.com/)
- **Vector Store**: [FAISS](https://github.com/facebookresearch/faiss)
- **Embeddings**: `all-MiniLM-L6-v2` (HuggingFace)
- **Model Provider**: Google Gemini API

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A Google Cloud API Key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/student-jagat/knowledge-base-rag.git
   cd knowledge-base-rag
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

### Running the Application

You can run the full stack using the provided batch script (Windows):
```bash
./run.bat
```

Or run services manually:

**1. Start the Backend API**
```bash
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**2. Start the Frontend User Interface**
```bash
python -m streamlit run frontend/app.py
```

## 📂 Project Structure

```
knowledge-base-rag/
├── backend/
│   ├── main.py          # FastAPI Entry Point
│   ├── rag.py           # RAG Chain & Model Logic
│   ├── ingestion.py     # File Processing & Chunking
│   └── vector_store.py  # FAISS Vector Database Management
├── frontend/
│   └── app.py           # Streamlit UI
├── data/                # Stored Uploaded Files & FAISS Index
├── tests/
│   ├── test_gemini.py   # Model Availability Check
│   └── test_query.py    # API Endpoint Test
├── requirements.txt     # Python Dependencies
├── run.bat              # One-click startup script
└── README.md            # Project Documentation
```

## 🧩 How It Works

1. **Upload**: User uploads a document via Streamlit.
2. **Ingest**: Backend splits text into chunks and creates embeddings using HuggingFace.
3. **Store**: Embeddings are saved locally in a FAISS vector index.
4. **Query**: User asks a question.
5. **Retrieve**: System searches for the most relevant text chunks.
6. **Generate**: Gemini LLM generates an answer using the retrieved chunks as context.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements.

---
*Built with ❤️ by Jagat Student*
