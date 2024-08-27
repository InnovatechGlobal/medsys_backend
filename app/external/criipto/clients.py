import base64
from urllib.parse import quote

from pydantic import AnyHttpUrl

from app.auth.annotations import BankIDOAuth2Services
from app.common.exceptions import InternalServerError
from app.core.settings import get_settings
from app.external._request import InternalRequestClient

# Globals
settings = get_settings()


class InternalCriiptoVerifyClient:
    """
    Internal client for criipto verify interactions
    """

    def __init__(self) -> None:
        self.base_url = settings.CRIIPTO_VERIFY_DOMAIN
        self.client_id = settings.CRIIPTO_VERIFY_CLIENT_ID
        self.client_secret = settings.CRIIPTO_VERIFY_CLIENT_SECRET
        self.request = InternalRequestClient(base_url=settings.CRIIPTO_VERIFY_DOMAIN)

    async def generate_oauth2_url(
        self, *, service: BankIDOAuth2Services, token: str, redirect_url: AnyHttpUrl
    ):
        """
        Generate the oauth2 url
        """
        # Set acr value
        if service == "nobankid":
            acr_values = "urn:grn:authn:no:bankid"
        else:
            raise InternalServerError(
                f"Invalid bank id service: {service}",
                loc="app.external.criipto.clients.InternalCriiptoVerifyClient.generate_oauth2_url",
            )

        url = (
            f"{self.base_url}/oauth2/authorize?"
            "response_type=code"
            "&response_mode=query"
            f"&client_id={self.client_id}"
            f"&redirect_uri={str(redirect_url)}"
            f"&acr_values={acr_values}"
            f"&scope=openid&state={token}"
        )
        return url

    async def verify_code(self, *, code: str, redirect_url: str):
        """
        Verify code
        """

        # Combine the encoded values with a colon separator
        encoded_secrets = f"{quote(self.client_id)}:{quote(self.client_secret)}"

        # Base64 encode the combined string
        encoded_string = base64.b64encode(encoded_secrets.encode("utf-8")).decode()

        response = await self.request.post(
            endpoint=(
                "/oauth2/token?"
                "grant_type=authorization_code"
                f"&code={code}"
                f"&client_id={self.client_id}"
                f"&redirect_uri={redirect_url}"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encoded_string}",
            },
        )

        return response.json()
