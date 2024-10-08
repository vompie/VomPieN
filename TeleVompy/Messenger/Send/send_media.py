from aiogram.types import InputMediaPhoto, InputMediaVideo
from ..messenger import Messenger, Message


class SendMedia(Messenger):
    def __init__(self, file: InputMediaPhoto | InputMediaVideo, *args, **kwargs):
        """ 
        Send the one photo or video to the chat
        
        Parameters
        ----------
        - file (`InputMediaPhoto` | `InputMediaVideo`): Represents a photo or video to be sent
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)
        self.__file = file

    def __coroutine_send_photo(self, photo: InputMediaPhoto) -> callable:
        """ Coroutine to send a photo with caption """
        return self.bot.send_photo(
            chat_id=self.User.chat_id, 
            photo=photo.media,
            caption=photo.caption,
            reply_markup=self.Page.keyboard,
            message_effect_id=self.Page.effect, 
            parse_mode=self.Content.parse_mode,
            **self.kwargs
        )

    def __coroutine_send_video(self, video: InputMediaVideo) -> callable:
        """ Coroutine to send a video with caption """
        return self.bot.send_video(
            chat_id=self.User.chat_id, 
            video=video.media,
            caption=video.caption,
            width=video.width,
            height=video.height,
            duration=video.duration,
            reply_markup=self.Page.keyboard,
            message_effect_id=self.Page.effect, 
            parse_mode=self.Content.parse_mode,
            **self.kwargs
        )
    
    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        if isinstance(self.__file, InputMediaVideo):
            return await self.__coroutine_send_video(video=self.__file)
        return await self.__coroutine_send_photo(photo=self.__file)
