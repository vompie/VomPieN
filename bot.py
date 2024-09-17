from TeleVompy.Engine.engine import SingleTonBotEngine
from TeleVompy.Interface.filters import Filters
from settings import bot_token

# import logging

# Включите логирование
# logging.basicConfig(level=logging.INFO)

Engine = SingleTonBotEngine(token=bot_token)
Filter = Filters()


# Main loop
async def main():
    from commands import cmd_start, other_msgs
    from callbacks import model_callbacks, block_callbacks, other_callback

    # Registration commands
    # Engine.dp.message.register(cmd_start, Filter.Command("start"))
    Engine.dp.message.register(other_msgs, )

    # Registration callbacks
    Engine.dp.callback_query.register(model_callbacks, Filter.model)
    Engine.dp.callback_query.register(block_callbacks, Filter.blocked_model)
    Engine.dp.callback_query.register(other_callback, )

    # Start bot polling
    await Engine.dp.start_polling(Engine.bot, skip_updates=True)
