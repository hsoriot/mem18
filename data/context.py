"""Contextual Retrieval: generate context prefixes for chunks.

Strategy B: Use an LLM to generate a one-sentence context prefix for each
chunk, given the surrounding session as background.  Falls back to Strategy C
(template-based, zero LLM cost) when no LLM is provided.

The context prefix is prepended to chunk text **only for embedding**.  The
original chunk text is preserved for display / feeding to the chat LLM.
"""

from __future__ import annotations

from chatbot_clone.data.chunker import TextChunk, _format_message
from chatbot_clone.data.loader import ChatMessage

_CONTEXT_PROMPT = (
    "以下是一段聊天会话中的全部消息：\n"
    "<session>\n{session_text}\n</session>\n\n"
    "以下是从中提取的一个片段：\n"
    "<chunk>\n{chunk_text}\n</chunk>\n\n"
    "请用一句简短的中文概括这个片段的对话背景（包括时间、参与者、讨论话题），"
    "不要复述对话内容本身。只输出这一句话，不要加任何前缀。"
)


# ---------------------------------------------------------------------------
# Strategy C: template-based context (zero cost)
# ---------------------------------------------------------------------------

def generate_template_context(chunk: TextChunk) -> str:
    """Build a context prefix from chunk metadata alone (no LLM call).

    Returns a short sentence like:
        "这是2024-06-02，小明、朋友B之间关于RAG的对话。"
    """
    meta = chunk.metadata
    parts: list[str] = []

    # Time
    time_start = meta.get("time_start")
    if time_start:
        date_str = time_start[:10]  # "2024-06-02"
        parts.append(f"这是{date_str}")

    # Senders
    senders = meta.get("senders", [])
    if len(senders) > 1:
        parts.append(f"{'、'.join(senders)}之间的对话。")
    elif len(senders) == 1:
        parts.append(f"{senders[0]}的发言。")
    else:
        parts.append("的对话。")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Strategy B: LLM-generated context
# ---------------------------------------------------------------------------

def generate_llm_context(
    chunk: TextChunk,
    session_messages: list[ChatMessage],
    llm_client,
) -> str:
    """Use an LLM to generate a one-sentence context prefix.

    Args:
        chunk: The TextChunk to generate context for.
        session_messages: All messages in the chunk's session (for background).
        llm_client: A LangChain chat model (ChatOpenAI / ChatAnthropic / etc.)
                     that supports `.invoke([HumanMessage(...)])`.

    Returns:
        A short context string (typically one sentence).
    """
    from langchain_core.messages import HumanMessage

    session_text = "\n".join(_format_message(m) for m in session_messages)
    prompt = _CONTEXT_PROMPT.format(
        session_text=session_text,
        chunk_text=chunk.text,
    )
    response = llm_client.invoke([HumanMessage(content=prompt)])
    return response.content.strip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def add_context_to_chunks(
    chunks: list[TextChunk],
    sessions: list[list[ChatMessage]] | None = None,
    llm_client=None,
) -> list[TextChunk]:
    """Add a context prefix to each chunk for embedding.

    The context is stored in `metadata["context_prefix"]`.  The original
    `text` field is **not** modified.

    Callers that build embedding text should concatenate:
        context_prefix + "\\n" + chunk.text

    Args:
        chunks: List of TextChunk objects (must have `session_id` in metadata).
        sessions: The session list from `split_sessions()`, indexed by
                  session_id.  Required for Strategy B (LLM).  If None and
                  llm_client is provided, falls back to Strategy C.
        llm_client: Optional LangChain chat model.  If None, uses template
                    fallback (Strategy C).

    Returns:
        The same list of TextChunk objects, each with `metadata["context_prefix"]`
        populated.
    """
    # Build session lookup
    session_map: dict[int, list[ChatMessage]] = {}
    if sessions:
        for idx, sess in enumerate(sessions):
            session_map[idx] = sess

    for chunk in chunks:
        session_id = chunk.metadata.get("session_id")
        session_msgs = session_map.get(session_id) if session_id is not None else None

        if llm_client is not None and session_msgs is not None:
            # Strategy B: LLM-generated context
            try:
                prefix = generate_llm_context(chunk, session_msgs, llm_client)
            except Exception:
                # Fallback to template on any LLM error
                prefix = generate_template_context(chunk)
        else:
            # Strategy C: template-based
            prefix = generate_template_context(chunk)

        chunk.metadata["context_prefix"] = prefix

    return chunks
