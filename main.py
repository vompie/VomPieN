import asyncio
from bot_service.bot import main


def start_bot():
    asyncio.run(main())


if __name__ == '__main__':
    start_bot()
