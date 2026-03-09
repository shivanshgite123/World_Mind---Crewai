# 🌐 AI News Summarizer (CrewAI Edition)

A production-ready AI application that summarizes real-time global news using a **Retrieval Augmented Generation (RAG)** pipeline orchestrated by **CrewAI**.

## Architecture

```
User Query → Streamlit UI → FastAPI Backend → CrewAI Crew
                                                    ↓
                              ┌─────────────────────────────────────┐
                              │  Agent 1: News Research Specialist  │
                              │  Tool: WebSearchTool (Tavily)       │
                              │         ↓ stores in ChromaDB        │
                              ├─────────────────────────────────────┤
                              │  Agent 2: News Analyst & Summarizer │
                              │  Tool: RAGRetrieveTool (ChromaDB)   │
                              │         ↓ sends to Gemini AI        │
                              └─────────────────────────────────────┘
                                                    ↓
                                         News Summary Output
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI Orchestration | **CrewAI** (Sequential Process) |
| RAG Framework | LangChain |
| Web Search | Tavily API |
| Vector Database | ChromaDB (local) |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| LLM | Google Gemini 1.5 Flash |

## Project Structure

```
news-crew-app/
├── app.py                  # Streamlit frontend
├── backend/
│   ├── main.py             # FastAPI app & /summarize endpoint
│   ├── agent.py            # CrewAI agents, tasks & crew runner
│   ├── rag_chain.py        # Tavily search + ChromaDB RAG
│   └── gemini_llm.py       # Gemini API wrapper
├── data/                   # ChromaDB persistent storage
├── requirements.txt
├── .env                    # API keys
└── README.md
```

## CrewAI Agents

### Agent 1 — News Research Specialist
- **Goal**: Search the web and store results in ChromaDB
- **Tool**: `WebSearchTool` — wraps Tavily search + ChromaDB ingestion

### Agent 2 — News Analyst & Summarizer
- **Goal**: Retrieve relevant docs and generate a bullet-point summary
- **Tool**: `RAGRetrieveTool` — wraps ChromaDB retrieval + Gemini generation

Both agents run in **sequential** order via `Process.sequential`.

## Setup

### 1. Get API Keys

- **Tavily**: Sign up free at [tavily.com](https://tavily.com) (1000 searches/month free)
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

## Example Queries

- `Latest AI breakthroughs 2024`
- `World political crisis today`
- `New vaccine updates and healthcare news`
- `Latest technology changes in IT industry`
- `Global climate change updates`
- `Stock market news today`
