# Knowledge-base Search Engine

A RAG (Retrieval-Augmented Generation) based search engine that allows users to upload documents (PDF/Text) and ask questions.

## Features
- **Document Ingestion**: Upload PDF or Text files.
- **Vector Search**: Indexed using ChromaDB.
- **LLM Integration**: Answers synthesized by LangChain (OpenAI/Gemini).
- **Interactive UI**: Built with Streamlit.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set API Key (create a `.env` file):
   ```env
   OPENAI_API_KEY=sk-...
   # OR
   GOOGLE_API_KEY=AIza...
   ```
3. Run Backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. Run Frontend:
   ```bash
   streamlit run frontend/app.py
   ```
