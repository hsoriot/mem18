"""CLI entry point for chatbot-clone."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


def ingest(args):
    """Ingest chat history into vector store."""
    from chatbot_clone.pipeline.data_pipeline import DataPipeline
    from chatbot_clone.vectorstore.manager import VectorStoreManager

    vs = VectorStoreManager(args.vectorstore)
    pipeline = DataPipeline(vs)

    file_path = args.file
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        file_type = "csv"
    elif ext == ".json":
        file_type = "json"
    else:
        print(f"Unsupported file type: {ext} (use .csv or .json)")
        sys.exit(1)

    n = pipeline.process_file(file_path, file_type)
    print(f"Done. {n} chunk(s) ingested into {args.vectorstore}")


def _make_checkpointer(db_uri: str | None, sqlite_path: str | None = None):
    """Create a checkpointer based on available configuration.

    Priority: Postgres > SQLite > in-memory.

    - *db_uri* / DATABASE_URI env var → PostgresSaver (multi-instance persistent)
    - *sqlite_path* / SQLITE_PATH env var → SqliteSaver (single-instance persistent)
    - otherwise → MemorySaver (lost on restart)
    """
    uri = db_uri or os.environ.get("DATABASE_URI")
    if uri:
        from langgraph.checkpoint.postgres import PostgresSaver

        checkpointer = PostgresSaver.from_conn_string(uri)
        checkpointer.setup()
        return checkpointer

    sq = sqlite_path or os.environ.get("SQLITE_PATH")
    if sq:
        from langgraph.checkpoint.sqlite import SqliteSaver

        # from_conn_string is a context manager; we enter it manually
        # and rely on process exit to close the connection.
        cm = SqliteSaver.from_conn_string(sq)
        saver = cm.__enter__()
        return saver

    from langgraph.checkpoint.memory import MemorySaver

    return MemorySaver()


def chat(args):
    """Interactive chat loop."""
    from chatbot_clone.agent import create_agent

    print("Loading agent...")
    checkpointer = _make_checkpointer(
        getattr(args, "db", None),
        sqlite_path=getattr(args, "sqlite", None),
    )
    agent = create_agent(
        persona_path=args.persona,
        vectorstore_path=args.vectorstore,
        checkpointer=checkpointer,
    )

    thread_id = args.thread_id
    config = {"configurable": {"thread_id": thread_id}}
    print(f"Ready! thread={thread_id}  Type your message (Ctrl+C or 'quit' to exit)\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if not user_input or user_input.lower() in ("quit", "exit", "q"):
            print("Bye!")
            break

        result = agent.invoke(
            {"user_input": user_input},
            config=config,
        )
        print(f"\nBot: {result['response']}\n")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="chatbot-clone",
        description="Personal chatbot that mimics your speaking style",
    )
    sub = parser.add_subparsers(dest="command")

    # --- ingest ---
    p_ingest = sub.add_parser("ingest", help="Ingest chat history into vector store")
    p_ingest.add_argument("file", help="Path to chat history file (.csv or .json)")
    p_ingest.add_argument(
        "--vectorstore", default="./vectorstore_data",
        help="Vector store directory (default: ./vectorstore_data)",
    )

    # --- chat ---
    p_chat = sub.add_parser("chat", help="Start interactive chat")
    p_chat.add_argument(
        "--persona", default="./examples/persona.yaml",
        help="Path to persona YAML (default: ./examples/persona.yaml)",
    )
    p_chat.add_argument(
        "--vectorstore", default="./vectorstore_data",
        help="Vector store directory (default: ./vectorstore_data)",
    )
    p_chat.add_argument(
        "--thread-id", dest="thread_id", default="default",
        help="Conversation thread ID, e.g. a user ID (default: 'default')",
    )
    p_chat.add_argument(
        "--db", default=None,
        help="Postgres connection URI for persistent history (default: env DATABASE_URI)",
    )
    p_chat.add_argument(
        "--sqlite", default=None,
        help="SQLite file path for persistent history, e.g. ./chatbot.db (default: env SQLITE_PATH)",
    )

    args = parser.parse_args()

    if args.command == "ingest":
        ingest(args)
    elif args.command == "chat":
        chat(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
