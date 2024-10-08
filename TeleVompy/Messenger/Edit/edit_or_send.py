from ..messenger import Messenger, Message
from ...Utils.base_class import dprint
from ..Send import SendAttachment
from ..Edit import *
from ..Delete import Delete


class EditOrSend(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Try to edit text and media of the message containing media or delete message and send new if got error
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """

        # if the message is sent by the user, then send new message
        if self.User.from_user:
            return await SendAttachment(self.User, self.Page, *self.args, **self.kwargs).execute()

        message = None
        try:
            if self.Page.Media.media:
                message = await EditMedia(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
            else:
                message = await EditMessage(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
        except Exception as e:
            dprint(self, f"edit error: {e}")
            """ 
            If it was not possible to edit the message, for example:
                the message is not available;
                the message is deleted;
                the message content does not match the new content;
                the message content has not changed;
                etc.
            """

        if isinstance(message, Message):
            return message
        
        # if got edit error -> delete old message and send new message
        await Delete(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
        return await SendAttachment(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()
