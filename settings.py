import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

home_dir: str = os.getenv("HOME_DIR")
bot_name: str = 'VomPieN'
bot_token: str = os.getenv("BOT_TOKEN")
