from app.common.exceptions import Forbidden, NotFound


class UserNotFound(NotFound):
    """
    Exception class for 404 User Not Found Exceptions
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("User Not Found", loc=loc)


class UserDeactivated(Forbidden):
    """
    Exception class for 403 User Account Has Been Deactivated Exception
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("User Account Has Been Deactivated", loc=loc)
