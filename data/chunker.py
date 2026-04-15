from datetime import datetime, timedelta
from pydantic import BaseModel
from chatbot_clone.data.loader import ChatMessage


class TextChunk(BaseModel):
    """A chunk of text with metadata (source, timestamp, senders, etc.)"""
    text: str
    metadata: dict


def _format_message(msg: ChatMessage) -> str:
    """Format a single ChatMessage into a display string."""
    parts = []
    if msg.timestamp:
        parts.append(f"[{msg.timestamp}]")
    if msg.sender:
        parts.append(f"{msg.sender}:")
    parts.append(msg.content)
    return " ".join(parts)


def _parse_timestamp(ts: str | None) -> datetime | None:
    """Try to parse a timestamp string into a datetime object."""
    if not ts:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return None


def split_sessions(
    messages: list[ChatMessage],
    gap_minutes: int = 30,
) -> list[list[ChatMessage]]:
    """Split messages into sessions based on time gaps.

    A new session starts when the time gap between two consecutive messages
    exceeds `gap_minutes`.  Messages without parseable timestamps are grouped
    with the preceding message.
    """
    if not messages:
        return []

    sessions: list[list[ChatMessage]] = []
    current_session: list[ChatMessage] = [messages[0]]
    prev_time = _parse_timestamp(messages[0].timestamp)

    for msg in messages[1:]:
        cur_time = _parse_timestamp(msg.timestamp)

        if prev_time is not None and cur_time is not None:
            gap = cur_time - prev_time
            if gap > timedelta(minutes=gap_minutes):
                sessions.append(current_session)
                current_session = []

        current_session.append(msg)
        if cur_time is not None:
            prev_time = cur_time

    if current_session:
        sessions.append(current_session)

    return sessions


def _build_chunk_metadata(
    messages: list[ChatMessage],
    session_id: int | None = None,
    chunk_index: int | None = None,
) -> dict:
    """Build rich metadata for a chunk from its constituent messages."""
    senders = sorted({m.sender for m in messages if m.sender})
    timestamps = [m.timestamp for m in messages if m.timestamp]
    meta: dict = {
        "message_count": len(messages),
        "senders": senders,
    }
    if timestamps:
        meta["time_start"] = timestamps[0]
        meta["time_end"] = timestamps[-1]
    if session_id is not None:
        meta["session_id"] = session_id
    if chunk_index is not None:
        meta["chunk_index"] = chunk_index
    return meta


def _merge_messages_into_chunks(
    messages: list[ChatMessage],
    chunk_size: int,
    session_id: int | None = None,
) -> list[TextChunk]:
    """Merge messages into chunks without ever splitting a single message.

    Messages are combined greedily: keep adding messages to the current chunk
    as long as the total text length stays within `chunk_size`.  When the next
    message would exceed the limit, emit the current chunk and start a new one.

    A single message whose formatted text exceeds `chunk_size` is placed in
    its own chunk (never truncated).
    """
    if not messages:
        return []

    chunks: list[TextChunk] = []
    current_msgs: list[ChatMessage] = []
    current_len = 0
    chunk_idx = 0

    for msg in messages:
        formatted = _format_message(msg)
        line_len = len(formatted) + 1  # +1 for the trailing newline

        if current_msgs and current_len + line_len > chunk_size:
            # Emit current chunk
            text = "\n".join(_format_message(m) for m in current_msgs)
            chunks.append(TextChunk(
                text=text,
                metadata=_build_chunk_metadata(current_msgs, session_id, chunk_idx),
            ))
            chunk_idx += 1
            current_msgs = []
            current_len = 0

        current_msgs.append(msg)
        current_len += line_len

    # Emit remaining messages
    if current_msgs:
        text = "\n".join(_format_message(m) for m in current_msgs)
        chunks.append(TextChunk(
            text=text,
            metadata=_build_chunk_metadata(current_msgs, session_id, chunk_idx),
        ))

    return chunks


def chunk_messages(
    messages: list[ChatMessage],
    chunk_size: int = 500,
    gap_minutes: int = 30,
    **_kwargs,
) -> list[TextChunk]:
    """Split chat messages into retrieval-friendly chunks.

    Strategy (L1 + L2 from the five-level chunking framework):
      1. **Session splitting** — cut at time gaps > `gap_minutes`.
      2. **Message-atomic merging** — within each session, greedily merge
         messages up to `chunk_size` characters without ever truncating a
         single message.

    This ensures:
      - No message is ever cut in the middle.
      - Different conversation topics (separated in time) land in separate
        chunks.
      - Each chunk carries rich metadata (senders, time range, session id).

    Args:
        messages: Cleaned ChatMessage list (output of the cleaner stage).
        chunk_size: Soft upper bound on chunk text length in characters.
        gap_minutes: Minimum gap (in minutes) to start a new session.

    Returns:
        List of TextChunk with text and metadata.
    """
    if not messages:
        return []

    sessions = split_sessions(messages, gap_minutes=gap_minutes)

    all_chunks: list[TextChunk] = []
    for session_id, session_msgs in enumerate(sessions):
        session_chunks = _merge_messages_into_chunks(
            session_msgs, chunk_size, session_id=session_id,
        )
        all_chunks.extend(session_chunks)

    return all_chunks
