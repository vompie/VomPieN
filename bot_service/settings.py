import os

from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
print(os.path.join(os.path.dirname(__file__), '.env'))

HOME_DIR: str = os.getenv("HOME_DIR") if os.getenv("HOME_DIR") else ''
BOT_NAME: str = 'VomPieN'
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY")
DB_FILE: str = f'{HOME_DIR}DB/database.sqlite'
LOGS_FILE: str = f'{HOME_DIR}Logs/bot_error.log'
DEBUG: bool = True
