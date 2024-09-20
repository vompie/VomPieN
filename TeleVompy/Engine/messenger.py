from .base_class import BaseClass
from .engine import SingleTonBotEngine

from aiogram.types import LinkPreviewOptions

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram import Bot
    from .user import User
    from ..Components.Page.page import Page, Content


class Messenger(BaseClass):
    def __init__(self, user: 'User | None' = None, page: 'Page | None' = None):
        """
        Initialize Messenger class with User and Page instances

        Parameters
        ----------
        - user (`User` | `None`): User instance for sending messages
        - page (`Page` | `None`): Page instance containing message content and settings
        """

        super().__init__()
        self.__bot = SingleTonBotEngine().bot
        self.__payments_token = SingleTonBotEngine().payments_token
        self.__User: User | None = user
        self.__Page: Page | None = page
        self.__Content: Content | None = self.__Page.Content if self.__Page else None
        self.__sent_replay: bool = False
        
    def __get_func(self, files: list, files_type: str) -> callable:
        """ Returns the `function` to send the message or `None` for media_group or `False` to no media """
        # More than one files
        if len(files) > 1:
            return None
        # No files
        if not len(files):
            return
        # Only one file
        if files_type == 'media':
            if hasattr(files, 'width'):
                # if the message has a video
                return self.__bot.send_video
            # if the message has a photo
            return self.__bot.send_photo
        elif files_type == 'audios':
            # if the message has an audio
            return self.__bot.send_audio
        elif files_type == 'documents':
            # if the message has a document
            return self.__bot.send_document

    async def send(self) -> None:
        """ Send the message to the chat """  
        try:
            # send files
            for key, value in self.__Page.Media.files().items():
                if not value:
                    continue
                func = self.__get_func(value, key)
                if func is None:
                    message = (await self.__bot.send_media_group(chat_id=self.__User.chat_id, media=value))[0]
                elif func:
                    message = await func(
                        self.__User.chat_id, value[0].media,
                        caption=self.__Content.content,
                        reply_markup=self.__Page.keyboard if not self.__sent_replay else None, 
                        message_effect_id=self.__Page.effect, parse_mode=self.__Content.parse_mode
                    )
                    self.__sent_replay = True if not self.__sent_replay else True
            # send message
            if not self.__sent_replay:
                message = await self.__bot.send_message(
                    chat_id=self.__User.chat_id, text=self.__Content.content,
                    reply_markup=self.__Page.keyboard, 
                    message_effect_id=self.__Page.effect, parse_mode=self.__Content.parse_mode,
                    link_preview_options=LinkPreviewOptions(is_disabled=not self.__Page.show_link_preview))
            self.__User.msg_id = message.message_id  # update message_id
        except Exception as e:
            if self.CfgEng.DEBUG : print(f"{self} send message error: {e}")

    async def edit(self) -> None:
        """ Edit the message in the chat """
        if self.__User.from_user:
            # if the message is sent by the user, then we can't edit message
            await self.send()
            return 
        try:
            if self.__Page.Media.media:
                # if the message has a media
                await self.__bot.edit_message_media(
                    chat_id=self.__User.chat_id,
                    message_id=self.__User.msg_id, 
                    media=self.__Page.Media.media[0], 
                    reply_markup=self.__Page.keyboard,
                )
            else:
                # if the message has no media
                await self.__bot.edit_message_text(
                    chat_id=self.__User.chat_id,
                    message_id=self.__User.msg_id,  
                    text=self.__Content.content,
                    reply_markup=self.__Page.keyboard,
                    parse_mode=self.__Content.parse_mode,
                    link_preview_options=LinkPreviewOptions(is_disabled=not self.__Page.show_link_preview)
                )
        except Exception as e:
            """ 
            If it was not possible to edit the message, for example:
                the message is not available;
                the message is deleted;
                the message was not sent by a bot;
                the message content does not match the new content;
                the message content has not changed;
                etc.
            """
            if self.CfgEng.DEBUG: print(f"{self} edit message error: {e}")
            await self.delete()
            await self.send() 
    
    async def alert(self) -> None:
        """ Alert the user about something """
        try:
            await self.__User.query.answer(
                text=self.__Page.Alert.text,
                show_alert=self.__Page.Alert.show_alert,
                url=self.__Page.Alert.url
            )
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} alert error: {e}")

    async def delete(self, User: dict | None = None) -> None:
        """
        Delete the message from the chat

        Parameters
        ----------
        User (`dict` | `None`): A dictionary containing 'chat_id' and 'msg_id' of the message to delete. 
        If `None`, delete the message associated with the Messenger instance
        """
        
        try:
            if not User:
                await self.__bot.delete_message(chat_id=self.__User.chat_id, message_id=self.__User.msg_id)
                return
            chat_id: int = User['chat_id']
            msg_id: int = User['msg_id']
            bot: Bot = User['bot']
            await bot.delete_message(chat_id, msg_id)             
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} delete message error: {e}") 

    async def delete_message_by_id(self, msg_id: int) -> None:
        """
        Delete the message from the chat by it's ID

        Parameters
        ----------
        msg_id (`int`): A 'msg_id' of the message to delete. 
        """

        try:
            await self.__bot.delete_message(chat_id=self.__User.chat_id, message_id=msg_id)           
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} delete message error: {e}") 

    async def nothing(self) -> None:
        """ Do nothing """
        return None

    async def invoice(self) -> None:
        """ Send the invoice message from the chat """
        try:
            await self.__bot.send_invoice(
                chat_id=self.__User.chat_id,
                title=self.__Page.Payment.title,
                description=self.__Page.Payment.description,
                provider_token=self.__payments_token,
                currency=self.__Page.Payment.currency,
                is_flexible=self.__Page.Payment.is_flexible,
                prices=self.__Page.Payment.prices,
                start_parameter=self.__Page.Payment.start_parameter,
                payload=self.__Page.Payment.payload,
                message_effect_id=self.__Page.effect
            )            
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} invoice message error: {e}")    
