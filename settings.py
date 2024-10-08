import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DEBUG: bool = True

PROJECT_DIR: str = os.getenv("PROJECT_DIR") if os.getenv("PROJECT_DIR") else ''
XRAY_DIR: str = os.getenv("XRAY_DIR") if os.getenv("PROJECT_DIR") else ''

BOT_NAME: str = os.getenv("BOT_NAME")
BOT_SMILE: str = '🧛🏻'
BOT_TOKEN: str = os.getenv("BOT_TOKEN")
ADMIN_SECRET_KEY: str = os.getenv("ADMIN_SECRET_KEY")

MAX_CLIENT_KEYS: int = 2
MAX_ADMINS_KEYS: int = 5
ALLOW_GENERATE: bool = int(os.getenv('ALLOW_GENERATE')) if os.getenv('ALLOW_GENERATE') else False

DB_FILE: str = os.path.join(PROJECT_DIR, 'database/base.db').replace('\\', '/')
DEFAULT_VLESS_FILE: str = os.path.join(PROJECT_DIR, 'xray_service/default_vless.json').replace('\\', '/')
VLESS_FILE: str = os.path.join(XRAY_DIR, 'confs/vless_inbounds.json').replace('\\', '/')
COPY_VLESS_FILE: str = os.path.join(XRAY_DIR, 'backup/vless_inbounds.json').replace('\\', '/')
STATS_FILE: str = os.path.join(PROJECT_DIR, 'statistics.json').replace('\\', '/')

PROTOCOL: str = 'vless'
SERVER_TYPE: str = 'http'
FINGERPRINT: str = 'random'
SECURITY: str = 'reality'
ALPN: str = 'h2'
OBFS: str = 'h2'
PACKET_ENCODING: str = 'xudp'

SERVER_IP: str = os.getenv("SERVER_IP")
SERVER_PORT: str = os.getenv("VLESS_PORT")
API_PORT: str = os.getenv("API_PORT")
SNI: str = os.getenv("REALITY_SERVER_NAMES")
HOST: str = os.getenv("HTTP_HOST")
PATH: str = os.getenv("HTTP_PATH")
PUBLICK_KEY: str = os.getenv("REALITY_PUBLICK_KEY")
ENCRYPTION: str = os.getenv("SERVER_ENCRYPTION")

TEMPLATE_KEY: str = f'{PROTOCOL}://UUID_KEY_HERE@{SERVER_IP}:{SERVER_PORT}/?encryption={ENCRYPTION}&type={SERVER_TYPE}&sni={SNI}&host={HOST}&path={PATH}&fp={FINGERPRINT}&security={SECURITY}&alpn={ALPN}&obfs={OBFS}&pbk={PUBLICK_KEY}&packetEncoding={PACKET_ENCODING}#{BOT_NAME}'
