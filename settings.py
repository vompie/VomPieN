import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DEBUG: bool = True
HOME_DIR: str = os.getenv("PROJECT_DIR") if os.getenv("PROJECT_DIR") else ''
BOT_NAME: str = 'VomPieN'
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY")
DB_FILE: str = os.path.join(HOME_DIR, 'DB/database.sqlite').replace('\\', '/')
LOGS_FILE: str = os.path.join(HOME_DIR, 'Logs/bot_error.log').replace('\\', '/')
DEFAULT_VLESS_FILE: str = os.path.join(HOME_DIR, 'xray_service/default_vless.json').replace('\\', '/')
