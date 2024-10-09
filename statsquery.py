from settings import XRAY_DIR, API_PORT
from xray_service.utils import execute_command


async def stats_query() -> str | bool:
    command = f"{XRAY_DIR}/xray api statsquery --server=127.0.0.1:{API_PORT}"
    return await execute_command(command=command)
