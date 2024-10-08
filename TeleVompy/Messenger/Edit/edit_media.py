from ..messenger import Messenger, Message


class EditMedia(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Edit text and media of the message containing media
        
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

        message = await self.bot.edit_message_media(
            chat_id=self.User.chat_id,
            message_id=self.User.msg_id, 
            media=self.Page.Media.media[0],
            reply_markup=self.Page.keyboard,
            **self.kwargs
        )
        return message
