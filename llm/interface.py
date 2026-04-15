from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from chatbot_clone.config import LLMConfig


class LLMInterface:
    """Unified interface for LLM providers"""

    def __init__(self, config: LLMConfig) -> None:
        """Initialize LLM client based on provider"""
        self.config = config

        if config.provider == "openai":
            kwargs = dict(
                model=config.model,
                api_key=config.api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            if config.base_url:
                kwargs["base_url"] = config.base_url
            self.client = ChatOpenAI(**kwargs)
        elif config.provider == "anthropic":
            kwargs = dict(
                model=config.model,
                api_key=config.api_key,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
            )
            if config.base_url:
                kwargs["anthropic_api_url"] = config.base_url
            self.client = ChatAnthropic(**kwargs)
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")

