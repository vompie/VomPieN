import asyncio

from settings import DEFAULT_VLESS_FILE, VLESS_FILE, COPY_VLESS_FILE
from xray_service.utils import prepare_server, upd_client, upd_client_by_tlg_id, make_and_save_vless, reboot_server


async def update_client(tlg_id: int, enabled: bool) -> bool:
    # prepare server and get base vless
    vless: dict = await prepare_server(file=DEFAULT_VLESS_FILE)

    # update client
    update_result: bool = await upd_client_by_tlg_id(tlg_id=tlg_id, columns=['is_enabled'], values=[enabled])
    if not update_result:
        return False
    
    # make and save new vless file
    result_vless_file: bool = await make_and_save_vless(vless=vless, from_file=VLESS_FILE, to_file=COPY_VLESS_FILE)
    if not result_vless_file:
        return False

    # reboot xray
    reboot_result = await reboot_server()
    return reboot_result


async def update_client_by_key_id(id: int, enabled: bool) -> bool:
    # prepare server and get base vless
    vless: dict = await prepare_server(file=DEFAULT_VLESS_FILE)

    # update client
    update_result: bool = await upd_client(id=id, columns=['is_enabled'], values=[enabled])
    if not update_result:
        return False
    
    # make and save new vless file
    result_vless_file: bool = await make_and_save_vless(vless=vless, from_file=VLESS_FILE, to_file=COPY_VLESS_FILE)
    if not result_vless_file:
        return False

    # reboot xray
    reboot_result = await reboot_server()
    return reboot_result


if __name__ == "__main__":
    asyncio.run(update_client(tlg_id=1))
