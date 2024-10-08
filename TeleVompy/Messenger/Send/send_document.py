from aiogram.types import InputMediaDocument
from ..messenger import Messenger, Message


class SendDocument(Messenger):
    def __init__(self, file: InputMediaDocument, *args, **kwargs):
        """ 
        Send the one document to the chat
        
        Parameters
        ----------
        - file (`InputMediaDocument`): Represents a file to be sent
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)
        self.__file = file

    def __coroutine_send_document(self, document: InputMediaDocument) -> callable:
        """ Coroutine to send a document with caption """
        return self.bot.send_document(
            chat_id=self.User.chat_id, 
            document=document.media,
            caption=document.caption,
            reply_markup=self.Page.keyboard,
            message_effect_id=self.Page.effect, 
            parse_mode=self.Content.parse_mode,
        )

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        return await self.__coroutine_send_document(document=self.__file)
