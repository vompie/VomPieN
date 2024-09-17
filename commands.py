from aiogram.types import Message
from aiogram.filters import CommandObject
from utils import IF, processing_basic_user_request


# /start
@IF.decor_del_msg
async def cmd_start(message: Message):
    """ This function handles the '/start' command. It try to create user and character """
    # character = await wellcome_to_the_game(message=message)
    # if character:
    #     # user and character was created
    #     await message.answer(GlobalTexts.wellcome)
    # await cmd_menu(message=message)
    pass


# other messages
@IF.decor_del_msg
async def other_msgs(message: Message, command: CommandObject | None = None):
    """ This function handles other messages """
    await processing_basic_user_request(message_query=message, model_name='MM')
    # await processing_basic_user_request(message_query=message, set_commands=True)
