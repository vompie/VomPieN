from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from aiogram.filters import CommandObject
from aiogram.filters.command import BotCommand

from ..Engine.engine import SingleTonBotEngine
from ..Utils import BaseClass, dprint


class Interface(BaseClass):
    """ Initialize Interface class with a `Bot` instance """

    def __init__(self):
        super().__init__()
        try:
            """ Get bot instance from SingleTonBotEngine """
            self.__bot = SingleTonBotEngine().bot
        except Exception as e:
            dprint(self, f"bot object not found in the SingleTonBotEngine: {e}")
            self.__bot = None
        
    def decor_del_msg_n_set_cmds(self, commands: list[dict] | None = None) -> callable:
        """
        Decorator function to delete user messages and set commands if need

        Parameters
        ----------
        commands (`list[dict]` | None): List of dict {'command': `str`, 'description': `str`}
        """

        def decorator(func: callable):
            async def wrapper(message_query: Message | CallbackQuery, command: CommandObject | None = None):
                await self.__delete_message(message_query)
                await self.set_commands(message_query, commands)
                if command and command.args:
                    return await func(message_query, command)
                return await func(message_query)
            return wrapper
        return decorator

    def decor_send_n_cancel_action(self, action_type: str = 'typing') -> callable:
        """
        Decorator function to send typing indicator and cancel action if needed
        
        Parameters
        ----------
        action_type (`str`): Type of action to send. Default is 'typing'
        """

        def decorator(func):
            async def wrapper(message_query: Message | CallbackQuery):
                try: 
                    await self.__bot.send_chat_action(chat_id=message_query.from_user.id, action=action_type)
                except Exception as e: 
                    dprint(self, f"send chat action error: {e}")
                await func(message_query)
                try: 
                    await self.__bot.send_chat_action(chat_id=message_query.from_user.id, action='cancel')
                except Exception as e: 
                    dprint(self, f"cancel chat action error: {e}")
            return wrapper
        return decorator

    async def set_commands(self, message_query: Message | CallbackQuery | None = None, commands: list[dict] = None, chat_id: int | None = None) -> None:
        """
        Function to set commands for the user

        Parameters
        ----------
        - message_query (`Message | CallbackQuery`): The aiogram.types.Message or aiogram.types.CallbackQuery instance
        - commands (`list[dict]`): List of dict {'command': `str`, 'description': `str`}
        """

        cmd = []
        try:
            for command in commands or []:
                cmd.append(BotCommand(command=command['command'], description=command['description']))
            if not cmd:
                return
            chat_id = message_query.from_user.id if message_query else chat_id
            await self.__bot.set_my_commands(commands=cmd, scope=BotCommandScopeChat(chat_id=chat_id))
        except Exception as e:
            dprint(self, f"set commands error: {e}") 

    async def __delete_message(self, message: Message) -> None:
        """ Asynchronously delete a message """
        if not isinstance(message, Message):
            return
        await self.delete_message(chat_id=message.from_user.id, msg_id=message.message_id)

    async def delete_message(self, chat_id: int, msg_id: int | None) -> None:
        """
        Delete a message by its chat_id and msg_id
        
        Parameters
        ----------
        - chat_id (`int`): ID of the chat
        - msg_id (`int` | `None`): ID of the message
        """
        
        if not msg_id: 
            return
        try:
            await self.__bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            dprint(self, f"delete message error: {e}")
