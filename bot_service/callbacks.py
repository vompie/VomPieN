from aiogram.types import CallbackQuery
from bot_service.utils import IF, processing_basic_user_request


async def model_callbacks(call: CallbackQuery):
    """
    This function handles Model callback queries

    Parameters
    ----------
    call (`CallbackQuery`): The aiogram CallbackQuery object containing the callback data
    """

    model = call.data.split(";", maxsplit=1)[0]
    await processing_basic_user_request(message_query=call, model_name=model)


@IF.decor_send_n_cancel_action()
async def block_callbacks(call: CallbackQuery):
    """
    This function handles blocking callback queries

    Parameters
    ----------
    call (`CallbackQuery`): The aiogram CallbackQuery object containing the callback data   
    """

    answer = call.data[1:].split(";", maxsplit=1)[0]
    await processing_basic_user_request(message_query=call, answer=answer)


@IF.decor_send_n_cancel_action()
async def other_callback(call: CallbackQuery):
    """
    This function handles other callback queries

    Parameters
    ----------
    call (`CallbackQuery`): The aiogram CallbackQuery object containing the callback data
    """
    
    print("model not found", call.data)
    await processing_basic_user_request(message_query=call)
