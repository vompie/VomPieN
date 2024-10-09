import os, shutil, aiofiles, subprocess
from json import loads, dumps
from uuid import uuid1

from database.sql import create_database, add_new_client, get_clients, delete_client, update_client, update_client_by_tlg_id


async def prepare_server(file: str) -> dict:
    """ Prepare the server """
    await create_database()
    return await get_default_vless(file=file)

async def apply_changes_server(from_file: str, to_file: str) -> bool:
    """ Apply changes to the server """
    # reboot server
    reboot_result = await reboot_server()
    if not reboot_result:
        # recovery server
        recovery_result = await recovery_server(from_file=from_file, to_file=to_file)
        if not recovery_result:
            print("Pzdc, that's all")
        return False
    return True



async def get_default_vless(file: str) -> dict:
    """ Get the default vless data """
    async with aiofiles.open(file, 'r') as f:
        inbounds = loads(await f.read())
    vless = inbounds['inbounds'][0]
    """ Set the default secret vless parameters """
    vless['listen'] = os.getenv('SERVER_IP')
    vless['port'] = int(os.getenv('VLESS_PORT'))
    vless['streamSettings']['httpSettings']['host'] = [os.getenv('HTTP_HOST')]
    vless['streamSettings']['httpSettings']['path'] = os.getenv('HTTP_PATH')
    vless['streamSettings']['realitySettings']['dest'] = os.getenv('REALITY_DEST')
    vless['streamSettings']['realitySettings']['serverNames'] = [os.getenv('REALITY_SERVER_NAMES')]
    vless['streamSettings']['realitySettings']['privateKey'] = os.getenv('REALITY_PRIVATE_KEY')
    return vless

async def make_and_save_vless(vless: dict, from_file: str, to_file: str) -> bool:
    """ Make a new vless configuration file and save it """
    # make new vless
    vless: dict = await make_new_vless(vless=vless, enabled=True)
    # copy last vless file
    copy_result: bool = await make_copy_vless(from_file=from_file, to_file=to_file)
    if not copy_result:
        return False
    # save new vless file
    save_result: bool = await save_vless_file(vless=vless, file=from_file)
    if not save_result:
        return False
    return True



async def create_and_save_client(tlg_id: str, level: int, enabled: bool = True) -> bool | int:
    """ Save a new client to the database """
    uuid = str(uuid1())
    return await add_new_client(tlg_id=tlg_id, uuid=uuid, email=f"{tlg_id}_{uuid[:5]}@telegram.com", level=level, enabled=enabled)

async def delete_client_by_id(id: int) -> bool:
    """ Delete a client from the database """
    return await delete_client(id=id)

async def upd_client(id: int, columns: list, values: list) -> bool:
    """ Update a client status in the database """
    return await update_client(id=id, columns=columns, values=values)

async def upd_client_by_tlg_id(tlg_id: int, columns: list, values: list) -> bool:
    """ Update a client status in the database """
    return await update_client_by_tlg_id(tlg_id=tlg_id, columns=columns, values=values)       



async def make_new_vless(vless: dict, enabled: bool | None = True) -> dict:
    """ Get clients all / enabled / disabled """
    clients = await get_clients(type=enabled)
    """ Make a new vless configuration file with the given clients """
    all_clients = [{"id": client['uuid'], "email": client['email']} for client in clients]
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
        await f.write(dumps({"inbounds": [vless]}))
    return True



async def execute_command(command: str) -> bool:
    """ Execute a command """
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            print('stdout', result.stdout)
            return True, result.stdout
        else:
            print('stderr', result.stderr)
            return False, result.stdout
    except Exception as e:
        print(f"Use command '{command}' error: {e}")
        return False, ""

async def reboot_server() -> bool:
    """ Reboot the server """
    cmd_result, _ = await execute_command(command='/usr/bin/systemctl restart xray')
    return cmd_result

async def recovery_server(from_file: str, to_file: str) -> bool:
    """ Recovery the server """
    copy_result: bool = await make_copy_vless(from_file=from_file, to_file=to_file)
    if not copy_result:
        return False
    return await reboot_server()
