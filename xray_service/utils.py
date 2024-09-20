import os, shutil, aiofiles
from json import loads, dumps
from uuid import uuid1

from database.sql import create_database, add_new_client, get_clients, delete_client


async def prepare_server(file: str) -> dict:
    """ Prepare the server """
    # create database
    await create_database()
    # get default vless
    return await get_default_vless(file=file)


async def get_default_vless(file: str) -> dict:
    """ Get the default vless data """
    async with aiofiles.open(file, 'r') as f:
        inbounds = loads(f.read())
    vless = inbounds['inbounds'][0]
    """ Set the default secret vless parameters """
    vless['listen'] = os.getenv('SERVER_IP')
    vless['port'] = os.getenv('VLESS_PORT')
    vless['streamSettings']['httpSettings']['host'] = [os.getenv('HTTP_HOST')]
    vless['streamSettings']['httpSettings']['path'] = os.getenv('HTTP_PATH')
    vless['streamSettings']['realitySettings']['dest'] = os.getenv('REALITY_DEST')
    vless['streamSettings']['realitySettings']['serverNames'] = [os.getenv('REALITY_SERVER_NAMES')]
    vless['streamSettings']['realitySettings']['privateKey'] = os.getenv('REALITY_PRIVATE_KEY')
    return vless

async def make_and_save_vless(vless: dict, old_file: str, new_file: str) -> bool:
    """ Make a new vless configuration file and save it """
    # make new vless
    vless: dict = await make_new_vless(vless=vless, enabled=True)
    # copy last vless file
    copy_result: bool = await make_copy_vless(from_file=old_file, to_file=new_file)
    if not copy_result:
        return False
    # save new vless file
    save_result: bool = await save_vless_file(vless=vless, file=new_file)
    if not save_result:
        return False
    return True


async def create_and_save_client(tlg_id: str, level: int, enabled: bool = True) -> bool | int:
    """ Save a new client to the database """
    return await add_new_client(tlg_id=tlg_id, uuid=str(uuid1()), email=f"{tlg_id}@telegram.id", level=level, enabled=enabled)

async def delete_client_by_id(id: int) -> bool:
    """ Delete a client from the database """
    return await delete_client(id=id)


async def make_new_vless(vless: dict, enabled: bool | None = True) -> dict:
    """ Get clients all / enabled / disabled """
    clients = await get_clients(type=enabled)
    """ Make a new vless configuration file with the given clients """
    all_clients = [{"id": client['uuid'], "email": client['email'], "level": client['level']} for client in clients]
    vless['settings']['clients'] = all_clients
    return vless

async def make_copy_vless(from_file: str, to_file: str) -> bool:
    """ Make a copy of the vless configuration file """
    try:
        shutil.copyfile(from_file, to_file)
    except Exception as e:
        print(f"Error making copy of vless file: {e}")
        return False
    return True

async def save_vless_file(vless: dict, file: str) -> bool:
    """ Save the vless configuration file """
    async with aiofiles.open(file, 'w') as f:
        await f.write(dumps(vless))
    return True


async def reboot_server() -> bool:
    # restart xray
    # check status
    return True
    # back copy of last vless file
    # copy_result: bool = make_copy_vless(old_file=LASTCOPY_VLESS_FILE, new_file=NEW_VLESS_FILE)
    # restart xray
    return False
