from aiogram.types import InlineKeyboardMarkup
from ..messenger import Messenger, Message


class EditReply(Messenger):
    def __init__(self, reply_markup: InlineKeyboardMarkup | None = None, *args, **kwargs):
        """ 
        Edit reply of the message
        
        Parameters
        ----------
        - reply_markup (`InlineKeyboardMarkup | None`): The new reply markup for the message
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)
        self.__reply_markup = reply_markup

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        return await self.bot.edit_message_reply_markup(chat_id=self.User.chat_id, message_id=self.User.msg_id, reply_markup=self.__reply_markup, **self.kwargs)
