from aiogram import Bot, Dispatcher

from ..Utils import dprint


class SingleTonBotEngine:
    """ The SingleTon Bot Engine initializes `Bot` from the aiogram library and `models` to access page models """
    __instance: 'SingleTonBotEngine' = None
    __bot: Bot | None = None
    __dp: Dispatcher | None = None
    __payments_token: str | None = None
    
    def __new__(cls, token: str | None = None, payments_token: str | None = None):
        if cls.__instance is None and not token:
            dprint('SingleTonBotEngine', 'need bot token to create instance')
            return cls.__instance
        if cls.__instance is None and token:
            dprint('SingleTonBotEngine', f'create instance with {token=}')
            cls.__instance = super(SingleTonBotEngine, cls).__new__(cls)
            cls.__bot = Bot(token=token)
            cls.__dp = Dispatcher()
            cls.__payments_token = payments_token
        return cls.__instance

    def __init__(self, token: str | None = None, payments_token: str | None = None):
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
        super().__init__()

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
