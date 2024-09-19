from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import Message, CallbackQuery

from TeleVompy.Engine.user import User
from TeleVompy.Engine.model import Model
from TeleVompy.Interface.window import Window
from TeleVompy.Interface.interface import Interface

from settings import BOT_NAME, ADMIN_SECRET_KEY
from database.sql import create_user, get_user, update_user


Models = Model().models
IF = Interface()


def extract_payload(command: CommandObject) -> str:
    """ This function processes the command with deeplink and returns the payload """
    return decode_payload(command.args)


async def set_deeplink_admin(message: Message, command: CommandObject) -> None:
    """ This function set admin level by payload """
    token = extract_payload(command=command)
    # if token_user_id.level_admin > 1:
    # await set_new_admin(tlg_id=message.from_user.id)


async def wellcome_to_the_bot(message: Message) -> bool | object:
    """ This function handles the wellcome to the game process """
    # get base information
    telegram_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else ''
    # create user
    user = await create_user(tlg_id=telegram_id, username=username)
    return user


async def get_user_or_create(message: Message) -> object:
    """ This function gets user or creates new user """
    await wellcome_to_the_bot(message=message)
    user = await get_user(tlg_id=message.from_user.id)
    return user


async def send_error(message_query: Message | CallbackQuery, model: str = 'ErrorMsg') -> None:
    """ This function sends an error message """
    window: Window = Models[model](user=User(message_query))
    await window.action()
    del window


async def check_secret_key(message_query: Message) -> bool:
    """ This function checks admin secret key """
    try:
        if message_query.text[0] != '*': 
            return False
        return message_query.text[1:] == ADMIN_SECRET_KEY
    except Exception as e:
        return False


async def set_new_super_admin(tlg_id: int) -> bool:
    """ This function sets new super admin user """
    return await update_user(tlg_id=tlg_id, columns=['is_admin'], values=[2])


async def set_new_admin(tlg_id: int) -> bool:
    """ This function sets new admin user """
    return await update_user(tlg_id=tlg_id, columns=['is_admin'], values=[1])


async def demoted_admin(tlg_id: int) -> bool:
    """ This function demotes admin user """
    return await update_user(tlg_id=tlg_id, columns=['is_admin'], values=[-1])


async def unset_admin(tlg_id: int) -> bool:
    """ This function unsets admin status """
    return await update_user(tlg_id=tlg_id, columns=['is_admin'], values=[0])


async def admin_level(message_query: Message | CallbackQuery) -> bool | int:
    """ This function checks if user is admin """
    user = await get_user(message_query.from_user.id)
    return user['is_admin'] if user else False


async def seppoku_admin(message_query: Message) -> bool:
    """ This function make seppoku """
    user = await get_user_or_create(message=message_query)
    if user['is_admin'] > 0:
        return await demoted_admin(tlg_id=user['tlg_id'])
    return False


async def processing_basic_user_request(
        message_query: Message | CallbackQuery, 
        model_name: str | None = None,
        answer: str | None = None, 
        message_key: str | None = None, 
        set_commands: bool = False,
        action_type: str | None = None
    ) -> None:
    """
    This function processes basic user requests (like '/start', '/profile', '/key', etc. and all callbacks)

    Parameters
    ----------
    - message_query (`Message` | `CallbackQuery`): Message or CallbackQuery object to process  
    - model_name (`str` | `None`): Name of the model to process the request
    - answer (`str` | `None`): Text to answer on callback
    - message_key (`str` | `None`): Key of the user messages to delete last copy of message
    - set_commands (`bool`): Flag to set commands to the bot
    - action_type (`str` | `None`): Type of Window's Messenger action
    """

    # template answers for blocked callbacks
    answers = {
        'user_not_select': 'Нужно выбрать пользователя',
        'admin_not_select': 'Нужно выбрать администратора',
        'key_not_select': 'Нужно выбрать ключ доступа',

        'cant_demoted': 'Нельзя разжаловать этого пользователя',
        'cant_promotion': 'Нельзя повысить этого пользователя',
        'cant_ban': 'Нельзя забанить этого пользователя',
        'cant_unban': 'Нельзя разабанить этого пользователя',
        'cant_create_key': 'Вы не можете создать еще один ключ доступа'
    }

    # create user if not exist
    user: dict = await get_user_or_create(message=message_query)

    # update commands
    if set_commands or user['is_admin'] == -1:
        await set_commands_to_user(message_query=message_query, is_admin=user['is_admin'], is_banned=user['is_banned'])

    # answer on callback
    if isinstance(message_query, CallbackQuery) and answer:
        await message_query.answer(answers.get(answer, ''))

    # delete last copy of message if need
    if message_key and not action_type:
        await IF.delete_message(chat_id=user['tlg_id'], msg_id=user[message_key])

    # if user is banned
    if user['is_banned']:
        await send_error(message_query=message_query, model='BanMsg')
        return

    # send window
    if model_name and message_query:
        window: Window = Models[model_name](user=User(message_query))
        if action_type:
            window.Action.action_type = action_type 
         # use action
        await window.action()
        # update message id
        if message_key and not action_type:
            await update_user(tlg_id=user['tlg_id'], columns=[message_key], values=[window.User.msg_id])
        # delete window
        del window


async def set_commands_to_user(message_query: Message | CallbackQuery, is_admin: bool = False, is_banned: bool = False) -> None:
    """ This function sets commands to the bot """
    commands = [
        {'command': 'menu', 'description': f'🌐 Меню {BOT_NAME}'},
        {'command': 'profile', 'description': '🧛🏻 Личный кабинет'},
        {'command': 'new_key', 'description': '🔑 Новый ключ'},
    ]
    if is_admin > 0:
        commands.append({'command': 'admin_panel', 'description': '🦇 Администрирование'})
    if is_banned:
        commands = [{'command': 'menu', 'description': '☠️ Заблокирован'}]    
    await IF.set_commands(message_query=message_query, commands=commands)
    if is_admin == -1:
        await unset_admin(tlg_id=message_query.from_user.id)
