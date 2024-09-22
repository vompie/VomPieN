from aiogram.filters import CommandObject
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.types import Message, CallbackQuery

from TeleVompy.Engine.engine import SingleTonBotEngine
from TeleVompy.Engine.user import User
from TeleVompy.Engine.model import Model
from TeleVompy.Interface.window import Window
from TeleVompy.Interface.interface import Interface

from settings import DEBUG, BOT_NAME, BOT_SMILE, ADMIN_SECRET_KEY, MAX_ADMINS_KEYS
from add_client import add_client
from update_client import update_client
from database.sql import create_user, get_user, update_user, get_user_keys
from database.sql import create_deeplink, get_deeplink, update_deeplink, increment_referals
from json import loads, dumps


Models = Model().models
IF = Interface()


async def send_msg(model: str, message_query: Message | CallbackQuery | None = None, chat_id: int | None = None, *args, **kwargs) -> None:
    """ This function sends an error message """
    if chat_id:
        window: Window = Models[model](user=User(chat_id=chat_id), *args, **kwargs)
    else:
        window: Window = Models[model](user=User(message_query), *args, **kwargs)
    await window.action()
    del window


async def read_deeplink(message: Message, command: CommandObject) -> bool | str:
    """ This function set admin level by payload """
    try:
        payload = loads(decode_payload(command.args))
        
        # get deeplink
        deeplink_id = payload['deeplink_id']
        deeplink = await get_deeplink(id=deeplink_id)
        if not deeplink or deeplink['is_used']:
            if DEBUG: print('Get deeplink error or deeplink already use')
            return False, False     

        # link for self
        if deeplink['tlg_id'] == message.from_user.id:
            if DEBUG: print('Cant open own deeplink')
            return False, False

        # get or create user
        user, was_created = await get_user_or_create(message_query=message, return_was_created_status=True)
        if not user:
            if DEBUG: print('Cant get or create new user')
            return False, False
        
        # if new user -> increment referals count
        if not was_created:
            await increment_referals(tlg_id=deeplink['tlg_id'])
        
        # get initiator
        initiator = await get_user(tlg_id=deeplink['tlg_id'])
        if not initiator:
            if DEBUG: print('Cant get initiator')
            return False, False
        
        # new admin
        if deeplink['type'] == 'new_admin':
            if initiator['is_banned'] or initiator['user_lvl'] < 1 or user['user_lvl'] > 0 or user['is_banned']:
                if DEBUG: print('Initiator or user was banned or initiator level < 1 or user level > 0')
                return False, False
            # update user lvl
            update_result = await update_user(tlg_id=user['tlg_id'], columns=['user_lvl'], values=[1])
            if not update_result:
                if DEBUG: print('Cant update user')
                return False, False
            await update_deeplink(id=deeplink_id, columns=['is_used'], values=[1])
            return f'Теперь ты администратор в {BOT_NAME} {BOT_SMILE}', 'AdminPanel'
        
        # new user
        elif deeplink['type'] == 'new_user':
            if not user['is_banned'] or initiator['is_banned'] or initiator['user_lvl'] < 1:
                if DEBUG: print('User not banned or initiator is banned or initiator is not admin')
                return True, 'MM'
            # unban user
            update_result = await update_user(tlg_id=user['tlg_id'], columns=['is_banned'], values=[0])
            if not update_result:
                return False, False
            # update client
            update_client_result = await update_client(tlg_id=user['tlg_id'], enabled=True)
            if not update_client_result:
                if DEBUG: print(f'Cant unban user (update client error)')
                return False, False
            await update_deeplink(id=deeplink_id, columns=['is_used'], values=[1])
            return f'С возвращением в {BOT_NAME} {BOT_SMILE}\nБольше так не хулигань', 'MM'
        
        # new key
        elif deeplink['type'] == 'new_key':
            if initiator['is_banned'] or initiator['user_lvl'] < 1 or user['is_banned']:
                if DEBUG: print('Initiator or user was banned or initiator level < 1')
                return False, False
            # max generate keys
            keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)
            max_keys = MAX_ADMINS_KEYS if initiator['user_lvl'] < 2 else 99
            if len(keys) >= max_keys:
                if DEBUG: print(f'Cant add new key: {len(keys)=} >= {max_keys=}')
                return False, False
            # add new key
            add_client_result = await add_client(tlg_id=user['tlg_id'])
            if not add_client_result:
                if DEBUG: print(f'Cant add new key (add client error)')
                return False, False
            await update_deeplink(id=deeplink_id, columns=['is_used'], values=[1])
            new_key_str = 'У тебя появился новый ключ ⤵️'
            if was_created:
                return new_key_str, 'Keys'
            return f'Добро пожаловать в {BOT_NAME} {BOT_SMILE}\nКстати! {new_key_str}', 'Keys'
    except Exception as e:
        if DEBUG: print(f'Read deeplink error: {e}')
        return False, False

async def new_deeplink(tlg_id: int, type: str) -> bool | str:
    """ This function creates deeplink for new admin / new user / new key """
    deeplink_id = await create_deeplink(tlg_id=tlg_id, type=type)  
    if not deeplink_id:
        return False
    payload = {'deeplink_id': deeplink_id}
    deeplink = await create_start_link(bot=SingleTonBotEngine().bot, payload=dumps(payload), encode=True)
    return deeplink


async def get_user_or_create(message_query: Message | CallbackQuery, return_was_created_status: bool = False) -> tuple[object, bool]:
    """ This function get user or create new user """
    was_created = True
    telegram_id = message_query.from_user.id
    username = message_query.from_user.username if message_query.from_user.username else ''
    user = await get_user(tlg_id=message_query.from_user.id)
    if not user:
        await create_user(tlg_id=telegram_id, username=username)
        was_created = False
    user = await get_user(tlg_id=message_query.from_user.id)
    if return_was_created_status:
        return user, was_created
    return user


async def check_secret_key(message: Message) -> bool:
    """ This function checks admin secret key """
    try:
        if message.text[0] != '*': 
            return False
        return message.text[1:] == ADMIN_SECRET_KEY
    except Exception as e:
        return False

async def set_new_super_admin(message: Message) -> bool:
    """ This function sets new super admin user """
    user = await get_user_or_create(message_query=message)
    if user['is_banned']:
        return
    return await update_user(tlg_id=user['tlg_id'], columns=['user_lvl'], values=[2])


async def admin_level(message_query: Message | CallbackQuery) -> bool | int:
    """ This function checks if user is admin """
    user = await get_user_or_create(message_query)
    return user['user_lvl'] if user else False

async def seppoku_admin(message_query: Message) -> bool:
    """ This function make seppoku """
    if await admin_level(message_query=message_query) > 0:
        return await update_user(tlg_id=message_query.from_user.id, columns=['user_lvl'], values=[-1])
    return False

async def unset_admin(tlg_id: int) -> bool:
    """ This function unsets admin status """
    return await update_user(tlg_id=tlg_id, columns=['user_lvl'], values=[0])


async def processing_basic_user_request(
        message_query: Message | CallbackQuery, 
        model_name: str | None = None,
        answer: str | None = None, 
        message_key: str | None = None, 
        set_commands: bool = False,
        action_type: str | None = None
    ) -> None:
    """
    This function processes basic user requests ('/start', '/menu', '/profile', '/new_key', '/seppoku', '/admin_panel' and all callbacks)

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
        'internal_error': 'Пумпумпум... ошибочка вышла',

        'user_admin_not_select': 'Нужно кого-нибудь выбрать',
        'user_not_select': 'Нужно выбрать пользователя',
        'admin_not_select': 'Нужно выбрать администратора',
        'key_not_select': 'Нужно выбрать ключ',

        'cant_demoted': 'Нельзя разжаловать этого пользователя',
        'cant_promotion': 'Нельзя повысить этого пользователя',
        'cant_ban': 'Нельзя забанить этого пользователя',
        'cant_unban': 'Нельзя разбанить этого пользователя',
        'cant_create_key': 'Нельзя создать еще один ключ'
    }

    # create user if not exist
    user: dict = await get_user_or_create(message_query=message_query)
    if not user:
        return await send_msg(message_query=message_query, model='ErrorMsg')

    # update commands
    if set_commands:
        await set_commands_to_user(message_query=message_query, user=user)

    # answer on callback
    if isinstance(message_query, CallbackQuery):
        await message_query.answer(answers.get(answer, ''))

    # delete last copy of message if need
    if message_key and not action_type:
        await IF.delete_message(chat_id=user['tlg_id'], msg_id=user[message_key])

    # if user is banned
    if user['is_banned']:
        return await send_msg(message_query=message_query, model='BanMsg')

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


async def set_commands_to_user(message_query: Message | CallbackQuery, user: dict) -> None:
    """ This function sets commands to the bot """
    commands = [
        {'command': 'menu', 'description': f'🌐 Меню {BOT_NAME}'},
        {'command': 'profile', 'description': f'{BOT_SMILE} Профиль'},
        {'command': 'new_key', 'description': '🔑 Новый ключ'},
    ]
    if user['user_lvl'] > 0:
        commands.append({'command': 'admin_panel', 'description': '🦇 Администрирование'})
    if user['is_banned']:
        commands = [{'command': 'menu', 'description': '☠️ Заблокирован'}]    
    await IF.set_commands(message_query=message_query, commands=commands)
