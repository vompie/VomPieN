import os
from json import loads, dumps
from uuid import uuid1

from DB.sql import add_new_client, get_enabled_clients, get_disabled_clients, get_clients


def get_default_vless(file: str) -> dict:
    """ Get the default vless data """
    with open(file, 'r') as f:
        inbounds = loads(f.read())
        return inbounds['inbounds'][0]

def set_vless_params(vless: dict) -> dict:
    """ Set the default secret vless parameters """
    vless['listen'] = os.getenv('SERVER_IP')
    vless['port'] = os.getenv('VLESS_PORT')
    vless['streamSettings']['httpSettings']['host'] = [os.getenv('HTTP_HOST')]
    vless['streamSettings']['httpSettings']['path'] = os.getenv('HTTP_PATH')
    vless['streamSettings']['realitySettings']['dest'] = os.getenv('REALITY_DEST')
    vless['streamSettings']['realitySettings']['serverNames'] = [os.getenv('REALITY_SERVER_NAMES')]
    vless['streamSettings']['realitySettings']['privateKey'] = os.getenv('REALITY_PRIVATE_KEY')
    return vless

def create_client(tlg_id: str, level: int) -> dict:
    """ Create a new client """ 
    client = {
        'id': str(uuid1()),
        'email': f"{tlg_id}@telegram.id",
        'level': level
    }
    return client

async def save_client(tlg_id: int, client: dict, enabled: bool = True) -> bool | int:
    """ Save a new client to the database """
    return await add_new_client(tlg_id=tlg_id, uuid=client['id'], email=client['email'], level=client['level'], enabled=enabled)

async def enabled_clients() -> bool | object:
    """ Get enabled clients """
    return await get_enabled_clients()

async def disabled_clients() -> bool | object:
    """ Get disabled clients """
    return await get_disabled_clients()

async def clients() -> bool | object:
    """ Get clients """
    return await get_clients()
