import asyncio
from database.sql import create_database
from settings import DEFAULT_VLESS_FILE, NEW_VLESS_FILE, LASTCOPY_VLESS_FILE
from xray_service.utils import get_default_vless, set_vless_params, make_new_vless, make_copy_vless, save_vless_file
from xray_service.utils import create_client, save_client, enabled_clients


async def add_client(tlg_id: int, level: int = 1) -> bool:
    # create database
    await create_database()

    # get default vless
    vless: dict = get_default_vless(file=DEFAULT_VLESS_FILE)
    # set vless params
    vless: dict = set_vless_params(vless=vless)

    # create client
    client: dict = create_client(tlg_id=tlg_id, level=level)
    # save client
    save_result = await save_client(tlg_id=tlg_id, client=client, enabled=True)
    if not save_result:
        return False
    # get enabled clients
    clients: list = await enabled_clients()

    # make new vless
    vless: dict = make_new_vless(vless=vless, clients=clients)
    # copy last vless file
    copy_result: bool = make_copy_vless(old_file=NEW_VLESS_FILE, new_file=LASTCOPY_VLESS_FILE)
    if not copy_result:
        return False
    # save new vless file
    save_result: bool = save_vless_file(vless=vless, file=NEW_VLESS_FILE)
    if not save_result:
        return False

    # restart xray

    # check status

    print("YES!")
    return True

    # recovery if error
    # back copy of last vless file
    # copy_result: bool = make_copy_vless(old_file=LASTCOPY_VLESS_FILE, new_file=NEW_VLESS_FILE)
    # restart xray
    return False


if __name__ == "__main__":
    asyncio.run(add_client(tlg_id=1))
