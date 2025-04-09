import secrets
import string

import fitz
import tiktoken
from docx import Document


async def generate_state_token(length: int = 10):
    """
    Generate state token
    """
    alphabet = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return token


async def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract text from pdf file
    """
    doc = fitz.open(filepath)
    content = ""
    for page in doc:
        content += page.get_text()  # type: ignore

    return content


async def extract_text_from_docx(filepath: str):
    """
    Extract text from docx file
    """

    doc = Document(filepath)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)


async def trim_text_to_token_limit(
    text: str, model: str = "gpt-4o", max_tokens: int = 128000
) -> str:
    """
    Trims input text so that it fits within the token limit for a given OpenAI model.

    Args:
        text (str): The input text.
        model (str): OpenAI model name (e.g., "gpt-4o", "gpt-4", "gpt-3.5-turbo").
        max_tokens (int): Maximum token limit.

    Returns:
        str: Trimmed text that fits within the token limit.
    """
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)

    if len(tokens) <= max_tokens:
        return text

    # Trim and decode
    trimmed_tokens = tokens[:max_tokens]
    return enc.decode(trimmed_tokens)
