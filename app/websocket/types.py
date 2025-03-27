from pydantic import BaseModel


class WSResponseTypes(BaseModel):
    """
    Websocket response 'type'
    """

    error: str = "error"
    validation_error: str = "validation-error"

    medchat_create: str = "medchat-create"

    medchatmsg_stream: str = "medchatmsg-stream"
    medchatmsg_stream_comp: str = "medchatmsg-stream-complete"

    medchattitle_stream: str = "medchat-title-stream"
    medchattitle_stream_comp: str = "medchat-title-stream-complete"
