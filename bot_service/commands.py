from aiogram.types import Message
from aiogram.filters import CommandObject
from bot_service.utils import IF, get_user_or_create, send_error, processing_basic_user_request
from bot_service.utils import set_deeplink_admin, check_secret_key, set_new_super_admin, admin_level, seppoku_admin

from TeleVompy.config import Cfg
from settings import BOT_NAME


# /start *deep_link*
@IF.decor_del_msg
async def cmd_start_deeplink(message: Message, command: CommandObject):
    """ This function handles the '/start deep_link' command. It processes the command with deeplink, creates a user and set admin level """
    user = await get_user_or_create(message_query=message)
    if not user:
        return await send_error(message_query=message)
    await message.answer(text=f'Добро пожаловать в {BOT_NAME} 🧛🏻', message_effect_id=Cfg.CfgMessageEffect.PETARD)
    await set_deeplink_admin(message=message, command=command)
    await cmd_menu(message=message)


# /start
@IF.decor_del_msg
async def cmd_start(message: Message):
    """ This function handles the '/start' command. It try to create user """
    user = await get_user_or_create(message_query=message)
    if not user:
        return await send_error(message_query=message)
    await message.answer(text=f'Добро пожаловать в {BOT_NAME} 🧛🏻', message_effect_id=Cfg.CfgMessageEffect.PETARD)
    await cmd_menu(message=message)


# /menu
@IF.decor_del_msg
async def cmd_menu(message: Message):
    """ This function handles the '/menu' command. It triggers the base action of the 'MM' model """
    await processing_basic_user_request(message_query=message, model_name='MM', message_key='main_msg_id', set_commands=True)


# /new_key
@IF.decor_del_msg
async def cmd_new_key(message: Message):
    """ This function handles the '/new_key' command. It triggers the base action of the 'NewKey' model """
    await processing_basic_user_request(message_query=message, model_name='NewKey', message_key='main_msg_id')


# /profile
@IF.decor_del_msg
async def cmd_profile(message: Message):
    """ This function handles the '/profile' command. It triggers the base action of the 'Profile' model """
    await processing_basic_user_request(message_query=message, model_name='Profile', message_key='main_msg_id')


# /admin_panel
@IF.decor_del_msg
async def cmd_admin_panel(message: Message):
    """ This function handles the '/admin_panel' command. It triggers the base action of the 'AdminPanel' model """
    if await admin_level(message_query=message) > 0:
        return await processing_basic_user_request(message_query=message, model_name='AdminPanel', message_key='main_msg_id')
    await processing_basic_user_request(message_query=message, model_name='MM', message_key='main_msg_id', set_commands=True) 


# /seppoku
@IF.decor_del_msg
async def cmd_seppoku(message: Message):
    """ This function handles the '/seppoku' command """
    await seppoku_admin(message_query=message)
    await processing_basic_user_request(message_query=message, model_name='MM', message_key='main_msg_id')


# other messages
@IF.decor_del_msg
async def other_msgs(message: Message, command: CommandObject | None = None):
    """ This function handles other messages """
    if (is_secret_key:=await check_secret_key(message=message)):
        await set_new_super_admin(message=message)
    await processing_basic_user_request(message_query=message, model_name='MM', message_key='main_msg_id', set_commands=is_secret_key)
