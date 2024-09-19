import os, shutil
from json import loads, dumps
from uuid import uuid1

from database.sql import add_new_client, get_clients, delete_client_by_id


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

async def delete_client(id: int) -> bool:
    """ Delete a client from the database """
    return await delete_client_by_id(id=id)

async def enabled_clients() -> bool | object:
    """ Get enabled clients """
    return await get_clients(type=True)

async def disabled_clients() -> bool | object:
    """ Get disabled clients """
    return await get_clients(type=False)

async def clients() -> bool | object:
    """ Get clients """
    return await get_clients(type=None)

def make_new_vless(vless: dict, clients: list) -> dict:
    """ Make a new vless configuration file with the given clients """
    all_clients = [{"id": c['uuid'], "email": c['email'], "level": c['level']} for c in clients]
    vless['settings']['clients'] = all_clients
    return vless

def make_copy_vless(old_file: str, new_file: str) -> bool:
    """ Make a copy of the vless configuration file """
    try:
        shutil.copyfile(old_file, new_file)
    except Exception as e:
        print(f"Error making copy of vless file: {e}")
        return False
    return True

def save_vless_file(vless: dict, file: str) -> bool:
    """ Save the vless configuration file """
    with open(file, 'w') as f:
        f.write(dumps(vless))
    return True
