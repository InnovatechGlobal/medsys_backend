from datetime import datetime


class CustomHTTPException(Exception):
    """
    Common base class for all http response exceptions
    """

    def __init__(self, msg: str, *, status_code: int, loc: list | None = None):
        self.msg = msg
        self.status_code = status_code
        self.loc = loc


class InternalServerError(Exception):
    """
    Common base class for all 500 internal server error responses
    """

    def __init__(self, msg: str, *, loc: str):
        self.msg = msg
        self.loc = loc
        self.timestamp = datetime.now()


class BadGatewayError(Exception):
    """
    Common base class for all 500 bad gateway error responses
    """

    def __init__(self, msg: str, *, loc: str, service: str):
        self.msg = msg
        self.loc = loc
        self.service = service
        self.timestamp = datetime.now()


class Unauthorized(CustomHTTPException):
    """
    Common exception class for 401 UNAUTHORIZED responses
    """

    def __init__(self, msg: str = "Unauthorized", *, loc: list | None = None):
        super().__init__(msg, status_code=401, loc=loc)


class Forbidden(CustomHTTPException):
    """
    Common exception class for 403 FORBIDDEN responses
    """

    def __init__(self, msg: str = "Forbidden", *, loc: list | None = None):
        super().__init__(msg, status_code=403, loc=loc)


class NotFound(CustomHTTPException):
    """
    Common exception class for 404 NOT FOUND responses
    """

    def __init__(self, msg: str, *, loc: list | None = None):
        super().__init__(msg, status_code=404, loc=loc)
