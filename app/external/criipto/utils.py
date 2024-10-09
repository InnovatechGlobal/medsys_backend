import jwt

from app.common.exceptions import Unauthorized
from app.external.criipto.clients import InternalCriiptoVerifyClient

criipt_client = InternalCriiptoVerifyClient()


async def decode_token(token: str):
    """
    Decode criipto token

    Args:
        token (str): The criipto id_token

    Returns:
        dict: The decoded token
    """
    try:
        # headers = jwt.get_unverified_header(token)

        data = jwt.decode(
            jwt=token,
            options={"verify_signature": False},
            # key=await criipt_client.get_public_key(kid=headers["kid"]),  # type: ignore
            # algorithms=[headers["alg"]],
        )

    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError) as e:
        print(e)
        raise Unauthorized(msg="Invalid Login Request")
    return data
