from pathlib import Path
from chatbot_clone.vectorstore.manager import VectorStoreManager
from chatbot_clone.data.loader import load_csv_messages, load_json_messages
from chatbot_clone.data.cleaner import clean_message, deduplicate_messages, filter_noise
from chatbot_clone.data.chunker import chunk_messages, split_sessions
from chatbot_clone.data.context import add_context_to_chunks


class DataPipeline:
    """Orchestrates data loading, cleaning, chunking, and embedding"""

    def __init__(
        self,
        vectorstore_manager: VectorStoreManager,
        context_llm=None,
    ) -> None:
        """Initialize pipeline with vector store.

        Args:
            vectorstore_manager: Vector store for persisting chunks.
            context_llm: Optional LangChain chat model for generating context
                         prefixes (Strategy B).  When ``None``, uses a zero-cost
                         template fallback (Strategy C).
        """
        self.vectorstore_manager = vectorstore_manager
        self.context_llm = context_llm
        self._processed_messages = set()

    def process_file(self, file_path: str, file_type: str) -> int:
        """Process chat history file and add to vector store. Returns number of chunks added."""
        # Validate file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Validate file type
        if file_type not in ["csv", "json"]:
            raise ValueError(f"Invalid file type: {file_type}. Must be 'csv' or 'json'")

        # Load messages
        if file_type == "csv":
            messages = load_csv_messages(file_path)
        else:
            messages = load_json_messages(file_path)

        # Clean messages
        cleaned_messages = [clean_message(msg) for msg in messages]

        # Deduplicate and filter
        deduplicated = deduplicate_messages(cleaned_messages)
        filtered_messages = filter_noise(deduplicated)

        # Track processed messages for incremental processing
        for msg in filtered_messages:
            message_id = f"{msg.timestamp}|{msg.sender}|{msg.content}"
            self._processed_messages.add(message_id)

        # Split sessions (needed for both chunking and context generation)
        sessions = split_sessions(filtered_messages)

        # Chunk messages
        chunks = chunk_messages(filtered_messages)

        # Add context prefixes (Strategy B with LLM, or Strategy C template)
        add_context_to_chunks(
            chunks,
            sessions=sessions,
            llm_client=self.context_llm,
        )

        # Add to vector store
        if chunks:
            self.vectorstore_manager.add_chunks(chunks)

        return len(chunks)

    def process_incremental(self, file_path: str, file_type: str) -> int:
        """Incrementally add new messages to vector store"""
        # Validate file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Validate file type
        if file_type not in ["csv", "json"]:
            raise ValueError(f"Invalid file type: {file_type}. Must be 'csv' or 'json'")

        # Load messages
        if file_type == "csv":
            messages = load_csv_messages(file_path)
        else:
            messages = load_json_messages(file_path)

        # Clean messages
        cleaned_messages = [clean_message(msg) for msg in messages]

        # Deduplicate and filter
        deduplicated = deduplicate_messages(cleaned_messages)
        filtered_messages = filter_noise(deduplicated)

        # Filter out already processed messages
        new_messages = []
        for msg in filtered_messages:
            message_id = f"{msg.timestamp}|{msg.sender}|{msg.content}"
            if message_id not in self._processed_messages:
                new_messages.append(msg)
                self._processed_messages.add(message_id)

        # Split sessions and chunk new messages
        sessions = split_sessions(new_messages)
        chunks = chunk_messages(new_messages)

        # Add context prefixes
        add_context_to_chunks(
            chunks,
            sessions=sessions,
            llm_client=self.context_llm,
        )

        # Add to vector store
        if chunks:
            self.vectorstore_manager.add_chunks(chunks)

        return len(chunks)
