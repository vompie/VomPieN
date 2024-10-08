from TeleVompy import SingleTonBotEngine, Filter

from settings import BOT_TOKEN


Engine = SingleTonBotEngine(token=BOT_TOKEN)
Filter = Filter()


# Main loop
async def main():
    from bot_service.commands import cmd_start_deeplink, cmd_start, cmd_menu, cmd_new_key, cmd_profile, cmd_admin_panel, cmd_seppoku, other_msgs
    from bot_service.callbacks import model_callbacks, block_callbacks, other_callback
    from database.sql import create_database

    # Create database and tables
    await create_database()

    # Registration commands
    Engine.dp.message.register(cmd_start_deeplink, Filter.CommandStart(deep_link=True))
    Engine.dp.message.register(cmd_start, Filter.Command("start"))
    Engine.dp.message.register(cmd_menu, Filter.Command("menu"))
    Engine.dp.message.register(cmd_new_key, Filter.Command("new_key"))
    Engine.dp.message.register(cmd_profile, Filter.Command("profile"))
    # Admin commands
    Engine.dp.message.register(cmd_admin_panel, Filter.Command("admin_panel"))
    Engine.dp.message.register(cmd_seppoku, Filter.Command("seppoku"))
    Engine.dp.message.register(other_msgs, )

    # Registration callbacks
    Engine.dp.callback_query.register(model_callbacks, Filter.Model)
    Engine.dp.callback_query.register(block_callbacks, Filter.ModelBlock)
    Engine.dp.callback_query.register(other_callback, )

    # Start bot polling
    await Engine.dp.start_polling(Engine.bot, skip_updates=True)
