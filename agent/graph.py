import logging

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from chatbot_clone.persona.manager import PersonaManager
from chatbot_clone.llm.interface import LLMInterface
from chatbot_clone.rag.retriever import RAGRetriever
from chatbot_clone.agent.state import AgentState

logger = logging.getLogger(__name__)

_FALLBACK_RESPONSE = "抱歉，我现在有点不在状态，等一下再聊吧。"


def create_agent_graph(
    persona_manager: PersonaManager,
    llm_interface: LLMInterface,
    rag_retriever: RAGRetriever,
    checkpointer=None,
) -> CompiledStateGraph:
    """Create LangGraph StateGraph with nodes: retrieve -> call_llm

    Messages history is managed automatically via the `messages` state field
    and a LangGraph checkpointer.
    """

    # LLM client with automatic retry (exponential backoff, 3 attempts)
    llm_with_retry = llm_interface.client.with_retry(
        stop_after_attempt=3,
    )

    def retrieve(state: AgentState) -> dict:
        """Node that retrieves context using RAG based on user_input."""
        query = state.get("user_input", "")
        contexts = rag_retriever.retrieve(query)
        return {"retrieved_context": contexts}

    def call_llm(state: AgentState) -> dict:
        """Node that calls LLM with system prompt + RAG context + full message history."""
        # Build system message: persona prompt + RAG context
        system_prompt = persona_manager.get_system_prompt()
        contexts = state.get("retrieved_context", [])
        context_text = "\n".join(contexts) if contexts else ""

        system_parts = [system_prompt]
        if context_text:
            system_parts.append(f"\n以下是与当前话题相关的历史对话片段，请参考其中的语气和用词：\n{context_text}")

        system_msg = SystemMessage(content="\n".join(system_parts))

        # Get conversation history from state, append current user_input
        history = list(state.get("messages", []))
        user_input = state.get("user_input", "")
        history.append(HumanMessage(content=user_input))

        # Assemble final messages: system + history
        all_messages = [system_msg] + history

        # Call LLM with retry; fallback on failure
        try:
            response = llm_with_retry.invoke(all_messages)
            response_text = response.content
        except Exception:
            logger.exception("LLM call failed after retries")
            response_text = _FALLBACK_RESPONSE

        # Return updates: response text + messages to accumulate
        return {
            "response": response_text,
            "messages": [
                HumanMessage(content=user_input),
                AIMessage(content=response_text),
            ],
        }

    # Build the graph
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("call_llm", call_llm)

    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "call_llm")
    workflow.add_edge("call_llm", END)

    return workflow.compile(checkpointer=checkpointer)
