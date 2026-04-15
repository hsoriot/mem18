import re
from chatbot_clone.data.loader import ChatMessage

# 中国大陆手机号：1开头，第二位3-9，共11位
_CN_PHONE_RE = re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)')
# 美式手机号
_US_PHONE_RE = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
_US_PHONE_PAREN_RE = re.compile(r'\(\d{3}\)\s*\d{3}[-.]?\d{4}')
# 身份证号：18位，最后一位可能是X
_ID_CARD_RE = re.compile(r'(?<!\d)\d{17}[\dXx](?!\d)')
# 邮箱
_EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
# URL
_URL_RE = re.compile(r'https?://\S+')
_WWW_RE = re.compile(r'www\.\S+')
# 判断是否有"实质内容"：中文字符、字母、数字
_HAS_CONTENT_RE = re.compile(r'[\u4e00-\u9fffA-Za-z0-9]')


def clean_message(message: ChatMessage) -> ChatMessage:
    """Clean a single message: strip whitespace, remove URLs, anonymize PII"""
    content = message.content.strip()

    # Remove URLs
    content = _URL_RE.sub('', content)
    content = _WWW_RE.sub('', content)

    # Anonymize phone numbers (CN + US)
    content = _CN_PHONE_RE.sub('[PHONE]', content)
    content = _US_PHONE_RE.sub('[PHONE]', content)
    content = _US_PHONE_PAREN_RE.sub('[PHONE]', content)

    # Anonymize ID card numbers
    content = _ID_CARD_RE.sub('[ID]', content)

    # Anonymize email addresses
    content = _EMAIL_RE.sub('[EMAIL]', content)

    # Clean up extra whitespace
    content = re.sub(r'\s+', ' ', content).strip()

    return ChatMessage(
        content=content,
        timestamp=message.timestamp,
        sender=message.sender,
    )


def deduplicate_messages(messages: list[ChatMessage]) -> list[ChatMessage]:
    """Remove duplicate messages based on content"""
    seen_contents = set()
    unique_messages = []

    for message in messages:
        if message.content not in seen_contents:
            seen_contents.add(message.content)
            unique_messages.append(message)

    return unique_messages


def filter_noise(messages: list[ChatMessage], min_length: int = 2) -> list[ChatMessage]:
    """Filter out low-quality messages (too short, only emojis/symbols, etc.)"""
    filtered_messages = []

    for message in messages:
        content = message.content.strip()

        # Filter by minimum length (2 for Chinese, as even 2 chars can be meaningful)
        if len(content) < min_length:
            continue

        # Must contain at least one Chinese char, letter, or digit
        # This filters pure emoji / punctuation messages
        if not _HAS_CONTENT_RE.search(content):
            continue

        filtered_messages.append(message)

    return filtered_messages
