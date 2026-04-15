from typing import Annotated, List

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class AgentState(TypedDict):
    """State schema for LangGraph agent: user_input, retrieved_context, response, etc."""
    user_input: str
    retrieved_context: List[str]
    response: str
    messages: Annotated[List[BaseMessage], add_messages]
