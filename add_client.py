from settings import DEFAULT_VLESS_FILE, VLESS_FILE, COPY_VLESS_FILE
from xray_service.utils import prepare_server, create_and_save_client, make_and_save_vless, apply_changes_server


async def add_client(tlg_id: int, level: int = 1) -> bool:
    # prepare server and get base vless
    vless: dict = await prepare_server(file=DEFAULT_VLESS_FILE)

    # create and save client
    save_result: bool = await create_and_save_client(tlg_id=tlg_id, level=level, enabled=True)
    if not save_result:
        return False
    
    # make and save new vless file
    result_vless_file: bool = await make_and_save_vless(vless=vless, from_file=VLESS_FILE, to_file=COPY_VLESS_FILE)
    if not result_vless_file:
        return False

    # apply changes
    return await apply_changes_server(from_file=COPY_VLESS_FILE, to_file=VLESS_FILE)
