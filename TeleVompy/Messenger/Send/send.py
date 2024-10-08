from aiogram.types import LinkPreviewOptions
from ..messenger import Messenger, Message


class Send(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Send the text message to the chat
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)

    
    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        message = await self.bot.send_message(
            chat_id=self.User.chat_id, 
            text=self.Content.content,
            reply_markup=self.Page.keyboard, 
            message_effect_id=self.Page.effect, 
            parse_mode=self.Content.parse_mode,
            link_preview_options=LinkPreviewOptions(is_disabled=not self.Page.show_link_preview),
            **self.kwargs
        )
        return message
