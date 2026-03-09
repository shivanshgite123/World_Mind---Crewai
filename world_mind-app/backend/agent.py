import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from rag_chain import search_and_store, retrieve_context
from gemini_llm import generate_summary

load_dotenv()


class AgentState(TypedDict):
    query: str
    context: str
    summary: str


def search_node(state: AgentState) -> AgentState:
    """Search the web and store documents in ChromaDB."""
    search_and_store(state["query"])
    return state


def summarize_node(state: AgentState) -> AgentState:
    """Retrieve context and generate summary with Gemini."""
    context = retrieve_context(state["query"])
    summary = generate_summary(state["query"], context)
    return {**state, "context": context, "summary": summary}


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("search", search_node)
    graph.add_node("summarize", summarize_node)
    graph.add_edge(START, "search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", END)
    return graph.compile()


_graph = build_graph()


def run_agent(query: str) -> str:
    """Run the LangGraph agent and return the summary."""
    result = _graph.invoke({"query": query, "context": "", "summary": ""})
    return result["summary"]
