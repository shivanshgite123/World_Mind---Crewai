import os
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

load_dotenv()

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
EMBED_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "news_articles"

_embeddings = SentenceTransformerEmbeddings(model_name=EMBED_MODEL)
_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
_tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_and_store(query: str) -> None:
    """Search Tavily, split results, and store in ChromaDB."""
    results = _tavily.search(query=query, search_depth="advanced", max_results=6)

    raw_texts = []
    for r in results.get("results", []):
        content = r.get("content", "").strip()
        title = r.get("title", "")
        url = r.get("url", "")
        if content:
            raw_texts.append(f"Title: {title}\nSource: {url}\n\n{content}")

    if not raw_texts:
        return

    chunks = _splitter.create_documents(raw_texts)

    # Always create fresh collection for the query
    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=_embeddings,
        persist_directory=CHROMA_DIR,
    )

    # Clear existing and add new docs
    try:
        db.delete_collection()
    except Exception:
        pass

    db = Chroma.from_documents(
        documents=chunks,
        embedding=_embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )
    db.persist()


def retrieve_context(query: str, k: int = 5) -> str:
    """Retrieve top-k relevant chunks from ChromaDB."""
    db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=_embeddings,
        persist_directory=CHROMA_DIR,
    )
    docs = db.similarity_search(query, k=k)
    return "\n\n---\n\n".join(d.page_content for d in docs)
