#  AI News Summarizer

A production-ready AI application that summarizes real-time global news using a **Retrieval Augmented Generation (RAG)** pipeline.

## Architecture

```
User Query → Streamlit UI → FastAPI Backend → LangGraph Agent
                                                     ↓
                                          Tavily Web Search
                                                     ↓
                                        ChromaDB (Vector Store)
                                                     ↓
                                           Gemini 1.5 Flash
                                                     ↓
                                          News Summary Output
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Orchestration | LangGraph |
| RAG Framework | LangChain |
| Web Search | Tavily API |
| Vector Database | ChromaDB (local) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM | Google Gemini 1.5 Flash |

## Project Structure

```
news-summary-app/
├── app.py                  # Streamlit frontend
├── backend/
│   ├── main.py             # FastAPI app & /summarize endpoint
│   ├── agent.py            # LangGraph agent (Search → Summarize)
│   ├── rag_chain.py        # Tavily search + ChromaDB RAG
│   └── gemini_llm.py       # Gemini API wrapper
├── data/                   # ChromaDB persistent storage
├── requirements.txt
├── .env                    # API keys
└── README.md
```

## Setup

### 1. Get API Keys

- **Tavily**: Sign up free at [tavily.com](https://tavily.com) (free tier: 1000 searches/month)
- **Gemini**: Get key at [aistudio.google.com](https://aistudio.google.com) (free tier available)

### 2. Configure Environment

Edit `.env`:
```
TAVILY_API_KEY=your_tavily_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

**Terminal 1 — Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

## Features

- **Category Buttons**: One-click queries for Politics , Technology , Health Care 
- **Custom Queries**: Enter any news topic
- **RAG Pipeline**: Web search → embeddings → vector retrieval → LLM synthesis
- **Persistent Storage**: ChromaDB stores vectors locally in `data/chroma_db/`
- **Modern UI**: Dark theme with gradient accents

## Example Queries

- `Latest AI breakthroughs 2024`
- `World political crisis today`
- `New vaccine updates and healthcare news`
- `Latest technology changes in IT industry`
- `Global climate change updates`
- `Stock market news today`
