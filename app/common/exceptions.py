class CustomHTTPException(Exception):
    """
    Common base class for all http response exceptions
    """

    def __init__(self, msg: str, *, status_code: int, loc: list | None = None):
        self.msg = msg
        self.status_code = status_code
        self.loc = loc
