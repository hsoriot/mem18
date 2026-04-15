from pydantic import BaseModel, Field, field_validator
import yaml
from typing import List, Literal, Optional


class LLMConfig(BaseModel):
    """Configuration for LLM provider (Claude or OpenAI)"""
    provider: Literal["openai", "anthropic"]
    model: str
    api_key: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    base_url: Optional[str] = None


class PersonaConfig(BaseModel):
    """Configuration schema for persona including name, style, catchphrases, examples"""
    name: str
    style: str
    catchphrases: List[str]
    examples: Optional[List[str]] = None


class RAGConfig(BaseModel):
    """Configuration for RAG retrieval parameters"""
    top_k: int = 5
    similarity_threshold: float = 0.7
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None


def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")
