from pydantic import BaseModel
import pandas as pd
import json
from pathlib import Path
from typing import Optional


class ChatMessage(BaseModel):
    """Structured chat message with timestamp, sender, content"""
    content: str
    timestamp: Optional[str] = None
    sender: Optional[str] = None


def load_csv_messages(file_path: str) -> list[ChatMessage]:
    """Load chat messages from CSV file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)

        if 'content' not in df.columns:
            raise ValueError("CSV must contain 'content' column")

        messages = []
        for _, row in df.iterrows():
            message_data = {'content': row['content']}
            if 'timestamp' in df.columns:
                message_data['timestamp'] = row['timestamp']
            if 'sender' in df.columns:
                message_data['sender'] = row['sender']
            messages.append(ChatMessage(**message_data))

        return messages
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except Exception as e:
        if isinstance(e, (FileNotFoundError, ValueError)):
            raise
        raise ValueError(f"Error parsing CSV file: {str(e)}")


def load_json_messages(file_path: str) -> list[ChatMessage]:
    """Load chat messages from JSON file"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        data = [data]

    messages = []
    for item in data:
        messages.append(ChatMessage(**item))

    return messages
