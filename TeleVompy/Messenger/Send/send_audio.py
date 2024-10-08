from aiogram.types import InputMediaAudio
from ..messenger import Messenger, Message


class SendAudio(Messenger):
    def __init__(self, file: InputMediaAudio, *args, **kwargs):
        """ 
        Send the one audio to the chat
        
        Parameters
        ----------
        - file (`InputMediaAudio`): Represents an audio file to be sent
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """
        
        super().__init__(*args, **kwargs)
        self.__file = file

    def __coroutine_send_audio(self, audio: InputMediaAudio) -> callable:
        """ Coroutine to send an audio with caption """
        return self.bot.send_audio(
            chat_id=self.User.chat_id, 
            audio=audio.media,
            duration=audio.duration,
            caption=audio.caption,
            reply_markup=self.Page.keyboard,
            message_effect_id=self.Page.effect, 
            parse_mode=self.Content.parse_mode,
        )

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        return await self.__coroutine_send_audio(audio=self.__file)
