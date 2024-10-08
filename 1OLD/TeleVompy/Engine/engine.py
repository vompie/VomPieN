from aiogram import Bot, Dispatcher
from .base_class import BaseClass


class SingleTonBotEngine(BaseClass):
    """ The SingleTon Bot Engine initializes `Bot` from the aiogram library and `models` to access page models """
    __instance: 'SingleTonBotEngine' = None
    __bot: Bot | None = None
    __dp: Dispatcher | None = None
    __payments_token: str | None = None
    
    def __new__(cls, token: str | None = "", payments_token: str | None = None, *args, **kwargs):
        if cls.__instance is None and not token:
            if BaseClass.CfgEng.DEBUG: print('"SingleTonBotEngine" -> need bot token to create instance')
            return cls.__instance
        if cls.__instance is None and token:
            if BaseClass.CfgEng.DEBUG: print(f'"SingleTonBotEngine" -> create instance with {token=}')
            cls.__instance = super(SingleTonBotEngine, cls).__new__(cls, *args, **kwargs)
            cls.__bot = Bot(token=token)
            cls.__dp = Dispatcher()
            cls.__payments_token = payments_token
        return cls.__instance

    def __init__(self, token: str | None = "", payments_token: str | None = None, *args, **kwargs):
        """ 
        Initializes the bot engine with the provided token and payments token
        
        Parameters
        ----------
        - token (`str` | `None`): The token for the bot
        - payments_token (`str` | `None`): The token for payments 
        
        Attributes
        ----------
        - bot (`Bot`): An instance of the `aiogram.Bot` class
        - dp (`Dispatcher`): A instance of the `aiogram.Dispatcher` class
        - payments_token (`str`): The token for payments
        """
        super().__init__(*args, **kwargs)

    @property
    def bot(self) -> Bot:
        """ Get the `bot` instance """
        return self.__bot

    @property
    def dp(self) -> Dispatcher:
        """ Get the `dp` instance """
        return self.__dp
    
    @property
    def payments_token(self) -> str:
        """ Get the payments token """
        return self.__payments_token
