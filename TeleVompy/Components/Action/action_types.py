import enum
from ...Messenger import *


class ActionTypes(enum.Enum):
    SEND = Send
    SEND_MEDIA = SendMedia
    SEND_AUDIO = SendAudio
    SEND_DOCUMENT = SendDocument    
    SEND_ATTACHMENT = SendAttachment

    EDIT = Edit
    EDIT_MESSAGE= EditMessage
    EDIT_MEDIA = EditMedia
    EDIT_OR_SEND = EditOrSend
    EDIT_REPLY = EditReply

    DELETE = Delete
    DELETE_BY_ID = DeleteById
    DELETE_AND_SEND = DeleteAndSend

    INVOICE = Invoice

    NOTHING = Nothing
    TOGGLE = Toggle
    CLICK = Click
    ALERT = Alert
    REDIRECT = Redirect
