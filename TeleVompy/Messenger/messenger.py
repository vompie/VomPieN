from aiogram.types import Message
from ..Engine.engine import SingleTonBotEngine
from ..Engine.model import Model
from ..Utils import BaseClass, dprint

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aiogram import Bot
    from ..Engine.user import User
    from ..Components.Page.page import Page, Content, Payload


class EditMessageError(Exception):
    def __init__(self, text):
        """ Initialize EditMessageError exception with error message """
        super().__init__(text)


class Messenger(BaseClass):
    """
    The parent class for child Action classes. 
        Initializes `bot`, `User`, `Page`, `Content`, `Models`, `relayed_payload` instances and `EditMesasgeError` for errors.
        The child class must have the `async execute` method, which will be called when sending the Window. 
        The `execute` method can be decorated with the `@Messenger.messenger_execute` method.
        For additional parameters for performing functions of the `aiogram.Bot` object, you can pass parameters to `kwargs`. Only for parameters that EXIST in the called methods of the `aiogram.Bot` object

    Attributes
    ----------
    - bot (`Bot`): The Bot instance for sending messages
    - payments_token (`str`): The token for payments    
    - User (`User`): The User instance for sending messages
    - Page (`Page`): The Page instance for content of sending messages  
    - Content (`Content`): The Content instance for Page    
    - Models (`Model`): The Model instance for getting models
    - relayed_payload (`Payload`): The relayed payload instance 
    - EditMessageError (`EditMessageError`): The exception for error handling when editing messages 
    - args (`Any`): Additional arguments for the Messenger class
    - kwargs (`Any`): Additional keyword arguments for the Messenger class
    """

    def __init__(self, user: 'User', page: 'Page', *args, **kwargs):
        """
        Initialize Messenger class with User and Page instances
        
        Parameters
        ----------
        - user (`User`): User instance for sending messages
        - page (`Page`): Page instance containing message content and settings
        """

        super().__init__()
        self.__bot: Bot = SingleTonBotEngine().bot # # a instance of bot object
        self.__payments_token: str = SingleTonBotEngine().payments_token # a payments token
        self.__User: User = user # a instance of User object
        self.__Page: Page = page # a instance of Page object
        self.__Content: Content = self.__Page.Content if self.__Page else None # a Content
        self.__Models: Model = Model().models # a instance of Model object
        self.__relayed_payload: Payload = self.__Page.relayed_payload # relayed payload
        self.__EditMessageError: EditMessageError = EditMessageError # EditMessageError exception with error message
        self.args = args # additional arguments for the Messenger class
        self.kwargs = kwargs # additional keyword arguments for the Messenger class

    @property
    def bot(self) -> 'Bot':
        """ Returns the Bot instance """
        return self.__bot

    @property
    def payments_token(self) -> 'str':
        """ Returns the payments token """
        return self.__payments_token

    @property
    def User(self) -> 'User':
        """ Returns the User instance """
        return self.__User

    @property
    def Page(self) -> 'Page':
        """ Returns the Page instance """
        return self.__Page
    
    @property
    def Content(self) -> 'Content':
        """ Returns the Content instance """
        return self.__Content
    
    @property
    def Models(self) -> Model:
        """ Returns the Model instance """
        return self.__Models    

    @property
    def relayed_payload(self) -> 'Payload': 
        """ Returns the relayed Payload object """
        return self.__relayed_payload
    
    @property
    def EditMessageError(self) -> EditMessageError:
        """ Returns the MessageError instance """
        return self.__EditMessageError

    def messenger_execute(func: callable):
        """ Decorator for executing a function with Messenger's context """
        async def wrapper(self: 'Messenger', *args, **kwargs) -> Message | bool:
            """ 
            Execute the Messengerr decorated function 
            
            Parameters
            ----------
            - func (`callable`): The decorated function to execute
            - args (`Any`): Positional arguments to be passed to the decorated function
            - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object
            
            Returns
            ------- 
            - message (`Message | bool`): The Message object returned by the decorated function, or `False` if an error occurred, or `True` for other
            """

            try:
                message: Message | bool = await func(self, *args, **kwargs)
                
                # update message_id
                if isinstance(message, Message):
                    self.__User.msg_id = message.message_id
                return message
            except self.__EditMessageError as e:
                dprint(self, f"edit message error: {e}")
            except Exception as e:
                dprint(self, f"execute error: {e}")
        return wrapper
