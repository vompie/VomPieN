from aiogram.types import Message, CallbackQuery

from ..Utils import BaseClass


class User(BaseClass):
    """
    A class to handle Telegram messages and callback queries

    Attributes
    ----------
    - chat_id (`int` | `None`): The ID of the chat where the message or callback query originated
    - msg_id (`int` | `None`): The ID of the message or callback query
    - payload (`str` | `None`): The payload of the message or callback query
    - from_user (`bool` | `None`): A flag indicating whether the message or callback query is from a user or bot
    - query (`CallbackQuery` | `None`): The instance of self CallbackQuery object

    Methods
    -------
    * __init__(`self`, message_query: `Message` | `CallbackQuery` | `User` | `None`, chat_id: `int` | `None`) -> `None`: 
        Initializes the User object with the given Message or CallbackQuery or User instance or (None and chat_id)
    * copy(`User`) -> `User`: Returns a copy of the `User` object without msg_id and payload
    """

    def __init__(self, message_query: 'Message | CallbackQuery | User | None' = None, chat_id: int | None = None):
        """ Initializes the User object with the given Message or CallbackQuery or User instance or (None and chat_id) """
        super().__init__()
        self.__chat_id: int | None = None
        self.__msg_id: int | None = None
        self.__from_user: bool = False
        self.__payload: str | None = None
        self.__query: CallbackQuery | None = None

        # if the message_query type is a message
        if isinstance(message_query, Message):
            self.__message_instance(message=message_query)

        # if the message_query type is a callback query
        elif isinstance(message_query, CallbackQuery):
            self.__callback_query_instance(callback_query=message_query)
        
        # if the message_query type is an User object
        elif isinstance(message_query, User):
            self.__user_instance(user=message_query)

        # if the message_query is None and chat_id type is an Int 
        elif isinstance(chat_id, int) and message_query is None:
            self.__naked_user_instance(chat_id=chat_id)

    @property
    def chat_id(self) -> int:
        """ Returns the ID of the chat where the message or callback query originated """
        return self.__chat_id
    
    @property
    def msg_id(self) -> int:
        """ Returns the ID of the message or callback query """
        return self.__msg_id
    
    @msg_id.setter
    def msg_id(self, id: int) -> None:
        """ Sets the ID of the message or callback query """
        self.__msg_id = id

    @property
    def payload(self) -> str:
        """ Returns the payload of the message or callback query """
        return self.__payload
 
    @payload.setter
    def payload(self, new_payload: str | None = '') -> None:
        """
        Sets the payload of the message or callback query

        Parameters
        ----------
        new_payload (`str` | `None`): The new payload. If None, the payload is set to an empty string
        """
        self.__payload = new_payload

    @property
    def from_user(self) -> bool:
        """ Returns a flag indicating whether the message or callback query is from a user """
        return self.__from_user

    @property
    def query(self) -> CallbackQuery:
        """ Returns the callback query object if the message type is a callback query, None otherwise """
        return self.__query

    def __message_instance(self, message: Message) -> None:
        """ Creates a new User instance from the Message object """
        self.__chat_id = message.from_user.id 
        self.__msg_id = message.message_id
        self.__from_user = not message.from_user.is_bot
        self.__payload = message.text

    def __callback_query_instance(self, callback_query: CallbackQuery) -> None:
        """ Creates a new User instance from the CallbackQuery object """
        self.__chat_id = callback_query.from_user.id 
        self.__msg_id = callback_query.message.message_id
        self.__payload = callback_query.data
        self.__query = callback_query

    def __user_instance(self, user: 'User') -> None:
        """ Creates a new User instance from the other User object """
        self.__chat_id = user.chat_id
        self.__from_user = user.from_user
        self.__query = user.query

    def __naked_user_instance(self, chat_id: int) -> None:
        """ Creates a new naked User instance from the given chat_id """
        self.__chat_id = chat_id

    def copy(self) -> 'User':
        """ Returns a copy of the User object without msg_id and payload """
        return User(self)
