import secrets
import string


async def generate_state_token(length: int = 10):
    """
    Generate state token
    """
    alphabet = string.ascii_letters + string.digits
    token = "".join(secrets.choice(alphabet) for _ in range(length))
    return token
