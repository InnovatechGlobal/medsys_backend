import base64
import os
import uuid
from typing import Literal

from app.core.settings import get_settings

# Globals
settings = get_settings()


async def save_base64_file(base64_str: str, file_type: Literal["pdf", "docx"]) -> str:
    """
    Save a base64-encoded file to disk and return the path.
    """

    if file_type not in ["pdf", "docx"]:
        raise ValueError("Unsupported file type")

    try:
        file_data = base64.b64decode(base64_str)
    except Exception:
        raise ValueError("Invalid base64 data")

    filename = f"{uuid.uuid4()}.{file_type}"
    file_path = settings.MEDIA_DIR + f"files/{filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(file_data)

    return str(file_path)
