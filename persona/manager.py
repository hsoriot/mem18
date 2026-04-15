import yaml
from pathlib import Path
from chatbot_clone.config import PersonaConfig


class PersonaManager:
    """Manages persona configuration and prompt generation"""

    def __init__(self, config_path: str) -> None:
        """Load persona configuration from YAML"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Persona config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            self._config_data = yaml.safe_load(f)

        self._name = self._config_data.get('name', '')
        self._style = self._config_data.get('style', '')
        self._catchphrases = self._config_data.get('catchphrases', [])
        self._examples = self._config_data.get('examples', [])

    def get_system_prompt(self) -> str:
        """Generate system prompt from persona config"""
        lines = []

        if self._name:
            lines.append(f"你是「{self._name}」，请完全模仿此人的说话方式来回复用户。")

        if self._style:
            lines.append(f"说话风格：{self._style}。")

        if self._catchphrases:
            phrases = "、".join(f"「{p}」" for p in self._catchphrases)
            lines.append(f"口头禅/常用语气词：{phrases}。请在合适的地方自然地使用它们。")

        if self._examples:
            lines.append("\n以下是此人的真实对话示例，请学习其语气、用词和回复结构：")
            for ex in self._examples:
                if isinstance(ex, dict):
                    user_msg = ex.get("user", "")
                    bot_msg = ex.get("assistant", "")
                    lines.append(f"  用户：{user_msg}")
                    lines.append(f"  {self._name}：{bot_msg}")

        lines.append("\n请用中文回复。保持此人的语气和风格，不要使用过于正式的措辞。")
        return "\n".join(lines)

    def get_example_dialogues(self) -> list[dict[str, str]]:
        """Get example dialogues for few-shot learning"""
        return self._examples if self._examples else []
