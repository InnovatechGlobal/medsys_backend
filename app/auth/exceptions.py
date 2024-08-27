from app.common.exceptions import NotFound


class OAuth2LoginAttemptNotFound(NotFound):
    """
    Exception class for 404 Oauth2 login attempt not found
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("Oauth2 Login Attempt Not Found", loc=loc)
