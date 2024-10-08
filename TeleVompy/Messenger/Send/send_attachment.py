from ..messenger import Messenger, Message
from ..Send import *


class SendAttachment(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Send attachments from the Page to the chat
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)
        self.__sent_replay = False
    
    def __get_func(self, files: list, files_type: str) -> 'SendMedia | SendAudio | SendDocument | None | bool':
        """ Returns the `object of needed class` to send the message or `None` for media group """
        # if more than one files -> will send by group
        if len(files) > 1:
            return None
        # if the message has one media (photo or video)
        elif files_type == 'media':
            return SendMedia(user=self.User, page=self.Page, file=files[0], *self.args, **self.kwargs)
        # if the message has one audio
        elif files_type == 'audios':
            return SendAudio(user=self.User, page=self.Page, file=files[0], *self.args, **self.kwargs)
        # if the message has one document
        elif files_type == 'documents':
            return SendDocument(user=self.User, page=self.Page, file=files[0], *self.args, **self.kwargs)
        return False

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        for key, value in self.Page.Media.files().items():
            # if not files for current type (media, audio, document) 
            if not value or not len(value):
                continue
            
            # get object to send current file type
            func = self.__get_func(value, key)

            # send group of media one type
            if func is None:
                message = (await self.bot.send_media_group(chat_id=self.User.chat_id, media=value))[0]
            # send one file
            elif func:
                message = await func.execute()
                if not self.__sent_replay and isinstance(message, Message):
                    self.__sent_replay = True

        # send message with reply and content
        if not self.__sent_replay:
            message = await Send(user=self.User, page=self.Page, *self.args, **self.kwargs).execute()

        return message
