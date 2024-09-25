import asyncio

from settings import DEFAULT_VLESS_FILE, VLESS_FILE, COPY_VLESS_FILE
from xray_service.utils import prepare_server, delete_client_by_id, make_and_save_vless, apply_changes_server


async def delete_client(id: int) -> bool:
    # prepare server and get base vless
    vless: dict = await prepare_server(file=DEFAULT_VLESS_FILE)

    # delete client
    delete_result = await delete_client_by_id(id=id)
    if not delete_result:
        return False
    
    # make and save new vless file
    result_vless_file: bool = await make_and_save_vless(vless=vless, from_file=VLESS_FILE, to_file=COPY_VLESS_FILE)
    if not result_vless_file:
        return False

    # apply changes
    return apply_changes_server(from_file=COPY_VLESS_FILE, to_file=VLESS_FILE)


if __name__ == "__main__":
    asyncio.run(delete_client(id=1))
