from app.common.exceptions import NotFound


class MedChatNotFound(NotFound):
    """
    Exception class for 404 MedChat Not Found
    """

    def __init__(self, *, loc: list | None = None):
        super().__init__("MedChat Not Found", loc=loc)
