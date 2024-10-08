from aiogram.filters.command import Command
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from .model import Model


class Filter:
    """
    A class to handle filters for Telegram bot
        
    Methods
    -------
    * __init__(self, Models: `dict`) -> `None`: Initializes the Filters class
    * CommandStart(self, deep_link: `bool` = `False`, deep_link_encoded: `bool` = `False`, ignore_case: `bool` = `False`, ignore_mention: `bool` = `False`) -> `CommandStart
    * Command(self, commands: `str` | `list` = `None`, prefix: `str` = "/", ignore_case: `bool` = `False`, ignore_mention: `bool` = `False`) -> `Command`
    * Model(self, call: `CallbackQuery`) -> `bool`: Return `True` if the callback data is a model
    * ModelBlock(self, call: `CallbackQuery`) -> `bool`: Return `True` if the callback data starts with '#'
    """
    
    def __init__(self):
        """ A class to handle filters for Telegram bot """
        super().__init__()
        self.__models: dict = Model().models

    def Command(self, commands: str | list = None, prefix: str = "/", ignore_case: bool = False, ignore_mention: bool = False, *args, **kwargs) -> Command:
        """ Check if the message starts with the command """
        kwargs['commands'] = commands
        kwargs['prefix'] = prefix
        kwargs['ignore_case'] = ignore_case
        kwargs['ignore_mention'] = ignore_mention
        return Command(*args, **kwargs)

    def CommandStart(self, deep_link: bool = False, deep_link_encoded: bool = False, ignore_case: bool = False, ignore_mention: bool = False, *args, **kwargs) -> CommandStart:
        """ Check if the message starts with '/start' and has deeplink """
        kwargs['deep_link'] = deep_link
        kwargs['deep_link_encoded'] = deep_link_encoded
        kwargs['ignore_case'] = ignore_case
        kwargs['ignore_mention'] = ignore_mention
        return CommandStart(*args, **kwargs)

    def Model(self, call: CallbackQuery) -> bool:
        """ Check if the callback data is a model """
        return any(list(map(lambda key: key in call.data, self.__models.keys())))

    def ModelBlock(self, call: CallbackQuery) -> bool:
        """ Check if the callback data starts with '#' then it blocked model """
        return call.data[0] == '#'
