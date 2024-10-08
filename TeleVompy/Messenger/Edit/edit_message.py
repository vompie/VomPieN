from aiogram.types import LinkPreviewOptions
from ..messenger import Messenger, Message


class EditMessage(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Edit text of the message
        
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

        # if the message is sent by the user, then can't edit message
        if self.User.from_user:
            raise self.EditMessageError("Can't edit not user message. Use `EDIT_OR_SEND`")

        message = await self.bot.edit_message_text(
            chat_id=self.User.chat_id,
            message_id=self.User.msg_id,  
            text=self.Content.content,
            reply_markup=self.Page.keyboard,
            parse_mode=self.Content.parse_mode,
            link_preview_options=LinkPreviewOptions(is_disabled=not self.Page.show_link_preview),
            **self.kwargs
        )
        return message
