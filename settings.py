import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DEBUG: bool = True
MAX_CLIENT_KEYS: int = 2

PROJECT_DIR: str = os.getenv("PROJECT_DIR") if os.getenv("PROJECT_DIR") else ''
XRAY_DIR: str = os.getenv("XRAY_DIR") if os.getenv("PROJECT_DIR") else ''

BOT_NAME: str = 'VomPieN'
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY")

DB_FILE: str = os.path.join(PROJECT_DIR, 'database/base.db').replace('\\', '/')
LOG_FILE: str = os.path.join(PROJECT_DIR, 'logs/bot_error.log').replace('\\', '/')

DEFAULT_VLESS_FILE: str = os.path.join(PROJECT_DIR, 'xray_service/default_vless.json').replace('\\', '/')
NEW_VLESS_FILE: str = os.path.join(XRAY_DIR, 'confs/vless_inbounds.json').replace('\\', '/')
LASTCOPY_VLESS_FILE: str = os.path.join(XRAY_DIR, 'backup/vless_inbounds.json').replace('\\', '/')
