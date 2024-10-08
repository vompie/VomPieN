from ..messenger import Messenger, Message
from ..Edit import *


class Edit(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Edit any type of the message
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window 
        
        Raise
        -----
        - `EditMessageError`: If the message is sent by the user and cannot be edited
        """
        
        # if the message is sent by the user, then we can't edit message
        if self.User.from_user:
            raise self.EditMessageError("Can't edit not user message. Use `EDIT_OR_SEND`")
        
        # if page has media files
        if self.Page.Media.media:
            return await EditMedia(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
        # if page has audio files ...
        # if page has document files ...
        # if page has no media files
        else:
            return await EditMessage(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
