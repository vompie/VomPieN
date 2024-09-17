from aiogram.types import Message, BotCommandScopeChat, CallbackQuery
from aiogram.filters import CommandObject
from aiogram.filters.command import BotCommand
from ..Engine.engine import BaseClass, SingleTonBotEngine


class Interface(BaseClass):
    """ Initialize Interface class with a `Bot` instance """

    def __init__(self):
        super().__init__()
        try:
            """ Get bot instance from SingleTonBotEngine """
            self.__bot = SingleTonBotEngine().bot
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} bot object not found in the SingleTonBotEngine: {e}")
            self.__bot = None
        
    def decor_del_msg_n_set_cmds(self, commands: list[dict] | None = None) -> callable:
        """
        Decorator function to delete user messages and set commands if need

        Parameters
        ----------
        commands (`list[dict]` | None): List of dict {'command': `str`, 'description': `str`}
        """

        def decorator(func):
            async def wrapper(message: Message, command: CommandObject | None = None):
                await self.__delete_message(message)
                if commands:
                    await self.set_commands(message, commands)
                await func(message, command)
            return wrapper
        return decorator

    def decor_set_cmds(self, commands: list[dict]) -> callable:
        """
        Decorator function to set commands

        Parameters
        ----------
        commands (`list[dict]`): List of dict {'command': `str`, 'description': `str`}
        """
        
        def decorator(func):
            async def wrapper(message_query: Message | CallbackQuery, command: CommandObject | None = None):
                await self.set_commands(message_query, commands)
                await func(message_query, command)
            return wrapper
        return decorator

    def decor_del_msg(self, func: callable) -> callable:
        """ Decorator function to delete user messages """
        async def wrapper(message: Message, command: CommandObject | None = None):
            await self.__delete_message(message)
            if command and command.args:
                await func(message, command)
            else:
                await func(message)
        return wrapper

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
                    if self.CfgEng.DEBUG: print(f"{self} send chat action error: {e}")
                await func(message_query)
                try: 
                    await self.__bot.send_chat_action(chat_id=message_query.from_user.id, action='cancel')
                except Exception as e: 
                    if self.CfgEng.DEBUG: print(f"{self} send cancel chat action error: {e}")
            return wrapper
        return decorator

    async def __delete_message(self, message: Message) -> None:
        """ Asynchronously delete a message """
        try:
            await self.__bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} delete message error: {e}") 

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
            for command in commands or {}:
                cmd.append(BotCommand(command=command['command'], description=command['description']))
            chat_id = message_query.from_user.id if message_query else chat_id
            await self.__bot.set_my_commands(commands=cmd, scope=BotCommandScopeChat(chat_id=chat_id))
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} set commands error: {e}")  

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
            if self.CfgEng.DEBUG: print(f"{self} delete message error: {e}")
