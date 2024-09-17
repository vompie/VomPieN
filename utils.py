from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import Message, CallbackQuery

from TeleVompy.Engine.user import User
from TeleVompy.Engine.model import Model
from TeleVompy.Interface.window import Window
from TeleVompy.Interface.interface import Interface


Models = Model().models
IF = Interface()



async def processing_basic_user_request(
        message_query: Message | CallbackQuery, 
        model_name: str | None = None,
        answer: str | None = None, 
        message_key: str | None = None, 
        set_commands: bool = False,
        action_type: str | None = None
    ) -> None:
    """
    This function processes basic user requests (like '/start', '/me', '/play', etc. and all callbacks)

    Parameters
    ----------
    - message_query (`Message` | `CallbackQuery`): Message or CallbackQuery object to process  
    - model_name (`str` | `None`): Name of the model to process the request
    - answer (`str` | `None`): Text to answer on callback
    - message_key (`str` | `None`): Key of the user messages to delete last copy of message
    - set_commands (`bool`): Flag to set commands to the bot
    - action_type (`str` | `None`): Type of Window's Messenger action
    """

    telegram_user_id = message_query.from_user.id

    # check user exist


    # answer on callback


    # delete last copy of message if need

    # send window
    if model_name and message_query:
        window: Window = Models[model_name](user=User(message_query))
        if action_type:
            window.Action.action_type = action_type 
         # use action
        await window.action()
        # delete window
        del window