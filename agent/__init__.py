import os
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph
from chatbot_clone.config import LLMConfig
from chatbot_clone.persona.manager import PersonaManager
from chatbot_clone.vectorstore.manager import VectorStoreManager
from chatbot_clone.rag.retriever import RAGRetriever
from chatbot_clone.llm.interface import LLMInterface
from chatbot_clone.agent.graph import create_agent_graph


def create_agent(
    persona_path: str,
    vectorstore_path: str,
    llm_config: LLMConfig | None = None,
    checkpointer=None,
) -> CompiledStateGraph:
    """Create fully configured agent with persona, RAG, and LLM"""
    persona_file = Path(persona_path)
    if not persona_file.exists():
        raise FileNotFoundError(f"Persona file not found: {persona_path}")

    persona_manager = PersonaManager(persona_path)
    vectorstore_manager = VectorStoreManager(vectorstore_path)
    rag_retriever = RAGRetriever(
        vectorstore_manager, top_k=5, similarity_threshold=0.3,
    )

    if llm_config is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        base_url = os.environ.get("ANTHROPIC_BASE_URL", None)
        llm_config = LLMConfig(
            provider="anthropic",
            model="aws-claude-opus-4-6",
            api_key=api_key,
            base_url=base_url,
            max_tokens=1024,
        )

    llm_interface = LLMInterface(llm_config)
    agent_graph = create_agent_graph(
        persona_manager, llm_interface, rag_retriever, checkpointer=checkpointer
    )
    return agent_graph
